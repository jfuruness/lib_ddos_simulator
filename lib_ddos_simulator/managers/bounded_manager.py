#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Bounded_Manager, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import random

from .manager import Manager

from ..utils import split_list


class Bounded_Manager(Manager):
    """Simulates a manager for a DDOS attack

    This Manager class uses a bounded shuffling algorithm"""

    __slots__ = ["num_attackers_guess"]

    runnable = True

    def __init__(self, *args, **kwargs):
        super(Bounded_Manager, self).__init__(*args, **kwargs)
        self.num_attackers_guess = None

    def detect_and_shuffle(self, *args):
        """Bounded Manager algorithm"""

        if self.num_attackers_guess is None:
            # Start attacker guess with # attacked buckets
            self.num_attackers_guess = len(self.attacked_buckets)

        # If number of attacked buckets is greater than guess
        if len(self.attacked_buckets) > self.num_attackers_guess:
            # Move attackers into # attacked_buckets - guess
            self.case_1()
        # Number of buckets < attacker guess * 3
        elif len(self.buckets) < self.num_attackers_guess * 3:
            # Move attackers into # attacked buckets + 1
            self.case_2()
        # Number of buckets >= attacker_guess * 3
        else:
            # Combine all every other non attacked bucket by reputation
            self.case_3()

        # Count # of times bucket not attacked
        self._incriment_buckets()

    def case_1(self):
        """When number of attacked buckets is greater than guess

        Move attackers into # attacked_buckets - guess"""

        # New buckets = total # attackers - old guess
        new_bucket_amnt = len(self.attacked_buckets)
        new_bucket_amnt -= self.num_attackers_guess
        # Shuffle attacked buckets with new amnt
        self._shuffle_attacked_buckets(new_bucket_amnt)
        # Reset attacker guess
        self.num_attackers_guess = len(self.attacked_buckets)

    def case_2(self):
        """Number of buckets < attacker guess * 3

        Move attackers into # attacked buckets + 1"""

        # Shuffle attacked users into num attacked buckets * 2
        # So one new bucket
        self._shuffle_attacked_buckets(len(self.attacked_buckets) + 1)

    def case_3(self):
        """Number of buckets >= attacker_guess * 3

        Combine non attacked buckets by reputation,
        add one to attacked buckets"""

        # Sorts buckets by reputation
        sorted_buckets = list(sorted(self.non_attacked_buckets,
                                     key=lambda x: x.turns_not_attacked))
        # For every other bucket
        for i in range(0, len(sorted_buckets), 2):
            try:
                # Combine the two buckets
                users = sorted_buckets[i].users
                users += sorted_buckets[i + 1].users
                sorted_buckets[i].users = users
                sorted_buckets[i + 1].users = []
            # last bucket
            except IndexError:
                # Odd # of buckets, just append the full bucket
                # NOTE: This should prob be changed
                # NOTE: Should evenly divide out amongst all buckets
                # NOTE: rather than having one last full bucket
                pass
        # Add one bucket to attackers and reorder
        self._shuffle_attacked_buckets(len(self.attacked_buckets) + 1)

    def _shuffle_attacked_buckets(self, new_bucket_amnt):
        """Detects/Moves attackers into new_bucket_amnt buckets and shuffles"""

        # Get rid of attackers if they are the only one in the bucket first
        new_attacked_buckets = [x for x in self.attacked_buckets if len(x) > 1]
        new_bucket_amnt = self._remove_attackers(new_attacked_buckets,
                                                 new_bucket_amnt)

        # Checking to make sure we didn't remove all attackers
        if len(self.attacked_buckets) > 0 and new_bucket_amnt > 0:
            # This can happen if we remove an attacker
            if new_bucket_amnt > len(self.attacked_users):
                new_bucket_amnt = len(self.attacked_users)
            users = self.attacked_users
            random.shuffle(users)

            # Clear out buckets
            for bucket in self.attacked_buckets:
                bucket.users = []

            for i, user_chunk in enumerate(split_list(users, new_bucket_amnt)):
                self.get_new_bucket().reinit(user_chunk)

    def _remove_attackers(self, new_attacked_buckets, new_bucket_amnt):
        """Removes attackers if they are the only one in the bucket"""

        old_num_buckets = len(self.attacked_buckets)
        # Removes attacked buckets and their attackers if bucket len is 1
        self.remove_attackers()
        diff = len(self.attacked_buckets) - old_num_buckets

        # If we removed attackers
        if diff > 0:
            # Remove buckets
            self.num_attackers_guess -= diff
            new_bucket_amnt -= diff
        return new_bucket_amnt

    def _incriment_buckets(self):
        """Incriments buckets by # turns not attacked in a row"""

        for bucket in self.used_buckets:
            if bucket.attacked:
                bucket.turns_not_attacked = 0
            else:
                bucket.turns_not_attacked += 1
