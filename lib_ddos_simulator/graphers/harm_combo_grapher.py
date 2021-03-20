#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the Combination_Grapher to graph ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from copy import deepcopy
import os

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
from statistics import mean, variance
from math import sqrt
from multiprocessing import cpu_count
from pathos.multiprocessing import ProcessingPool
import json

from .utility_combo_grapher import Utility_Combination_Grapher, Worst_Case_Attacker
from ..base_grapher import Base_Grapher

from ..attackers import Attacker
# Done this way to avoid circular imports
from ..ddos_simulators import ddos_simulator
from ..managers import Manager
from ..utils import Log_Levels

class Harm_Combination_Grapher(Utility_Combination_Grapher):
    """Compares managers against each other

    Plots total utility over all rounds on the Y axis
    Plots % of users that are attackers on the X axis
    """

    graph_attr = "harm"

    def worst_case_data(self, managers, scenario_data, attackers):
        """Creates a json of worst case attacker data"""

        # Create json of worst case attackers
        worst_case_scenario_data = {manager: {Worst_Case_Attacker: {"X": [],
                                                                    "Y": [],
                                                                    "YERR": [],
                                                                    "ATKS": []}
                                              }
                                    for manager in managers}
        for manager, manager_data in scenario_data.items():
            xs = manager_data[attackers[0]]["X"]
            for i, x in enumerate(xs):
                # should be changed to be abs max but whatevs
                max_harm = -100000000000000000000000
                worst_case_atk = None
                yerr = None
                for attacker in attackers:
                    if manager_data[attacker]["Y"][i] > max_harm:
                        max_harm = manager_data[attacker]["Y"][i]
                        worst_case_atk = attacker
                        yerr = manager_data[attacker]["YERR"][i]
                atk = Worst_Case_Attacker
                cur_data_point = worst_case_scenario_data[manager][atk]
                cur_data_point["X"].append(x)
                cur_data_point["Y"].append(max_harm)
                cur_data_point["YERR"].append(yerr)
                cur_data_point["ATKS"].append(worst_case_atk.__name__)

        return worst_case_scenario_data
