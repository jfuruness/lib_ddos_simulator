#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Sieve_Manager, which manages a cloud

This manager inherits Manager class and uses Sieve shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from random import shuffle
from .bucket import Bucket
from .manager import Manager
from .utils import split_list

class Sieve_Manager(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a sieve shuffling algorithm"""

    __slots__ = []

    def detect_and_shuffle(self, turn_num: int):
        """Detects attackers and shuffles"""

        self.detect(turn_num)
        self.shuffle()
        
    def detect(self, turn_num: int):
        new_users = []
        for user in self.users:
            if user.suspicion > self._threshold:
#                print(f"Detected {user.__class__.__name__} on turn {turn_num}")
                new_users.append(user)
            else:
                new_users.append(user)
        self.users = new_users

    def shuffle(self):
        """Performs sieve shuffle algorithm

        First updates suspicion of users.
        Then sorts users by suspicion.
        Then splits users into num buckets/2 chunks
        Then for each chunk, put in two buckets randomly
        """

        self._update_suspicion()
        num_buckets = len(self.buckets)
        self.buckets = []
        for user_chunk in split_list(self.users, num_buckets // 2):
            shuffle(user_chunk)
            # adds a new bucket with half the users of that chunk randomly
            self.buckets.append(Bucket(user_chunk[:len(user_chunk) // 2]))
            # adds a new bucket with half the users of that chunk randomly
            self.buckets.append(Bucket(user_chunk[len(user_chunk) // 2:]))

    def _update_suspicion(self):
        """Updates suspicion level of all users"""

        for bucket in self.buckets:
            bucket.update_suspicion()
        self.users.sort()
