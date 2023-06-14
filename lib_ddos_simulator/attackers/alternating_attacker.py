#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker


class Alternating_Attacker(Attacker):
    """Basic attacker class"""

    runnable = True
    paper = True
    instances = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = Alternating_Attacker.instances
        Alternating_Attacker.instances += 1

    def _attack(self, manager, turn):
        if self.id % 2 == 0 and turn % 2 == 0 and len(self.bucket > 1):
            self.bucket.attacked = True
        elif self.id % 2 != 0 and turn % 2 != 0 and len(self.bucket > 1):
            self.bucket.attacked = True
