#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This tests grapher functionality"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from itertools import product

import pytest

from ...ddos_simulator import DDOS_Simulator
from ...managers.manager import Manager


@pytest.mark.grapher
@pytest.mark.parametrize("tikz,high_res", list(product([True, False],
                                                       repeat=2)))
class Test_Grapher:
    @pytest.mark.filterwarnings("ignore:Gtk")  # problems with tikz
    @pytest.mark.filterwarnings("ignore:MatplotlibDeprecationWarning")
    def test_grapher(self, tikz, high_res):
        num_users = 12
        num_attackers = 4
        num_buckets = 4
        threshold = 10
        managers = Manager.runnable_managers
        rounds = 5
        DDOS_Simulator(num_users,
                       num_attackers,
                       num_buckets,
                       threshold,
                       managers,
                       save=True,
                       tikz=tikz,
                       high_res=high_res).run(rounds)
