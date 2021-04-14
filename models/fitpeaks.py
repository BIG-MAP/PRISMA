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
            equation += '+ {0}*({2}**2)/((x-{1})**2 + {2}**2)'.format(h,p,w) 
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

        lor_mix = 0.5
        gauss_mix = 1-lor_mix

        equation = 'y0'
        expression = 'lambda x,y0'

        for h, p, w in zip(height_labels,position_labels,width_labels):
            equation += '+ {3}*{0}*(2.71828183**(-0.69314718*((x-{1})/{2})**2)) + {4}*({0}*({2}**2))/((x-{1})**2+{2}**2)'.format(h, p, w, lor_mix, gauss_mix)
            expression += ',{0},{1},{2}'.format(h,p,w)

        return eval(expression + ': ' + equation)






class FitPeaks:

    battinfo_id = 'DD01S8MK'
    available_lineshapes = ['Lorentzian','Gaussian','Pseudo-Voight-50Lor']


    @staticmethod
    def bound_formatting(peak_bounds, guess_widths, max_counts):
        #Format peak_bounds and peak_widhts to parameter bounds for the curve fit function
        # init_guess   --> initial guesses for the fitting parameters: [y0,h1,p1,w1,h2,p2,w2,h3,p3,w3,...]
        # param_bounds --> 2-tuple of lists with lower and upper bounds for the fitting parameters: ([y0,h1,p1,w1,...],[y0,h1,p1,w1,...])

        #Bounds for y0
        init_guess = [0] 
        param_bounds_low = [-0.1*max_counts] 
        param_bounds_high = [0.1*max_counts] 


        #Bounds for all other parameters
        for width, bound in zip(guess_widths, peak_bounds):

            #guess height = 30% maximum height  | guess position: halfway between bounds | guess width: the one provided
            init_guess += [0.3*max_counts, 0.5*(bound[1]-bound[0]) + bound[0], width]

            #lower bound height = 0 | lower bound position: the one provided | lower bound width = 1
            param_bounds_low += [0,bound[0], 1] 

            #upper bound height = 110% max height | upper bound position: the one provided | upper bound width: 20 if width<10, 60 if 10<width<30, 200 if width>30
            param_bounds_high += [1.1*max_counts, bound[1], 20 if width<=10 else 60 if width<30 else 300]

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
                        'Position bounds': peak_bounds} 

        new_energies = spectrum.energies
        
        #formatting bounds and define fitting functions with external static method
        init_guess, param_bounds = FitPeaks.bound_formatting(peak_bounds, guess_widths, np.amax(spectrum.counts)) 
        fitting_function, single_peak_function = FitPeaks.fitting_functions(lineshape = lineshape, number_of_peaks = new_metadata['Number of peaks'])


        #fitting        
        fitted_coeffs,_ = curve_fit(fitting_function, spectrum.energies, spectrum.counts, p0=init_guess, bounds=param_bounds) 


        #store peaks and peak sum
        new_profiles = {peak_n : single_peak_function(spectrum.energies, *(np.append(fitted_coeffs[0],fitted_coeffs[3*peak_n+1:3*peak_n+4]))) for peak_n in range(new_metadata['Number of peaks'])}
        new_counts = (fitting_function(spectrum.energies, *fitted_coeffs)) #evaluate wavenumbers with the fitted coefficients


        #store fitting parameters
        new_metadata['Fitted parameters'] = {'y_0': fitted_coeffs[0]}
        for peak_n in range(new_metadata['Number of peaks']):
            new_metadata['Fitted parameters'].update({'h_{}'.format(peak_n+1) : fitted_coeffs[3*peak_n+1],
                                                    'p_{}'.format(peak_n+1): fitted_coeffs[3*peak_n+2],
                                                    'w_{}'.format(peak_n+1) : fitted_coeffs[3*peak_n+3]})


        return SpectrumPeakfit(energies = new_energies, counts = new_counts, parent = spectrum, profiles = new_profiles, metadata = new_metadata)
