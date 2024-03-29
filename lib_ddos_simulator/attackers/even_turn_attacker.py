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
    paper = True

    def _attack(self, manager, turn):
        if turn % 2:
            self.bucket.attacked = True
