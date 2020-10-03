#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Simulation, to simulate a DDOS attack"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from copy import deepcopy
import logging
import os
import random

from tqdm import trange

from .graphers import Animater, Grapher
from .attackers import Attacker, Basic_Attacker, Mixed_Attacker
from .simulation_objects import User
from . import utils

############################## DLETE THIS
class DOSE_Manager:
    pass

class DOSE_Attack_Event:
    """Purpose of this class is just to keep track of atk events

    helpful in dealing with DOSE stats
    """

    def __init__(self, bucket):
        self.users = bucket.users
        self.uids = set(x.id for x in bucket.users)
        # 3 is from their matplotlib code
        # This is CRPA val
        self.sus_added = DOSE_Manager.dose_atk_sus_to_add(bucket)

    def reduce_sus(self, users):
        for user in self.users:
            user.dose_atk_risk -= self.sus_added
        
        


class DDOS_Simulator:
    """Simulates a DDOS attack"""

    __slots__ = ["graph_kwargs", "good_users", "attackers", "users",
                 "managers", "grapher", "attacker_cls"]

    def __init__(self,
                 num_users: int,
                 num_attackers: int,
                 num_buckets: int,
                 threshold: int,
                 Manager_Child_Classes: list,
                 stream_level=logging.INFO,
                 # The graph kwargs
                 graph_dir: str = os.path.join("/tmp", "lib_ddos_simulator"),
                 tikz=False,
                 save=False,
                 high_res=False,
                 attacker_cls=Basic_Attacker):
        """Initializes simulation"""

        self.graph_kwargs = {"stream_level": stream_level,
                             "graph_dir": graph_dir,
                             "tikz": tikz,
                             "save": save,
                             "high_res": high_res}

        utils.config_logging(stream_level)

        self.good_users = [User(x) for x in range(num_users)]
        # This allows us to take mixes of attackers
        if isinstance(attacker_cls, Mixed_Attacker):
            # get_mix returns a list of attacker classes
            self.attackers = [X(i+len(self.good_users)) for i, X in
                              enumerate(attacker_cls.get_mix(num_attackers))]
        # If it is not a mixed attacker, simply initialize attackers
        else:
            self.attackers = [attacker_cls(x + len(self.good_users))
                              for x in range(num_attackers)]
        self.users = self.good_users + self.attackers
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

    def run(self, num_rounds: int, animate=False, graph_trials=True):
        """Runs simulation"""

        for manager in self.managers:
            # Sets up animator and turns
            random_seed = random.random()
            # Animations runs this twice to know how large to make anims
            for i in range(2):
                # Sets up animator and turns
                animater, turns = self.init_sim(manager,
                                                num_rounds,
                                                animate,
                                                graph_trials,
                                                random_seed,
                                                i)

                for turn in turns:
                    # Attackers attack
                    self.attack_buckets_incriment_lt(manager, turn)
                    # Record statistics
                    self.grapher.capture_data(turn, manager, self.attackers)
                    if animate and i == 1:
                        animater.capture_data(manager)
                    # Manager detects and removes suspicious users, then shuffles
                    
                    manager.detect_and_shuffle(turn)
                    # All buckets are no longer attacked for the next round
                    manager.reset_buckets()
                if animate:
                    if i == 1:
                        animater.run_animation(turn)
                # If we are not animating, not reason to run again
                else:
                    break
            if not animate:
                # Returns latest utility, used for combination graphing
                return self.grapher.graph(graph_trials, self.attacker_cls)

    def init_sim(self, manager, num_rounds, animate, graph_trials, seed, i):
        """Sets up animator and turn list"""

        # Seeded so that exactly the same trial is run twice
        random.seed(seed)
        manager.reinit()
        # We can only animate one manager at a time
        animater = Animater(manager,
                            **self.graph_kwargs) if animate and i else None
        # If we are graphing for just one manager
        # Print and turn on tqdm
        if graph_trials:
            algo_name = manager.__class__.__name__
            turns = trange(num_rounds, desc=f"Running {algo_name}")
        # If we are comparing managers, multiprocessing is used
        # So no tqdm as to not have garbled output
        else:
            turns = range(num_rounds)

        return animater, turns

    def attack_buckets_incriment_lt(self, manager, turn):
        """Attackers attack, adds 1 to user lifetime"""

        manager.get_animation_statistics()
        for user in manager.users:
            # Used in DOSE for connection lifetime
            user.conn_lt += 1
            if isinstance(user, Attacker):
                user.attack(turn)
                assert user.bucket in manager.buckets

        if isinstance(manager, DOSE_Manager):
            for bucket in manager.attacked_buckets:
                manager.dose_atk_events.append(DOSE_Attack_Event(bucket))
