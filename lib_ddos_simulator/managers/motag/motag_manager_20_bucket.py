#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Motag, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .motag_base import Motag_Manager


class Motag_Manager_20_Bucket(Motag_Manager):
    runnable = True
    paper = True
    prox = 20
    percent_users_to_save = .95
    name = "(20)-MOTAG"
