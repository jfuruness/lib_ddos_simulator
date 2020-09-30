#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Protag_Manager, which manages a cloud

This manager inherits Manager class and uses Protag shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"


from .bucket import Bucket
from .manager import Manager
from .utils import split_list
import random

class Kpo_Manager(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a protag shuffling algorithm"""

    __slots__ = []
        
    def detect_and_shuffle(self, turn_num: int):
        """Protag algorithm"""
        users_to_remove = []
        old_buckets = self.buckets
        # should this be copy.deepcopy???
     
        self.buckets = []
        attackednum = 0
        users_to_shuffle = []
        for bucket in old_buckets:
            if bucket.attacked:
                attackednum +=1
                for user in bucket.users:
                    users_to_shuffle.append(user)
                # Only one user and attacked, so remove both
                if len(bucket) == 1:
                    users_to_remove.extend(bucket.users)
                # else:
                #     # Attacked with more than one user, split in two
                #     for user_chunk in split_list(bucket.users, 2):
                #         self.buckets.append(Bucket(user_chunk))
            else:
                # Not attacked, do not change
                self.buckets.append(bucket)
        random.shuffle(users_to_shuffle)

        if attackednum == len(old_buckets):
            attackednum = attackednum*2
        else:
            attackednum +=1
        if attackednum > len(users_to_shuffle):
            attackednum = len(users_to_shuffle)
        if attackednum > 0:
            for user_chunk in split_list(users_to_shuffle, attackednum):
                self.buckets.append(Bucket(user_chunk))

        self.users = [x for x in self.users if x not in users_to_remove]
        self.attackers_detected += len(users_to_remove)
