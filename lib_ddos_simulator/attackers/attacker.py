#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Attacker, for attackers in simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from ..simulation_objects import User


class Attacker(User):
    """Simulates an attacker for a DDOS attack"""

    # Horns is used for animations
    __slots__ = ["horns"]

    og_face_color = "r"

    # Whether attacker attacks alone or not
    lone = False

    # List of attackers that inherit from this class
    runnable_attackers = []

    # https://stackoverflow.com/a/43057166/8903959
    def __init_subclass__(cls, **kwargs):
        """This method essentially creates a list of all subclasses

        This is allows us to know all attackers that have been created
        """

        super().__init_subclass__(**kwargs)
        assert hasattr(cls, "runnable"), "Subclass must have runnable bool"
        if cls.runnable and not cls.lone:
            cls.runnable_attackers.append(cls)

    def take_action(self, manager, turn):
        """Action that user takes every round"""

        User.take_action(self, manager, turn)
        self.attack(turn)
        assert self.bucket in manager.buckets

    def attack(self, turn):
        """Attacks the bucket it's in"""

        # Don't attack if another attacker attacked
        if self.lone and self.bucket.attacked:
            return
        else:
            self._attack(turn)

    def _attack(self, turn):
        """Set bucket to be attacked"""

        self.bucket.attacked = True
