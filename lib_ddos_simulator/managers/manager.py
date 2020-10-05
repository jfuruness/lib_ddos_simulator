#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Manager, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from random import shuffle

from ..attackers import Attacker
from ..simulation_objects import Bucket, User
from ..utils import split_list


class Manager:
    """Simulates a manager for a DDOS attack"""

    __slots__ = ["users", "_threshold", "buckets", "attackers_detected",
                 "eliminated_users", "og_num_buckets", "max_users_y",
                 "max_buckets", "og_user_order", "bucket_id", "og_json",
                 "downed_json"]

    runnable_managers = []

    # https://stackoverflow.com/a/43057166/8903959
    def __init_subclass__(cls, **kwargs):
        """This method essentially creates a list of all subclasses"""

        super().__init_subclass__(**kwargs)

        assert hasattr(cls, "runnable"), "Must add runnable class attr"

        # Only attack if it's runnable
        if cls.runnable:
            # Ignore all sus funcs > 0, too many managers
            if (hasattr(cls, "suspicion_func_num")
                    and cls.suspicion_func_num != 0):
                pass
            else:
                cls.runnable_managers.append(cls)
                Manager.runnable_managers.append(cls)

        for q in [Manager, cls]:
            # Sorts alphabetically
            q.runnable_managers = list(sorted(set(q.runnable_managers),
                                              key=lambda x: x.__name__))

    def __init__(self,
                 num_buckets: int,
                 users: list,
                 threshold: int = 0,
                 # Used in animations
                 max_users_y=0,
                 max_buckets=0):
        """inits buckets and stores threshold"""

        # NOTE: should prob change this and have self.users
        # NOTE: be a property iterating over self.buckets
        self.users = users
        self.og_user_order = [x.id for x in self.users]
        self._threshold = threshold
        self.og_num_buckets = num_buckets
        self.buckets = []
        # Divide users evenly among buckets
        for _id, user_chunk in enumerate(split_list(self.users, num_buckets)):
            self.buckets.append(Bucket(user_chunk, _id))
        self.bucket_id = _id + 1

        if max_buckets > 0:
            self.add_additional_buckets(max_buckets)
        self.attackers_detected = 0
        self.eliminated_users = []
        # Simple error checks
        self.validate()

        # Animation statistics
        self.max_users_y = max_users_y
        self.max_buckets = max_buckets
        self.get_animation_statistics()

    def reinit(self):
        users_dict = {x.id: x for x in self.users + self.eliminated_users}
        for user in users_dict.values():
            user.suspicion = 0
            user.conn_lt = 0
            user.dose_atk_risk = 0
        self.__init__(self.og_num_buckets,
                      # Reorder users to how they were originally
                      [users_dict[x] for x in self.og_user_order],
                      self._threshold,
                      max_users_y=self.max_users_y,
                      max_buckets=self.max_buckets)

    def take_action(self, turn=0):
        """Actions to take every turn"""

        self.record_dose_events()
        # Detects and removes suspicious users, then shuffles
        self.detect_and_shuffle(turn)
        # All buckets are no longer attacked for the next round
        self.reset_buckets()

    def record_dose_events(self):
        """Only DOSE does this, ignore"""
        pass

    def get_new_bucket(self):
        try:
            return self.non_used_buckets[0]
        except IndexError:
            self.buckets.append(Bucket(id=self.bucket_id))
            self.bucket_id += 1
            return self.buckets[-1]

    def add_additional_buckets(self, max_buckets):
        """Must add additional buckets depending on algo"""

        new_buckets = max_buckets - len(self.buckets)
        self.buckets += [Bucket() for _ in range(new_buckets)]

    def validate(self):
        """Simple error checks"""

        assert len(self.users) > 0, "No users? Surely a bug?"
        for user in self.users:
            assert user.bucket in self.buckets

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

    def reset_buckets(self):
        """Sets all buckets to not be attacked"""

        self.get_animation_statistics()
        for bucket in self.buckets:
            bucket.attacked = False

    def remove_attackers(self):
        """Removes buckets and attackers if bucket is attacker and len is 1"""

        caught_attackers = []
        for bucket in self.buckets:
            if bucket.attacked and len(bucket) == 1:
                self.attackers_detected += 1
                self.eliminated_users.extend(bucket.users)
                caught_attackers.extend(bucket.users)
                bucket.users = []
                bucket.attacked = True

        # Prob not needed, just in case
        self.users = []
        for bucket in self.buckets:
            self.users.extend(bucket.users)

        return caught_attackers

    @property
    def attackers(self):
        """Returns all attackers"""

        return [x for x in self.users if isinstance(x, Attacker)]

    @property
    def used_buckets(self):
        """Returns all buckets with users"""

        return [x for x in self.buckets if len(x) > 0]

    @property
    def unused_buckets(self):
        """Returns all unused buckets"""

        return [x for x in self.buckets if len(x) == 0]

    @property
    def non_used_buckets(self):
        return self.unused_buckets

    def get_animation_statistics(self):
        cur_max_users_y = max(len(x) for x in self.buckets)
        self.max_users_y = max(cur_max_users_y, self.max_users_y)
        self.max_buckets = max(len(self.buckets), self.max_buckets)

    def add_user(self, user: User):
        """Adds user to lowest bucket.

        If no buckets are accepting new users, then redistribute buckets

        For larger scale simulation, a better sorting algo should
        be used. But for now we don't call it

        NOTE that a sorting algo must be used because sometimes buckets
        lose users since the manager detects them as an attacker
        """

        assert False, "Not yet implimented"

    @property
    def json(self):
        """For flask app, returns json of {bucket_id: user_ids}"""

        buckets = {bucket.id: list(sorted([x.id for x in bucket.users]))
                   for bucket in self.used_buckets}
        eliminated = list(sorted(x.id for x in self.eliminated_users)),
        return {"bucket_mapping": buckets,
                "eliminated_users": eliminated,
                "manager": self.__class__.__name__}

    def get_buckets_by_ids(self, ids):
        """Returns a list of buckets by ids"""

        return [x for x in self.buckets if x.id in set(ids)]
