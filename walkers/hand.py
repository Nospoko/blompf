import numpy as np
from utils import midi as um
from walkers import merw as wm
from walkers import finger as wf

class Hand(object):
    """ Wrapper for multiple fingers """
    def __init__(self):
        """ el Creador """
        # Init finger container
        self.fingers = []
        # Meta-walkers container as well
        self.specials = []

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
        pass

class ExampleHand(Hand):
    """ Wrapper for multiple fingers """
    def __init__(self):
        """ el creador """
        # Init parent
        Hand.__init__(self)

        self.uptime_walker = wm.UpTimeWalker(2)
        self.uptime_ticks_left = 32

        # Add 5 fingers
        for start in [48 + 12 * it for it in range(5)]:
            self.fingers.append(wf.MerwFinger(start))

        # Add special tasks
        # (chords, scale changes, and other power-ups)

        # Assumes we start ad C-maj/A-min scale
        self.scale_notes = [[60, 0, 40, 100]]

        self.speed_histo = []
        self.scale_histo = []

    def get_scale_notes(self):
        """ Return notes coresponding to the changes of scale """
        return self.scale_notes

    def special_tasks(self, timetick):
        """ Whatever the wheather """
        if self.uptime_ticks_left is 0:
            # Play chord
            howmany = 0
            for fin in self.fingers:
                if np.random.random() < 0.81:
                    fin.hitme()
                    howmany += 1
            print 'chord at', timetick, 'with {} fingers'.format(howmany)

            # Shuffle speed (-1 as fast is set to be mre likely)
            speeds = [-1, -1, -1, 0, +1]
            speed = np.random.choice(speeds)
            print 'changin speed to:', speed
            self.speed_histo.append(speed)

            for fin in self.fingers:
                if np.random.random() < 1.81:
                    fin.set_prefered_speed(speed)

            # Shift scale 3 up or 5 down
            shift_factor = np.random.random()
            if shift_factor < 0.2:
                shift = 7
            elif shift_factor < 0.4:
                shift = 5
            elif shift_factor < 0.6:
                shift = 5
            elif shift_factor < 0.8:
                shift = 7
            else:
                shift = -7

            # Move scale value from previous one
            # FIXME uncertain about the sign here
            scale_pitch = self.scale_notes[-1][0] - shift

            # Prevent going off the keyboard
            if scale_pitch < 60:
                scale_pitch += 12
            elif scale_pitch >= 72:
                scale_pitch -= 12
            self.scale_notes.append([scale_pitch, timetick, 40, 100])

            new_piczes = []
            new_volumes = []
            for finger in self.fingers:
                # Change scale in each finger
                # finger.pitch_walker.shift_scale(shift)

                # And prefered pitch value
                if np.random.random() < 0.2:
                    finger.set_prefered_pitch(-1)
                    new_piczes.append(-1)
                else:
                    # TODO some meta-preference would be nice
                    new_picz = 0 + np.floor(90.0 * np.random.random())
                    # print 'set new picz:', new_picz
                    finger.set_prefered_pitch(new_picz)
                    new_piczes.append(new_picz)

                if np.random.random() < 0.6:
                    finger.set_prefered_volume(-1)
                    new_volumes.append(-1)
                else:
                    new_vol = 30 + np.floor(80 * np.random.random())
                    finger.set_prefered_volume(new_vol)
                    new_volumes.append(new_vol)

            print 'new piczes:', new_piczes
            print 'new volumes:', new_volumes

            # Reset cunter
            self.uptime_ticks_left = self.uptime_walker.next_value() -1
        else:
            self.uptime_ticks_left -= 1
