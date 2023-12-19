
# © Copyright 2021, PRISMA’s Authors



import numpy as np
import scipy as sp


from prisma.spectrum1 import Spectrum


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

    return Spectrum(indexes = new_indexes, counts = new_counts, metadata = new_metadata)



def downsample(spectrum, downsampling_factor:int):

    if downsampling_factor>1:    

        samples_decimated = int(len(spectrum.counts)/downsampling_factor)
        min_index, max_index = min(spectrum.indexes), max(spectrum.indexes)

        new_counts = sp.signal.decimate(spectrum.counts, downsampling_factor)
        new_indexes = np.linspace(min_index, max_index, samples_decimated, endpoint=False)

        return Spectrum(indexes = new_indexes, counts = new_counts)

    else:
        return spectrum





def reject_outliers(spectrum, outliers_threshold=0.0):
    
    if outliers_threshold > 0.0:

        differential_counts = np.abs(np.diff(spectrum.counts, n=2, prepend=spectrum.counts[0], append=spectrum.counts[-1]))
        q1, q3 = np.percentile(differential_counts, [25, 75])
        iqr = q3 - q1

        outliers_idxs = np.where((differential_counts < q1 - outliers_threshold * iqr) | (differential_counts > q3 + outliers_threshold *  iqr))[0]

        if outliers_idxs.size == 0: #if there are no outliers
            return spectrum
        else:
            outlier_groups =  np.split(outliers_idxs, np.where(np.diff(outliers_idxs)>1)[0]+1) #neighboring points are also classified as outliers. This groups an outlier and its neighbors
            outliers_idxs_no_neighbors = [group[np.argmax(differential_counts[group])] for group in outlier_groups] #This select the outlier as the maximum value among its neigbors

            new_counts = spectrum.counts.copy()
            new_counts[outliers_idxs_no_neighbors] = np.nan
            new_indexes = spectrum.indexes

        return Spectrum(indexes = new_indexes, counts = new_counts)
    
    else:
        return spectrum


