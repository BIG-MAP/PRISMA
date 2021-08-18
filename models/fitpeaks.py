import numpy as np
from scipy.optimize import curve_fit 

from models.spectrum import SpectrumPeakfit



class Lineshapes:

    @staticmethod
    def lorentzians(npeaks=1):
        """Returns a function of npeaks number of lorentzian profiles to be used for curve fitting
        The returned function is: returned_function(x, y0, h1, p1, w1, h2, p2, w2 ,h3 ,p3 ,w3...)
        """

        height_labels = ['h{}'.format(n) for n in range(1,npeaks+1)]
        width_labels = ['w{}'.format(n) for n in range(1,npeaks+1)]
        position_labels = ['p{}'.format(n) for n in range(1,npeaks+1)]

        equation = 'y0'
        expression = 'lambda x,y0'

        for h, p, w in zip(height_labels,position_labels,width_labels):
            equation += '+ {0}/(((x-{1})**2)/({2}**2) + 1)'.format(h,p,w) 
            expression += ',{0},{1},{2}'.format(h,p,w)

        return eval(expression + ': ' + equation)



    @staticmethod
    def gaussians(npeaks=1):
        """Returns a function of npeaks number of gaussian profiles to be used for curve fitting
        The returned function is: returned_function(x, y0, h1, p1, w1, h2, p2, w2 ,h3 ,p3 ,w3...)
        """

        height_labels = ['h{}'.format(n) for n in range(1,npeaks+1)]
        width_labels = ['w{}'.format(n) for n in range(1,npeaks+1)]
        position_labels = ['p{}'.format(n) for n in range(1,npeaks+1)]

        equation = 'y0'
        expression = 'lambda x,y0'

        for h, p, w in zip(height_labels,position_labels,width_labels):
            equation += '+ {0}*(2.71828183**(-0.69314718*((x-{1})/{2})**2))'.format(h,p,w) 
            expression += ',{0},{1},{2}'.format(h,p,w)

        return eval(expression + ': ' + equation)



    @staticmethod
    def pseudo_voight_50(npeaks=1):
        """Returns a function of npeaks number of pseudo-voight profiles with 50% lorentzian/gaussian mixing
        The returned function is: returned_function(x, y0, h1, p1, w1, h2, p2, w2 ,h3 ,p3 ,w3...)
        """

        height_labels = ['h{}'.format(n) for n in range(1,npeaks+1)]
        width_labels = ['w{}'.format(n) for n in range(1,npeaks+1)]
        position_labels = ['p{}'.format(n) for n in range(1,npeaks+1)]

        lor_mix = 0.5 #proportion og lorentzian. lor_mix = 1 - gauss_mix

        equation = 'y0'
        expression = 'lambda x,y0'

        for h, p, w in zip(height_labels,position_labels,width_labels):
            equation += '+ {0}*({3}*(2.71828183**(-0.69314718*((x-{1})/{2})**2)) + (1-{3})/(((x-{1})**2)/({2}**2) + 1))'.format(h, p, w, lor_mix)
            expression += ',{0},{1},{2}'.format(h,p,w)

        return eval(expression + ': ' + equation)






