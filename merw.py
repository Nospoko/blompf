from potentials import *
import potentials as pt
from merwmidi import make_midi
import random

class Merw(object):
    """ Most generic walker, perfect for pitch control """
    def __init__(self, size):
        """ quo vadis """
        self.size = size
        self.values = range(self.size)

        # FIXME this must have been such a grand idea
        # now crap, at least pls rename this TODO
        self.pot = pt.E_potential(self.size)

        # These are cool
        self.S = self.pot.get_S()
        self.A = self.pot.get_A()

    def set_scale_shift(self, shift):
        """ Shifts scale """
        self.pot.set_scale_shift(shift)

    def set_prefered(self, prefered):
        """ Probability bender """
        self.pot.set_prefered(prefered)

    def get_S(self):
        """ Dig deep """
        return self.pot.get_S()

    def get_A(self):
        """ yup """
        return self.pot.get_A()

    # FIXME this seems crap
    def get_next_value(self, current_id):
        """ Takes a next merw step """
        # idx - previous index
        S = self.pot.get_S()

        out = pt.randomly_draw(self.values, S[:, current_id])
        return out

