#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class DOSE_Manager, which manages a cloud

This manager inherits Manager class and uses DOSE shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .dose_attack_event import DOSE_Attack_Event

from ..manager import Manager

from ...utils import split_list


class DOSE_Manager(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a DOSE shuffling algorithm

    FLAWS WITH DOSE
    CRPA and RPR are hardcoded
    the lonedrone risk is not accounted for in fig 4, 5
        but is in 6, and isn't in their code
    attackers randomly attack with 1/8 chance
        -not stated in the paper, makes algos do better
    number of relays can 16X with just one attacker/1k users?
    potentially more with more users (or attackers?)
    with RPR set to 1, lone drone cost forces 1 user to a bucket?
    """

    __slots__ = ["dose_atk_events"]

    runnable = True

    # Single threat case hardcoded to 2 in DOSE code
    # Multithreat case is hardcoded to 3 in DOSE code
    CRPA = 3
    # Hardcoded to 1 in DOSE code (risk per relay)
    RPR = 1

    def __init__(self, *args, **kwargs):
        super(DOSE_Manager, self).__init__(*args, **kwargs)
        # Inner list of (users_set (includes attackers), dose_atk_added)
        self.dose_atk_events = []

    def record_dose_events(self):
        """Keep track of all attacks

        This allows us to remove attacks when ready
        """

        for bucket in self.attacked_buckets:
            self.dose_atk_events.append(DOSE_Attack_Event(bucket))

    def detect_and_shuffle(self, *args):
        """DOSE algorithm"""

        self.remove_attackers()

        for bucket in self.attacked_buckets:
            for user in bucket.users:
                # Suspicion to add:
                # CRPA = 3 in their matplotlib code
                user.dose_atk_risk += self.dose_atk_sus_to_add(bucket)

        for bucket in self.used_buckets:
            new_bucket_amnt = sum(x.dose_risk
                                  for x in bucket.users) // self.RPR
            if new_bucket_amnt > 1:
                if new_bucket_amnt > len(bucket.users):
                    new_bucket_amnt = len(bucket.users)
                user_chunks = split_list(bucket.users, int(new_bucket_amnt))
                bucket.users = []
                # DOSE does not specify any sorting
                for user_chunk in user_chunks:
                    self.get_new_bucket().reinit(user_chunk)

    def remove_attackers(self):
        caught_attackers = super(DOSE_Manager, self).remove_attackers()
        for attacker in caught_attackers:
            old_events = self.dose_atk_events.copy()
            self.dose_atk_events = []
            for event in old_events:
                if attacker.id in event.uids:
                    # reduce
                    event.reduce_sus()
                else:
                    self.dose_atk_events.append(event)
        # Their paper does not specify any sort of bucket combining
        # Also their code does not have any bucket combining

    @staticmethod
    def dose_atk_sus_to_add(bucket):
        # Single threat case hardcoded to 2
        # Multithreat case is hardcoded to 3
        return DOSE_Manager.CRPA / len(bucket)
