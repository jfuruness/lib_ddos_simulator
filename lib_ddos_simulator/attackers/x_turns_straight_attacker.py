#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from math import log2
from .attacker import Attacker


class X_Turns_Straight_Attacker(Attacker):
    """Attacker that attacks for x turns straight"""

    runnable = False
    paper = False

    def __init__(self, *args, **kwargs):
        assert not self.runnable or hasattr(self, "turns_in_a_row")
        super(X_Turns_Straight_Attacker, self).__init__(*args, **kwargs)

    def _attack(self, manager, turn):
        if not (turn % self.turns_in_a_row == 0 and turn > 0):
            self.bucket.attacked = True


class Log2n_Turns_Straight_Attacker(Attacker):
    """Attacker that attacks for x turns straight"""

    runnable = True
    paper = True

    def _attack(self, manager, turn):
        # NOTE: To make it faster for 10k users, we've hardcoded this for 13
        # num_users = len(manager.connected_users)
        # turns_in_a_row = int(log2(num_users))
        turns_in_a_row = 13
        if not (turn % turns_in_a_row == 0 and turn > 0):
            # Only attack when you are not alone
            if len(self.bucket) > 1:
                self.bucket.attacked = True


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
