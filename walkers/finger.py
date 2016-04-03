import numpy as np

class Finger(object):
    """ Abstracts a separate human finger's piano abilities """
    def __init__(self):
        """ yo """
        self.notes = []

    def get_notes(self):
        """ Return pieciolinia """
        return self.notes

    def play(self, time):
        """ Hits a note when time is right """
        if self.is_it_now(time):
            self.make_note()
        else:
            pass

    def make_note(self):
        """ Generates a new note played by this finger """
        # All of those must be implemented
        pitch       = self.next_pitch()
        # TODO consider expressing time in ticks (int)
        time        = self.next_time()
        duration    = self.next_duration()
        volume      = self.next_volume()

        self.notes.append([pitch, time, duration, volume])

    def is_it_now(self, time):
        """ Rhytm depends on this function """
        # TODO this is fake
        return np.random.random() > 0.5

    def next_pitch(self):
        """ Choose note """
        pitch = self.pitch_walker.get_next()

        return pitch

class ExampleFinger(Finger):
    """ Example class exploring finger possibilites """
    def __init__(self):
        # Init parent class
        Finger.__init__(self)

    def is_it_now(self, time):
        """ Time is tick """
        # Play a note every 8 ticks
        itis = time % 8 is 0
        return itis

    def next_pitch(self):
        """ Choose note frequency """
        # Dupa
        return 70

    def next_duration(self):
        """ Choose note length """
        # Here it is always 4 tick long
        duration = 4
        return duration

    def next_volume(self):
        """ Choose volume """
        # Whatever here
        volume = 80 * 20 * np.random.random()
        return volume

    def next_time(self):
        """ This is tricky """
        # TODO implement me
        return 0.0


