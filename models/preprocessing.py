
import numpy as np
from models.spectrum import SpectrumProcessed


class Preprocessing:


    @staticmethod
    def trimming(spectrum, within):
        """ Trim raw spectrum
        * within [float,float]: lower and upper limits of the range to be studied 
        """  
        batt_info_id = '0XH81'

        #check the interval        
        if len(within) == 2 and within[0] >= min(spectrum.energies) and within[1] <= max(spectrum.energies): 

            idxs_within = np.where((spectrum.energies>within[0]) & (spectrum.energies<within[1]),True, False) #nparray of booleans

            new_metadata = {'Process':'Trimming','Process ID': batt_info_id, 'Trim interval': within}
            new_energies = spectrum.energies[idxs_within] 
            new_counts   = spectrum.counts[idxs_within]

            return SpectrumProcessed(energies = new_energies, counts = new_counts, parent = spectrum, metadata = new_metadata)

        else:
            #ERROR 'within' interval outside the wavenumber region or not recognized             
            spectrum.trimmed['metadata'] = {'trim interval': 'Error: Trim intervals outside the energy region'}
            return None




    @staticmethod
    def smooth_assymlsq(spectrum, parameters):
        pass
