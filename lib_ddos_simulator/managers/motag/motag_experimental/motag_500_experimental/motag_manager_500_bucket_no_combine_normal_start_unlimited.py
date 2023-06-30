#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Motag, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from ...motag_base import Motag_Manager


class Motag_Manager_500_Bucket_No_Combine_Normal_Start_Unlimited(Motag_Manager):
    runnable = True
    paper = True
    prox = 500
    percent_users_to_save = .95
    name = "(500)-MOTAG non merging unlimited servers"
    merge_buckets = False
    hidden_step = False
    unlimited_servers = True
