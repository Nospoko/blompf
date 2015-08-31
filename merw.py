import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as lg
# For probability
import random
import bisect
import collections

N_ = 12
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
    for it in range(N_):
        for jt in range(N_):
            if V[jt] == 0:
                S[it,jt] = 0.
            else:
                S[it,jt] = V[it]/V[jt] * A[it,jt]/d
    return S

def randomly_draw(values, q):
    # q is of course probabilities
    idx = choice(q)
    return values[idx]

def they_interact(i, j):
    scale = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    n = len(scale)

    if scale[i%n] == scale[j%n] == 1: # Nice python!
        return True

    # Else
    return False


# Calculate probability matix holding S
A = np.random.random((N_, N_))/1e4
for it in range(N_):   
    for jt in range(it-8, it+9): # Wtf python
        if jt >= 0 and jt < N_:
            if they_interact(it,jt):
    #            print it, jt
                A[it, jt] = 10
#        if abs(it-jt) == 1 and jt>=0 and jt < N_:
#            A[it, jt] = 0.123

# Here
S = calc_S(A)

# Prepare histogram
score = np.zeros(N_)

# Prepare list of indexes
values = range(N_)

# Merw starting position set
pos = 1

# Walk
for it in range(int(5e4)):
    score[pos] += 1
    pos = randomly_draw(values, S[:,pos])


plt.imshow(S)
plt.show()

plt.plot(score,'ko')
plt.show()
