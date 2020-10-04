#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Grapher to graph ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import os

import matplotlib.pyplot as plt

from .base_grapher import Base_Grapher

from ..managers import Manager


class Grapher(Base_Grapher):
    """graphs a DDOS attack"""

    __slots__ = ["_data", "good_users", "attackers"]

    def __init__(self, managers, good_users, attackers, **kwargs):
        """Initializes simulation"""

        super(Grapher, self).__init__(**kwargs)

        self.good_users: int = good_users
        self.attackers: int = attackers

        # Dictionary for recording stats
        self._data = {manager: {"X": [],
                                "Y": {"num_buckets": [],
                                      "total_serviced": [],
                                      "percent_serviced": [],
                                      "percent_detected": [],
                                      "utility": []}}
                      for manager in managers}

    def capture_data(self, round_num: int, manager: Manager, attackers: list):
        """Captures data for the round

        round_num, num_buckets, total_serviced, percent_serviced
        percent_detected, utility
        """

        self._data[manager]["X"].append(round_num)

        cur_data = self._data[manager]["Y"]

        # num buckets
        cur_data["num_buckets"].append(len(manager.used_buckets))

        # num serviced
        serviced = (sum(len(x) for x in manager.non_attacked_buckets))

        # total serviced
        cur_data["total_serviced"].append(serviced)

        # Percentage serviced
        percent_serviced = serviced * 100 / len(manager.users)
        cur_data["percent_serviced"].append(percent_serviced)

        # Percent detected
        if len(attackers) == 0:
            percent_detected = 100
        else:
            percent_detected = manager.attackers_detected * 100 / len(attackers)
        cur_data["percent_detected"].append(percent_detected)

        # Utility: total number ever serviced / total number of buckets used
        total_ever_serviced = sum(cur_data["total_serviced"])
        total_ever_buckets = sum(cur_data["num_buckets"])
        utility = total_ever_serviced / total_ever_buckets
        cur_data["utility"].append(utility)

    def graph(self, graph_trials, attacker_cls):
        """Graphs data"""

        # If not graph_trials, then this data is being used in combo grapher
        if not graph_trials:
            # Return dict of manager_cls: total_utility
            return self.get_utility_dict()

        # Format graph
        fig, axs = self._get_formatted_fig_axs()

        # Charts the data
        self.chart_data(axs)

        # Moves graphs over and adds legend to the middle
        self.add_legend(axs)

        # Saves graph with specified kwargs (see Base_Grapher)
        self.save_graph(os.path.join(self.graph_dir, "trials.png"), plt)

        # Return dict of manager_cls: total_utility to be used in combo grapher
        return self.get_utility_dict()

    def _get_formatted_fig_axs(self):
        """Creates and formats axes"""

        # Number of subplots is equal to amnt of stats tracked
        for key, val in self._data.items():
            num_subplots = len(val["Y"])
        # Creates subplots
        fig, axs = plt.subplots(num_subplots, sharex=True)
        # Title
        fig.suptitle(f"{self.good_users} users, {self.attackers} attackers")

        # For each manager
        for manager, manager_data in self._data.items():
            # For each stat tracked
            for key_i, (key, val) in enumerate(manager_data["Y"].items()):
                # Find the maximum y value
                max_y_limit = 0
                for m in self._data.values():
                    if max(m["Y"][key]) > max_y_limit:
                        max_y_limit = max(m["Y"][key])
                # Set max y value
                axs[key_i].set_ylim(-1, max_y_limit + max_y_limit // 10)
                # Label axis
                axs[key_i].set(xlabel="Round num", ylabel=key)

        return fig, axs

    def get_utility_dict(self):
        """Returns a dictionary of managers to final utility score"""

        return {manager.__class__: self._data[manager]["Y"]["utility"][-1]
                for manager in self._data}

    def chart_data(self, axs):
        """Charts data from the managers"""

        # For each manager
        for manager_index, manager in enumerate(self._data):
            # For each statistic tracked
            for i, (key, val) in enumerate(self._data[manager]["Y"].items()):
                # Chart stat with different style for each manager
                axs[i].errorbar(self._data[manager]["X"],  # X val
                                val,  # Y value
                                label=manager.__class__.__name__,
                                ls=self.styles(manager_index),
                                marker=self.markers(manager_index))

    def add_legend(self, axs):
        """Moves graph over and adds legend"""

        # Move graph over to the left
        # https://stackoverflow.com/a/4701285/8903959
        for ax in axs:
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        handles, labels = ax.get_legend_handles_labels()

        # Put a legend to the right of the middle graph
        axs[len(axs) // 2].legend(handles,
                                  labels,
                                  loc='center left',
                                  bbox_to_anchor=(1, 0.5))
