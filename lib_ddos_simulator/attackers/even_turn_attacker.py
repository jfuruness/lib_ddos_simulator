#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker


class Even_Turn_Attacker(Attacker):
    """Attacker that only attacks on every even turn"""

    runnable = True

    def _attack(self, turn):
        if turn % 2:
            self.bucket.attacked = True


class Even_Turn_Lone_Attacker(Even_Turn_Attacker):
    """Attacks on even turns if no attacker in it's bucket attacked"""

    lone = True
