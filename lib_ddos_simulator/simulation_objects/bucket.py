#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Bucket, for service bucket in sim"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .. import attackers
from .user import User
from .user_status import User_Status


class Bucket:
    """Simulates a Bucket that provides service for users"""

    # patch used in animations
    __slots__ = ["users", "attacked", "patch",
                 "turns_not_attacked", "states", "id"]

    def __init__(self, users=[], id=0, attacked=False):
        """Stores users"""

        self.users = users
        self.id = id
        for user in users:
            user.bucket = self
            user.status = User_Status.CONNECTED
        self.attacked = attacked
        self.turns_not_attacked = 0
        # For animations
        self.states = []

    def __hash__(self):
        return self.id

    def reinit(self, user_chunk):
        """Kept only for backwards compatability"""

        self.__init__(users=user_chunk, id=self.id, attacked=False)

    @property
    def attackers(self):
        return [x for x in self.users if isinstance(x, attackers.Attacker)]

    def __str__(self):
        """Returns users inside of bucket"""

        return str(self.users)

    def __len__(self):
        """Number of users in bucket"""

        return len(self.users)

    def add_user(self, user):
        """Adds user if not over _max_users, returns True, else False"""

        if len(self.users) > self._max_users:
            assert False, "Not yet implimented"
            return False
        else:
            self.users.append(user)
            return True

    def update_suspicion(self):
        """Updates suspicion level of all users in bucket"""

        multiplier = int(self.attacked)
        for user in self.users:
            user.suspicion += (1 / len(self.users)) * multiplier
