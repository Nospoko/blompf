import time
import pickle
import string
import numpy as np
from utils import midi as um
from walkers import hand as wh
from walkers import merw as wm
import matplotlib.pyplot as plt
from utils import harmony as uh
from walkers import finger as wf

def main():
    """ python main.py """
    # Prepare random two-letter prefix
    low = string.ascii_lowercase
    prefix = "".join(list(np.random.choice(list(low), 2)))
    prefix += '_'

    print 'Generated prefix: ', prefix

    # How many steps will walker walk
    # 2k ~ 60s
    nof_steps = 512*6

    hand = wh.ExampleHand()

    # Make music
    for tick in range(nof_steps):
        hand.play(tick)

    # Show full piano-roll
    hand_notes = hand.get_notes()
    # um.show_piano_roll(hand.get_notes())

    # Save everything
    midipath = 'scores/'

    handfile = midipath + prefix + 'hand.mid'
    um.matrix_to_midi(hand_notes, handfile)
    print 'Notes saved to: ', handfile

    # Show chord-only piano-roll
    chord_notes = hand.meta_walkers['chord'].get_notes()
    # FIXME why aren't they ending properply?
    # Extend for compatibility with the hand notes
    chord_notes[-1][2] = hand_notes[-1][1] +\
                         hand_notes[-1][2] -\
                         chord_notes[-1][1]
    # um.show_piano_roll(chord_notes)

    chordfile = midipath + prefix + 'chords.mid'
    um.matrix_to_midi(chord_notes, chordfile)
    print 'Chords saved to: ', chordfile

    # Show key-only piano-roll
    scale_notes = hand.meta_walkers['scale'].get_notes()
    # Extend those as well
    scale_notes[-1][2] = hand_notes[-1][1] +\
                         hand_notes[-1][2] -\
                         scale_notes[-1][1]
    # um.show_piano_roll(scale_notes)

    scalefile = midipath + prefix + 'scales.mid'
    um.matrix_to_midi(scale_notes, scalefile)
    print 'Scales saved to: ', scalefile

    finger_notes = []
    for fi in hand.fingers:
        fi_notes = fi.get_notes()
        fi_notes[-1][2] = hand_notes[-1][1] +\
                          hand_notes[-1][2] -\
                          fi_notes[-1][1]
        finger_notes.append(fi_notes)

    # Save played notes and some meta-notes
    savepath = prefix + 'blompf_data.pickle'
    savedick = { 'hand'     : hand_notes,
                 'chord'    : chord_notes,
                 'scale'    : scale_notes,
                 'fingers'  : finger_notes }

    with open(savepath, 'wb') as fout:
        pickle.dump(savedick, fout)
    print 'Blompf data dict saved to: ', savepath

    # Have fun
    return hand

if __name__ == '__main__':
    """ what up """
    hand = main()
