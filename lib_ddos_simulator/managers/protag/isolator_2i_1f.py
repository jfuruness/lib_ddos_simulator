#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Protag_Manager, which manages a cloud

This manager inherits Manager class and uses Protag shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from math import sqrt

from .protag_manager_base import Protag_Manager_Base

from ...simulation_objects import User_Status
from ...utils import split_list

class Isolator_2i_1f(Protag_Manager_Base):
    """Simulates a manager for a DDOS attack

    This Manager class uses a protag shuffling algorithm

    this manager class also merges buckets in a smart way"""

    __slots__ = []

    runnable = True
    conservative = False
    name = "(2,1)-ISOLATOR"

    def remove_attackers(self):
        """had to be moved into combine buckets func"""

        pass


    def combine_buckets(self):
        """Merge all non attacked buckets"""


        attacked_buckets = self.attacked_buckets
        merge_buckets = set()
        new_tracked_splits = []
        for tracked_split in self.tracked_splits:
            mergeable = False
            remove_buckets = []
            for bucket in tracked_split:
                if bucket.attacked or len(bucket) == 0:
                    # Remove the attacked bucket id from good buckets
                    remove_buckets.append(bucket)
            for bucket in remove_buckets:
                tracked_split.discard(bucket)
                merge_buckets.discard(bucket)
                mergeable = True
            # Mergeable if attacked, or 0 buckets in tracked_split
            if mergeable:
                for bucket in tracked_split:
                    merge_buckets.add(bucket)
            else:
                new_tracked_splits.append(tracked_split)


        attackers_guess = len(attacked_buckets) + len(new_tracked_splits)
        for bucket in attacked_buckets:
            if len(bucket) == 1:
                self.attackers_detected += 1
                self.change_user_status(bucket.users[0], User_Status.ELIMINATED)
                bucket.users[0].bucket = None
                self.remove_bucket(bucket)
                attackers_guess -= 1

        self.tracked_splits = new_tracked_splits
        users = []
        # Get all users that are not in the tracked splits and aren't attacked
        for bucket in self.non_attacked_buckets:
            in_tracked_splits = False
            for tracked_split in self.tracked_splits:
                if bucket in tracked_split:
                    in_tracked_splits = True
            if bucket in merge_buckets:
                in_tracked_splits = True
            if in_tracked_splits is False:
                merge_buckets.add(bucket)
        # Sorted to preserve deterministic randomness
        for bucket in sorted(list(merge_buckets), key=lambda x: x.id):
            users.extend(bucket.users)
            self.remove_bucket(bucket)
        assert len(set(users)) == len(users)
        if self.conservative:
            split_num = max(min(len(users), attackers_guess), 1)
        elif getattr(self, "sqrt", False):
            split_num = int(sqrt(max(min(len(users), attackers_guess), 1)))
            if split_num == 0:
                split_num = 1
        else:
            split_num = 1

        if split_num > 1 and len(merge_buckets) > 0:
            for user_chunk in split_list(users, split_num):
                self.get_new_bucket().reinit(user_chunk)
        elif split_num == 1 and len(merge_buckets) > 0:
            self.get_new_bucket().reinit(users)
        elif split_num < 1:
            assert False, "Split num must be 1 or more"
