
import numpy as np
from models.spectrum import SpectrumProcessed


class Preprocessing:


    @staticmethod
    def trimming(spectrum, within):
        """ Trim raw spectrum
        * within [float,float]: lower and upper limits of the range to be studied 
        """  
        batt_info_id = '0XH81'        
        new_metadata = {'Process':'Trimming','Process ID': batt_info_id}

        idxs_within = np.where((spectrum.energies>within[0]) & (spectrum.energies<within[1]),True, False) #nparray of booleans

        #trimming interval outside spectrum.energies
        if np.all(~idxs_within):
            new_energies = spectrum.energies
            new_counts   = spectrum.counts

        else:
            new_energies = spectrum.energies[idxs_within] 
            new_counts   = spectrum.counts[idxs_within]
            new_metadata['Trim interval'] = within

        
        new_metadata['Trim interval'] = [min(within[0],np.amin(spectrum.energies)),max(within[1],np.amax(spectrum.energies))]

        return SpectrumProcessed(energies = new_energies, counts = new_counts, parent = spectrum, metadata = new_metadata)




    @staticmethod
    def smooth_assymlsq(spectrum, parameters):
        pass
