import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def asymmetric_least_squares(counts, log_p, log_lambda):
    param_p, param_lambda = 10**log_p, 10**log_lambda

    nan_counts_mask = np.isnan(counts)
    if np.any(nan_counts_mask):  # interpolation of nans

        non_nan_counts = np.interp(
            np.arange(len(counts)),
            np.arange(len(counts))[~nan_counts_mask],
            counts[~nan_counts_mask],
        )
    else:
        non_nan_counts = counts

    m = len(non_nan_counts)
    D = sparse.diags(
        [1, -2, 1], [0, -1, -2], shape=(m, m - 2)
    )  # sparse representation of difference_2 matrix
    w = np.ones(m)  # initial -symmetric- weights
    W = sparse.spdiags(w, 0, m, m)  # weight matrix with initial weights
    iterations = 20

    for _ in range(iterations):

        W.setdiag(w)  # wiegth matrix is updated with newest weights
        C = W + param_lambda * D.dot(
            D.transpose()
        )  # matrix summarizing the fit and smooth penalties
        baseline = spsolve(C, w * non_nan_counts)
        updated_w = param_p * (non_nan_counts > baseline) + (1 - param_p) * (
            non_nan_counts < baseline
        )

        if np.linalg.norm(w) == np.linalg.norm(updated_w):
            break
        else:
            w = updated_w

    new_counts = non_nan_counts - baseline
    new_counts[nan_counts_mask] = np.nan
    return new_counts, baseline
