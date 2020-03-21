#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Bucket, for service bucket in sim"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

class Bucket:
    """Simulates a Bucket that provides service for users"""

    __slots__ = ["users", "_max_users", "attacked"]
  
    def __init__(self, users: list = [], max_users=100000000):
        """Stores users"""

        assert len(users) < max_users, "Too many users, over max_users"

        self.users = users
        for user in users:
            user.bucket = self
        self._max_users = max_users
        self.attacked = False

    def __str__(self):
        """Returns users inside of bucket"""

        return self.users

    def __len__(self):
        """Number of users in bucket"""

        return len(self.users)

    def add_user(self, user):
        """Adds user if not over _max_users, returns True, else False"""

        if len(self.users) > self._max_users:
            return False
        else:
            self.users.append(user)
            return True

    def update_suspicion(self):
        """Updates suspicion level of all users in bucket"""

        multiplier = 1 if self.attacked else -1
        for user in self.users:
            user.suspicion += (1 / len(self.users)) * multiplier
