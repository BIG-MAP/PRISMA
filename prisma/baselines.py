# © Copyright 2021, PRISMA’s Authors

import numpy as np
from scipy.sparse.linalg import spsolve
from scipy import sparse

from prisma.spectrum1 import Spectrum


BATTINFO_ID = '99YH6S'
PROCESS_TYPE = 'Baseline correction'


def asymmetric_least_squares(spectrum, log_p=-1.5, log_lambda=7):

    new_metadata = {'Process': PROCESS_TYPE,
                    'Process ID': BATTINFO_ID,
                    'Method':'Assymetric Least Squares',
                    'Log10(p)':log_p, 'Log10(lambda)':log_lambda}


    param_p, param_lambda = 10**log_p, 10**log_lambda

    nan_counts_mask = np.isnan(spectrum.counts)
    if np.any(nan_counts_mask): #interpolation of nans

        non_nan_counts = np.interp(np.arange(len(spectrum.counts)), 
                                np.arange(len(spectrum.counts))[~nan_counts_mask], 
                                spectrum.counts[~nan_counts_mask])   
    else:
        non_nan_counts = spectrum.counts
        

    m = len(non_nan_counts)
    D = sparse.diags([1,-2,1],[0,-1,-2],shape=(m,m-2)) #sparse representation of difference_2 matrix
    w = np.ones(m) #initial -symmetric- weights
    W = sparse.spdiags(w,0,m,m) #weight matrix with initial weights
    iterations = 20

    for _ in range(iterations):

        W.setdiag(w) #wiegth matrix is updated with newest weights
        C = W + param_lambda*D.dot(D.transpose()) # matrix summarizing the fit and smooth penalties
        z = spsolve(C,w*non_nan_counts)
        updated_w = param_p*(non_nan_counts>z) + (1-param_p)*(non_nan_counts<z)

        if np.linalg.norm(w) == np.linalg.norm(updated_w):
            break
        else:
            w = updated_w 
    
    new_counts = non_nan_counts - z
    new_counts[nan_counts_mask] = np.nan
    new_indexes = spectrum.indexes

    return Spectrum(indexes = new_indexes, counts = new_counts, baseline = z, metadata = new_metadata)
