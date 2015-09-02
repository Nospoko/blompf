import numpy as np
# For probability
import random
import bisect
import collections
import scipy.linalg as lg


# TODO - circular conditions
# TODO - move A-creation to separate method

# Probability helpers
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

def randomly_draw(values, q):
    # q is of course a vector with probabilities
    idx = choice(q)
    return values[idx]


class E_potential(object):
    def __init__(self, size):
        self.size = size
        self.prefered = 0
        self.calc_A()
#        self.simple_A()
        self.calc_S()

    def set_prefered(self, prefered):
        self.prefered = prefered
        self.calc_A()
        self.calc_S()

    def they_interact(self, i, j):
        scale = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
        n = len(scale)

        if scale[i%n] == scale[j%n] == 1: # Nice python!
            return True
        # Else
        return False

    def get_potential(self):
        # Show potential 
        x = range(self.size)
        y = [self.merw_pot(s) for s in x]
        plt.plot(x,y)
        plt.show()

    def get_A(self):
        return self.A
    def get_S(self):
        return self.S

    def simple_A(self):
        A = np.zeros((self.size, self.size))
        k = 3
        for it in range(self.size):
            for jt in range(it-k ,it+k+1):
                if jt == it + 1 or jt == it -1:
                    if jt >= 0 and jt < self.size:
                        A[it,jt] = 1
        self.A = A

    def merw_pot(self, i, prefered = 0):
        ret = 1. - ((i-prefered)/float(self.size))**2
        return ret

    def calc_A(self):
        #A = np.random.random((self.size, self.size))/1e3
        A = np.zeros((self.size, self.size))
        noise = 1e-4
        k = 4
        for it in range(self.size):
            for jt in range(it-k, it+k+1): # wtf python
                if jt >= 0 and jt < self.size:
                    if self.they_interact(it,jt):
                        A[it, jt] = 1
                        if not self.prefered == 0:
                            A[it, jt] *= self.merw_pot(it, self.prefered)
                    else:
                        A[it, jt] += noise
        self.A = A

    def calc_S(self):
        S = np.zeros(self.A.shape)
        d, V = lg.eigh(self.A, eigvals = (self.size-1, self.size-1))
        for it in range(self.size):
            for jt in range(self.size):
                if V[jt] == 0:
                    print 'this should never happen'
                    S[it,jt] = 0.
                else:
                    S[it,jt] = V[it]/V[jt] * self.A[it,jt]/d
        self.S = S


