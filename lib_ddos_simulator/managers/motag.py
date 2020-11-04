#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Bounded_Manager, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from math import comb
import random

from .attackers import Attacker
from .manager import Manager

from ..utils import split_list


class Motag_Manager(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a bounded shuffling algorithm"""

    __slots__ = []

    runnable = True
    prox = 30

    def detect_and_shuffle(self, *args):
        """Bounded Manager algorithm"""

        self.greed_assign()

    def greedy_assign(self, num_insiders=None, attacked_users=None, prox=None):
        """Greedy algorithm from motag paper"""

        (num_insiders,
         attacked_users,
         prox) = self.get_greedy_init_vals(num_insiders, attacked_users, prox)

        if attacked_users <= prox:
            for user in attacked_users:
                self.get_new_bucket().reinit([user])
        elif prox = 1:
            self.get_new_bucket().reinit(attacked_users)
        elif num_insiders = 0:
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
                self.get_new_bucket.reinit(users_to_add)
            self.greedy_assign(attacked_users,
                               remaining_insiders,
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
        if prox is None:
            prox = self.prox
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
            save = comb(client - i, insider) * i / comb(client, insider)
            if save > _max:
                _max = save
                max_assign = i
        return max_assign
