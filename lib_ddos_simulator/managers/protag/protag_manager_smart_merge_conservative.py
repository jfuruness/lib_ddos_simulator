#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Protag_Manager, which manages a cloud

This manager inherits Manager class and uses Protag shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"


from .protag_manager_smart_merge import Protag_Manager_Smart_Merge

from ...simulation_objects import User_Status
from ...utils import split_list

class Protag_Manager_Smart_Merge_Conservative(Protag_Manager_Smart_Merge):
    """Simulates a manager for a DDOS attack

    This Manager class uses a protag shuffling algorithm

    this manager class also merges buckets in a smart way"""

    __slots__ = []

    runnable = True
    conservative = True
