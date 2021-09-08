import numpy as np
from scipy.optimize import curve_fit 

from prisma.spectrum import SpectrumPeakfit
import prisma.lineshapes

#Identifiers
BATTINFO_ID = 'DD01S8MK'

#Constants
RESOLVABLE_WIDTH_FACTOR = 3 #minimum resolvable width = factor * minimum difference between datapoint indexes


# ***********************************HELPER FUNCTIONS******************************

def prisma_peak_defaults(peak_bounds, max_widths, spectrum):
    #Format peak_bounds and peak_widhts to parameter bounds for the curve fit function
    # init_guess   --> initial guesses for the fitting parameters: [y0,h1,p1,w1,h2,p2,w2,h3,p3,w3,...]
    # param_bounds --> 2-tuple of lists with lower and upper bounds for the fitting parameters: ([y0,h1,p1,w1,...],[y0,h1,p1,w1,...])
    overall_max_counts = np.amax(spectrum.counts)

    limit_resolvable_width = RESOLVABLE_WIDTH_FACTOR*np.abs(spectrum.indexes[1]-spectrum.indexes[0])

    #Bounds for y0
    init_guess = [0] 
    param_bounds_low = [-0.1*overall_max_counts] 
    param_bounds_high = [0.1*overall_max_counts] 


    #Bounds for all other parameters
    for width, bound in zip(max_widths, peak_bounds):
        
        max_counts_within_bounds = np.amax(spectrum.counts[(spectrum.indexes>bound[0]) & (spectrum.indexes<bound[1])])

        #guess height = 30% maximum height  | guess position: halfway between bounds | guess width: half the maximum width provided or 5% more of min_resolvable_width, whoever is greater
        init_guess += [0.3*max_counts_within_bounds, 0.5*(bound[1]-bound[0]) + bound[0], max(1.05*limit_resolvable_width,width/2)]

        #lower bound height = 0 | lower bound position: the one provided | lower bound width: minimum resolvable width
        param_bounds_low += [0, bound[0], limit_resolvable_width] 

        #upper bound height = 110% max height | upper bound position: the one provided | upper bound width: the one provided or 10% more of min_resolvable_width, whoever is greater
        param_bounds_high += [1.1*max_counts_within_bounds, bound[1], max(1.1*limit_resolvable_width,width)]


    return init_guess, (param_bounds_low, param_bounds_high)



def get_fitting_functions(lineshape, number_of_peaks):

    if lineshape == 'Lorentzian':
        fitting_function = prisma.lineshapes.lorentzians(number_of_peaks)
        single_peak_function = prisma.lineshapes.lorentzians(1)

    elif lineshape == 'Gaussian':
        fitting_function = prisma.lineshapes.gaussians(number_of_peaks)
        single_peak_function = prisma.lineshapes.gaussians(1)

    elif lineshape == 'Pseudo-Voight 50% Lorentzian':
        fitting_function = prisma.lineshapes.pseudo_voight_50(number_of_peaks)
        single_peak_function = prisma.lineshapes.pseudo_voight_50(1)
    
    return fitting_function, single_peak_function



# ********************************FITTING FUNCTION********************************

def fit_peaks(spectrum, peak_bounds, guess_widths, lineshape = 'Lorentzian'):
    """Fits peaks in the spectrum with a lorentzian profile. Parameters:
    * peak_bounds: [(low1,high1),(low2,high2),(low3,high3),...] list of 2-tuples with lower and upper bounds for the peak positions
    * guess_widths: [w1,w2,w3,...] initial guesses for the peak widths
    """

    new_metadata = {'Process': 'Peak fitting',
                    'Process ID': BATTINFO_ID,
                    'Peak lineshapes': lineshape,
                    'Number of peaks': len(guess_widths),
                    'Initial widths':  guess_widths,
                    'Position bounds': peak_bounds, 
                    'Fitting success': False} 

    new_indexes = spectrum.indexes
    
    #formatting bounds and define fitting functions with helper functions
    init_guess, param_bounds = prisma_peak_defaults(peak_bounds, guess_widths, spectrum) 
    fitting_function, single_peak_function = get_fitting_functions(lineshape = lineshape, number_of_peaks = new_metadata['Number of peaks'])

    #fitting 
    try:               
        fitted_coeffs,_ = curve_fit(fitting_function, spectrum.indexes, spectrum.counts, p0=init_guess, bounds=param_bounds, ftol=1e-8) 

        #store peaks and peak sum
        new_profiles = {peak_n : single_peak_function(spectrum.indexes, *(np.append(fitted_coeffs[0],fitted_coeffs[3*peak_n+1:3*peak_n+4]))) for peak_n in range(new_metadata['Number of peaks'])}
        new_counts = (fitting_function(spectrum.indexes, *fitted_coeffs)) #evaluate wavenumbers with the fitted coefficients

        new_metadata['Fitting success'] = True

    except RuntimeError:
        nan_vector = np.full(len(new_indexes), np.nan)
        fitted_coeffs = np.full(3*new_metadata['Number of peaks']+1, np.nan)
        new_profiles = {peak_n : nan_vector for peak_n in range(new_metadata['Number of peaks'])}
        new_counts = nan_vector
        new_metadata['Fitting success'] = False


    #store fitting parameters
    new_metadata['Fitted parameters'] = {'y_0': fitted_coeffs[0]}
    for peak_n in range(new_metadata['Number of peaks']):
        new_metadata['Fitted parameters'].update({'h_{}'.format(peak_n+1) : fitted_coeffs[3*peak_n+1],
                                                'p_{}'.format(peak_n+1): fitted_coeffs[3*peak_n+2],
                                                'w_{}'.format(peak_n+1) : fitted_coeffs[3*peak_n+3]})


    return SpectrumPeakfit(indexes = new_indexes, counts = new_counts, parent = spectrum, profiles = new_profiles, metadata = new_metadata)
