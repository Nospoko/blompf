import numpy as np
import itertools as itr
import scipy.linalg as lg
from utils import probability as up
from matplotlib import pyplot as plt

class Merwer(object):
    """ Most abstract maximal enthropy random walker """
    def __init__(self, values, first_id=0):
        """ quo vadis """
        # Values to walk over, by default we should get
        # a infinite well potential situation over those
        self.values     = values
        self.size       = len(self.values)

        # This is the walking space
        self.id_space = range(self.size)

        # We might want to have an option to turn
        # the mer-walking off and start cycling through
        # the values
        self.is_merw = True
        self.cyclic_ids = itr.cycle(self.id_space)

        # TODO fiddle with that also
        self.max_dist = 2

        # This is the walking element
        self.current_id = first_id

        # Init histogram container
        self.histogram = np.zeros_like(self.values)
        self.histogram[self.current_id] += 1

        # Initialize probability matrices
        self.make_S()

    def set_values(self, values):
        """ And update updatebles """
        self.values     = values
        self.size       = len(values)
        self.id_space   = range(self.size)
        self.cyclic_ids = itr.cycle(self.id_space)

        # Re-init histogram container
        self.histogram = np.zeros_like(self.values)

        # Recalculate probabilities
        self.make_S()

    def make_A(self):
        """ Prepare A-matrix """
        A = np.zeros((self.size, self.size))

        # TODO This param should be manipulated!
        max_dist = self.max_dist

        # Create interaction matrix A
        for it in range(self.size):
            for jt in range(it - max_dist, it + max_dist + 1):
                if jt >= 0 and jt < self.size:
                    A[it, jt] = self.A_it_jt(it, jt)
        self.A = A

    def A_it_jt(self, it, jt = 0):
        """ This defines merw-interactions """
        return 1

    def make_S(self):
        """ And that other one """
        self.make_A()
        S = np.zeros_like(self.A)

        # Palic, sadzic, diagonalizowac
        d, V = lg.eigh(self.A, eigvals = (self.size-1, self.size-1))
        for it in range(self.size):
            for jt in range(self.size):
                if V[jt] == 0:
                    # I don't know why this was here
                    # print 'this should never happen'
                    S[it,jt] = 0.
                else:
                    S[it,jt] = V[it]/V[jt] * self.A[it,jt]/d
        self.S = S

    def set_max_step(self, howfar):
        """ Length of a maximal jump """
        self.max_dist = howfar

        # Rebuild
        self.make_S()

    def set_probabilism(self, isit):
        """ Toggle random walk / cycling """
        self.is_merw = isit

    def get_histogram(self):
        """ Research helper """
        return self.id_space, self.histogram

    def show_histogram(self):
        """ Pretty please keep plots pretty """
        plt.bar(self.values, self.histogram, color = 'k', alpha = 0.5)
        plt.show()

    def current_value(self):
        """ No movement here """
        return self.values[self.current_id]

    def next_value(self):
        """ Make a merw step """
        if self.is_merw:
            # Probabilism
            # self.update_S()
            probabilities = self.S[:, self.current_id]

            # Get next ID
            next_id = up.randomly_draw(self.id_space, probabilities)
            self.current_id = next_id
        else:
            # Determinism
            self.current_id = self.cyclic_ids.next()

        # Update histogram
        self.histogram[self.current_id] += 1

        # Return value
        return self.values[self.current_id]

    # FIXME those are not most abstract
    def set_interaction_grid(self, grid):
        """ This defines possible transitions """
        # Something like:
        # grid = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1] * 8
        self.interaction_grid = grid

class BiasedWalker(Merwer):
    """ Walker atracted to some value """
    def __init__(self, values, first_id):
        """ Konstrutkor """
        # By default set bias to NO BIAS
        self.bias = -1

        # Init parent
        Merwer.__init__(self, values, first_id)

    def set_bias(self, prefered):
        """ Sets prefered value, lower than 0 is NO BIAS """
        self.bias       = prefered

        # Update probabilities
        self.make_S()

    def A_it_jt(self, it, jt = 0):
        """ Aij definition (symmetric - does it need to be?) """
        # FIXME some analytical research could be fruitful here
        # pdf = up.cauchy_pdf(self.bias, self.bias_power)
        # out = 1.0 + pdf(it)

        # Early (working) version
        # out = 1.0 - (1.0 * abs(self.bias - it)/self.size)
        pdf = up.tomek_pdf(self.bias)
        out = pdf(it)

        return out

    def show_bias(self):
        """ Plot atractor """
        x = np.linspace(min(self.id_space), max(self.id_space), 1001)
        y = self.A_it_jt(x)
        plt.plot(x, y)
        plt.show()

# TODO do this
class PotentialWalker(Merwer):
    """ Walker with properly defined merw-potential """
    def __init__(self, values, first_id):
        """ This constructs """
        Merwer.__init__(self, values, first_id)

    def A_it_jt(self, it, jt = 0):
        """ Interaction matrix including potential as defined by jd """
        dist = abs(it - jt)
        if dist == 2:
            return 1
        if dist == 1:
            return 1
        elif dist == 0:
            out = 2 - 2.*(1.*(it - 5 )/len(self.values) )**2
            return out
        else:
            return 0

class TimeWalker(BiasedWalker):
    """ Rhytm lives here """
    def __init__(self):
        """ nope """
        # Possible note values are always powers of 2
        # This is in ticks unit
        values = [2**it for it in range(1,9)]

        # TODO is this good
        values[0] = 8

        first_id = np.random.choice(range(3,6))

        # Init parent
        BiasedWalker.__init__(self, values, first_id)

        # No sudden time changes
        self.set_max_step(1)

class PitchWalker(BiasedWalker):
    """ Specialised for harmony manipulations """
    def __init__(self, first_pitch):
        """ el Creador, first pitch should lay on the scale? """
        # MIDI note numbers for typical 8-octave keybord go 21::108
        values = range(21, 109)
        # TODO some try - except for value error might be useful
        first_id = values.index(first_pitch)

        # Major           [C, -, D, -, E, F, -, G, -, A, -, H]
        self.major_grid = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
        self.interaction_grid = self.major_grid
        BiasedWalker.__init__(self, values, first_id)

        self.set_max_step(4)

    def set_scale(self, grid):
        """ Avaiable notes are defined by this 1/0 grid """
        self.interaction_grid = grid
        # UPDATE NEEDED KURWA
        self.make_S()

    # OBSOLETE ?
    def shift_scale(self, shift):
        """ This is importando """
        self.interaction_grid = np.roll(self.interaction_grid, shift)
        self.make_S()

    def A_it_jt(self, it, jt = 0):
        """ Pitch oriented A matrix definition """
        # Find on-scale positions of the iterators
        vit = self.values[it]
        vjt = self.values[jt]

        # Modulo octave
        nit = vit % len(self.interaction_grid)
        njt = vjt % len(self.interaction_grid)

        # Only ones on interaction grid can play together
        if self.interaction_grid[nit] == self.interaction_grid[njt] == 1:
            pdf = up.tomek_pdf(self.bias)
            return pdf(it)
        else:
            # TODO Why is this necessary?
            return 0.00000000001

class VolumeWalker(BiasedWalker):
    """ Volume dedicated """
    def __init__(self, first_vol):
        """ el Creador """
        # MIDI volume goes 0::127
        values      = range(128)
        first_id    = first_vol
        BiasedWalker.__init__(self, values, first_id)

        # By default allow more distinct volume changes
        self.set_max_step(15)

    def set_volume(self, vol):
        """ simple """
        self.set_bias(vol)