class FitPeaks:

    battinfo_id = 'DD01S8MK'
    available_lineshapes = ['Lorentzian','Gaussian','Pseudo-Voight-50Lor']


    @staticmethod
    def bound_formatting(peak_bounds, max_widths, spectrum):
        #Format peak_bounds and peak_widhts to parameter bounds for the curve fit function
        # init_guess   --> initial guesses for the fitting parameters: [y0,h1,p1,w1,h2,p2,w2,h3,p3,w3,...]
        # param_bounds --> 2-tuple of lists with lower and upper bounds for the fitting parameters: ([y0,h1,p1,w1,...],[y0,h1,p1,w1,...])
        overall_max_counts = np.amax(spectrum.counts)

        limit_resolvable_width = 4*np.abs(spectrum.energies[1]-spectrum.energies[0])

        #Bounds for y0
        init_guess = [0] 
        param_bounds_low = [-0.1*overall_max_counts] 
        param_bounds_high = [0.1*overall_max_counts] 


        #Bounds for all other parameters
        for width, bound in zip(max_widths, peak_bounds):
            
            max_counts_within_bounds = np.amax(spectrum.counts[(spectrum.energies>bound[0]) & (spectrum.energies<bound[1])])

            #guess height = 30% maximum height  | guess position: halfway between bounds | guess width: half the maximum width provided or 5% more of min_resolvable_width, whoever is greater
            init_guess += [0.3*max_counts_within_bounds, 0.5*(bound[1]-bound[0]) + bound[0], max(1.05*limit_resolvable_width,width/2)]

            #lower bound height = 0 | lower bound position: the one provided | lower bound width: minimum resolvable width
            param_bounds_low += [0, bound[0], limit_resolvable_width] 

            #upper bound height = 110% max height | upper bound position: the one provided | upper bound width: the one provided or 10% more of min_resolvable_width, whoever is greater
            param_bounds_high += [1.1*max_counts_within_bounds, bound[1], max(1.1*limit_resolvable_width,width)]

        # print('low bounds:')
        # print(param_bounds_low)
        # print('init guess:')
        # print(init_guess)
        # print('high bounds:')
        # print(param_bounds_high)

        return init_guess, (param_bounds_low, param_bounds_high)




    @staticmethod
    def fitting_functions(lineshape, number_of_peaks):

        if lineshape == 'Lorentzian':
            fitting_function = Lineshapes().lorentzians(number_of_peaks)
            single_peak_function = Lineshapes().lorentzians(1)

        elif lineshape == 'Gaussian':
            fitting_function = Lineshapes().gaussians(number_of_peaks)
            single_peak_function = Lineshapes().gaussians(1)

        elif lineshape == 'Pseudo-Voight 50% Lorentzian':
            fitting_function = Lineshapes().pseudo_voight_50(number_of_peaks)
            single_peak_function = Lineshapes().pseudo_voight_50(1)
        
        return fitting_function, single_peak_function




    @staticmethod
    def fit_peaks(spectrum, peak_bounds, guess_widths, lineshape = 'Lorentzian'):
        """Fits peaks in the spectrum with a lorentzian profile. Parameters:
        * peak_bounds: [(low1,high1),(low2,high2),(low3,high3),...] list of 2-tuples with lower and upper bounds for the peak positions
        * guess_widths: [w1,w2,w3,...] initial guesses for the peak widths
        """

        new_metadata = {'Process': 'Peak fitting',
                        'Process ID': FitPeaks.battinfo_id,
                        'Peak lineshapes': lineshape,
                        'Number of peaks': len(guess_widths),
                        'Initial widths':  guess_widths,
                        'Position bounds': peak_bounds, 
                        'Fitting success': False} 

        new_energies = spectrum.energies
        
        #formatting bounds and define fitting functions with external static method
        init_guess, param_bounds = FitPeaks.bound_formatting(peak_bounds, guess_widths, spectrum) 
        fitting_function, single_peak_function = FitPeaks.fitting_functions(lineshape = lineshape, number_of_peaks = new_metadata['Number of peaks'])

        #fitting 
        try:               
            fitted_coeffs,_ = curve_fit(fitting_function, spectrum.energies, spectrum.counts, p0=init_guess, bounds=param_bounds, ftol=1e-8) 

            #store peaks and peak sum
            new_profiles = {peak_n : single_peak_function(spectrum.energies, *(np.append(fitted_coeffs[0],fitted_coeffs[3*peak_n+1:3*peak_n+4]))) for peak_n in range(new_metadata['Number of peaks'])}
            new_counts = (fitting_function(spectrum.energies, *fitted_coeffs)) #evaluate wavenumbers with the fitted coefficients

            new_metadata['Fitting success'] = True

        except RuntimeError:
            nan_vector = np.full(len(new_energies), np.nan)
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


        return SpectrumPeakfit(energies = new_energies, counts = new_counts, parent = spectrum, profiles = new_profiles, metadata = new_metadata)
