import numpy as np
from utils import midi as um
from walkers import merw as wm
from matplotlib import pyplot as plt

class Finger(object):
    """ Abstracts a separate human finger's piano abilities """
    def __init__(self):
        """ yo """
        # Init note container
        self.notes = []

        # Start with a note
        self.ticks_left = 0

        print 'finger was created'

    def clear(self):
        """ Remove all previously played notes """
        # FIXME histogram doesn't get cleared
        self.notes = []

    def get_notes(self):
        """ Return pieciolinia """
        return self.notes

    def show_piano_roll(self):
        """ Show pieciolinia """
        um.show_piano_roll(self.notes)

    def play(self, timetick):
        """ Hits a note when time is right """
        if self.is_it_now(timetick):
            self.make_note(timetick)
        else:
            pass

    def make_note(self, timetick):
        """ Generates a new note played by this finger """
        note_start  = timetick
        # All of those must be implemented
        pitch       = self.next_pitch(timetick)
        duration    = self.next_duration(timetick)
        volume      = self.next_volume(timetick)

        # Create note
        self.notes.append([pitch, note_start, duration, volume])

        # Reset cunter (-1 acounts for something FIXME)
        self.ticks_left = duration - 1

    def hitme(self):
        """ Force this finger to play as soon """
        # Last note should in that case end earlier than expected
        if len(self.notes) > 0:
            self.notes[-1][2] -= self.ticks_left
        self.ticks_left = 0

    def is_it_now(self, timetick):
        """ Rhytm depends on this function """
        # TODO another walker could be in control of that
        # Forced hit every so often
        # if self.up_time_walker.now(timetick):
        #     self.ticks_left = 0

        # if timetick % 42 is 0:
        #     self.ticks_left = 0

        if self.ticks_left is 0:
            return True
        else:
            self.ticks_left -= 1
            return False

    def next_pitch(self, timetick):
        """ Choose note """
        pitch = self.pitch_walker.get_next()

        return pitch

class MerwFinger(Finger):
    """ Properly improvising finger """
    def __init__(self, first_picz):
        """ yonstructor """
        Finger.__init__(self)
        # Init merwish walkers
        first_vol           = 70
        self.volume_walker  = wm.VolumeWalker(first_vol)
        # FIXME some id-value fuckup
        self.pitch_walker   = wm.PitchWalker(first_picz)
        # Note length are powers of 2 only
        self.time_walker = wm.TimeWalker()

    def next_duration(self, timetick):
        """ Note length (value) in ticks """
        dur = self.time_walker.next_value()
        return dur

    def next_pitch(self, timetick):
        """ melody """
        picz = self.pitch_walker.next_value()
        return picz

    def next_volume(self, timetick):
        """ velocity """
        vol = self.volume_walker.next_value()
        # TODO Adding accents would be possible just here
        return vol

    def set_scale(self, scale):
        """ Sets the scale grid """
        # Get ulamkowy position on the keybord
        cid = self.pitch_walker.current_id
        preposition = 1.0*cid / self.pitch_walker.size
        self.pitch_walker.set_scale(scale)

        # Recalculate position, try to land in the same place
        postposition = preposition * self.pitch_walker.size
        self.pitch_walker.current_id = int(postposition)

    def set_prefered_pitch(self, picz):
        """ sets the prefered pitch, bitch, -1 turn off """
        self.pitch_walker.set_bias(picz)

    def set_prefered_speed(self, slowfastnone):
        """ Sets how often notes are hit, arguments should be +1, 0, -1 """
        # FIXME this is esoteric as fuck
        # Slow
        if slowfastnone == 1:
            bias = self.time_walker.size - 1#7
        # Fast
        if slowfastnone == -1:
            bias = 1
        # Neither
        if slowfastnone == 0:
            bias = -1

        self.time_walker.set_bias(bias)

    def set_prefered_volume(self, vol):
        """ forte, piano """
        self.volume_walker.set_bias(vol)

    def show_histograms(self):
        """ Show histograms from all of the random walkers """
        v_ids, v_hist = self.volume_walker.get_histogram()
        # One row, Three columns, first plot
        plt.subplot(131)
        plt.title('volume')
        plt.bar(v_ids, v_hist, color='k', alpha=0.5)
        plt.xlim([0,128])

        p_ids, p_hist = self.pitch_walker.get_histogram()
        # second plot
        plt.subplot(132)
        plt.title('pitch')
        plt.bar(p_ids, p_hist, color='c', alpha=0.5)
        plt.xlim([0,128])

        t_ids, t_hist = self.time_walker.get_histogram()
        # third
        plt.subplot(133)
        plt.title('durations (log)')
        plt.bar(t_ids, t_hist, color='r', alpha=0.5)

        plt.show()

# OBSOLETE?
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

