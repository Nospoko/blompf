import numpy as np
import matplotlib.pyplot as plt
import merw as mw

if __name__ == '__main__':

    # How many positions can walker occupy
    nof_spots = 80

    # Calculate probability matix holding S
    walker = mw.Merw(nof_spots)

    # Do research
    histogram = np.zeros(nof_spots)

    # Prepare list of indexes
    values = range(nof_spots)

    # Pitches are what we actually calculate
    # and they start from 30 and iterate like indexes
    pitches = [x + 30 for x in values]

    # Merw starting position set
    pos = 33
    positions = []

    # Walk

    # Prepare meta potential for testing
    # Number of iterations
    def meta_pot(it):
        ret = 70.0 * (0.5 * (1.0 + np.cos(8.*it*np.pi/N_)))
        #print ret
        return ret

    for it in range(N_):
        # Histogram
        histogram[pos] += 1

        positions.append(pos)
        next_pos = merw.get_next_value(pos)

        # Move
        if (it%20 == 0):
            shift = random.randint(-5,5)
            shift = 3
            merw.set_scale_shift(shift)
            print it, '/', N_, 'current position: ', pos,\
                    'changing scale:', shift
        merw.set_prefered(int(meta_pot(it)))

        # Switcheroo
        pos = next_pos

    # Create final pitches vector
    merw_pitches = [pitches[pos] for pos in positions]
    # Make midi file with calculated pitches
    make_midi(merw_pitches)


    #S = merw.get_S(); plt.imshow(S); plt.show()
    S = merw.get_S(); plt.imshow(S); plt.savefig('S.png')
    plt.clf()

    #plt.plot(histogram,'ko'); plt.show()
    plt.plot(histogram,'ko'); plt.savefig('histogram.png')
    plt.clf()
#
#    plt.plot(positions, 'ko'); plt.show()
    plt.plot(positions, 'ko'); plt.savefig('walk.png')
    plt.clf()
