import numpy as np
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

        # TODO fiddle with that also
        self.max_dist = 2

        # This is the walking element
        self.current_id = first_id

        # This is the walking space
        self.id_space = range(self.size)

        # Init histogram container
        self.histogram = np.zeros_like(self.values)
        self.histogram[self.current_id] += 1

        # Initialize probability matrices
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
        # self.update_S()
        probabilities = self.S[:, self.current_id]

        # Get next ID
        next_id = up.randomly_draw(self.id_space, probabilities)
        self.current_id = next_id

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

class VolumeWalker(BiasedWalker):
    """ Volume dedicated """
    def __init__(self, first_vol):
        """ el Creador """
        # MIDI volume goes 0::127
        values      = range(128)
        first_id    = first_vol
        BiasedWalker.__init__(self, values, first_id)

    def set_volume(self, vol):
        """ simple """
        self.set_bias(vol)

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

class TimeWalker(BiasedWalker):
    """ Rhytm lives here """
    def __init__(self, first_id):
        """ nope """
        # Possible note values are always powers of 2
        # This is in ticks unit
        values = [2**it for it in range(1,9)]

        # Init parent
        BiasedWalker.__init__(self, values, first_id)

        # No sudden time changes
        self.set_max_step(1)

# TODO This should be a abstract walker with time values 
# related to musical measures (larger scale than single notes)
class UpTimeWalker(BiasedWalker):
    """ Rhytm lives here """
    def __init__(self, first_id):
        """ nope """
        # FIXME This walker differes only by values from
        # the other TimeWalker, ergo it's obsolete

        # Possible note values are always powers of 2
        # This is in ticks unit
        values = [8 + 8*it for it in range(3, 7)]

        # Init parent
        BiasedWalker.__init__(self, values, first_id)

        # No (very) sudden time changes
        self.set_max_step(3)

# Everything below probably deserves its own file
# And this could probably be something abstract
class HandWalker(object):
    """ Abstract class for walkers of the hand """
    def __init__(self, fingers):
        """ Reference to the finger list is obligatory here """
        # TODO add/remove fingers?
        self.fingers = fingers

        self.time_walker = TimeWalker(3)
        # Starts with a chord
        self.ticks_left = 0

        # We want to get MIDI files out of this as well
        self.notes = []

    def next_duration(self, timetick):
        """ Wtf """
        dur = self.time_walker.next_value()
        return dur

    def is_it_now(self, timetick):
        """ Timekeeping """
        if self.ticks_left == 0:
            return True
        else:
            # Iterate
            self.ticks_left -= 1
            return False

    def get_notes(self):
        """ Returns notes showing activity of this walker """
        # range(-1) is empty list
        for it in range(len(self.notes)-1):
            new_dur = self.notes[it+1][1] - self.notes[it][1]-0
            self.notes[it][2] = new_dur

        return self.notes

    def play(self, timetick):
        """ This should be overriden """
        # Keep this kind of logic in your walkers:
        if self.is_it_now(timetick):
            self.ticks_left -= 1
            dur = self.next_duration()
            self.ticks_left = dur - 1
        else:
            pass

class ChordWalker(HandWalker):
    """ This forces all of the hands fingers to hit a chord """
    def __init__(self, fingers):
        """ yo """
        HandWalker.__init__(self, fingers)

    def play(self, timetick):
        """ Do your job """
        if self.is_it_now(timetick):
            # How long till the next chord strucks
            duration = self.next_duration(timetick)

            howmany = 0
            for finger in self.fingers:
                # TODO This should be a parameter
                if np.random.random() < 0.71:
                    # Forces finger to play at this timetick
                    finger.hitme()
                    howmany += 1
            print 'Chord at {} with {} fingers | time {}'\
                    .format(timetick, howmany, timetick)

            # Take note
            self.notes.append([60, timetick, 16, 80])

            # Reset cunter
            self.ticks_left = duration - 1
        else:
            pass

class ScaleWalker(HandWalker):
    """ This is used to control the scale hand is playing on """
    def __init__(self, fingers):
        """ el Creador """
        HandWalker.__init__(self, fingers)

        # TODO Make it a thing
        # Add some twist:
        # self.time_walker.values = [40 + 10 * it for it in range(10)]

        # Do not start with a scale change
        self.ticks_left = self.next_duration(0)

        self.shift = 0
        # Major           [C, -, D, -, E, F, -, G, -, A, -, H]
        self.c_maj_grid = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
        self.tonic_grid = [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        self.subdo_grid = [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        self.domin_grid = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        self.third_grid = [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        self.weird_grid = [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0]
        self._grid_cunter = 0

        # FIXME This should not be hard-coded in here
        # But keep track from the beginning
        self.notes.append([60, 0, 40, 100])

    def play(self, timetick):
        """ ayayay """
        if self.is_it_now(timetick):
            # How long till the next scale change
            duration = self.next_duration(timetick)

            # Maybe Shift scale 
            shift = 0
            if np.random.random() < 0.2:
                # range(4)
                shifts = [0, 1, 2, 3]
                shift = np.random.choice(shifts)

            # Cumulate shift
            self.shift += shift

            # Move scale value from previous one
            scale_pitch = self.notes[-1][0] + shift

            # Prevent going off the keyboard
            if scale_pitch < 60:
                scale_pitch += 12
            elif scale_pitch >= 72:
                scale_pitch -= 12

            self.notes.append([scale_pitch, timetick, 40, 100])

            print 'Moving scale by {} | time = {}'\
                    .format(self.shift, timetick)

            # Maybe for each finger separateley?
            # Set new scales
            # Randomistically
            if True:
                rndm = np.random.random()
                if rndm < 0.2:
                    scale = np.roll(self.domin_grid, self.shift)
                    print '---> Dominanta!'
                elif rndm < 0.4:
                    scale = np.roll(self.tonic_grid, self.shift)
                    print '---> Tonika!'
                elif rndm < 0.6:
                    scale = np.roll(self.subdo_grid, self.shift)
                    print '---> Subdominanta!'
                elif rndm < 0.7:
                    scale = np.roll(self.third_grid, self.shift)
                    print '---> Ten trzeci'
                elif rndm < 0.9:
                    scale = np.roll(self.weird_grid, self.shift)
                    print '---> Dafuq chord'
                else:
                    scale = np.roll(self.c_maj_grid, self.shift)
                    print '---> Wszystko!'
            else:
                # Deterministically
                which = self._grid_cunter % 5
                self._grid_cunter += 1
                if which is 0:
                    scale = np.roll(self.tonic_grid, self.shift)
                    print 'Deterministic tonic'
                elif which is 1:
                    scale = np.roll(self.subdo_grid, self.shift)
                    print 'Subdominanta!'
                elif which is 2:
                    scale = np.roll(self.domin_grid, self.shift)
                    print 'Dominanta!'
                # elif which is 3:
                #     scale = np.roll(self.third_grid, self.shift)
                #     print 'Ten trzeci'
                else:
                    scale = np.roll(self.c_maj_grid, self.shift)
                    print 'Wszystko!'


            for finger in self.fingers:
                # in each finger
                finger.set_scale(scale)

            # Reset cunter
            self.ticks_left = duration - 1
        else:
            pass

