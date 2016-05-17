import time
import numpy as np
from utils import midi as um
from walkers import hand as wh
from walkers import merw as wm
import matplotlib.pyplot as plt
from walkers import finger as wf

def main(prefix = ''):
    """ python main.py """
    # How many steps will walker walk
    # 2k ~ 60s
    nof_steps = 14*512

    hand = wh.ExampleHand()

    for tick in range(nof_steps):
        hand.play(tick)

        if tick % 200 is 0:
            print 'main loop is now at tick:', tick

    # Show full piano-roll
    # um.show_piano_roll(hand.get_notes())

    midipath = 'scores/'

    handfile = midipath + prefix + 'hand.mid'
    um.matrix_to_midi(hand.get_notes(), handfile)
    print 'Notes saved to: ', handfile

    # Show chord-only piano-roll
    chord_notes = hand.meta_walkers['chord'].get_notes()
    # um.show_piano_roll(chord_notes)

    chordfile = midipath + prefix + 'chords.mid'
    um.matrix_to_midi(chord_notes, chordfile)
    print 'Chords saved to: ', chordfile

    # Show key-only piano-roll
    scale_notes = hand.meta_walkers['scale'].get_notes()
    # um.show_piano_roll(scale_notes)

    scalefile = midipath + prefix + 'scales.mid'
    um.matrix_to_midi(scale_notes, scalefile)
    print 'Scales saved to: ', scalefile

    return hand

if __name__ == '__main__':
    """ what up """
    hand = main()
