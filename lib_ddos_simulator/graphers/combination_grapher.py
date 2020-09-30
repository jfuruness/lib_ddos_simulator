#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Combination_Grapher to graph ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import os

import matplotlib.pyplot as plt
import shutil
import logging
import shutil
from statistics import mean, variance
from math import sqrt
from multiprocessing import cpu_count
from pathos.multiprocessing import ProcessingPool
from tqdm import tqdm
import json

from .attacker import Attacker
from .manager import Manager
from .sieve_manager import Sieve_Manager
from .protag_manager import Protag_Manager

from .kpo_manager import Kpo_Manager
from .miad_manager import Miad_Manager
from .bounded_manager import Bounded_Manager



from . import utils
from .ddos_simulator import DDOS_Simulator
class Worst_Case_Attacker:
    pass

class Combination_Grapher:

    __slots__ = ["stream_level", "graph_path"]

    def __init__(self, stream_level=logging.INFO, graph_path="/tmp/lib_ddos/"):
        utils.config_logging(stream_level)
        self.stream_level = stream_level
        self.graph_path = graph_path

    def run(self,
            managers=Sieve_Manager.runnable_managers[-1:] + [Protag_Manager,
                                                             Kpo_Manager,
                                                             Bounded_Manager],# + Miad_Manager.runnable_managers,
            attackers=Attacker.runnable_attackers,
            num_buckets_list=[10],
            users_per_bucket_list=[10 ** i for i in range(1,3)],
            num_rounds_list=[10 ** i for i in range(1,3)],
            trials=100):

        if os.path.exists(self.graph_path):
            shutil.rmtree(self.graph_path)
            os.makedirs(self.graph_path)

        # +1 for worst case attacker
        pbar_total = len(num_buckets_list) * len(users_per_bucket_list) * len(num_rounds_list) * len(attackers)

#        pbar = tqdm(total=total, desc=f"Running Scenarios")

        _pathos_num_buckets_list = []
        _pathos_users_per_bucket = []
        _pathos_num_rounds = []
        for num_buckets in num_buckets_list:
            for users_per_bucket in users_per_bucket_list:
                for num_rounds in num_rounds_list:
                    for attacker in attackers + [Worst_Case_Attacker]:
                        graph_dir = os.path.join(self.graph_path, attacker.__name__)
                        if not os.path.exists(graph_dir):
                            os.makedirs(graph_dir)

                    _pathos_num_buckets_list.append(num_buckets)
                    _pathos_users_per_bucket.append(users_per_bucket)
                    _pathos_num_rounds.append(num_rounds)

        p = ProcessingPool(nodes=cpu_count())
        total = len(_pathos_num_rounds)
        p.map(self.get_graph_data, [attackers] * total, _pathos_num_buckets_list, _pathos_users_per_bucket,
              _pathos_num_rounds, [managers] * total, [trials] * total,
              list(range(total)), list([pbar_total] * total))
        p.close()
        p.join()
        p.clear()


    def get_graph_data(self,
                       attackers,
                       num_buckets,
                       users_per_bucket,
                       num_rounds,
                       managers,
                       trials,
                       num,
                       total_num):
        scenario_data = {manager: {attacker: {"X": [],
                                              "Y": [],
                                              "YERR": []}
                                   for attacker in attackers}
                             for manager in managers}

        for attacker in attackers:
            # https://stackoverflow.com/a/16910957/8903959
            cpt = sum([len(files) for r, d, files in os.walk(self.graph_path)])
            print(f"Starting: {cpt + 1}/{total_num}        \r")
            percent_attackers_list = [i / 100 for i in range(1,50)]

            for manager in managers:
                manager_data = scenario_data[manager][attacker]
                for percent_attackers in percent_attackers_list:
                    manager_data["X"].append(percent_attackers)
                    Y = []
                    # TRIALS
                    for _ in range(trials):
                        # Get the utility for each trail and append it
                        Y.append(self.run_scenario(attacker,
                                                   num_buckets,
                                                   users_per_bucket,
                                                   num_rounds,
                                                   percent_attackers,
                                                   manager))
                    manager_data["Y"].append(mean(Y))
                    err_length = 1.645 * 2 * (sqrt(variance(Y))/sqrt(len(Y)))
                    manager_data["YERR"].append(err_length)

            self.graph_scenario(scenario_data,
                                num_buckets,
                                users_per_bucket,
                                num_rounds,
                                attacker)
        # Create json of worst case attackers
        worst_case_scenario_data = {manager: {Worst_Case_Attacker: {"X": [],
                                                                    "Y": [],
                                                                    "YERR": [],
                                                                    "ATKS": []}}
                                    for manager in managers}
        for manager, manager_data in scenario_data.items():
            xs = manager_data[attackers[0]]["X"]
            for i, x in enumerate(xs):
                # should be changed to be abs max but whatevs
                min_utility = 100000000000000000000000
                worst_case_atk = None
                yerr = None
                for attacker in attackers:
                    if manager_data[attacker]["Y"][i] < min_utility:
                        min_utility = manager_data[attacker]["Y"][i]
                        worst_case_atk = attacker
                        yerr = manager_data[attacker]["YERR"][i]
                atk = Worst_Case_Attacker
                worst_case_scenario_data[manager][atk]["X"].append(x)
                worst_case_scenario_data[manager][atk]["Y"].append(min_utility)
                worst_case_scenario_data[manager][atk]["YERR"].append(yerr)
                worst_case_scenario_data[manager][atk]["ATKS"].append(worst_case_atk.__name__)

        self.graph_scenario(worst_case_scenario_data,
                            num_buckets,
                            users_per_bucket,
                            num_rounds,
                            Worst_Case_Attacker,
                            write_json=True)

    def run_scenario(self,
                     attacker,
                     num_buckets,
                     users_per_bucket,
                     num_rounds,
                     percent_attackers,
                     manager):

        users = num_buckets * users_per_bucket
        attackers = int(users * percent_attackers)
        good_users = users - attackers
        # No longer used, but maybe in the future
        threshold = 0
        simulator = DDOS_Simulator(good_users,
                                   attackers,
                                   num_buckets,
                                   threshold,
                                   [manager],
                                   self.stream_level,
                                   self.graph_path, 
                                   attacker_cls=attacker)
        # dict of {manager: final utility}
        utilities_dict =  simulator.run(num_rounds, graph_trials=False)
        return utilities_dict[manager]

    def graph_scenario(self, scenario_data, num_buckets, users_per_bucket, num_rounds, attacker, write_json=False):

        fig, axs, title = self._get_formatted_fig_axs(scenario_data,
                                                      num_buckets,
                                                      users_per_bucket,
                                                      num_rounds, attacker)

        for manager_index, manager in enumerate(scenario_data):
