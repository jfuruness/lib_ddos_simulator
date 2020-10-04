#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This tests grapher functionality"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import pytest

from ...ddos_simulator import DDOS_Simulator
from ...managers import Sieve_Manager_V0_S0


@pytest.mark.slow
@pytest.mark.animater
class Test_Animater:
    @pytest.mark.filterwarnings("ignore:.*Deprecation.*")
    @pytest.mark.filterwarnings("ignore:Gdk")
    def test_animater(self):
        num_users = 6
        num_attackers = 3
        num_buckets = 3
        threshold = 10
        # Only doing one for speed
        managers = [Sieve_Manager_V0_S0]
        rounds = 3
        DDOS_Simulator(num_users,
                       num_attackers,
                       num_buckets,
                       threshold,
                       managers,
                       save=True,
                       high_res=False).run(rounds,
                                           animate=True,
                                           graph_trials=False)
