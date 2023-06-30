#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Motag, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from ...motag_base import Motag_Manager


class Motag_Manager_500_Bucket_Invalid(Motag_Manager):
    runnable = True
    paper = True
    prox = 500
    percent_users_to_save = .95
    name = "(500)-MOTAG Invalid"

    def __init__(self, num_buckets: int, users: list):
        """inits buckets and stores threshold"""

        # Ignore num buckets, always start with proxy
        super().__init__(num_buckets=self.prox, users=users)