#            for x, y, yerr in zip(scenario_data[manager]["X"],
#                                  scenario_data[manager]["Y"],
#                                  scenario_data[manager]["YERR"]):
            axs.errorbar(scenario_data[manager][attacker]["X"],  # X val
                         scenario_data[manager][attacker]["Y"],  # Y value
                         yerr=scenario_data[manager][attacker]["YERR"],
                         label=f"{manager.__name__}",
                         ls=self.styles(manager_index),
                         marker=self.markers(manager_index))

        # https://stackoverflow.com/a/4701285/8903959
        box = axs.get_position()
        axs.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        handles, labels = axs.get_legend_handles_labels()

        # Put a legend to the right of the current axis
        axs.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))
#        plt.show()
        graph_dir = os.path.join(self.graph_path, attacker.__name__)
        graph_path = os.path.join(graph_dir, f"{title}.png")
        plt.savefig(graph_path)
        plt.close()
        if write_json:
            with open(graph_path.replace("png", "json"), "w") as f:
                data = {m.__name__: {atk.__name__: end_dict for atk, end_dict in m_data.items()}
                        for m, m_data in scenario_data.items()}
                json.dump(data, f)
#        import tikzplotlib
#        tikzplotlib.save(os.path.join(self._path, "test.tex"))

    def styles(self, index):
        """returns styles and markers for graph lines"""

        styles = ["-", "--", "-.", ":", "solid", "dotted", "dashdot", "dashed"]
        styles += styles.copy()[::-1]
        styles += styles.copy()[0:-2:2]
        return styles[index]

    def markers(self, index):

        markers = [".", "1", "*", "x", "d", "2", "3", "4"]
        markers += markers.copy()[0:-2:2]
        markers += markers.copy()[::-1]
        return markers[index]

    def _get_formatted_fig_axs(self, scenario_data, num_buckets, users_per_bucket, num_rounds, attacker):
        """Creates and formats axes"""

        fig, axs = plt.subplots(figsize=(20,10))
        title = f"Scenario: buckets: {num_buckets}, users: {users_per_bucket * num_buckets}, rounds: {num_rounds}, attacker_cls: {attacker.__name__}"
        fig.suptitle(title)
        max_y_limit = 0
        for _, manager_data in scenario_data.items():
            if max(manager_data[attacker]["Y"]) > max_y_limit:
                max_y_limit = max(manager_data[attacker]["Y"])
        axs.set_ylim(-1, max_y_limit + 5)
        axs.set(xlabel="Percent Attackers", ylabel="Utility")

        return fig, axs, title