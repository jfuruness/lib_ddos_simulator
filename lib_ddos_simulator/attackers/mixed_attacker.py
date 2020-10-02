#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker
from .basic_attacker import Basic_Attacker
from .random_attacker import Fifty_Percent_Lone_Attacker
from .patient_attacker import Wait_For_One_Addition_Lone_Attacker
from .patient_attacker import Wait_For_Two_Additions_Lone_Attacker
from .patient_attacker import Wait_For_Three_Additions_Lone_Attacker


class Mixed_Attacker(Attacker):
    """Returns a mix of attacker for the simulation"""

    runnable = True

    @staticmethod
    def get_mix(num_attackers):
        attacker_classes = []
        for attacker_cls in [Fifty_Percent_Lone_Attacker,
                             Wait_For_One_Addition_Lone_Attacker,
                             Wait_For_Two_Additions_Lone_Attacker,
                             Wait_For_Three_Additions_Lone_Attacker]:
            # 10% of everything
            for _ in range(int(num_attackers * .1)):
                attacker_classes.append(attacker_cls)
        # The rest are basic attackers
        for _ in range(len(attacker_classes) - num_attackers):
            attacker_classes.append(Basic_Attacker)
        return attacker_classes
