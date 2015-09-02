import numpy as np
import matplotlib.pyplot as plt
from potentials import *

class Merw(object):
    def __init__(self, size):
        self.size = size
        self.values = range(self.size)
        self.pot = E_potential(self.size)
        self.S = self.pot.get_S()
        self.A = self.pot.get_A()
    def set_prefered(self, prefered):
        self.pot.set_prefered(prefered)
    def get_S(self):
        return self.pot.get_S()
    def get_A(self):
        return self.pot.get_A()
    def get_next_value(self, idx, time=0):
        # idx - previous index
        # time - variable to control potential
        S = self.pot.get_S()
        return randomly_draw(self.values, S[:,idx])

if __name__ == '__main__':

    # Calculate probability matix holding S
    merw = Merw(N_)

    # Prepare histogram
    score = np.zeros(N_)

    # Prepare list of indexes
    values = range(N_)

    # Merw starting position set
    pos = 33
    positions = []

    # Walk
    intervals = []

    # Prepare meta potential for testing
    # Number of iterations
    N_ = 250
    def meta_pot(it):
        ret = 70.0 * (0.5 * (1.0 + np.cos(8.*it*np.pi/N_)))
        print ret
        return ret

    for it in range(N_):
        positions.append(pos)
        next_pos = merw.get_next_value(pos)
        merw.set_prefered(int(meta_pot(it)))

        # Histogram
        score[pos] += 1

        # Intervals plot
        intervals.append(abs(next_pos - pos))

        # Switcheroo
        pos = next_pos

        if (it%50 == 1):
            print it, '/', N_


    S = merw.get_S(); plt.imshow(S); plt.show()

    #plt.plot(score,'ko'); plt.show()

    plt.plot(positions, 'ko'); plt.show()
