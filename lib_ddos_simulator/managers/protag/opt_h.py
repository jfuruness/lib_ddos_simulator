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

from ...simulation_objects import Bucket
from ...utils import split_list

class Opt_H(Protag_Manager_Base):
    """Simulates a manager for a DDOS attack

    This Manager class uses a protag shuffling algorithm

    this manager class never merges buckets"""

    __slots__ = []

    runnable = True

    def combine_buckets(self):
        pass

    def detect_and_shuffle(self,turn,*args):
        self.remove_attackers()
        self.combine_buckets()
        bucks = self.attacked_buckets
        for bucket in bucks:
            user_chunks = split_list(bucket.users, len(bucket.users))
            self.remove_bucket(bucket)
            split_set = set()
            for user_chunk in user_chunks:
                new_bucket = self.get_new_bucket()
                new_bucket.reinit(user_chunk)
                split_set.add(new_bucket)
            self.tracked_splits.append(split_set)
