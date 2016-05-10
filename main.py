import numpy as np
from utils import midi as um
from walkers import hand as wh
from walkers import merw as wm
import matplotlib.pyplot as plt
from walkers import finger as wf

def main():
    """ python main.py """
    # How many steps will walker walk
    # 2k ~ 60s
    nof_steps = 1500

    hand = wh.ExampleHand()

    for tick in range(nof_steps):
        hand.play(tick)

        if tick % 200 is 0:
            print 'main loop is now at tick:', tick

    um.show_piano_roll(hand.get_notes())

    um.matrix_to_midi(hand.get_notes())

    return hand

if __name__ == '__main__':
    """ what up """
    hand = main()
