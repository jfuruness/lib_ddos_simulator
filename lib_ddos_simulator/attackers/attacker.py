#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Attacker, for attackers in simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from random import random

from .user import User

class Attacker(User):
    """Simulates an attacker for a DDOS attack"""

    # Horns is used for animations
    __slots__ = ["horns"]

    lone = False

    runnable_attackers = []
    # https://stackoverflow.com/a/43057166/8903959
    def __init_subclass__(cls, **kwargs):
        """This method essentially creates a list of all subclasses
        This is incredibly useful for a few reasons. Mainly, you can
        strictly enforce proper templating with this. And also, you can
        automatically add all of these things to things like argparse
        calls and such. Very powerful tool.
        """

        super().__init_subclass__(**kwargs)
        cls.runnable_attackers.append(cls)


    def attack(self, turn):
        """Attacks the bucket it's in"""

        if self.lone and self.bucket.attacked:
            return
        else:
            self._attack(turn)

    def _attack(self, turn):
        self.bucket.attacked = True

class Basic_Attacker(Attacker):
    pass

class Basic_Lone_Attacker(Basic_Attacker):
    lone = True

class Even_Turn_Attacker(Attacker):
    def _attack(self, turn):
        if turn % 2:
            self.bucket.attacked = True

class Even_Turn_Lone_Attacker(Even_Turn_Attacker):
    lone = True

class Fifty_Percent_Attacker(Attacker):
    def _attack(self, turn):
        if random() < .5:
            self.bucket.attacked = True

class Fifty_Percent_Lone_Attacker(Fifty_Percent_Attacker):
    lone = True

class Ten_Percent_Attacker(Attacker):
    def _attack(self, turn):
        if random() < .1:
            self.bucket.attacked = True

class Ten_Percent_Lone_Attacker(Ten_Percent_Attacker):
    lone = True

class Wait_For_One_Addition_Attacker(Attacker):
    num_additions = 1

    def add_additions(self, turn):
        if turn == 0:
            self.starting_users = len(self.bucket)
            self.total_additions = 0
        if len(self.bucket.users) > self.starting_users:
            self.total_additions += 1
            self.starting_users = len(self.bucket.users)

    def _attack(self, turn):
        self.add_additions(turn)
        if self.total_additions > self.num_additions:
            self.bucket.attacked = True

class Wait_For_One_Addition_Lone_Attacker(Wait_For_One_Addition_Attacker):
    lone = True

class Wait_For_Two_Additions_Attacker(Wait_For_One_Addition_Attacker):
    num_additions = 2

class Wait_For_Two_Additions_Lone_Attacker(Wait_For_Two_Additions_Attacker):
    lone = True

class Wait_For_Three_Additions_Attacker(Wait_For_One_Addition_Attacker):
    num_additions = 2

class Wait_For_Three_Additions_Lone_Attacker(Wait_For_Three_Additions_Attacker):
    lone = True

class Mixed_Attacker(Attacker):
    @staticmethod
    def get_mix(num_attackers):
        attacker_classes = []
        for attacker_cls in [Fifty_Percent_Lone_Attacker,
                             Wait_For_One_Addition_Lone_Attacker,
                             Wait_For_Two_Additions_Lone_Attacker,
                             Wait_For_Three_Additions_Lone_Attacker]:
            for _ in range(int(og_num_attackers * .1)):
                attacker_classes.append(attacker_cls)
        for _ in range(len(attacker_classes) - num_attackers):
            attacker_classes.append(Basic_Attacker)
        return attacker_classes 
