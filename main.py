import numpy as np
import matplotlib.pyplot as plt
from utils import midi as um
from walkers import finger as wf
from walkers import hand as wh
from walkers import merw as wm

if __name__ == '__main__':
    """ what up """
    # How many steps will walker walk
    nof_steps = 1000

    biased = wm.BiasedWalker(50)
    path = [biased.current_value()]

    prefered = lambda x: 50
    gamma    = lambda x: 0.08 + 20.0 * x / nof_steps

    for tick in range(nof_steps):
        biased.set_bias(50, gamma(tick))
        path.append(biased.next_value())

        if tick%10 is 0:
            print tick

    plt.plot(path, 'ko')
    plt.show()

    # hand = wh.ExampleHand()
    #
    # for tick in range(nof_steps):
    #     hand.play(tick)
    #
    # um.show_piano_roll(hand.get_notes())

    # TODO New interface:
    # hands = create_hands()
    # for c_time in range(nof_steps):
    #     hands.set_something(c_time)
    #     for finger in hands:
    #         finger.play(c_time)
    # notes = hands.get_notes()
    # create_midi(notes)
