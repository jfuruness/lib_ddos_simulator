#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Simulation, to simulate a DDOS attack"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import random

from .ddos_simulator import DDOS_Simulator

from ..simulation_objects import Fluid_User
from ..attackers import Attacker


class Fluid_DDOS_Simulator(DDOS_Simulator):
    """Simulates a DDOS attack"""

    def __init__(self, *args, **kwargs):
        kwargs["user_cls"] = Fluid_User
        super(Fluid_DDOS_Simulator, self).__init__(*args, **kwargs)

    def add_users(self, manager, round_num):
        """Adds users to sim (connects them). Override this method

        Should return a list of user ids to add"""

        og_users = self.og_num_attackers = self.og_num_users
        og_percent_users = self.og_num_users / og_users

        current_good_users = len([1 for x in manager.connected_users
                                 if not isinstance(x, Attacker)])
        current_attackers = len(manager.connected_users) - current_good_users
        current_percent_users = current_good_users / len(manager.connected_users)


        if random.random() > og_percent_users or current_percent_users < og_percent_users:
            if len(manager.disconnected_users) > 2:
                return [manager.disconnected_users[0].id]
            else:
                _id = self.next_unused_user_id
                self.next_unused_user_id += 1
                return [_id]
        else:
            return []

    def add_attackers(self, manager, round_num):
        """Adds attackers to sim (connects them). Override this method

        Should return a list of attackers to add"""

        og_users = self.og_num_attackers = self.og_num_users
        percent_attackers = self.og_num_attackers / og_users

        current_good_users = len([1 for x in manager.connected_users
                                 if not isinstance(x, Attacker)])
        current_attackers = len(manager.connected_users) - current_good_users
        current_percent_attackers = current_attackers / len(manager.connected_users)

        if random.random() > percent_attackers or current_percent_attackers < percent_attackers:
            _id = self.next_unused_user_id
            self.next_unused_user_id += 1
            return [_id]
