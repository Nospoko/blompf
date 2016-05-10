import numpy as np
from utils import midi as um
from walkers import merw as wm
from walkers import finger as wf

class Arm(object):
    """ Arm is supposed to be above the Hand in object hierarchy """
    def __init__(self):
        """ el Creador """
        # Each arm can have multiple hands
        self.hands      = []
        # Container for possible Hand tasks
        self.handjobs   = []
