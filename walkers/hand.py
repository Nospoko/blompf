import numpy as np
from walkers import finger as wf
from utils import midi as um

class Hand(object):
    """ Wrapper for multiple fingers """
    def __init__(self):
        """ el creador """
        # Init finger container
        self.fingers = []

    def play(self, timetick):
        """ Progress notes """
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

        # Add 5 fingers
        for start in [40 + 5*it for it in range(5)]:
            self.fingers.append(wf.MerwFinger(start))

    def twist_fingers(self):
        """ Randomly set some prefered pitch values """
        # TODO Do the pitches correctly!
        for finger in self.fingers:
            if np.random.random() < 0.5:
                finger.set_prefered_pitch(-1)
            else:
                new_picz = 20 + np.floor(60.0 * np.random.random())
                finger.set_prefered_pitch(new_picz)

