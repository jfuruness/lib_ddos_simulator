#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class User, for users in simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from math import e
import random

class User:
    """Simulates a user for a DDOS attack"""

    # patch, text used in animations
    __slots__ = ["id", "suspicion", "bucket", "patch", "text", "points",
                 "suspicions", "exp_conn_lt", "conn_lt", "dose_atk_risk",
                 "track_suspicion", "status", "turns_attacked_in_a_row",
                 "random_sort_id"]

    def __init__(self, identifier: int, suspicion: float = 0, bucket=None):
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
        # Expected connection lifetime
        # This was hardcoded in DOSE paper
        self.exp_conn_lt = 100
        # Connection lifetime (incriments each round)
        self.conn_lt = 0
        self.dose_atk_risk = 0
        self.status = None
        self.turns_attacked_in_a_row = 0

    def take_action(self, *args):  # Note that args are manager, turn
        """Action that user takes every round"""

        # Used in DOSE for connection lifetime
        self.conn_lt += 1
        if self.bucket.attacked:
            self.turns_attacked_in_a_row += 1
        else:
            self.turns_attacked_in_a_row = 0

    # For animations, since dose has it's own suspicion of sorts
    def get_suspicion(self):
        if self.dose_risk > 0:
            return self.dose_risk
        else:
            return self.suspicion

    @property
    def dose_risk(self):
        return self.lone_drone_suspicion + self.dose_atk_risk

    @property
    def lone_drone_suspicion(self):
        """Lone drone suspicion for dose algorithm"""

        return e ** (-self.conn_lt / self.exp_conn_lt)

    def __lt__(self, other):
        """Comparison operator for users"""

        if isinstance(other, User):
            return self.suspicion < other.suspicion

    def __repr__(self):
        """For printing"""

        # Uses class name so that it also works for attackers
        return f"{self.__class__.__name__} {self.id}:{self.suspicion}"
