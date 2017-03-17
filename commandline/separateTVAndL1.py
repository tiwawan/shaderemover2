import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt
from skimage import transform

def separateTVAndL1(M, sp, max_iters=30):
    """
    separate matrix m into smooth and sparse components
    M: 2-d ndarray
    sp:strength of sparseness
    max_iters: maximum number of iterations
    """
    
    m = M.shape[0]
    n = M.shape[1]

    L = cvx.Variable(m,n)
    S = cvx.Variable(m,n)

    #ob = cvx.Minimize(cvx.norm(L,'nuc') + 0.05*cvx.norm(S, 1))
    ob = cvx.Minimize(cvx.tv(L) + sp*cvx.norm(S, 1))

    co = [M == L + S]

    prob = cvx.Problem(ob, co)

    result = prob.solve(solver='SCS', max_iters=30);

    return L.value, S.value


def removeShade(im_orig, rescaled_size):
    w_orig = im_orig.shape[1]
    h_orig = im_orig.shape[0]

    im_resize = transform.resize(im_orig, (rescaled_size,rescaled_size))
    
    L, S = separateTVAndL1(im_resize, 0.2)

    L_origsize = transform.resize(L, (h_orig, w_orig))

    S_origsize = im_orig - L_origsize

    minS = np.min(S_origsize)

    S_origsize = S_origsize - minS
    S_origsize = S_origsize / (-minS)
    #S_origsize[S_origsize<0] = 0
    
    return S_origsize


if __name__ == "__main__":
    L, S = separateTVAndL1(np.ones((100,100)), 0.2, 30)
    plt.imshow(S, cmap='gray');
    plt.colorbar();
    plt.show();
