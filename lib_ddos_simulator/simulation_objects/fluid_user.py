#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class User, for users in simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import random

from .user import User

class Fluid_User(User):
    """Simulates a user for a DDOS attack"""

    # patch, text used in animations
    __slots__ = []

    def disconnect(self, round_num):
        """Inherit to include when user will disconnect"""

        return (self.conn_lt / self.exp_conn_lt) > random.random()
