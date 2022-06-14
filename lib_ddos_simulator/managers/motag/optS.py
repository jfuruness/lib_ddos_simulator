#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Motag, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .motag_base import Motag_Manager


class Opt_S(Motag_Manager):
    runnable = True
    paper = False
    prox = 1
    percent_users_to_save = .95
