#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker


class Herzberg_Motag_Attacker(Attacker):
    """Basic attacker class"""

    runnable = True
    paper = True

    def _attack(self, manager, turn):
        """desc below

        If it is the last user in a bucket,
            do nothing, so motag will not know it is you
        else if there is a bucket with no attackers that is larger than your own:
            # This is to get added to the service bucket
            do nothing
        else:
            attack
        """

        # I'm not supposed to be on this project
        # So whatever. Time to monkey patch
        if not hasattr(manager, "turn_dict"):
            manager.turn_dict = {}
        if manager.turn_dict.get(turn) is None:
            attackers = manager.connected_attackers
            least_big_attacker = min(attackers, key=lambda x: len(x.bucket))
            manager.turn_dict[turn] = least_big_attacker.bucket.id



        # If the attacker is the last one left, do not attack
        # Or else the attacker would be discovered
        if len(self.bucket) == 1:
            pass
        elif self.bucket.id == manager.turn_dict[turn]:
            pass
        else:
            self.bucket.attacked = True
