#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker


class Patient_Attacker(Attacker):
    """Attacker waits until they are in a combined bucket before attacking"""

    runnable = False

    def add_additions(self, turn):
        """Records number of times their bucket size increased"""

        if turn == 0:
            self.starting_users = len(self.bucket)
            self.total_additions = 0
        if len(self.bucket.users) > self.starting_users:
            self.total_additions += 1
            self.starting_users = len(self.bucket.users)

    def _attack(self, turn):
        """Attacks only if the bucket size has increased num_additions times"""

        self.add_additions(turn)
        if self.total_additions > self.num_additions:
            self.bucket.attacked = True


class Wait_For_One_Addition_Attacker(Patient_Attacker):
    """Attacker waits until they are in a combined bucket before attacking"""

    runnable = True
    num_additions = 1


class Wait_For_One_Addition_Lone_Attacker(Wait_For_One_Addition_Attacker):
    """Attacker waits until they are in a combined bucket before attacking

    and only attacks when no other attacker attacks in their bucket"""

    lone = True


class Wait_For_Two_Additions_Attacker(Patient_Attacker):
    """Attacker waits until their bucket size increased twice to attack"""
    runnable = True
    num_additions = 2


class Wait_For_Two_Additions_Lone_Attacker(Wait_For_Two_Additions_Attacker):
    """Attacker waits until their bucket size increased thrice to attack

    and only attacks when no other attacker attacks in their bucket"""

    lone = True


class Wait_For_Three_Additions_Attacker(Patient_Attacker):
    """Attacker waits until their bucket size increased thrice to attack"""

    runnable = True
    num_additions = 3


class Wait_For_Three_Additions_Lone_Attacker(Wait_For_Three_Additions_Attacker):
    """Attacker waits until their bucket size increased thrice to attack

    and only attacks when no other attacker attacks in their bucket"""

    lone = True
