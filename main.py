import numpy as np
import matplotlib.pyplot as plt
from utils import midi as um
from walkers import finger as wf
from walkers import hand as wh

if __name__ == '__main__':
    """ what up """
    # How many steps will walker walk
    nof_steps = 250
    hand = wh.ExampleHand()

    for tick in range(nof_steps):
        hand.play(tick)

    um.show_piano_roll(hand.get_notes())

    # TODO New interface:
    # hands = create_hands()
    # for c_time in range(nof_steps):
    #     hands.set_something(c_time)
    #     for finger in hands:
    #         finger.play(c_time)
    # notes = hands.get_notes()
    # create_midi(notes)
