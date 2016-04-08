import numpy as np
import matplotlib.pyplot as plt
from utils import midi as um
from walkers import finger as wf
from walkers import hand as wh
from walkers import merw as wm

if __name__ == '__main__':
    """ what up """
    # How many steps will walker walk
    nof_steps = 500

    biased = wm.BiasedWalker(20)
    path = [biased.current_value()]

    wavy = lambda x: np.cos(2.0 * x) * np.sin(5.0 * x)
    prefered = lambda x: 50 + 40 * wavy(7.2 * x / nof_steps)

    for tick in range(nof_steps):
        biased.set_bias(prefered(tick))
        path.append(biased.next_value())

        if tick%10 is 0:
            print tick

    biased.show_histogram()

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
