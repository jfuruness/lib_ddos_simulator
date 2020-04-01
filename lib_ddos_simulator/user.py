#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class User, for users in simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

class User:
    """Simulates a user for a DDOS attack"""

    # patch, text used in animations
    __slots__ = ["id", "suspicion", "bucket", "patch", "text", "points",
                 "suspicions"]

    # Used in animations
    patch_radius = 1
    patch_padding = .25
  
    def __init__(self, identifier: int, suspicion: float = 0, bucket = None):
        """Stores user values"""

        # Used to differentiate users
        self.id = identifier
        # Managers suspicion level
        self.suspicion = suspicion
        # Bucket the user is in for service
        self.bucket = bucket
        # Used for animation
        self.points = []
        self.suspicions = []

    def __lt__(self, other):
        """Comparison operator for users"""

        if isinstance(other, User):
            return self.suspicion < other.suspicion

    def __repr__(self):
        """For printing"""

        # Uses class name so that it also works for attackers
        return f"{self.__class__.__name__} {self.id}"

    @staticmethod
    def patch_length():
        return User.patch_radius * 2 + User.patch_padding * 2
