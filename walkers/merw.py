import numpy as np
import itertools as itr
import scipy.linalg as lg
from utils import harmony as uh
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
                if V[it] == 0:
                    # I don't know why this was here
                    # print 'this should never happen'
                    S[it,jt] = 0.
                else:
                    S[it,jt] = V[jt]/V[it] * self.A[it,jt]/d
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
            # probabilities = self.S[:, self.current_id]
            probabilities = self.S[self.current_id, :]

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
    def __init__(self, values, first_id, symmetric):
        """ Konstrutkor """
        # By default set bias to NO BIAS
        self.bias = -1
        self.symmetric = False

        # Init parent
        Merwer.__init__(self, values, first_id)

    def set_bias(self, prefered):
        """ Sets prefered value, lower than 0 is NO BIAS """
        self.bias       = prefered

        if self.bias >= 0:
            self.symmetric = False

        if self.bias < 0:
            self.symmetric = True

        self.symmetric = False
        # Update probabilities
        self.make_S()

    def make_S(self):
        """ Transition probabilities matrix """
        self.make_A()
        S = np.zeros_like(self.A)

        if self.symmetric == True:
            # Find the maximum eigenvalue and the corresponding eigenvector
            d, V = lg.eigh(self.A, eigvals = (self.size-1, self.size-1))

        if self.symmetric == False:
            # Find eigenvalues and eigenvectors
            d, V = lg.eig(self.A)
            # Find the maximum eigenvalue
            imax = np.argmax(d)
            d = np.max(d)
            # and the corresponding eigenvector
            V = V[:,imax]

        for it in range(self.size):
            for jt in range(self.size):
                if V[it] != 0:
                    S[it,jt] = V[jt]/V[it] * self.A[it,jt]/d
        self.S = S

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
        BiasedWalker.__init__(self, values, first_id, True)

        # No sudden time changes
        self.set_max_step(1)

class PitchWalker(BiasedWalker):
    """ Specialised for harmony manipulations """
    def __init__(self, first_pitch):
        """ el Creador, first pitch should lay on the scale? """
        # All possible keys
        self.all_values        = uh.piano_keys()
        self.global_size       = len(self.all_values)
        self.global_id_space   = range(self.global_size)

        # Major           [C, -, D, -, E, F, -, G, -, A, -, H]
        self.major_grid = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
        self.interaction_grid = self.major_grid

        # Keys allowed by the grid
        values = self.make_values()
        # TODO some try - except for value error might be useful
        first_id = values.index(first_pitch)
        BiasedWalker.__init__(self, values, first_id, True)

        # Reinit histogram container
        # so that it contains all_values, not just values
        self.histogram = np.zeros_like(self.all_values)

        # "global" first_pitch id 
        # (refering to all_values, not vallues)
        global_first_id = self.global_id(self.current_id)
        self.histogram[global_first_id] += 1

    def make_values(self):
        """ Creates a list of values for a given grid """
        # Init value container
        values = []
        # 1st value mod octave
        first_step = self.all_values[0] % len(self.interaction_grid)

        # Roll the grid so that it starts at the first_step
        grid_shift = len(self.interaction_grid) - first_step
        rolled_grid = np.roll(self.interaction_grid, grid_shift)

        # Iterate cyclically (?) over the rolled_grid     
        cycle = itr.cycle(rolled_grid)
        value = self.all_values[0]         # 21
        last_value = self.all_values[-1]   # 108
        while value <= last_value:
            in_grid = cycle.next()
            # if the value if allowed by the grid
            if in_grid == 1:
                values.append(value)
            value += 1

        return values

    def update(self):
        self.values     = self.make_values()
        self.size       = len(self.values)
        self.id_space   = range(self.size)
        self.cyclic_ids = itr.cycle(self.id_space)
        self.make_S()

    def set_scale(self, grid):
        """ Avaiable notes are defined by this 1/0 grid """
        self.interaction_grid = grid
        self.update()

    # OBSOLETE ?
    def shift_scale(self, shift):
        """ This is importando """
        self.interaction_grid = np.roll(self.interaction_grid, shift)
        self.update()

    def global_id(self, local_id):
        """ Global to local idx converter """
        value = self.values[local_id]
        global_id = self.all_values.index(value)
        return global_id

    def A_it_jt(self, it, jt = 0):
        """ Aij definition """
        pdf = up.tomek_pdf(self.bias)
        global_it = self.global_id(it)
        # pdf refers to all the keys, not just allowed ones
        out = pdf(global_it)
        return out

    def get_histogram(self):
        """ Research helper """
        return self.global_id_space, self.histogram

    def show_histogram(self):
        """ Pretty please keep plots pretty """
        plt.bar(self.all_values, self.histogram, color = 'k', alpha = 0.5)
        plt.show()

    def next_value(self):
        """ Make a merw step """
        if self.is_merw:
            # Probabilism
            probabilities = self.S[self.current_id, :]

            # Get next ID
            next_id = up.randomly_draw(self.id_space, probabilities)
            self.current_id = next_id
        else:
            # Determinism
            self.current_id = self.cyclic_ids.next()

        # Update histogram
        # Here is the only change wrt parent next_value() function
        global_current_id = self.global_id(self.current_id)
        self.histogram[global_current_id] += 1

        # Return value
        return self.values[self.current_id]

    def show_bias(self):
        """ Plot atractor """
        x = np.linspace(min(self.global_id_space), max(self.global_id_space), 1001)
        y = self.A_it_jt(x)
        plt.plot(x, y)
        plt.show()

class VolumeWalker(BiasedWalker):
    """ Volume dedicated """
    def __init__(self, first_vol):
        """ el Creador """
        # MIDI volume goes 0::127
        values      = range(128)
        first_id    = first_vol
        BiasedWalker.__init__(self, values, first_id, True)

        # By default allow more distinct volume changes
        self.set_max_step(15)

    def set_volume(self, vol):
        """ simple """
        self.set_bias(vol)

class GraphWalker(BiasedWalker):
    def __init__(self, first_chord, graph)  :
        # number of vertices
        self.graph     = graph
        self.n_vert    = len(graph)

        # vertices numeration starts from 1
        values      = range(1, self.n_vert + 1)
        first_id    = first_chord

        # Init parent
        BiasedWalker.__init__(self, values, first_id, False)

        # Allow interaction between every pair of indices
        self.set_max_step(self.n_vert)

    def make_A(self):
        """ Prepare adjacency matrix """
        A = np.zeros((self.size, self.size))

        for it in range(self.size):
            for jt in range(self.size):
                    A[it, jt] = self.A_it_jt(it, jt)
        self.A = A

    def A_it_jt(self, it, jt):
        # vertices numeration starts from 1
        if jt + 1 in self.graph[it + 1]:
            # if there is an edge from it to jt
            return 1
        else:
            # no edge
            return 0

