#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This package runs a DDOS simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

# Done here for deterministicness
import random
random.seed(0)

# http://matplotlib.1069221.n5.nabble.com/How-to-turn-off-matplotlib-DEBUG-msgs-td48822.html
import matplotlib
import logging
mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)

# Importing all due to large number of attacker types
from .attackers import *

from .ddos_simulator import DDOS_Simulator
from .graphers import Animater, Combination_Grapher, Grapher

# Importing all due to large number of manager types
from .managers import *
