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


class Protag_Manager_Merge(Protag_Manager_Base):
    """Simulates a manager for a DDOS attack

    This Manager class uses a protag shuffling algorithm

    this manager class also merges buckets if not attacked"""

    __slots__ = []

    runnable = True

    def combine_buckets(self):
        """Merge all non attacked buckets"""

        users = []
        for bucket in self.non_attacked_buckets:
            users.extend(bucket.users)
            bucket.users = []
        merged_bucket = self.get_new_bucket()
        merged_bucket.reinit(users)
