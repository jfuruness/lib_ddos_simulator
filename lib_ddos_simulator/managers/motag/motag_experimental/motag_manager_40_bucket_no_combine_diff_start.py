#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Motag, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from ..motag_base import Motag_Manager


class Motag_Manager_40_Bucket_No_Combine_Diff_Start(Motag_Manager):
    runnable = True
    paper = True
    prox = 40
    percent_users_to_save = .95
    name = "(40)-MOTAG no merge, diff start"
    merge_buckets = False
    hidden_step = True
