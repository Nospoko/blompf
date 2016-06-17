import numpy as np
import itertools as itr

class ChordGenerator(object):
    """ Will create any kind of triad with any kind of addition """
    def __init__(self):
        """ For now this is just shitload of chords wrapper """
        # Create basic triads for the base C scale
        # Major           [C, -, D, -, E, F, -, G, -, A, -, H]
        self.full_scale = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]

        self.triads = {
                      # [C, -, D, -, E, F, -, G, -, A, -, H]
                    1 : [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                    2 : [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                    3 : [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    4 : [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                    5 : [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    6 : [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                    7 : [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
                    }

        self.sextic = {
                      # [C, -, D, -, E, F, -, G, -, A, -, H]
                    1 : [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
                    2 : [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                    3 : [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    4 : [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                    5 : [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    6 : [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
                    7 : [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1]
                    }

        self.septimic = {
                      # [C, -, D, -, E, F, -, G, -, A, -, H]
                    1 : [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    2 : [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                    3 : [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    4 : [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
                    5 : [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
                    6 : [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
                    7 : [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1]
                    }

        self.nonic = {
                      # [C, -, D, -, E, F, -, G, -, A, -, H]
                    1 : [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                    2 : [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0],
                    3 : [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1],
                    4 : [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                    5 : [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                    6 : [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                    7 : [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
                    }

    def get_triad(self, which):
        """ Simple triads """
        return self.triads[which]

    def get_sextic(self, which):
        """ With sext """
        return self.sextic[which]

    def get_septimic(self, which):
        """ With seventh """
        return self.septimic[which]

    def get_nonic(self, which):
        """ Get chord with added ninth """
        return self.nonic[which]
