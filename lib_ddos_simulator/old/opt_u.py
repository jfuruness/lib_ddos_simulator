#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Sieve_Manager, which manages a cloud

This manager inherits Manager class and uses Sieve shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .sieve_manager_base import Sieve_Manager_Base
from .sieve_manager_v0 import Sieve_Manager_V0


class Opt_U(Sieve_Manager_V0):
    runnable = True
    paper = True
    def get_buckets_to_sort(self):
        return self.attacked_buckets
    start_number_of_buckets = 2
    def detect_and_shuffle(self, *args):
        self.remove_attackers()
        buckets = self.get_buckets_to_sort()
        if len(buckets) > 0:
            self._reorder_buckets(buckets)
            self._sort_buckets(buckets)

    suspicion_func_num = 1
