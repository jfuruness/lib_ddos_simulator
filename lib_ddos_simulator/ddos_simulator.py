#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Simulation, to simulate a DDOS attack"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, a97gorbenko@gmail.com"
__status__ = "Development"

import logging
from random import shuffle
from tqdm import trange
from .user import User
from .attacker import Attacker

class DDOS_Simulator:
    """Simulates a DDOS attack"""
  
    def __init__(self,
                 num_users: int,
                 num_attackers: int,
                 num_buckets: int,
                 threshold: int,
                 Manager_Child_Class: int):
        """Initializes simulation"""

        self.good_users = [User(x) for x in range(num_users)]
        self.attackers = [Attacker(x) for x in range(num_attackers)]                                
        self.users = self.good_users + self.attackers
        # Shuffle so attackers are not at the end
        shuffle(self.users)
        # Creates manager and distributes users evenly across buckets
        self.manager = Manager_Child_Class(num_buckets, self.users, threshold)

    def run(self, num_rounds: int):
        """Runs simulation"""

        for turn in trange(num_rounds):
            atk_sus = [attacker.suspicion for attacker in self.attackers]
            usr_sus = [user.suspicion for user in self.users]
            # Attackers attack
            self.attack_buckets()
            # Manager detects and removes suspicious users, then shuffles
            self.manager.detect_and_shuffle(turn)
            # All buckets are no longer attacked for the start of the next round
            self.manager.reset_buckets()

    def attack_buckets(self):
        """Attackers attack"""

        for attacker in self.attackers:
            attacker.attack()
