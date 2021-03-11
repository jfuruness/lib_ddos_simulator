#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Simulation, to simulate a DDOS attack"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from copy import deepcopy
import os
import random

from tqdm import trange

from ..graphers import Animater, Grapher
from ..attackers import Attacker, Basic_Attacker, Mixed_Attacker
from .. import managers
from ..simulation_objects import User
from .. import utils


class DDOS_Simulator:
    """Simulates a DDOS attack"""

    def __init__(self,
                 num_users: int,
                 num_attackers: int,
                 num_buckets: int,
                 threshold: int,
                 Manager_Child_Classes: list,
                 debug=False,
                 # The graph kwargs
                 graph_dir: str = os.path.join("/tmp", "lib_ddos_simulator"),
                 tikz=False,
                 save=False,
                 high_res=False,
                 animate=False,
                 attacker_cls=Basic_Attacker,
                 user_cls=User):
        """Initializes simulation"""

        self.og_num_attackers = num_attackers
        self.og_num_users = num_users
        self.graph_kwargs = {"debug": debug,
                             "graph_dir": graph_dir,
                             "tikz": tikz,
                             "save": save,
                             "high_res": high_res}

        # Ids start at one to make rows easier for animations for buckets
        self.good_users = [user_cls(x) for x in range(1, num_users + 1)]

        self.attackers = self.get_attackers(num_attackers, attacker_cls)

        self.users = self.good_users + self.attackers

        self.next_unused_user_id = len(self.users)
        # Shuffle so attackers are not at the end
        random.shuffle(self.users)
        # Creates manager and distributes users evenly across buckets
        self.managers = [X(num_buckets, deepcopy(self.users), threshold)
                         for X in Manager_Child_Classes]

        # Creates graphing class to capture data
        self.grapher = Grapher(self.managers,
                               len(self.good_users),
                               len(self.attackers),
                               **self.graph_kwargs)
        self.attacker_cls = attacker_cls
        self.user_cls = user_cls

    def run(self, num_rounds: int, animate=False, graph_trials=True):
        """Runs simulation"""

        for manager in self.managers:
            self.run_sim(manager, num_rounds, animate, graph_trials)
            assert False, "Perform animation here"

        # Returns latest utility, used for combination graphing
        return self.grapher.graph(graph_trials, self.attacker_cls)

    def run_sim(self, manager, num_rounds, animate: bool, graph_trials: bool):
        """Initializes sim for a single manager and runs"""

        animater = Animater(manager,
                            self.user_cls,
                            self.attacker_cls,
                            **self.graph_kwargs)
        for turn in range(num_rounds):
            # Attackers attack, users record stats
            self.user_actions(manager, turn)
            # Record data
            self.record(turn, manager, animater)
            # Manager detects and removes suspicious users, then shuffles
            # Then reset buckets to not attacked
            manager.take_action(turn)

########################
### Helper Functions ###
########################

    def user_actions(self, manager, turn):
        """Attackers attack, adds 1 to user lifetime"""

        # Attackers attack first
        for user in manager.connected_attackers:
            user.take_action(manager, turn)
        # Users go second
        for user in manager.connected_good_users:
            user.take_action(manager, turn)

    def record(self, turn, manager, animater):
        """Records statistics for graphs"""

        print("Not capturing data for grapher")
        #self.grapher.capture_data(turn, manager)
        if self.animate:
            self.animater.capture_data(manager)
