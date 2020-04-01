#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Attacker, for attackers in simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .user import User

class Attacker(User):
    """Simulates an attacker for a DDOS attack"""

    # Horns is used for animations
    __slots__ = ["horns"]

    def attack(self):
        """Attacks the bucket it's in"""

        self.bucket.attacked = True  
