from walkers import finger as wf

class ExampleHand(object):
    """ Wrapper for multiple fingers """
    def __init__(self):
        """ el creador """
        # Init finger container
        self.fingers = []

        # Add 5 fingers
        for start in [60 + 5*it for it in range(5)]:
            self.fingers.append(wf.ExampleFinger(start))

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
