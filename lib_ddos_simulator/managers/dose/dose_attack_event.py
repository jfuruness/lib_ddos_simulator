#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class DOSE_Attack_Event, which records attacks

Useful for DOSE shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"


from . import dose_manager


class DOSE_Attack_Event:
    """Purpose of this class is just to keep track of atk events

    helpful in dealing with DOSE stats
    """

    def __init__(self, bucket):
        self.users = bucket.users
        self.uids = set(x.id for x in bucket.users)
        # 3 is from their matplotlib code
        # This is CRPA val
        self.sus_added = dose_manager.DOSE_Manager.dose_atk_sus_to_add(bucket)

    def reduce_sus(self):
        for user in self.users:
            user.dose_atk_risk -= self.sus_added
