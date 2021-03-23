#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Bounded_Manager, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import random

import scipy.special

from .manager import Manager

from ..attackers import Attacker
from ..utils import split_list

class Motag_Manager(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a bounded shuffling algorithm

    Drawbacks of this paper:
    Really this algo is completely useless
    The never run thier sims with more than 5% attackers
    They estimate attackers when attackers are 3% or less
        -as this # goes up it becomes incredibly worse
    They estimate attackers when attackers are ~= #buckets
        -obvi this will do well, this is trivial
    They don't specify what to do with good buckets
    They set % users to service, but a good attacker can
        always work around this #
    We don't estimate real # of attackers, but use actual #
        -in reality, their algorithm would perform much worse
    LOL bugs in their sudo code. If shuffled buckets only have attackers,
        then there is division by zero error (since max_proxy returns 0)
        RIP MOTAG what a dumb paper
    It gets worse - doing binomials causes the code to run a super long time!
    """

    __slots__ = []

    runnable = True
    paper = True
    prox = 3#20
    percent_users_to_save = .95

    def detect_and_shuffle(self, *args):
        """Motag Manager algorithm"""

        self.remove_attackers()
        self.combine_buckets()
        serviced_users = sum([len(x) for x in self.non_attacked_buckets])
        # LOL just drop the buckets
        if serviced_users / len(self.connected_users) > self.percent_users_to_save:
            for bucket in self.attacked_buckets:
                self.disconnect_users([x.id for x in bucket.users])

        else:
            self.greedy_assign()

    def greedy_assign(self, num_insiders=None, attacked_users=None, prox=None):
        """Greedy algorithm from motag paper"""

        (num_insiders,
         attacked_users,
         prox) = self.get_greedy_init_vals(num_insiders, attacked_users, prox)

        #print(f"greedy assign called {num_insiders}, {attacked_users}, {prox}")

        if len(attacked_users) <= prox:
            for user in attacked_users:
                self.get_new_bucket().reinit([user])

        elif prox == 1:
            self.get_new_bucket().reinit(attacked_users)

        elif num_insiders == 0:
            if len(attacked_users) > 0:
                user_chunks = split_list(attacked_users, prox)
                for user_chunk in user_chunks:
                    self.get_new_bucket().reinit(user_chunk)

        else:
            w = self.max_proxy(len(attacked_users),
                               len(attacked_users) - 1,
                               num_insiders)
            assert w > 0, str(len(attacked_users)) + " " + str(num_insiders)
            prox_to_fill = len(attacked_users) // w
            if prox_to_fill >= prox:
                prox_to_fill = prox - 1

            remaining_attacked_users = len(attacked_users) - prox_to_fill * w
            remaining_prox = prox - prox_to_fill
            remaining_insiders = round(num_insiders * remaining_attacked_users
                                       / len(attacked_users))
            for _ in range(prox_to_fill):
                users_to_add = attacked_users[:w]
                attacked_users = attacked_users[w:]
                self.get_new_bucket().reinit(users_to_add)

            self.greedy_assign(remaining_insiders,
                               attacked_users,
                               remaining_prox)

    def get_greedy_init_vals(self, num_insiders, attacked_users, prox):
        """Gets values to initialize greedy algorithm"""

        # sudo code algo 1 from MOTAG
        if num_insiders is None:
            num_insiders = self.get_approx_insiders(self.attacked_buckets)
        if attacked_users is None:
            attacked_users = []
            for bucket in self.attacked_buckets:
                attacked_users.extend(bucket.users)
                self.remove_bucket(bucket)
            random.shuffle(attacked_users)
        if prox is None:
            prox = self.prox - len(self.non_attacked_buckets)
        return num_insiders, attacked_users, prox

    def get_approx_insiders(self, buckets):
        # NOTE that they estimate the number of insiders,
        # but we just give it the exact amount, since they do not 
        # include this equation for the estimation
        # This means the true motag algo would perform worse
        # Much, much worse
        num_attackers = 0
        for bucket in self.attacked_buckets:
            for user in bucket.users:
                if isinstance(user, Attacker):
                    num_attackers += 1
        return num_attackers

    def max_proxy(self, client, upper_bound, insider):
        """Algo as defined in algo 1 for motag paper"""

        #print("max proxy called")
        _max = 0
        max_assign = 0
        for i in range(upper_bound + 1):
            #print(client)
            #print(i)
            #print(insider)
            numerator = scipy.special.comb(client - i,
                                           insider,
                                           exact=True) * i
            denominator = scipy.special.comb(client, insider, exact=True)
            save = numerator / denominator
            #print(f"num: {numerator} de: {denominator}")
            if save > _max:
                _max = save
                max_assign = i
        # If max assign is 0, return 1 instead
        # NOTE: This is a bug in their sudo code that we are fixing
        return max(max_assign, 1)

    def combine_buckets(self):
        """Merge all non attacked buckets"""

        users = []
        for bucket in self.non_attacked_buckets:
            users.extend(bucket.users)
            self.remove_bucket(bucket)
        if len(users) > 0:
            self.get_new_bucket().reinit(users)
