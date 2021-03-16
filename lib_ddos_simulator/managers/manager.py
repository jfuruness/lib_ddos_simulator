#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Manager, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import random

from ..attackers import Attacker
from ..simulation_objects import Bucket, User, User_Status
from ..utils import split_list


class Manager:
    """Simulates a manager for a DDOS attack"""

    runnable_managers = []
    # Managers we are including in our paper
    paper_managers = []

    # https://stackoverflow.com/a/43057166/8903959
    def __init_subclass__(cls, **kwargs):
        """This method essentially creates a list of all subclasses"""

        super().__init_subclass__(**kwargs)

        assert hasattr(cls, "runnable"), f"{cls.__name__}: add runnable attr"

        # Only attack if it's runnable
        if cls.runnable:
            # Ignore all sus funcs > 0, too many managers
            if (hasattr(cls, "suspicion_func_num")
                    and cls.suspicion_func_num != 0):
                pass
            else:
                cls.runnable_managers.append(cls)
                Manager.runnable_managers.append(cls)
                if cls.paper:
                    cls.paper_managers.append(cls)
                    Manager.paper_managers.append(cls)

        for q in [Manager, cls]:
            # Sorts alphabetically
            q.runnable_managers = list(sorted(set(q.runnable_managers),
                                              key=lambda x: x.__name__))
            # Sorts alphabetically
            q.paper_managers = list(sorted(set(q.paper_managers),
                                           key=lambda x: x.__name__))


    def __init__(self, num_buckets: int, users: list):
        """inits buckets and stores threshold"""

        # Used in some managers
        self.num_attackers_guess = None
        # Users id dict
        self.users = {x.id: x for x in users}

        # Create the buckets for the users
        self.buckets = []
        # Ids start at 1 for animations
        # Divide users evenly among buckets
        for _id, user_chunk in enumerate(split_list(users,
                                                    num_buckets)):
            self.buckets.append(Bucket(user_chunk, _id + 1))
        self.bucket_id = _id + 2

        self.attackers_detected = 0

        # Simple error checks
        self.validate()

    def take_action(self, turn=0):
        """Actions to take every turn"""

        # Detects and removes suspicious users, then shuffles
        self.detect_and_shuffle(turn)
        # All buckets are no longer attacked for the next round
        self.reset_buckets()

    def get_new_bucket(self):
        try:
            bucket = self.non_used_buckets[0]
            return self.non_used_buckets[0]
        except IndexError:
            self.buckets.append(Bucket(id=self.bucket_id))
            self.bucket_id += 1
            return self.buckets[-1]

    def get_new_buckets(self, num_to_get):
        buckets = []
        non_used_buckets = self.non_used_buckets
        for i in range(num_to_get):
            try:
                buckets.append(non_used_buckets[i])
            except IndexError:
                self.buckets.append(Bucket(id=self.bucket_id))
                self.bucket_id += 1
                buckets.append(self.buckets[-1])
        return buckets

    def validate(self):
        """Simple error checks"""

        assert len(self.users) > 0, "No users? Surely a bug?"
        for user in self.users.values():
            assert user.bucket in self.buckets

    def reset_buckets(self):
        """Sets all buckets to not be attacked"""

        for bucket in self.buckets:
            bucket.attacked = False

    def remove_attackers(self):
        """Removes buckets and attackers if bucket is attacker and len is 1"""

        caught_attackers = []
        for bucket in self.used_buckets:
            if bucket.attacked and len(bucket) == 1:
                self.attackers_detected += 1
                for user in bucket.users:
                    user.status = User_Status.ELIMINATED
                    user.bucket = None
                caught_attackers.extend(bucket.users)
                bucket.users = []
                bucket.attacked = True
        return caught_attackers

    def disconnect_users(self, disconnect_user_ids):
        """Disconnect users. Set status to disconnected"""

        for _id in disconnect_user_ids:
            user = self.users[_id]
            assert user.status == User_Status.CONNECTED
            user.bucket.users.remove(user)
            user.bucket = None
            user.status = User_Status.DISCONNECTED

    def get_buckets_by_ids(self, ids):
        """Returns a list of buckets by ids"""

        return [x for x in self.buckets if x.id in set(ids)]

##################################
### Convenience property funcs ###
##################################

    @property
    def attacked_buckets(self):
        """Return all attacked buckets"""

        return [x for x in self.used_buckets if x.attacked]

    @property
    def non_attacked_buckets(self):
        """Returns all non attacked buckets"""

        return [x for x in self.used_buckets if not x.attacked]

    @property
    def attacked_users(self):
        """Returns all attacked users"""

        attacked_users = []
        for bucket in self.attacked_buckets:
            attacked_users.extend(bucket.users)
        return attacked_users



    @property
    def connected_users(self):
        return self._get_connected_users()

    def _get_connected_users(self, filter_func=None):
        if filter_func is None:
            return [x for x in self.users.values()
                    if x.status == User_Status.CONNECTED]
        else:
            return [x for x in self.users.values()
                    if x.status == User_Status.CONNECTED
                    and filter_func(x)]

    @property
    def eliminated_users(self):
        return [x for x in self.users.values()
                if x.status == User_Status.ELIMINATED]

    @property
    def disconnected_users(self):
        return [x for x in self.users.values()
                if x.status == User_Status.DISCONNECTED]

    @property
    def serviced_users(self):
        return self._get_connected_users(lambda x: x.bucket.attacked is False)

    @property
    def attacked_users(self):
        return self._get_connected_users(lambda x: x.bucket.attacked is True)

    @property
    def connected_attackers(self):
        return self._get_connected_users(lambda x: isinstance(x, Attacker))

    @property
    def connected_good_users(self):
        return self._get_connected_users(lambda x: not isinstance(x, Attacker))

    @property
    def used_buckets(self):
        return [x for x in self.buckets if len(x) > 0]

    @property
    def non_used_buckets(self):
        return [x for x in self.buckets if len(x) == 0]
