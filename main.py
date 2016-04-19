import numpy as np
import matplotlib.pyplot as plt
from utils import midi as um
from walkers import finger as wf
from walkers import hand as wh
from walkers import merw as wm

def main():
    """ python main.py """
    # How many steps will walker walk
    nof_steps = 10000

    hand = wh.ExampleHand()

    for tick in range(nof_steps):
        hand.play(tick)

        if tick % 200 is 0:
            print tick

    um.show_piano_roll(hand.get_notes())

    um.matrix_to_midi(hand.get_notes())

    return hand

if __name__ == '__main__':
    """ what up """
    hand = main()
