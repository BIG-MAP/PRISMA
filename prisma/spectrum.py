# © Copyright 2021, PRISMA’s Authors
import numpy as np
import math
import scipy as sp
from typing import Optional
from scipy.optimize import curve_fit
import prisma.util.peak_fitting_helpers

"""Templates of Spectrum object"""


class Spectrum:
    object_identifiers = {"Class": "Spectrum", "BattInfo ID": "00X0X0"}

    def __init__(
        self,
        indexes: np.ndarray,
        counts: np.ndarray,
        baseline: Optional[np.ndarray] = None,
        profiles: Optional[dict] = None,
        peaks: Optional[dict] = None,
        **kwargs
    ):
        self.indexes = indexes
        self.RESOLVABLE_WIDTH_FACTOR = 3  # minimum resolvable width = factor *
        # minimum difference between datapoint indexes
        self.counts = counts
        self.baseline = baseline
        self.profiles = profiles
        self.peaks = peaks
        self.__load_metadata(**kwargs)

    def __load_metadata(self, **kwargs):

        self.metadata = {}
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.metadata.update(value)
            else:
                self.metadata.update({key: value})

    def trimming(self, within):
        """Trim raw spectrum
        * within [float,float]: lower and upper limits
        of the range to be studied
        """
        new_metadata = {
            "Process": "Trimming",
            "Process ID": self.object_identifiers["BattInfo ID"],
        }
        spectrum = self
        idxs_within = np.where(
            (spectrum.indexes > within[0]) &
            (spectrum.indexes < within[1]),
            True,
            False
        )  # nparray of booleans

        # trimming interval outside spectrum.indexes
        if np.all(~idxs_within):
            new_indexes = spectrum.indexes
            new_counts = spectrum.counts

        else:
            new_indexes = spectrum.indexes[idxs_within]
            new_counts = spectrum.counts[idxs_within]
            new_metadata["Trim interval"] = within

        new_metadata["Trim interval"] = [
            min(within[0], np.amin(spectrum.indexes)),
            max(within[1], np.amax(spectrum.indexes)),
        ]

        return Spectrum(
            indexes=new_indexes,
            counts=new_counts,
            metadata=new_metadata
        )

    def downsample(self, downsampling_factor: int):
        spectrum = self
        if downsampling_factor > 1:
            samples_decimated = math.ceil(len(spectrum.counts) /
                                          downsampling_factor)
            min_index: float = min(spectrum.indexes)
            max_index: float = max(spectrum.indexes)
            new_counts = sp.signal.decimate(
                spectrum.counts, downsampling_factor, zero_phase=True
            )
            '''has to be flipped to not mirror, why?'''
            new_indexes = np.linspace(
                max_index, min_index, samples_decimated, endpoint=False
            )

            return Spectrum(indexes=new_indexes, counts=new_counts,
                            metadata=spectrum.metadata)

        else:
            return spectrum

    def reject_outliers(self, outliers_threshold=0.0):
        spectrum = self
        if outliers_threshold > 0.0:

            differential_counts = np.abs(
                np.diff(
                    spectrum.counts,
                    n=2,
                    prepend=spectrum.counts[0],
                    append=spectrum.counts[-1],
                )
            )
            q1, q3 = np.percentile(differential_counts, [25, 75])
            iqr = q3 - q1

            outliers_idxs = np.where(
                (differential_counts < q1 - outliers_threshold * iqr)
                | (differential_counts > q3 + outliers_threshold * iqr)
            )[0]

            if outliers_idxs.size == 0:  # if there are no outliers
                return spectrum
            else:
                outlier_groups = np.split(
                    outliers_idxs, np.where(np.diff(outliers_idxs) > 1)[0] + 1
                )  # neighboring points are also classified as outliers.
                # This groups an outlier and its neighbors
                outliers_idxs_no_neighbors = [
                    group[np.argmax(differential_counts[group])]
                    for group in outlier_groups
                ]  # This select the outlier as the maximum value
                # among its neighbors

                new_counts = spectrum.counts.copy()
                new_counts[outliers_idxs_no_neighbors] = np.nan
                new_indexes = spectrum.indexes.copy()
                new_indexes[outliers_idxs_no_neighbors] = np.nan
                new_counts = new_counts[~np.isnan(new_counts)]
                new_indexes = new_indexes[~np.isnan(new_indexes)]

            return Spectrum(
                indexes=new_indexes,
                counts=new_counts,
                metadata=spectrum.metadata,
            )

        else:
            return spectrum

    def baseline_correction(self, log_p=-1.5, log_lambda=7):
        PROCESS_TYPE = "Baseline Correction"
        BATTINFO_ID = self.object_identifiers["BattInfo ID"]
        new_metadata = {
            "Process": PROCESS_TYPE,
            "Process ID": BATTINFO_ID,
            "Method": "Assymetric Least Squares",
            "Log10(p)": log_p,
            "Log10(lambda)": log_lambda,
        }
        spectrum = self
        baseline_correction = (
            prisma.util.baseline_corrections.asymmetric_least_squares(
                spectrum.counts, log_p, log_lambda
            )
        )
        z = baseline_correction[1]
        new_counts = baseline_correction[0]
        new_indexes = spectrum.indexes

        return Spectrum(
            indexes=new_indexes,
            counts=new_counts,
            baseline=z,
            metadata=new_metadata
        )

    # ***************************FITTING FUNCTION***************************

    def fit_peaks(
        self, peak_bounds, guess_widths, lineshape_peak="Lorentzian"
    ):
        """Fits peaks in the spectrum with a lorentzian profile. Parameters:
        * peak_bounds: [(low1,high1),(low2,high2),(low3,high3),...]
          list of 2-tuples with lower and upper bounds for the peak positions
        * guess_widths: [w1,w2,w3,...] initial guesses for the peak widths
        """

        new_metadata = {
            "Process": "Peak fitting",
            "Process ID": self.object_identifiers["BattInfo ID"],
            "Peak lineshapes": lineshape_peak,
            "Number of peaks": len(guess_widths),
            "Initial widths": guess_widths,
            "Position bounds": peak_bounds,
            "Fitting success": False,
        }
        spectrum = self
        new_indexes = spectrum.indexes

        # formatting bounds and define fitting functions with helper functions
        init_guess, param_bounds = (
            prisma.util.peak_fitting_helpers.prisma_peak_defaults(
                peak_bounds, guess_widths
            )
        )
        fitting_function, single_peak_function = (
            prisma.util.peak_fitting_helpers.get_fitting_functions(
                lineshape_peak, new_metadata["Number of peaks"]
            )
        )

        # fitting
        try:
            fitted_coeffs, _ = curve_fit(
                fitting_function,
                spectrum.indexes,
                spectrum.counts,
                p0=init_guess,
                bounds=param_bounds,
                ftol=1e-6,
                xtol=1e-6,
            )

            # store peaks and peak sum
            new_profiles = {
                peak_n: single_peak_function(
                    spectrum.indexes,
                    *(
                        np.append(
                            fitted_coeffs[0],
                            fitted_coeffs[3 * peak_n + 1: 3 * peak_n + 4]
                        )
                    )
                )
                for peak_n in range(new_metadata["Number of peaks"])
            }
            new_counts = fitting_function(
                spectrum.indexes, *fitted_coeffs
            )  # evaluate wavenumbers with the fitted coefficients

            new_metadata["Fitting success"] = True

        except RuntimeError:
            nan_vector = np.full(len(new_indexes), np.nan)
            fitted_coeffs = np.full(
                3 * new_metadata["Number of peaks"] + 1, np.nan
            )
            new_profiles = {
                peak_n: nan_vector
                for peak_n in range(new_metadata["Number of peaks"])
            }
            new_counts = nan_vector
            new_metadata["Fitting success"] = False

        # store fitting parameters
        new_metadata["Fitted parameters"] = {"y_0": fitted_coeffs[0]}
        for peak_n in range(new_metadata["Number of peaks"]):
            new_metadata["Fitted parameters"].update(
                {
                    "h_{}".format(peak_n + 1): fitted_coeffs[3 * peak_n + 1],
                    "p_{}".format(peak_n + 1): fitted_coeffs[3 * peak_n + 2],
                    "w_{}".format(peak_n + 1): fitted_coeffs[3 * peak_n + 3],
                }
            )

        return Spectrum(
            indexes=new_indexes,
            counts=new_counts,
            parent=spectrum,
            profiles=new_profiles,
            metadata=new_metadata,
        )

    @property
    def class_id(self):
        return (
            self.__class__.object_identifiers
        )  # return the class variable of the class instantiating the object


if __name__ == "__main__":
    print("This is a Spectrum object template")
    # print(dir(test_object))
    # print(type(test_object.__str__()))
