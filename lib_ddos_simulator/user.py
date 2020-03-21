#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class User, for users in simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, a97gorbenko@gmail.com"
__status__ = "Development"

class User:
    """Simulates a user for a DDOS attack"""
  
    def __init__(self, identifier: int, suspicion: float = 0, bucket = None):
        """Stores user values"""

        # Used to differentiate users
        self.id = identifier
        # Managers suspicion level
        self.suspicion = suspicion
        # Bucket the user is in for service
        self.bucket = bucket

    def __lt__(self, other):
        """Comparison operator for users"""

        if isinstance(other, User):
            return self.suspicion < other.suspicion

    def __repr__(self):
        """For printing"""

        # Uses class name so that it also works for attackers
        return f"{self.__class__.__name__} {self.id}"

