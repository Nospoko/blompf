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

def choice(weights):
    # Normalize weights to 1! XXX
    cdf_vals = cdf(weights)
    x = random.random()
    idx = bisect.bisect(cdf_vals, x)
    return idx


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
    return values[choice(q)]


# Calculate probability matix holding S
A = np.zeros((N_, N_))
for it in range(N_):
    for jt in range(it-2, it+3):
        if abs(it-jt) == 1 and jt>=0 and jt < N_:
            A[it, jt] = 10;
# Here
S = calc_S(A)

# Prepare histogram
score = np.zeros(N_)

# Prepare list of indexes
values = range(N_)

# Merw starting position set
pos = 20

# Walk
for it in range(int(1e6)):
    score[pos] += 1
    pos = randomly_draw(values, S[:,pos])


plt.imshow(S)
plt.show()

plt.plot(score,'ko')
plt.show()
