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
# Removed because logging inhibits multiprocessing
#mpl_logger = logging.getLogger('matplotlib')
#mpl_logger.setLevel(logging.WARNING)

# Importing all due to large number of attacker types
from .attackers import *
from .attackers import Basic_Attacker, Even_Turn_Attacker


from .animations import Animater
from .ddos_simulators import DDOS_Simulator
from .graphers import Combination_Grapher, Grapher

# Importing all due to large number of manager types
from .managers import Manager, Bounded_Manager, Sieve_Manager_Base
from .managers import Sieve_Manager_KPO_S0, Sieve_Manager_V0_S0, Sieve_Manager_V1_S0
from .managers import Sieve_Manager_V0_W_Stop_S0
from .managers import Protag_Manager_Base, Protag_Manager_Merge

from .managers import Protag_Manager_No_Merge
from .managers import Isolator_2i_1f
from .managers import Isolator_3i_1f
from .managers import Isolator_2i_kf
from .managers import Isolator_3i_kf
from .managers import Isolator_2i_SQRT_kf
from .managers import Isolator_3i_SQRT_kf


from .managers import Motag_Manager_3_Bucket
from .managers import Motag_Manager_20_Bucket
from .managers import Motag_Manager_40_Bucket
from .managers import Motag_Manager_200_Bucket
from .managers import Motag_Manager_500_Bucket
from .managers import Opt_H
from .managers import Opt_S
