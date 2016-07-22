import numpy as np
import itertools as itr
from utils import midi as um
from walkers import merw as wm
from utils import harmony as uh
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

        # Return sorted
        notes.sort(key=lambda x: x[1]+x[2])

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
        for start in [70, 64, 38, 40, 59]:
            finger = wf.MerwFinger(start)
            # This might allow chord only walks over the whole piano
            finger.pitch_walker.set_max_step(4)
            self.fingers.append(finger)

        # TODO Make one RhythmWalker encapsulating multiple ChordWalkers
        # This has its own rhythm
        chord_walker = ChordWalker(self.fingers)
        a_rhythms = [16, 32, 48, 64, 16, 96, 128,
                     112, 16, 80, 16, 48, 32, 16]
        # a_rhythms = [124, 24, 24, 32, 132, 148, 48, 48, 16, 116, 16]
        chord_walker.time_walker.set_values(a_rhythms)
        chord_walker.time_walker.set_probabilism(True)
        self.meta_walkers.update({'chord' : chord_walker})

        # Chord walking duet ???
        b_chord_walker = ChordWalker(self.fingers)
        b_rhythms = [32, 32, 32, 16, 16, 32, 16, 16, 112, 32, 32, 16, 112]

        b_chord_walker.time_walker.set_values(b_rhythms)
        # b_chord_walker.time_walker.set_probabilism(True)
        self.meta_walkers.update({'chord_b' : b_chord_walker})

        # TODO consider some kind of signal/slot mechanism?
        scale_walker    = ScaleWalker(self.fingers)
        self.meta_walkers.update({'scale' : scale_walker})

        # TODO Think of some better name for this fellow
        m_volume_walker = MetaVolumeWalker(self.fingers)
        self.meta_walkers.update({'volume' : m_volume_walker})

        # Currently speed is set for every finger separateley
        speed_walker    = SpeedWalker(self.fingers)
        self.meta_walkers.update({'speed' : speed_walker})

        # This is fun
        pitch_twist     = PitchTwister(self.fingers)
	# FIXME what is up with this, negotiate with chord walkers maybe?
        pitch_twist.time_walker.values = [42 for it in range(8)]
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

        self.time_walker = wm.TimeWalker()
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

        # Return sorted pls
        self.notes.sort(key=lambda x: x[1]+x[2])

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

        # Make Chords go deterministically pls
        self.time_walker.set_probabilism(False)

    def play(self, timetick):
        """ Do your job """
        if self.is_it_now(timetick):
            # How long till the next chord strucks
            duration = self.next_duration(timetick)

            howmany = 0
            for finger in self.fingers:
                # TODO This should be a parameter
                if np.random.random() < 0.4:
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

        # self.time_walker.current_id += 2
        # TODO Make it a thing
        # Add some twist:
        # time_vals = [123 for _ in range(10)]
        # time_vals = [32 for _ in range(10)]
	time_vals = [128, 32, 128, 32, 64, 128, 64, 32, 16, 32, 128]
        self.time_walker.set_values(time_vals)

        # Do not start with a scale change
        self.ticks_left = self.next_duration(0)

        # Fibbonnaccish cycle
        # Make random
        self.shifts = itr.cycle([1, 2, 5, 6, 4])
        self.shift = 0
        # TODO Try to abstract this out somehow
        # Major           [C, -, D, -, E, F, -, G, -, A, -, H]
        self.full_scale = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]

        self.chord_generator = uh.ChordGenerator()
        self.graph = {
                    1: [4, 5, 3, 2, 6, 7],
                    2: [5],
                    3: [1, 4, 6],
                    4: [5, 1, 7],
                    5: [1, 6],
                    6: [4],
                    7: [1]
                    }

        self.chord = 1

        # FIXME This should not be hard-coded in here
        # But keep track from the beginning
        self.notes.append([60, 0, 40, 100])

    def chord_prog(self):
        """ Make chords progress """
        possible = self.graph[self.chord]
        self.chord = np.random.choice(possible)

        # TODO Add logs pls
        rndm = np.random.random()
        if rndm < 0.1:
            grid = self.chord_generator.get_triad(self.chord)
        elif rndm < 0.35:
            grid = self.chord_generator.get_sextic(self.chord)
        elif rndm < 0.7:
            grid = self.chord_generator.get_septimic(self.chord)
        else:
            grid = self.chord_generator.get_nonic(self.chord)

        return grid

    def play(self, timetick):
        """ ayayay """
        if self.is_it_now(timetick):
            # How long till the next scale change
            duration = self.next_duration(timetick)

            # Maybe Shift scale 
            shift = 0
            if np.random.random() < 1.8:
                # range(5)
                # shifts = [2, 3, 4, 5]
                # shift = np.random.choice(shifts)
                shift = self.shifts.next()
                print '--- SCALE CHANGE | ', shift

                # Move scale value from previous one
                scale_pitch = self.notes[-1][0] + shift

                # Prevent going off the keyboard
                if scale_pitch < 60:
                    scale_pitch += 12
                elif scale_pitch >= 72:
                    scale_pitch -= 12
                self.notes.append([scale_pitch, timetick, 40, 100])

            # Cumulate shift
            self.shift += shift

            # Maybe for each finger separateley?
            # Set new scales
            if np.random.random() < 0.1:
                scale = np.roll(self.full_scale, self.shift)
                print '---> Full scale!'
            else:
                chord = self.chord_prog()
                scale = np.roll(chord, self.shift)
                print '---> ', chord

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
            speeds = [-1, -1, 0, 1]

            new_speeds = []

            # Set the same speed for each finger
            speed = np.random.choice(speeds)
            for finger in self.fingers:
                if np.random.random() < 0.81:
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
                if np.random.random() < 0.45:
                    finger.set_prefered_pitch(-1)
                    new_piczes.append(-1)
                else:
                    # TODO some meta-preference would be nice
                    # 88 is the number of keys on our keyboard
                    sector_low = 0
                    sector_range = 64
                    val = np.floor(sector_range * np.random.random())
                    new_picz = sector_low + val
                    # print 'set new picz:', new_picz
                    finger.set_prefered_pitch(new_picz)

                    # Maybe hit
                    if np.random.random() > 0.8:
                        finger.hitme()

                    # Log
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

