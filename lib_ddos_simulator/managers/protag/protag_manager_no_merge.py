#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Protag_Manager, which manages a cloud

This manager inherits Manager class and uses Protag shuffling algorithm
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"


from .protag_manager_base import Protag_Manager_Base

from ...simulation_objects import Bucket
from ...utils import split_list

class Protag_Manager_No_Merge(Protag_Manager_Base):
    """Simulates a manager for a DDOS attack

    This Manager class uses a protag shuffling algorithm

    this manager class never merges buckets"""

    __slots__ = []

    runnable = True

    def combine_buckets(self):
        pass
