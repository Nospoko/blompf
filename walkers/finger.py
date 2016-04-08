import numpy as np
from walkers import merw as wm

class Finger(object):
    """ Abstracts a separate human finger's piano abilities """
    def __init__(self):
        """ yo """
        self.notes = []

    def clear(self):
        """ Remove all previously played notes """
        self.notes = []

    def get_notes(self):
        """ Return pieciolinia """
        return self.notes

    def play(self, timetick):
        """ Hits a note when time is right """
        if self.is_it_now(timetick):
            self.make_note(timetick)
        else:
            pass

    def make_note(self, timetick):
        """ Generates a new note played by this finger """
        # TODO consider expressing time in ticks (int)
        note_start  = timetick
        # All of those must be implemented
        pitch       = self.next_pitch(timetick)
        duration    = self.next_duration(timetick)
        volume      = self.next_volume(timetick)

        self.notes.append([pitch, note_start, duration, volume])

    def is_it_now(self, timetick):
        """ Rhytm depends on this function """
        # TODO this is fake
        return np.random.random() > 0.5

    def next_pitch(self, timetick):
        """ Choose note """
        pitch = self.pitch_walker.get_next()

        return pitch

class ExampleFinger(Finger):
    """ Exemplary class exploring finger possibilites """
    def __init__(self, something = 0):
        """ le Constructor """
        # Init parent class
        Finger.__init__(self)
        self.first = something

    def is_it_now(self, timetick):
        """ Time is tick """
        # Play a note every 8 ticks
        itis = timetick % 8 is 0
        return itis

    def next_pitch(self, timetick):
        """ Choose note frequency """
        # Dupa
        out = self.first + 20 * np.cos(7.0 * timetick / 200)
        return out

    def next_duration(self, timetick):
        """ Choose note length """
        # Here it is always 4 tick long
        if timetick % 24 is 0:
            duration = 8
        else:
            duration = 4

        return duration

    def next_volume(self, timetick):
        """ Choose volume """
        # Whatever here
        if timetick % 24 is 0:
            volume = 120
        else:
            volume = 80 + 10 * np.random.random()
        return volume

class MerwFinger(Finger):
    """ Properly improvising finger """
    def __init__(self):
        """ yonstructor """
        Finger.__init__(self)
        # TODO Init merwish walkers
        # self.volume_walker = wm.VolumeWalker()
        print 'szalom'

    def is_it_now(self, timetick):
        """ merw way of the rhythm """
        pass

    def next_pitch(self, timetick):
        """ melody """
        # pitchmerw.set_something_depending_on_the(timetick)
        # return pitchmerw.get_next()
        pass

    # TODO This should be the simplest
    def next_volume(self, timetick):
        """ velocity """
        # Updates probabilities
        # self.volume_walker.set_time(timetick)

        # Makes a step
        # vol = self.volume_walker.get_next()
        # return vol
        pass

    def next_duration(self, timetick):
        """ Note length in ticks """
        # duration_merw.set_potentials(timetick)
        # return duration_merw.get_next()
        pass

