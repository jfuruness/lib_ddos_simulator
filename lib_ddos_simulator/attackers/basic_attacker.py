#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a class that inherits from Attacker"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .attacker import Attacker


class Basic_Attacker(Attacker):
    """Basic attacker class"""

    runnable = True

class Basic_Lone_Attacker(Basic_Attacker):
    """Attacks every turn if no attacker in it's bucket attacked"""

    lone = True
