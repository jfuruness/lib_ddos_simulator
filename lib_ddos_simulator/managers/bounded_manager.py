#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Protag_Manager, which manages a cloud

This manager inherits Manager class and uses Protag shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
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

        if turn_num == 0:
            self.num_attackers_guess = len(self.attacked_buckets)

        if len(self.attacked_buckets) > self.num_attackers_guess:
            new_bucket_amnt = len(self.attacked_buckets)
            new_bucket_amnt -= self.num_attackers_guess
            self._shuffle_attacked_buckets(new_bucket_amnt)
            self.num_attackers_guess = len(self.attacked_buckets)

        elif len(self.buckets) < self.num_attackers_guess * 3:
            # Shuffle attacked users into num attacked buckets * 2
            # So one new bucket
            self._shuffle_attacked_buckets(len(self.attacked_buckets) + 1)
        else:
            new_non_attacked_buckets = []
            # Sorts buckets by reputation
            sorted_buckets = list(sorted(self.non_attacked_buckets,
                                         key=lambda x: x.turns_not_attacked))
            for i in range(0, len(sorted_buckets), 2):
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
        new_attacked_buckets = [x for x in self.attacked_buckets if len(x) > 1]
        new_bucket_amnt = self._remove_attackers(new_attacked_buckets,
                                                 new_bucket_amnt)

        if len(self.attacked_buckets) > 0 and new_bucket_amnt > 0:
            users = self.attacked_users
            shuffle(users)
            new_attacked_buckets = [Bucket(user_chunk) for user_chunk in
                                    split_list(users,
                                               new_bucket_amnt)]
            self.buckets = self.non_attacked_buckets + new_attacked_buckets

    def _remove_attackers(self, new_attacked_buckets, new_bucket_amnt):
        diff = len(self.attacked_buckets) - len(new_attacked_buckets)
        if diff > 0:
            self.buckets = new_attacked_buckets + self.non_attacked_buckets
            self.num_attackers_guess -= diff
            self.attackers_detected += diff
            # Just in case, prob not needed
            self.users = []
            for bucket in self.buckets:
                self.users.extend(bucket.users)
            new_bucket_amnt -= diff
        return new_bucket_amnt

    def _incriment_buckets(self):
        for bucket in self.buckets:
            if bucket.attacked:
                bucket.turns_not_attacked = 0
            else:
                bucket.turns_not_attacked += 1
