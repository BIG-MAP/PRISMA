import numpy as np
from prisma.util.lineshapes import lorentzians, gaussians, pseudo_voight_50


def prisma_peak_defaults(self, peak_bounds, max_widths):
    # Format peak_bounds and peak_widhts to parameter bounds for the curve
    # fit function
    # init_guess   --> initial guesses for the fitting parameters:
    # [y0, h1, p1, w1, h2, p2, w2, h3, p3, w3, ...]
    # initial guesses for the fitting parameters
    # param_bounds --> 2-tuple of lists with lower and upper bounds for
    # the fitting parameters: ([y0,h1,p1,w1,...],[y0,h1,p1,w1,...])
    spectrum = self

    overall_max_counts = np.amax(spectrum.counts)

    limit_resolvable_width = self.RESOLVABLE_WIDTH_FACTOR * np.abs(
        spectrum.indexes[1] - spectrum.indexes[0]
    )

    # Bounds for y0
    init_guess = [0]
    param_bounds_low = [-0.1 * overall_max_counts]
    param_bounds_high = [0.1 * overall_max_counts]

    # Bounds for all other parameters
    for width, bound in zip(max_widths, peak_bounds):

        max_counts_within_bounds = np.amax(
            spectrum.counts[
                (spectrum.indexes > bound[0]) &
                (spectrum.indexes < bound[1])
            ]
        )

        # guess height = 30% maximum height
        # guess position: halfway between bounds
        # guess width: half the maximum width provided or 5% more of
        # min_resolvable_width, whoever is greater
        init_guess += [
            0.3 * max_counts_within_bounds,
            0.5 * (bound[1] - bound[0]) + bound[0],
            max(1.05 * limit_resolvable_width, width / 2),
        ]

        # lower bound height = 0 | lower bound position: the one provided |
        # lower bound width: minimum resolvable width
        param_bounds_low += [0, bound[0], limit_resolvable_width]

        # upper bound height = 110% max height | upper bound position:
        # the one provided | upper bound width: the one provided or 10%
        # more of min_resolvable_width, whoever is greater
        param_bounds_high += [
            1.1 * max_counts_within_bounds,
            bound[1],
            max(1.1 * limit_resolvable_width, width),
        ]

    return init_guess, (param_bounds_low, param_bounds_high)


def get_fitting_functions(self, lineshape, number_of_peaks):
    if lineshape == 'Lorentzian':
        fitting_function = lorentzians(
            number_of_peaks
        )
        single_peak_function = lorentzians(1)

    elif lineshape == 'Gaussian':
        fitting_function = gaussians(
            number_of_peaks
        )
        single_peak_function = gaussians(1)

    elif lineshape == 'Pseudo-Voight 50% Lorentzian':
        fitting_function = pseudo_voight_50(
            number_of_peaks
        )
        single_peak_function = pseudo_voight_50(1)

    return fitting_function, single_peak_function
