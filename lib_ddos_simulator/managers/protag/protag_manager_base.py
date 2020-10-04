#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Protag_Manager, which manages a cloud

This manager inherits Manager class and uses Protag shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"


from ..manager import Manager

from ...utils import split_list


class Protag_Manager_Base(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a protag shuffling algorithm"""

    __slots__ = []

    runnable = False

    def __init__(self, *args, **kwargs):
        """Error checking"""

        msg = "Must have a combine buckets method, even if it's empty"""
        assert self.runnable is False or hasattr(self, "combine_buckets"), msg

        super(Protag_Manager_Base, self).__init__(*args, **kwargs)

    def detect_and_shuffle(self, *args):
        """Protag algorithm"""

        # Removes bucket/attacker if bucket is attacked and len is 1
        # Increase detected by 1 for every attacker removed
        self.remove_attackers()
        self.combine_buckets()

        bucks = self.attacked_buckets
        for bucket in self.attacked_buckets:
            # Attacked with more than one user, split in two
            user_chunk1, user_chunk2 = split_list(bucket.users, 2)
            bucket.reinit(user_chunk1)
            self.get_new_bucket().reinit(user_chunk2)
