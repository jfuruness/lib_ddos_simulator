#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Sieve_Manager, which manages a cloud

This manager inherits Manager class and uses Sieve shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from functools import reduce
from random import shuffle

from .bucket import Bucket
from .manager import Manager
from .utils import split_list

class Sieve_Manager(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a sieve shuffling algorithm"""

    __slots__ = []

    runnable_managers = []
    # https://stackoverflow.com/a/43057166/8903959
    def __init_subclass__(cls, **kwargs):
        """This method essentially creates a list of all subclasses
        This is incredibly useful for a few reasons. Mainly, you can
        strictly enforce proper templating with this. And also, you can
        automatically add all of these things to things like argparse
        calls and such. Very powerful tool.
        """

        super().__init_subclass__(**kwargs)
        if hasattr(cls, "suspicion_func_num"):
            cls.runnable_managers.append(cls)

    def __init__(self, *args, **kwargs):
        """Stores suspicion functions"""

        super(Sieve_Manager, self).__init__(*args, **kwargs)
        self.suspicion_funcs = [self._update_suspicion_0,
                                self._update_suspicion_1,
                                self._update_suspicion_2]
        self._update_suspicion = self.suspicion_funcs[self.suspicion_func_num]

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


class Sieve_Manager_V0(Sieve_Manager):
    """Sieve Manager detect and shuffle algorithm version 1"""

    def detect_and_shuffle(self, turn_num: int):
        """Performs sieve shuffle algorithm

        First updates suspicion of users.
        Then sorts users by suspicion.
        Then splits users into num buckets/2 chunks
        Then for each chunk, put in two buckets randomly
        """

        self._update_suspicion()
        self._reorder_buckets(self.buckets)
        self._sort_buckets(self.buckets)

class Sieve_Manager_V0_S0(Sieve_Manager_V0):
    suspicion_func_num = 0

class Sieve_Manager_V0_S1(Sieve_Manager_V0):
    suspicion_func_num = 1

class Sieve_Manager_V0_S2(Sieve_Manager_V0):
    suspicion_func_num = 2

class Sieve_Manager_V1(Sieve_Manager):
    """Sieve Manager detect and shuffle algorithm version 1"""

    def detect_and_shuffle(self, turn_num: int):
        """Performs sieve shuffle algorithm

        First updates suspicion of users.
        Then sorts users by suspicion.
        Then splits users into num buckets/2 chunks
        Then for each chunk, put in two buckets randomly
        """

        self._update_suspicion()
        attacked_buckets = [x for x in self.buckets if x.attacked]
        if len(attacked_buckets) > 0:
            self._reorder_buckets(attacked_buckets)
            self._sort_buckets(attacked_buckets)

class Sieve_Manager_V1_S0(Sieve_Manager_V1):
    suspicion_func_num = 0

class Sieve_Manager_V1_S1(Sieve_Manager_V1):
    suspicion_func_num = 1

class Sieve_Manager_V1_S2(Sieve_Manager_V1):
    suspicion_func_num = 2
