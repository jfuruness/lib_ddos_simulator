#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Protag_Manager, which manages a cloud

This manager inherits Manager class and uses Protag shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from random import shuffle

from .bucket import Bucket
from .manager import Manager
from .utils import split_list

class Bounded_Manager(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a protag shuffling algorithm"""

    __slots__ = ["num_attackers_guess"]

    def __init__(self, *args, **kwargs):
        super(Bounded_Manager, self).__init__(*args, **kwargs)
        self.num_attackers_guess = 0

    def detect_and_shuffle(self, turn_num: int):
        """Protag algorithm"""

        if len(self.attacked_buckets) > self.num_attackers_guess:
            self.num_attackers_guess = len(self.attacked_buckets)
            # 2x guess is the new number of buckets
            new_bucket_amnt = len(self.attacked_buckets) * 2
            new_bucket_amnt -= len(self.non_attacked_buckets)
            if new_bucket_amnt == len(self.attacked_buckets):
                new_bucket_amnt += 1
            self._shuffle_attacked_buckets(new_bucket_amnt)

        elif len(self.buckets) < self.num_attackers_guess * 3:
            # Shuffle attacked users into num attacked buckets * 2
            # So one new bucket
            self._shuffle_attacked_buckets(len(self.attacked_buckets) + 1)
        else:
            new_non_attacked_buckets = []
            # Sorts buckets by reputation
            sorted_buckets = list(sorted(self.non_attacked_buckets,
                                         key=lambda x: x.turns_not_attacked))
            for i in range(0, len(self.sorted_buckets), 2):
                try:
                    users = sorted_buckets[i].users
                    users += sorted_buckets[i + 1].users
                    new_non_attacked_buckets.append(Bucket(users))
                # last bucket
                except IndexError:
                    new_non_attacked_buckets.append(sorted_buckets[i])
            self.buckets = new_non_attacked_buckets + self.attacked_buckets
            # Add one bucket to attackers and reorder
            self._shuffle_attacked_buckets(len(self.attacked_buckets) + 1)

        self._incriment_buckets()
            
    def _shuffle_attacked_buckets(self, new_bucket_amnt):
        print(len(self.attacked_buckets))
        print(len(self.attacked_users))
        print(new_bucket_amnt)
        users = self.attacked_users
        shuffle(users)
        new_attacked_buckets = [Bucket(user_chunk) for user_chunk in
                                split_list(users,
                                           new_bucket_amnt)]
        self.buckets = self.non_attacked_buckets + new_attacked_buckets

    def _incriment_buckets(self):
        for bucket in self.buckets:
            if bucket.attacked:
                bucket.turns_not_attacked = 0
            else:
                bucket.turns_not_attacked += 1
