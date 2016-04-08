import numpy as np
from matplotlib import pyplot as plt
import scipy.linalg as lg
from utils import probability as up

class Merwer(object):
    """ Most abstract maximal enthropy random walker """
    def __init__(self, values, first_id=0):
        """ quo vadis """
        # Values to walk over, by default we should get
        # a infinite well potential situation over those
        self.values     = values
        self.size       = len(self.values)

        # This is the walking element
        self.current_id = first_id

        # This is the walking space
        self.id_space = range(self.size)

        # Init histogram container
        self.histogram = np.zeros_like(self.values)
        self.histogram[self.current_id] += 1

        # Initialize probability matrices
        self.make_S()

        # FIXME those are not defects!
        # Prepare merw 'defects' (no defects by default)
        self.interaction_grid = np.ones_like(self.values)

    def make_A(self):
        """ Prepare A-matrix """
        A = np.zeros((self.size, self.size))
        # Length of a 
        max_dist = 1
        for it in range(self.size):
            for jt in range(it - max_dist, it + max_dist + 1):
                if jt >= 0 and jt < self.size:
                    A[it, jt] = 1
        self.A = A

    def make_S(self):
        """ And that other one """
        self.make_A()
        S = np.zeros_like(self.A)

        # Palic, sadzic, diagonalizowac
        d, V = lg.eigh(self.A, eigvals = (self.size-1, self.size-1))
        for it in range(self.size):
            for jt in range(self.size):
                if V[jt] == 0:
                    print 'this should never happen'
                    S[it,jt] = 0.
                else:
                    S[it,jt] = V[it]/V[jt] * self.A[it,jt]/d
        self.S = S

    def show_histogram(self):
        """ Pretty please keep plots pretty """
        plt.bar(self.values, self.histogram, color = 'k', alpha = 0.5)
        plt.show()

    def current_value(self):
        """ No movement here """
        return self.values[self.current_id]

    def next_value(self):
        """ Make a merw step """
        # self.update_S()
        probabilities = self.S[:, self.current_id]

        # Get next ID
        next_id = up.randomly_draw(self.id_space, probabilities)
        self.current_id = next_id

        # Update histogram
        self.histogram[self.current_id] += 1

        # Return value
        return self.values[self.current_id]

    def update_S(self):
        """ Re-do the S matrix """
        if self.S_update_needed:
            self.make_A()
            self.make_S()

    # FIXME this is not most abstract
    def set_interaction_grid(self, grid):
        """ This defines possible transitions """
        # Something like:
        # grid = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1] * 8
        self.interaction_grid = grid

    def set_emotional_parameter(self, happy):
        """ This shall grow """
        pass

class VolumeWalker(Merwer):
    """ Simplest neeeded implementation of mer walker """
    def __init__(self, values, first_id):
        """ fin: rakentaja """
        # Construct parent
        Merwer.__init__(self, values, first_id)
