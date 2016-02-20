import numpy as np
import random
import bisect
import collections
import scipy.linalg as lg

# TODO - circular conditions
# TODO - move A-creation to separate method

def cdf(weights):
    """ Cumulative distribution function """
    # Normalization, container, iterator
    total = sum(weights)
    result = []
    cumsum = 0.0

    # Construct
    for w in weights:
        cumsum += w
        result.append(cumsum / total)

    # Give back
    return result

def choice(normalized_weights):
    """ Returns id of randomly chosen weight """
    cdf_vals = cdf(normalized_weights)
    x = np.random.random()
    # Seems important
    idx = bisect.bisect(cdf_vals, x)
    return idx

def randomly_draw(values, q):
    """ Changes probability into reality """
    idx = choice(q)
    return values[idx]

class E_potential(object):
    """ Some serious class o_O """
    def __init__(self, size):
        """ """
        self.size = size
        self.prefered = 0

        # Initialize interaction grid (piano keys)
        self.scale = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]

        # Based on that generate probability matrix S
#        self.simple_A()
        self.calc_S()

    # XXX - set this before self.prefered
    def set_scale_shift(self, shift):
        """ Set it """
        self.scale = np.roll(self.scale, shift)
        print self.scale
        self.calc_S()

    def set_prefered(self, prefered):
        """ You want it """
        self.prefered = prefered
        self.calc_S()

    def they_interact(self, i, j):
        """ This dictates A and S shapes """

        n = len(self.scale)

        if self.scale[i%n] == self.scale[j%n] == 1: # Nice python!
            return True
        else:
            return False

    def show_potential(self):
        """ Plot """
        x = range(self.size)
        y = [self.merw_pot(s) for s in x]
        plt.plot(x,y)
        plt.show()

    def get_A(self):
        """ wtf """
        return self.A

    def get_S(self):
        """ Nice """
        return self.S

    def simple_A(self):
        """ Dummy """
        A = np.zeros((self.size, self.size))
        k = 3
        for it in range(self.size):
            for jt in range(it-k ,it+k+1):
                if jt == it + 1 or jt == it -1:
                    if jt >= 0 and jt < self.size:
                        A[it,jt] = 1
        self.A = A

    # FIXME ? maybe store this hashed
    def merw_pot(self, i, prefered = 0):
        """ wtf """
        ret = 1. - ((i-prefered)/float(self.size))**2
        return ret

    def calc_A(self):
        """ dafuq """
        #A = np.random.random((self.size, self.size))/1e3
        A = np.zeros((self.size, self.size))
        noise = 1e-4
        k = 4
        for it in range(self.size):
            for jt in range(it-k, it+k+1): # wtf python
                if jt >= 0 and jt < self.size:
                    if self.they_interact(it,jt):
                        A[it, jt] = 1
                        # Ja pierdole co to kurwa jest
                        if not self.prefered == 0:
                            A[it, jt] *= self.merw_pot(it, self.prefered)
                    else:
                        A[it, jt] += noise
        self.A = A

    def calc_S(self):
        """ is this """
        self.calc_A()
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

