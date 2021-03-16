#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker


class Never_Last_Attacker(Attacker):
    """Basic attacker class"""

    runnable = True

    def _attack(self, manager, turn):
        if len(self.bucket) > 1:
            self.bucket.attacked = True
        elif len(self.bucket) == 0:
            assert False, "This should never happen"
