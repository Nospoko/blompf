import time
import pickle
import string
import numpy as np
import logging as log
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

    # Start logging
    logfile = 'logs/' + prefix + '.log'
    log.basicConfig(format = "[%(asctime)s](%(module)s:"
                             "%(funcName)s:%(lineno)d) %(message)s",
                    datefmt   = '%I:%M:%S',
                    level     = log.DEBUG,
                    filename  = logfile)

    print 'Generated prefix: ', prefix

    # Adjust time in seconds
    # This is set also in utils.midi
    time_per_tick = 2**-5
    intro_time = 3
    music_time = 1 * 60 + 0 - intro_time
    final_tick = int(music_time / time_per_tick)
    # Remove a little at the end to let it ring
    nof_steps = final_tick - 40

    # Define metre (5/4)
    metre_up   = 5.
    metre_down = 4.
    whole_note = 2**6
    bar_length = int((metre_up/metre_down)*whole_note)
    
    # Time left after the end of the last bar
    after_eof_bar = nof_steps % bar_length
    # Shorten the piece so that it ends along with a bar
    nof_steps -= after_eof_bar

    # Player
    hand = wh.ExampleHand(bar_length)

    # Make music
    for tick in range(nof_steps):
        hand.play(tick)

    # Show full piano-roll
    hand_notes = hand.get_notes()
    hand_notes[-1][2] = final_tick - hand_notes[-1][1]
    # um.show_piano_roll(hand.get_notes())

    # Save everything
    midipath = 'scores/'

    handfile = midipath + prefix + 'hand.mid'
    um.matrix_to_midi(hand_notes, handfile)
    print 'Notes saved to: ', handfile

    # Show chord-only piano-roll
    chord_notes = hand.meta_walkers['rhythm'].get_notes()
    # FIXME why aren't they ending properply?
    # Extend for compatibility with the hand notes
    chord_notes[-1][2] = final_tick - chord_notes[-1][1]

    print hand_notes[-1][1], hand_notes[-1][2]
    # um.show_piano_roll(chord_notes)
    chordfile = midipath + prefix + 'chords' + '.mid'
    um.matrix_to_midi(chord_notes, chordfile)
    print 'Chords saved to: ', chordfile

    # Show key-only piano-roll
    scale_notes = hand.meta_walkers['scale'].get_notes()
    # Extend those as well
    scale_notes[-1][2] = final_tick + scale_notes[-1][1]

    scalefile = midipath + prefix + 'scales.mid'
    um.matrix_to_midi(scale_notes, scalefile)
    print 'Scales saved to: ', scalefile

    finger_notes = []
    for fi in hand.fingers:
        fi_notes = fi.get_notes()
        fi_notes[-1][2] = final_tick + fi_notes[-1][1]
        finger_notes.append(fi_notes)

    # Save played notes and some meta-notes
    savepath = prefix + 'blompf_data.pickle'
    savedict = { 'hand'     : hand_notes,
                 'chord'    : chord_notes,
                 'scale'    : scale_notes,
                 'fingers'  : finger_notes }

    with open(savepath, 'wb') as fout:
        pickle.dump(savedict, fout)
    print 'Blompf data dict saved to: ', savepath

    log.info("finished {}".format(savepath))

    # Have fun
    return hand

if __name__ == '__main__':
    """ what up """
    hand = main()
