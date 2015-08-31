import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as lg
# For probability
import random
import bisect
import collections

N_ = 40
k_ = 2

def cdf(weights):
    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        result.append(cumsum / total)
    return result

def choice(population, weights):
    # Normalize weights to 1! XXX
    assert len(population) == len(weights)
    cdf_vals = cdf(weights)
    x = random.random()
    print x
    idx = bisect.bisect(cdf_vals, x)
    return population[idx]


def calc_S(A):
    S = np.zeros(A.shape)
    d, V = lg.eigh(A, eigvals = (N_-1, N_-1))
    print V.shape, d.shape
    for it in range(N_):
        for jt in range(N_):
            S[it,jt] = V[it]/V[jt] * A[it,jt]/d
    return S

def randomly_draw(values, q):
    # q is of course probabilities
    pass

A = np.zeros((N_, N_))
pos = 20

for it in range(N_):
    for jt in range(it-2, it+3):
        if abs(it-jt) == 1 and jt>=0 and jt < N_:
            A[it, jt] = 10;


#for it in range(1000):

S = calc_S(A)
plt.imshow(S)
plt.show()
