import numpy as np
import matplotlib.pyplot as plt
from utils import midi as um
from walkers import finger as wf

if __name__ == '__main__':
    """ what up """
    # How many steps will walker walk
    nof_steps = 250
    finger = wf.ExampleFinger()

    for tick in range(nof_steps):
        finger.play(tick)

    um.show_piano_roll(finger.get_notes())

    # TODO New interface:
    # hands = create_hands()
    # for c_time in range(nof_steps):
    #     hands.set_something(c_time)
    #     for finger in hands:
    #         finger.play(c_time)
    # notes = hands.get_notes()
    # create_midi(notes)
