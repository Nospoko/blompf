import numpy as np
from walkers import merw as wm
from walkers import finger as wf
from utils import midi as um

class Hand(object):
    """ Wrapper for multiple fingers """
    def __init__(self):
        """ el Creador """
        # Init finger container
        self.fingers = []

    def special_tasks(self, timestick):
        """ All kinds of things """
        pass

    def play(self, timetick):
        """ Progress notes """
        self.special_tasks(timetick)

        for finger in self.fingers:
            finger.play(timetick)

    def get_notes(self):
        """ Concetanated notes from each finger """
        notes = []

        for finger in self.fingers:
            for note in finger.get_notes():
                notes.append(note)

        return notes

    def show_piano_roll(self):
        """ Pieciolinia """
        um.show_piano_roll(self.get_notes())

class ExampleHand(Hand):
    """ Wrapper for multiple fingers """
    def __init__(self):
        """ el creador """
        # Init parent
        Hand.__init__(self)

        self.uptime_walker = wm.UpTimeWalker(2)
        self.uptime_ticks_left = 0

        # Add 5 fingers
        for start in [30 + 11 * it for it in range(5)]:
            self.fingers.append(wf.MerwFinger(start))

        self.speed_histo = []
        self.scale_histo = []

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
            speeds = [-1, -1, 0, +1]
            speed = np.random.choice(speeds)
            print 'changin speed to:', speed
            self.speed_histo.append(speed)

            for fin in self.fingers:
                if np.random.random() < 0.81:
                    fin.set_prefered_speed(speed)

            # Shift scale 3 up or 5 down
            shift_factor = np.random.random()
            if shift_factor < 0.2:
                shift = 3
            elif shift_factor < 0.4:
                shift = 5
            elif shift_factor < 0.6:
                shift = 7
            elif shift_factor < 0.8:
                shift = 9
            else:
                shift = -2

            self.scale_histo.append(shift)
            print 'scale shift:', shift

            new_piczes = []
            new_volumes = []
            for finger in self.fingers:
                # Change scale in each finger
                finger.pitch_walker.shift_scale(shift)

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

            # Some other tricks
            self.twist_fingers()

            # Reset cunter
            self.uptime_ticks_left = self.uptime_walker.next_value() -1
        else:
            self.uptime_ticks_left -= 1

    def twist_fingers(self):
        """ Randomly set some prefered pitch values """
        # This is not happening
        if np.random.random() < 0.0:
            go_major = np.random.random() > 0.5
            print 'changin scale majority to', go_major
            for finger in self.fingers:
                finger.pitch_walker.set_scale_major(go_major)

