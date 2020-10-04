#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker


class X_Turns_Straight_Attacker(Attacker):
    """Attacker that attacks for x turns straight"""

    runnable = False

    def __init__(self, *args, **kwargs):
        assert not self.runnable or hasattr(self, "turns_in_a_row")
        super(X_Turns_Straight_Attacker, self).__init__(*args, **kwargs)

    def _attack(self, turn):
        if not (turn % self.turns_in_a_row == 0 and turn > 0):
            self.bucket.attacked = True


class X_Turns_Straight_Lone_Attacker(X_Turns_Straight_Attacker):
    """Attacks on even turns if no attacker in it's bucket attacked"""

    lone = True


class Three_Turns_Straight_Attacker(X_Turns_Straight_Attacker):
    """Attacker that attacks for x turns straight"""

    runnable = True
    turns_in_a_row = 3


class Ten_Turns_Straight_Attacker(X_Turns_Straight_Attacker):
    """Attacker that attacks for x turns straight"""

    runnable = True
    turns_in_a_row = 10


class Twenty_Turns_Straight_Attacker(X_Turns_Straight_Attacker):
    """Attacker that attacks for x turns straight"""

    runnable = True
    turns_in_a_row = 10
