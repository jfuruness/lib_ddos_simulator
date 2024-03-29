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

from ..animations import Animater
from ..graphers import Grapher
from ..attackers import Attacker, Basic_Attacker
from .. import managers
from ..simulation_objects import User
from .. import utils


class DDOS_Simulator:
    """Simulates a DDOS attack"""

    def __init__(self,
                 num_users: int,
                 num_attackers: int,
                 num_buckets: int,
                 Manager_Child_Classes: list,
                 debug=False,
                 # The graph kwargs
                 graph_dir: str = os.path.join("/tmp", "lib_ddos_simulator"),
                 tikz=False,
                 save=False,
                 high_res=False,
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

        self.num_users_to_user_orderings = dict()
        # Creates manager and distributes users evenly across buckets
        self.managers = [X(num_buckets, self._get_users(num_users,
                                                        num_attackers,
                                                        user_cls,
                                                        attacker_cls))
                         for X in Manager_Child_Classes]

        # Creates graphing class to capture data
        self.grapher = Grapher(self.managers,
                               num_users,
                               num_attackers,
                               **self.graph_kwargs)
        self.attacker_cls = attacker_cls
        self.user_cls = user_cls

    def _get_users(self, num_users, num_attackers, user_cls, attacker_cls):

        key = (num_users, num_attackers)

        if key not in self.num_users_to_user_orderings:
            # Ids start at one to make rows easier for animations for buckets
            good_users = [user_cls(x) for x in range(1, num_users + 1)]

            attackers = attacker_cls.get_attackers(num_users + 1,
                                                        num_attackers)

            self.users = good_users + attackers
            random.shuffle(self.users)
            self.num_users_to_user_orderings[key] = self.users

        else:
            self.users = list()
            for old_user in self.num_users_to_user_orderings[key]:
                cls = attacker_cls if isinstance(old_user, Attacker) else user_cls
                self.users.append(cls(old_user.id))

        self.next_unused_user_id = len(self.users)
        return self.users

    def randomly_order_users(self):
        # Shuffle so attackers are not at the end
        if len(self.users) not in self.num_users_to_user_orderings:
            ordering = [x.id for x in self.users]
            random.shuffle(ordering)
            self.num_users_to_user_orderings[len(self.users)] = tuple(ordering)
        ordering = self.num_users_to_user_orderings[len(self.users)]
        temp_id_to_user_dict = {x.id: x for x in self.users}
        self.users = [temp_id_to_user_dict[x] for x in ordering]


    def run(self, num_rounds: int, animate=False, graph_trials=True):
        """Runs simulation"""

        for manager in self.managers:
            self.run_sim(manager, num_rounds, animate, graph_trials)

        # Returns latest utility, used for combination graphing
        return self.grapher.graph(graph_trials, self.attacker_cls)

    def run_sim(self, manager, num_rounds, animate: bool, graph_trials: bool):
        """Initializes sim for a single manager and runs"""

        if animate:
            animater = Animater(manager,
                                self.user_cls,
                                self.attacker_cls,
                                **self.graph_kwargs)
        else:
            animater = None
        for turn in range(num_rounds):
            if turn % 100 == 0:
                # or ("motag" in manager.__class__.__name__.lower() and turn % 10 == 0):
                #pass
                print(f"round {turn} manager {manager.__class__.__name__} atk {self.attacker_cls.__name__}")
            # Attackers attack, users record stats
            self.user_actions(manager, turn)
            # Record data
            self.record(turn, manager, animate, animater)
            # Manager detects and removes suspicious users, then shuffles
            # Then reset buckets to not attacked
            manager.take_action(turn)

        if animate:
            animater.run_animation(num_rounds)

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

    def record(self, turn, manager, animate, animater):
        """Records statistics for graphs"""

        self.grapher.capture_data(turn, manager)
        if animate:
            animater.capture_data(manager)
