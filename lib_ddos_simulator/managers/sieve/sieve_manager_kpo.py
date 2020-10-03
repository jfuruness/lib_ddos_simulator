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


class Sieve_Manager_KPO(Sieve_Manager_Base):
    """Sieve Manager detect and shuffle algorithm version 1"""

    runnable = False

    def get_buckets_to_sort(self):
        # Double attacked buckets if atked buckets == total
        if len(self.attacked_buckets) == len(self.used_buckets):
            buckets_to_add = len(self.attacked_buckets)
        elif len(self.attacked_buckets) > 0:
            buckets_to_add = 1
        else:
            buckets_to_add = 0
        return self.attacked_buckets + [self.get_new_bucket()
                                        for _ in range(buckets_to_add)]
    


class Sieve_Manager_KPO_S0(Sieve_Manager_KPO):
    runnable = True
    suspicion_func_num = 0


class Sieve_Manager_KPO_S1(Sieve_Manager_KPO):
    runnable = True
    suspicion_func_num = 1


class Sieve_Manager_KPO_S2(Sieve_Manager_KPO):
    runnable = True
    suspicion_func_num = 2
