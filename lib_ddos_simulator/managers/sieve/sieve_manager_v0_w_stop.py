#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Sieve_Manager, which manages a cloud

This manager inherits Manager class and uses Sieve shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .sieve_manager_v0 import Sieve_Manager_V0


class Sieve_Manager_V0_W_Stop(Sieve_Manager_V0):
    """Sieve Manager detect and shuffle algorithm version 1"""

    runnable = False

    def drop_buckets(self):
        """Drops buckets for certain conditions"""

        if len(self.serviced_users) >= len(self.connected_users) * 2 / 3:
            self.disconnect_users([x.id for x in self.attacked_users
                                   if x.turns_attacked_in_a_row >= 10])


class Sieve_Manager_V0_W_Stop_S0(Sieve_Manager_V0_W_Stop):
    runnable = True
    suspicion_func_num = 0


class Sieve_Manager_V0_W_Stop_S1(Sieve_Manager_V0_W_Stop):
    runnable = True
    suspicion_func_num = 1


class Sieve_Manager_V0_W_Stop_S2(Sieve_Manager_V0_W_Stop):
    runnable = True
    suspicion_func_num = 2
