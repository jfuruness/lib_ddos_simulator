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
    paper = True

    bucket_contains_other_attackers = dict()

    def _attack(self, manager, turn):
        """Only attack if the bucket contains other attackers"""
        key = (manager.__class__, turn)
        contains_other_attackers = self.bucket_contains_other_attackers.get(
            key
        )
        if contains_other_attackers is None:
            contains_other_attackers = False
            for x in self.bucket.users:
                if isinstance(x, Attacker) and self is not x:
                    contains_other_attackers = True
                    break
            self.bucket_contains_other_attackers[key] = contains_other_attackers
        if contains_other_attackers:
            self.bucket.attacked = True
