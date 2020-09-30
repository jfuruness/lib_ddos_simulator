#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Manager, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .bucket import Bucket
from .user import User
from .utils import split_list

class Manager:
    """Simulates a manager for a DDOS attack"""

    __slots__ = ["users", "_threshold", "buckets", "attackers_detected"]
  
    def __init__(self, num_buckets: int, users: list, threshold: int):
        """inits buckets and stores threshold"""

        self.users = users
        assert len(self.users) > 0, "No users? Surely a bug?"
        self._threshold = threshold
        self.buckets = [Bucket(user_chunk) for user_chunk in
                        split_list(self.users, num_buckets)]
        for user in self.users:
            assert user.bucket in self.buckets
        self.attackers_detected = 0

    @property
    def attacked_buckets(self):
        return [x for x in self.buckets if x.attacked]

    @property
    def non_attacked_buckets(self):
        return [x for x in self.buckets if not x.attacked]

    @property
    def attacked_users(self):
        attacked_users = []
        for bucket in self.attacked_buckets:
            attacked_users.extend(bucket.users)
        return attacked_users
            
    def reset_buckets(self):
        """Sets all buckets to not be attacked"""

        for bucket in self.buckets:
            bucket.attacked = False

    def add_user(self, user: User):
        """Adds user to lowest bucket.

        If no buckets are accepting new users, then redistribute buckets

        For larger scale simulation, a better sorting algo should
        be used. But for now we don't call it

        NOTE that a sorting algo must be used because sometimes buckets
        lose users since the manager detects them as an attacker
        """

        1/0
