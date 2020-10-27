#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Simulation, to simulate a DDOS attack"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .ddos_simulator import DDOS_Simulator

from ..simulation_objects import Fluid_User


class Fluid_DDOS_Simulator(DDOS_Simulator):
    """Simulates a DDOS attack"""

    def __init__(self, *args, **kwargs):
        kwargs["user_cls"] = Fluid_User
        super(Fluid_DDOS_Simulator, self).__init__(*args, **kwargs)

    def add_users(self, round_num):
        """Adds users to sim (connects them). Override this method

        Should return a list of user ids to add"""

        _id = self.next_unused_user_id
        self.next_unused_user_id += 1
        return [_id]

    def add_attackers(self, round_num):
        """Adds attackers to sim (connects them). Override this method

        Should return a list of attackers to add"""

        _id = self.next_unused_user_id
        self.next_unused_user_id += 1
        return [_id]
