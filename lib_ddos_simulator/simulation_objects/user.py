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

    # Used in animations
    patch_radius = 1
    patch_padding = .25
    og_face_color = "g"

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
        self.random_sort_id = random.random()

    def take_action(self, *args):  # Note that args are manager, turn
        """Action that user takes every round"""

        # Used in DOSE for connection lifetime
        self.conn_lt += 1
        if self.bucket.attacked:
            self.turns_attacked_in_a_row += 1
        else:
            self.turns_attacked_in_a_row = 0

    def disconnect(self, round_num):
        """Inherit to include when user will disconnect"""

        return False

    # For animations, since dose has it's own suspicion of sorts
    def get_suspicion(self):
        if self.suspicion > 0:
            return self.suspicion
        elif self.dose_risk > self.lone_drone_suspicion:
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
            if self.suspicion == other.suspicion:
                if self.random_sort_id == other.random_sort_id:
                    print("Add code to ensure random sort ids are unique")
                    return random.random() < .5
                else:
                    return self.random_sort_id < other.random_sort_id
            else:
                return self.suspicion < other.suspicion

    def __repr__(self):
        """For printing"""

        # Uses class name so that it also works for attackers
        return f"{self.__class__.__name__} {self.id}:{self.suspicion}"

    @staticmethod
    def patch_length():
        """Returns animation object length"""

        return User.patch_radius * 2 + User.patch_padding * 2
