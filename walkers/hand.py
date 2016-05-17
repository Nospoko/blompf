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

        # FIXME this is shit
        self.uptime_walker = wm.UpTimeWalker(2)
        self.uptime_ticks_left = 32

        # Add 5 fingers
        for start in [48 + 12 * it for it in range(5)]:
            finger = wf.MerwFinger(start)
            # Go to D-maj
            finger.pitch_walker.shift_scale(2)
            self.fingers.append(finger)

        # TODO Is this what you want
        # Each should have its own TimeWalker
        # We also might want to move it to the abstract parent
        chord_walker = wm.ChordWalker(self.fingers)
        self.meta_walkers.update({'chord' : chord_walker})
        scale_walker = wm.ScaleWalker(self.fingers)
        self.meta_walkers.update({'scale' : scale_walker})
        # speed_walker = wm.SpeedWalker(self.fingers)
        # self.meta_walkers.update({'speed' : speed_walker})

        self.speed_histo = []

    def special_tasks(self, timetick):
        """ Whatever the wheather """
        # FIXME this here for tmp
        for walker in self.meta_walkers.itervalues():
            walker.play(timetick)

        if self.uptime_ticks_left is 0:
            # Shuffle speed (-1 as fast is set to be mre likely)
            speeds = [-1, -1, -1, 0, +1]
            speed = np.random.choice(speeds)
            print 'changin speed to:', speed
            self.speed_histo.append(speed)

            for fin in self.fingers:
                fin.set_prefered_speed(speed)

            # Shuffle volumes
            new_volumes = []
            for finger in self.fingers:
                if np.random.random() < 0.6:
                    finger.set_prefered_volume(-1)
                    new_volumes.append(-1)
                else:
                    new_vol = 30 + np.floor(80 * np.random.random())
                    finger.set_prefered_volume(new_vol)
                    new_volumes.append(new_vol)

            print 'new volumes:', new_volumes

            # Shuffle piczes
            new_piczes = []
            for finger in self.fingers:
                # And prefered pitch value
                if np.random.random() < 0.15:
                    finger.set_prefered_pitch(-1)
                    new_piczes.append(-1)
                else:
                    # TODO some meta-preference would be nice
                    # 88 is number of keys on our keyboard
                    new_picz = 0 + np.floor(88.0 * np.random.random())
                    # print 'set new picz:', new_picz
                    finger.set_prefered_pitch(new_picz)
                    new_piczes.append(new_picz)

            print 'new piczes:', new_piczes

            # Reset cunter
            self.uptime_ticks_left = self.uptime_walker.next_value() -1
        else:
            self.uptime_ticks_left -= 1
