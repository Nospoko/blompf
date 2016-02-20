import numpy as np
import matplotlib.pyplot as plt
import merwmidi as mm
import merw as mw

if __name__ == '__main__':
    """ what up """
    # How many positions can walker occupy
    nof_spots = 80

    # How many steps will walker walk
    nof_steps = 25000

    # Handles probabilities and potentials
    walker = mw.Merw(nof_spots)

    # Does research
    histogram = np.zeros(nof_spots)

    # Pitches are what we actually calculate
    # and they start from 30 and iterate like indexes
    pitches = [x + 30 for x in range(nof_spots)]

    # Merw starting position set
    pos = 33
    positions = []

    # First orbit 50
    # walker.set_prefered(50)

    for it in range(nof_steps):
        # Histogram
        histogram[pos] += 1

        positions.append(pos)
        next_pos = walker.get_next_value(pos)

        # Move
        if (it%20 == 0 and False):
            shift = np.random.randint(-5,5)
            shift = 3
            walker.set_scale_shift(shift)
            print it, '/', nof_steps, 'current position: ', pos,\
                    'changing scale:', shift

        if (it == nof_steps / 2):
            print "Testing some dumb method at iteration", it
            # Change orbit
            # walker.set_prefered(10)

        # Move, actually
        pos = next_pos

    # Create final pitches vector
    walker_pitches = [pitches[pos] for pos in positions]
    # Make midi file with calculated pitches
    # mm.make_midi(walker_pitches)

    plt.plot(histogram,'ko')
    plt.show()

    # plt.plot(positions, 'ko')
    # plt.show()
