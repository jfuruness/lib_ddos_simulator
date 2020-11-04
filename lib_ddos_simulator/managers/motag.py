#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Bounded_Manager, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import random

from .manager import Manager

from ..attackers import Attacker
from ..utils import split_list


import operator as op
from functools import reduce

# https://stackoverflow.com/a/4941932/8903959
# Not python3.8, normally just use math.comb
def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2


class Motag_Manager(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a bounded shuffling algorithm"""

    __slots__ = []

    runnable = True
    prox = 20
    percent_users_to_save = .95

    def detect_and_shuffle(self, *args):
        """Bounded Manager algorithm"""





        serviced_users = sum([len(x) for x in self.non_attacked_buckets])
        # LOL just drop the buckets
        if serviced_users / len(self.connected_users) > self.percent_users_to_save:
            for bucket in self.attacked_buckets:
                self.eliminate_users_list([x.id for x in bucket.users])

        else:
            self.greedy_assign()




    def greedy_assign(self, num_insiders=None, attacked_users=None, prox=None):
        """Greedy algorithm from motag paper"""

        (num_insiders,
         attacked_users,
         prox) = self.get_greedy_init_vals(num_insiders, attacked_users, prox)

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
                bucket.users = []
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
        for bucket in buckets:
            for user in bucket.users:
                if isinstance(user, Attacker):
                    num_attackers += 1
        return num_attackers

    def max_proxy(self, client, upper_bound, insider):
        """Algo as defined in algo 1 for motag paper"""

        _max = 0
        max_assign = 0
        for i in range(upper_bound + 1):
            save = ncr(client - i, insider) * i / ncr(client, insider)
            if save > _max:
                _max = save
                max_assign = i
        return max_assign
