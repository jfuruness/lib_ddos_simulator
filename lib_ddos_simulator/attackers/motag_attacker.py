#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker


class Motag_Attacker(Attacker):
    """Basic attacker class"""

    runnable = True

    def _attack(self, manager, turn):
        """desc below

        If it is the last user in a bucket,
            do nothing, so motag will not know it is you
        else if there is a bucket with no attackers that is larger than your own:
            # This is to get added to the service bucket
            do nothing
        else:
            attack
        """

        # If the attacker is the last one left, do not attack
        # Or else the attacker would be discovered
        if len(self.bucket) == 1:
            pass
        # Don't bother computing this math if the bucket is already attacked
        elif self.bucket.attacked is False:
            non_attacked_buckets = manager.non_attacked_buckets
            if len(non_attacked_buckets) > 0:
                # If there is a bigger non attacked bucket, do nothing
                # This will get you put in the service bucket
                for bucket in non_attacked_buckets:
                    if len(bucket) > len(self.bucket):
                        return

                # If we reached here, none are bigger. Attack!
                self.bucket.attacked = True
            else:
                self.bucket.attacked = True
