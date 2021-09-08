import numpy as np
from scipy.sparse.linalg import spsolve
from scipy import sparse

from prisma.spectrum import SpectrumProcessed


BATTINFO_ID = '99YH6S'
PROCESS_TYPE = 'Baseline correction'


def asymmetric_least_squares(spectrum, log_p=-1.5, log_lambda=7):

    new_metadata = {'Process': PROCESS_TYPE,
                    'Process ID': BATTINFO_ID,
                    'Method':'Assymetric Least Squares',
                    'Log10(p)':log_p, 'Log10(lambda)':log_lambda}


    param_p, param_lambda = 10**log_p, 10**log_lambda

    m = len(spectrum.counts)
    D = sparse.diags([1,-2,1],[0,-1,-2],shape=(m,m-2)) #sparse representation of difference_2 matrix
    w = np.ones(m) #initial -symmetric- weights
    W = sparse.spdiags(w,0,m,m) #weight matrix with initial weights
    iterations = 20

    for _ in range(iterations):

        W.setdiag(w) #wiegth matrix is updated with newest weights
        C = W + param_lambda*D.dot(D.transpose()) # matrix summarizing the fit and smooth penalties
        z = spsolve(C,w*spectrum.counts)
        updated_w = param_p*(spectrum.counts>z) + (1-param_p)*(spectrum.counts<z)

        if np.linalg.norm(w) == np.linalg.norm(updated_w):
            break
        else:
            w = updated_w 
    
    new_counts = spectrum.counts - z
    new_indexes = spectrum.indexes

    return SpectrumProcessed(indexes = new_indexes, counts = new_counts, parent = spectrum, metadata = new_metadata)
