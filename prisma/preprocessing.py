
import numpy as np
from prisma.spectrum import Spectrum


BATTINFO_ID = '0XH81'


def trimming(spectrum, within):
    """ Trim raw spectrum
    * within [float,float]: lower and upper limits of the range to be studied 
    """  
     
    new_metadata = {'Process':'Trimming','Process ID': BATTINFO_ID}

    idxs_within = np.where((spectrum.indexes>within[0]) & (spectrum.indexes<within[1]),True, False) #nparray of booleans

    #trimming interval outside spectrum.indexes
    if np.all(~idxs_within):
        new_indexes = spectrum.indexes
        new_counts   = spectrum.counts

    else:
        new_indexes = spectrum.indexes[idxs_within] 
        new_counts   = spectrum.counts[idxs_within]
        new_metadata['Trim interval'] = within

    
    new_metadata['Trim interval'] = [min(within[0],np.amin(spectrum.indexes)),max(within[1],np.amax(spectrum.indexes))]

    return Spectrum(indexes = new_indexes, counts = new_counts, parent = spectrum, metadata = new_metadata)




def smooth_assymlsq(spectrum, parameters):
    #To be implemented
    pass


def reject_outliers_std_method(spectrum, parameters):
    #To be implemented
    pass
