#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Sieve_Manager, which manages a cloud

This manager inherits Manager class and uses Sieve shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from functools import reduce
from random import shuffle

from .manager import Manager

from ..utils import split_list


class Sieve_Manager_Base(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a sieve shuffling algorithm"""

    __slots__ = []

    runnable_managers = []

    # https://stackoverflow.com/a/43057166/8903959
    def __init_subclass__(cls, **kwargs):
        """This method essentially creates a list of all subclasses"""

        super().__init_subclass__(**kwargs)
        if hasattr(cls, "suspicion_func_num"):
            cls.runnable_managers.append(cls)

    def __init__(self, *args, **kwargs):
        """Stores suspicion functions"""

        super(Sieve_Manager_Base, self).__init__(*args, **kwargs)
        self.suspicion_funcs = [self._update_suspicion_0,
                                self._update_suspicion_1,
                                self._update_suspicion_2]
        self._update_suspicion = self.suspicion_funcs[self.suspicion_func_num]

    def _reorder_buckets(self, buckets):

        users = []
        for bucket in buckets:
            users.extend(bucket.users)
        for bucket, user_chunk in zip(buckets, split_list(list(sorted(users)),
                                                          len(buckets))):
            bucket.__init__(user_chunk)

    def _sort_buckets(self, buckets):
        if len(buckets) == 1:
            shuffle(buckets[0].users)
        elif len(buckets) % 2 == 0:
            self._shuffle_buckets(buckets, num_buckets_per_round=2)
        # This must mean that it is odd
        # So do the first three, then do the rest to make it even
        else:
            self._shuffle_buckets(buckets[:3], num_buckets_per_round=3)
            if len(buckets) > 3:
                self._shuffle_buckets(buckets[3:],
                                      num_buckets_per_round=2)

    def _shuffle_buckets(self, buckets, num_buckets_per_round):
        """Shuffle buckets between themselves"""

        current_index = 0
        while current_index < len(buckets):
            cur_buckets = [buckets[current_index + i]
                           for i in range(num_buckets_per_round)]
            shuffled_users = reduce(lambda x, y: x+y,
                                    [bucket.users for bucket in cur_buckets])
            shuffle(shuffled_users)
            user_chunks = split_list(shuffled_users, num_buckets_per_round)
            for bucket, user_chunk in zip(cur_buckets, user_chunks):
                bucket.__init__(user_chunk)
            current_index += num_buckets_per_round

    def _update_suspicion_0(self):
        """Updates suspicion level of all users"""

        for bucket in self.buckets:
            multiplier = 1 if bucket.attacked else 0
            for user in bucket.users:
                user.suspicion += (1 / len(bucket)) * multiplier

    def _update_suspicion_1(self):
        """Updates suspicion level of all users"""

        for bucket in self.buckets:
            multiplier = 1 if bucket.attacked else 0
            for user in bucket.users:
                user.suspicion += multiplier

    def _update_suspicion_2(self):
        """Updates suspicion level of all users"""

        for bucket in self.buckets:
            multiplier = 1 if bucket.attacked else -1
            for user in bucket.users:
                user.suspicion += (1 / len(bucket)) * multiplier
