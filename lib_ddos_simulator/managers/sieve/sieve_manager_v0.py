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


class Sieve_Manager_V0(Sieve_Manager_Base):
    """Sieve Manager detect and shuffle algorithm version 1"""

    runnable = False

    def get_buckets_to_sort(self):
        return self.used_buckets


class Sieve_Manager_V0_S0(Sieve_Manager_V0):
    runnable = True
    suspicion_func_num = 0


class Sieve_Manager_V0_S1(Sieve_Manager_V0):
    runnable = True
    suspicion_func_num = 1


class Sieve_Manager_V0_S2(Sieve_Manager_V0):
    runnable = True
    suspicion_func_num = 2
