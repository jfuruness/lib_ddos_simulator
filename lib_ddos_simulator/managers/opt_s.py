#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Motag, which manages a cloud"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .manager import Manager


class Opt_S(Manager):
    """Runs on 1 server and does nothing"""

    runnable = True
    paper = True
    name = "MinC"

    def detect_and_shuffle(self, turn, *args):
        """No op for this manager"""

        pass
