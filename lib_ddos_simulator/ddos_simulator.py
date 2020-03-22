#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Simulation, to simulate a DDOS attack"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import logging
from random import shuffle
from tqdm import trange

from .user import User
from .attacker import Attacker
from .manager import Manager
from . import utils

class DDOS_Simulator:
    """Simulates a DDOS attack"""

    __slots__ = ["good_users", "attackers", "users", "manager"]
  
    def __init__(self,
                 num_users: int,
                 num_attackers: int,
                 num_buckets: int,
                 threshold: int,
                 Manager_Child_Class: Manager,
                 stream_level=logging.INFO):
        """Initializes simulation"""

        utils.config_logging(stream_level)

        self.good_users = [User(x) for x in range(num_users)]
        self.attackers = [Attacker(x) for x in range(num_attackers)]                                
        self.users = self.good_users + self.attackers
        # Shuffle so attackers are not at the end
        shuffle(self.users)
        # Creates manager and distributes users evenly across buckets
        self.manager = Manager_Child_Class(num_buckets, self.users, threshold)

    def run(self, num_rounds: int):
        """Runs simulation"""

        algo_name = self.manager.__class__.__name__
        for turn in trange(num_rounds, desc=f"Running {algo_name}"):
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

class Round_Info:
    """Stores round info. Used instead of db for simplicity"""

    def __init__(self, manager: Manager):
        """Stores information for the round"""

        self.num_buckets_used = len(manager.buckets)
        self.users_serviced = sum(len(x) for x in manager.buckets
                                  if not x.attacked)
        self.attackers_detected = 
        self.percent_users_serviced = 
        self.percent_attackers_detected = 
