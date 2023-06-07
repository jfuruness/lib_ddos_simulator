#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker


class Until_Percentage_Attacker(Attacker):
    """Basic attacker class"""

    runnable = False
    paper = False

    def _attack(self, manager, turn):
        # Users that don't have attacker in their bucket
        users_wout_attacker_in_bucket = 0

        # For each bucket in the manager
        for bucket in manager.used_buckets.values():
            # IF the bucket does not contain attackers
            if len(bucket.attackers) == 0:
                # Add users to the users that would get service
                users_wout_attacker_in_bucket += len(bucket)

        # Percentage of users that will get service if we attack
        p_serviced = users_wout_attacker_in_bucket / len(manager.connected_users)

        # If it's worth attacking
        # If percentage of users serviced is less than the acceptable percentage
        # And if we are not the last in the bucket
        if p_serviced < self.percentage_serviced and len(self.bucket) > 1:
            self.bucket.attacked = True


class Until_50_Percent_Attacker(Until_Percentage_Attacker):
    """Basic attacker class"""

    runnable = False
    paper = True

    percentage_serviced = .5
