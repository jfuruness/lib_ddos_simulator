#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Protag_Manager, which manages a cloud

This manager inherits Manager class and uses Protag shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, a97gorbenko@gmail.com"
__status__ = "Development"


from .bucket import Bucket
from .manager import Manager
from .utils import split_list

class Protag_Manager(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a protag shuffling algorithm"""

        
    def detect_and_shuffle(self, turn_num: int):
        """Protag algorithm"""

        old_buckets = self.buckets
        users_to_remove = []
        self.buckets = []
        for bucket in old_buckets:
            if bucket.attacked:
                # Only one user and attacked, so remove both
                if len(bucket) == 1:
                    users_to_remove.extend(bucket.users)
                else:
                    # Attacked with more than one user, split in two
                    for user_chunk in split_list(bucket.users, len(bucket) // 2):
                        self.buckets.append(Bucket(user_chunk))
            else:
                # Not attacked, do not change
                self.buckets.append(bucket)
        self.users = [x for x in self.users if x not in users_to_remove]
        for user in users_to_remove:
            pass # print(f"Removed {user.__class__.__name__} on turn {turn_num}")
