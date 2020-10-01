#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Manager, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from ..Simulation_Objects import Bucket, User
from ..utils import split_list


class Manager:
    """Simulates a manager for a DDOS attack"""

    __slots__ = ["users", "_threshold", "buckets", "attackers_detected"]

    def __init__(self, num_buckets: int, users: list, threshold: int):
        """inits buckets and stores threshold"""

        # NOTE: should prob change this and have self.users
        # NOTE: be a property iterating over self.buckets
        self.users = users
        self._threshold = threshold
        # Divide users evenly among buckets
        self.buckets = [Bucket(user_chunk) for user_chunk in
                        split_list(self.users, num_buckets)]
        self.attackers_detected = 0
        # Simple error checks
        self.validate()

    def validate(self):
        """Simple error checks"""

        assert len(self.users) > 0, "No users? Surely a bug?"
        for user in self.users:
            assert user.bucket in self.buckets

    @property
    def attacked_buckets(self):
        """Return all attacked buckets"""

        return [x for x in self.buckets if x.attacked]

    @property
    def non_attacked_buckets(self):
        """Returns all non attacked buckets"""

        return [x for x in self.buckets if not x.attacked]

    @property
    def attacked_users(self):
        """Returns all attacked users"""

        attacked_users = []
        for bucket in self.attacked_buckets:
            attacked_users.extend(bucket.users)
        return attacked_users

    def reset_buckets(self):
        """Sets all buckets to not be attacked"""

        for bucket in self.buckets:
            bucket.attacked = False

    def remove_attackers(self):
        """Removes buckets and attackers if bucket is attacker and len is 1"""

        new_buckets = []
        for bucket in self.buckets:
            if bucket.attacked and len(bucket) == 1:
                self.attackers_detected += 1
            else:
                new_buckets.append(bucket)

        self.buckets = new_buckets
        # Prob not needed, just in case
        self.users = []
        for bucket in self.buckets:
            self.users.extend(bucket.users)

    def add_user(self, user: User):
        """Adds user to lowest bucket.

        If no buckets are accepting new users, then redistribute buckets

        For larger scale simulation, a better sorting algo should
        be used. But for now we don't call it

        NOTE that a sorting algo must be used because sometimes buckets
        lose users since the manager detects them as an attacker
        """

        assert False, "Not yet implimented"
