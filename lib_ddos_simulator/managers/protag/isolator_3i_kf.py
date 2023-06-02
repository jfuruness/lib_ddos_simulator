#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Protag_Manager, which manages a cloud

This manager inherits Manager class and uses Protag shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"


from .isolator_2i_kf import Isolator_2i_kf

from ...simulation_objects import User_Status
from ...utils import split_list

class Isolator_3i_kf(Isolator_2i_kf):
    """Simulates a manager for a DDOS attack

    This Manager class uses a protag shuffling algorithm

    this manager class also merges buckets in a smart way"""

    __slots__ = []

    split_factor = 3
    name = "(3,k)-ISOLATOR"
