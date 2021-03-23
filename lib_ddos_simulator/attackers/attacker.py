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

    # List of attackers that inherit from this class
    runnable_attackers = []
    # List of attackers that are in our paper (the rest are too weak)
    paper_attackers = []
    # Default to True
    paper = True

    # https://stackoverflow.com/a/43057166/8903959
    def __init_subclass__(cls, **kwargs):
        """This method essentially creates a list of all subclasses

        This is allows us to know all attackers that have been created
        """

        super().__init_subclass__(**kwargs)
        assert hasattr(cls, "runnable"), "Subclass must have runnable bool"
        if cls.runnable:
            cls.runnable_attackers.append(cls)
            if cls.paper:
                cls.paper_attackers.append(cls)

    def take_action(self, manager, turn):
        """Action that user takes every round"""

        self._attack(manager, turn)
        User.take_action(self, manager, turn)
        assert self.bucket.id in manager.used_buckets

    def _attack(self, manager, turn):
        """Set bucket to be attacked"""

        self.bucket.attacked = True

    @classmethod
    def get_attackers(cls, next_id, num_attackers):
        return [cls(_id + next_id) for _id in range(num_attackers)]
