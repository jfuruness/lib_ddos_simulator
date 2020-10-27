#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class User_Status, for users in simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from enum import Enum

class User_Status(Enum):
    """Possible users status"""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ELIMINATED = "eliminated"
