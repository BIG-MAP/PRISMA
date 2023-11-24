
# © Copyright 2021, PRISMA’s Authors



import numpy as np
import scipy as sp


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



def downsample(spectrum, downsampling_factor:int):

    if downsampling_factor>1:    

        samples_decimated = int(len(spectrum.counts)/downsampling_factor)
        min_index, max_index = min(spectrum.indexes), max(spectrum.indexes)

        new_counts = sp.signal.decimate(spectrum.counts, downsampling_factor)
        new_indexes = np.linspace(min_index, max_index, samples_decimated, endpoint=False)

        return Spectrum(indexes = new_indexes, counts = new_counts)

    else:
        return spectrum





def reject_outliers(spectrum, remove_outliers:bool):
    
    ## TO DO: CHANGE TO DETECT OUTLIERS USING DIFFS not the main vaules.
    if remove_outliers:
        q1, q3 = np.percentile(spectrum.counts, [25, 75])
        mask = (spectrum.counts >= q1 - 1.5 * (q3 - q1)) & (spectrum.counts <= q3 + 1.5 * (q3 - q1))

        new_indexes = spectrum.indexes[mask]
        new_counts = spectrum.counts[mask]

        return Spectrum(indexes = new_indexes, counts = new_counts)
    
    else:
        return spectrum

