#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Folder contains all attacker classes"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker
from .basic_attacker import Basic_Attacker, Basic_Lone_Attacker
from .even_turn_attacker import Even_Turn_Attacker, Even_Turn_Lone_Attacker
from .mixed_attacker import Mixed_Attacker
from .patient_attacker import Wait_For_One_Addition_Attacker
from .patient_attacker import Wait_For_One_Addition_Lone_Attacker
from .patient_attacker import Wait_For_Two_Additions_Attacker
from .patient_attacker import Wait_For_Two_Additions_Lone_Attacker
from .patient_attacker import Wait_For_Three_Additions_Attacker
from .patient_attacker import Wait_For_Three_Additions_Lone_Attacker
from .random_attacker import Fifty_Percent_Attacker
from .random_attacker import Fifty_Percent_Lone_Attacker
from .random_attacker import Ten_Percent_Attacker
from .random_attacker import Ten_Percent_Lone_Attacker
from .x_turns_straight_attacker import *
