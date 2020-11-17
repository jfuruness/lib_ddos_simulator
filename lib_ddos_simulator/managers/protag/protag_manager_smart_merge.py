#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Protag_Manager, which manages a cloud

This manager inherits Manager class and uses Protag shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"


from .protag_manager_base import Protag_Manager_Base

from ...simulation_objects import User_Status
from ...utils import split_list

class Protag_Manager_Smart_Merge(Protag_Manager_Base):
    """Simulates a manager for a DDOS attack

    This Manager class uses a protag shuffling algorithm

    this manager class also merges buckets in a smart way"""

    __slots__ = []

    runnable = True
    conservative = False

    def remove_attackers(self):
        """had to be moved into combine buckets func"""

        pass
                

    def combine_buckets(self):
        """Merge all non attacked buckets"""

        merge_buckets = set()
        new_tracked_splits = []
        for tracked_split in self.tracked_splits:
            attacked = False
            for bucket in self.attacked_buckets:
                if bucket in tracked_split:
                    # Remove the attacked bucket id from good buckets
                    tracked_split.discard(bucket)
                    merge_buckets.discard(bucket)
                    # Add all non attacked buckets in split to merge
                    for buck in tracked_split:
                        merge_buckets.add(buck)
                    attacked = True
            if not attacked:
                new_tracked_splits.append(tracked_split)
        for bucket in self.attacked_buckets:
            if len(bucket) == 1:
                self.attackers_detected += 1
                bucket.users[0].status = User_Status.ELIMINATED
                bucket.users = []
                bucket.attacked = False
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
            bucket.users = []
        assert len(set(users)) == len(users)
        if self.conservative:
            split_num = min(len(users), len(self.tracked_splits))
        else:
            split_num = 1
        if split_num > 0:
            for user_chunk in split_list(users, split_num):
                self.get_new_bucket().reinit(user_chunk)
