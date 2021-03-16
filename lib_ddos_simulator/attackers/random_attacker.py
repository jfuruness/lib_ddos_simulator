#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from random import random

from .attacker import Attacker


class Random_Attacker(Attacker):
    """Attacks at random self._percent_change_attack of the time"""

    runnable = False
    paper = False

    def _attack(self, manager, turn):
        if random() < self._percent_chance_attack:
            self.bucket.attacked = True


class Fifty_Percent_Attacker(Random_Attacker):
    """Attacks at random 50% of the time"""

    runnable = True
    _percent_chance_attack = .5


class Ten_Percent_Attacker(Random_Attacker):
    """Attacks at random 10% of the time"""

    _percent_chance_attack = .1
    runnable = True
