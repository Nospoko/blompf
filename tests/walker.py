import numpy as np
from matplotlib import pyplot as plt
from utils import probability as up
from walkers import merw as wm

def test_biased():
    """ Perform some tests to see if BiasedWalker works as expected """
    # Declare test's intensity
    nof_steps = 5000

    # Start from 40 / 127
    walker = wm.BiasedWalker(range(100), 40)

    # Increase bias_power linearly
    bias_power = lambda x: 0.1 + 30.0 * x / nof_steps

    # Change prefered value as well
    bias_value = lambda x: 60 + 40.0 * np.cos(12 * np.pi * x/nof_steps)
    bias = 60

    path = [walker.current_value()]

    bias_switch = True

    for tick in range(nof_steps):
        # Change bias in larger steps
        if tick % 2000 is 0:
            bias_switch = not bias_switch
            print bias_switch, ' is the state of switch'
            if bias_switch:
                walker.set_bias(bias, 30)
            else:
                walker.set_bias(bias, 0.1)
            # walker.set_bias(bias, bias_power(tick))

        # qDebug() <<
        if tick % 50 is 0:
            print "Step: {}".format(tick)

        # FIXME walker should probably remember its path
        path.append(walker.next_value())

    walker.show_histogram()
    plt.plot(path, 'co')
    plt.show()

    return walker
