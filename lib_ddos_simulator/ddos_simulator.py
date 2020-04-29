#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Simulation, to simulate a DDOS attack"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from copy import deepcopy
import logging
from random import shuffle

from tqdm import trange

from .animater import Animater
from .attacker import Attacker
from .grapher import Grapher
from .manager import Manager
from .user import User
from . import utils

class DDOS_Simulator:
    """Simulates a DDOS attack"""

    __slots__ = ["good_users", "attackers", "users", "managers", "grapher"]
  
    def __init__(self,
                 num_users: int,
                 num_attackers: int,
                 num_buckets: int,
                 threshold: int,
                 Manager_Child_Classes: list,
                 stream_level=logging.INFO,
                 graph_path: str = "/tmp/lib_ddos/"):
        """Initializes simulation"""

        utils.config_logging(stream_level)

        self.good_users = [User(x) for x in range(num_users)]
        self.attackers = [Attacker(x) for x in range(num_attackers)]                                
        self.users = self.good_users + self.attackers
        # Shuffle so attackers are not at the end
        shuffle(self.users)
        # Creates manager and distributes users evenly across buckets
        self.managers = [X(num_buckets, deepcopy(self.users), threshold)
                         for X in Manager_Child_Classes]

        # Creates graphing class to capture data
        self.grapher = Grapher(graph_path,
                               self.managers,
                               len(self.good_users),
                               len(self.attackers))

    def run(self, num_rounds: int, animate: bool = False):
        """Runs simulation"""

        for manager in self.managers:
            if animate:
                animater = Animater(manager)
            algo_name = manager.__class__.__name__
            for turn in trange(num_rounds, desc=f"Running {algo_name}"):
                # Attackers attack
                self.attack_buckets(manager)
                self.grapher.capture_data(turn, manager, self.attackers)
                if animate:
                    animater.capture_data(manager)
                # Manager detects and removes suspicious users, then shuffles
                manager.detect_and_shuffle(turn)
                # All buckets are no longer attacked for the next round
                manager.reset_buckets()
            if animate:
                animater.run_animation(turn)
        self.grapher.graph()

    def attack_buckets(self, manager):
        """Attackers attack"""

        for user in manager.users:
            if isinstance(user, Attacker):
                user.attack()
                assert user.bucket in manager.buckets
