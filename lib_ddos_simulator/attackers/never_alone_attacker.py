#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker


class Never_Alone_Attacker(Attacker):
    """Basic attacker class"""

    runnable = True

    def _attack(self, manager, turn):
        attacker_count = sum([1 for x in self.bucket.users
                              if isinstance(x, Attacker)])
        if attacker_count > 1:
            self.bucket.attacked = True
        elif attacker_count == 0:
            assert False, "This should never happen"
        

class Never_Alone_Lone_Attacker(Never_Alone_Attacker):
    """Attacks every turn if no attacker in it's bucket attacked"""

    lone = True
