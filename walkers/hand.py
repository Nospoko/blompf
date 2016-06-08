import numpy as np
from utils import midi as um
from walkers import merw as wm
from walkers import finger as wf

class Hand(object):
    """ Wrapper for multiple fingers """
    def __init__(self):
        """ el Creador """
        # Init finger container
        self.fingers        = []
        # Meta-walkers container as well
        # Those are different object so we need a dict to differentiate
        # (Altough currently this feature is not used)
        # Each of the meta walkers must have a .play(timetick) method
        self.meta_walkers   = {}

    def get_notes(self):
        """ Concetanated notes from each finger """
        notes = []

        for finger in self.fingers:
            for note in finger.get_notes():
                notes.append(note)

        return notes

    def play(self, timetick):
        """ Progress notes """
        self.special_tasks(timetick)

        # TODO This is how we want this
        # for special in self.specials:
        #     special.play(timetick)

        for finger in self.fingers:
            finger.play(timetick)

    def show_piano_roll(self):
        """ Pieciolinia """
        um.show_piano_roll(self.get_notes())

    def special_tasks(self, timestick):
        """ All kinds of things """
        for walker in self.meta_walkers.itervalues():
            walker.play(timetick)

class ExampleHand(Hand):
    """ Wrapper for multiple fingers """
    def __init__(self):
        """ el creador """
        # Init parent
        Hand.__init__(self)

        # Add 5 fingers [C E G c c]
        # Those are the zero-notes from which we jump
        # onto the first ones
        for start in [30, 41, 48, 49, 62]:
            finger = wf.MerwFinger(start)
            # This might allow chord only walks over the whole piano
            finger.pitch_walker.set_max_step(5)
            self.fingers.append(finger)

        # This has its own rhythm
        chord_walker = ChordWalker(self.fingers)
        self.meta_walkers.update({'chord' : chord_walker})

        # Chord walking duet ???
        # b_chord_walker = ChordWalker(self.fingers)
        # b_chord_walker.time_walker.values = [32+8*it for it in range(6)]
        # self.meta_walkers.update({'chord_b' : b_chord_walker})

        # TODO consider some kind of signal/slot mechanism?
        scale_walker = ScaleWalker(self.fingers)
        self.meta_walkers.update({'scale' : scale_walker})

        # TODO Think of some better name for this fellow
        m_volume_walker = MetaVolumeWalker(self.fingers)
        self.meta_walkers.update({'volume' : m_volume_walker})

        # Currently speed is set for every finger separateley
        speed_walker = SpeedWalker(self.fingers)
        self.meta_walkers.update({'speed' : speed_walker})

        # This is fun
        pitch_twist = PitchTwister(self.fingers)
        self.meta_walkers.update({'pitchtwist' : pitch_twist})

    def special_tasks(self, timetick):
        """ Whatever the wheather """
        for walker in self.meta_walkers.itervalues():
            walker.play(timetick)

class HandWalker(object):
    """ Abstract class for walkers of the hand """
    def __init__(self, fingers):
        """ Reference to the finger list is obligatory here """
        # TODO add/remove fingers?
        self.fingers = fingers

        self.time_walker = wm.TimeWalker(3)
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
        # TODO This seems unnecessary
        HandWalker.__init__(self, fingers)

    def play(self, timetick):
        """ Do your job """
        if self.is_it_now(timetick):
            # How long till the next chord strucks
            duration = self.next_duration(timetick)

            howmany = 0
            for finger in self.fingers:
                # TODO This should be a parameter
                if np.random.random() < 0.81:
                    # Forces finger to play at this timetick
                    finger.hitme()
                    howmany += 1
            print 'ooo Chord at {} with {} fingers | time {}'\
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

        self.time_walker.current_id += 3
        # TODO Make it a thing
        # Add some twist:
        self.time_walker.values = [64 for it in range(10)]

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
            if np.random.random() < 0.42:
                # range(4)
                shifts = range(5)
                shift = np.random.choice(shifts)
                print '--- SCALE CHANGE | ', shift

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

            # Maybe for each finger separateley?
            # Set new scales
            # Randomistically
            if True:
                rndm = np.random.random()
                if rndm < 0.25:
                    scale = np.roll(self.domin_grid, self.shift)
                    print '---> Dominanta!'
                elif rndm < 0.3:
                    scale = np.roll(self.tonic_grid, self.shift)
                    print '---> Tonika!'
                elif rndm < 0.5:
                    scale = np.roll(self.subdo_grid, self.shift)
                    print '---> Subdominanta!'
                # elif rndm < 0.89:
                #     scale = np.roll(self.weird_grid , self.shift)
                #     print '---> Awkward!'
                else:
                    scale = np.roll(self.c_maj_grid, self.shift)
                    print '---> Wszystko!'
            else:
                # Deterministically
                which = self._grid_cunter % 4
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
                    scale = np.roll(self.tonic_grid, self.shift)
                    print 'Tonic!'


            for finger in self.fingers:
                # in each finger
                finger.set_scale(scale)

            # Reset cunter
            self.ticks_left = duration - 1
        else:
            pass

class SpeedWalker(HandWalker):
    def play(self, timetick):
        """ Work """
        if self.is_it_now(timetick):
            # How long till the next chord strucks
            duration = self.next_duration(timetick)

            # Shuffle speed (-1 as fast is set to be mre likely)
            speeds = [-1, 0, 1]

            new_speeds = []

            for finger in self.fingers:
                if np.random.random() < 0.81:
                    speed = np.random.choice(speeds)
                    finger.set_prefered_speed(speed)
                    new_speeds.append(speed)
                else:
                    # FIXME Why is there no turn off speed setting?
                    # Do not change speed
                    new_speeds.append(-10)

            # Reset cunter
            self.ticks_left = duration - 1

            print '+++ Speed set to: ', new_speeds, " | ", timetick

class PitchTwister(HandWalker):
    """ HI """
    def play(self, timetick):
        """ YO """
        if self.is_it_now(timetick):
            # How long till the next chord strucks
            duration = self.next_duration(timetick)

            new_piczes = []

            for finger in self.fingers:
                # And prefered pitch value
                if np.random.random() < 0.15:
                    finger.set_prefered_pitch(-1)
                    new_piczes.append(-1)
                else:
                    # TODO some meta-preference would be nice
                    # 88 is the number of keys on our keyboard
                    new_picz = 0 + np.floor(88.0 * np.random.random())
                    # print 'set new picz:', new_picz
                    finger.set_prefered_pitch(new_picz)
                    finger.hitme()
                    new_piczes.append(new_picz)

            # Reset cunter
            self.ticks_left = duration - 1

            print '^^^ new piczes:', new_piczes

class MetaVolumeWalker(HandWalker):
    """ Volume dynamics controller """
    def __init__(self, fingers):
        """ Konstruktor """
        # Seems obsolete
        HandWalker.__init__(self, fingers)

    def play(self, timetick):
        """ Do your job """
        if self.is_it_now(timetick):
            # How long till the next chord strucks
            duration = self.next_duration(timetick)

            new_volumes = []
            for finger in self.fingers:
                if np.random.random() < 0.81:
                    new_vol = 50 + np.floor(70 * np.random.random())
                    finger.set_prefered_volume(new_vol)
                    new_volumes.append(new_vol)
                else:
                    # Turn off
                    finger.set_prefered_volume(-1)
                    new_volumes.append(-1)

            # Reset cunter
            self.ticks_left = duration - 1

            print '---> Volumes set: ', new_volumes, ' |', timetick

