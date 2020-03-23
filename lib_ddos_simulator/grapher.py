#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Grapher to graph ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import os

import matplotlib.pyplot as plt
import shutil

from .manager import Manager

class Grapher:
    """graphs a DDOS attack"""

    __slots__ = ["_path", "_data", "good_users", "attackers"]
  
    def __init__(self, path, managers, num_good_users, num_attackers):
        """Initializes simulation"""

        self._path = path
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

        self.good_users = num_good_users
        self.attackers = num_attackers

        self._data = {manager: {"X": [],
                                "Y": {"num_buckets": [],
                                      "percent_serviced": [],
                                      "percent_detected": []}}
                                for manager in managers}

    def capture_data(self, round_num: int, manager: Manager, attackers: list):
        """Captures data for the round"""

        self._data[manager]["X"].append(round_num)
        # num buckets
        self._data[manager]["Y"]["num_buckets"].append(len(manager.buckets))
        # num serviced
        serviced = (sum(len(x) for x in manager.buckets if not x.attacked))        
        self._data[manager]["Y"]["percent_serviced"].append(
            serviced * 100 / len(manager.users))
        # num detected
        self._data[manager]["Y"]["percent_detected"].append(
            manager.attackers_detected * 100 / len(attackers))

    def graph(self):
        """Graphs data"""

        fig, axs = self._get_formatted_fig_axs()

        for manager_index, manager in enumerate(self._data):
            for i, (key, val) in enumerate(self._data[manager]["Y"].items()):
                axs[i].errorbar(self._data[manager]["X"],  # X val
                                val,  # Y value
                                label=manager.__class__.__name__,
                                ls=self.styles(manager_index),
                                 marker=self.markers(manager_index))

        # https://stackoverflow.com/a/4701285/8903959
#        for ax in axs:
#            box = ax.get_position()
#            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#
#        handles, labels = ax.get_legend_handles_labels()
#
#        # Put a legend to the right of the current axis
#        axs[1].legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()

    def styles(self, index):
        """returns styles and markers for graph lines"""

        styles = ["-", "--", "-.", ":", "solid", "dotted", "dashdot", "dashed"]
        return styles[index]

    def markers(self, index):

        markers = [".", "1", "*", "x", "d", "2", "3", "4"]
        return markers[index]

    def _get_formatted_fig_axs(self):
        """Creates and formats axes"""

        fig, axs = plt.subplots(3, sharex=True)
        fig.suptitle(f"{self.good_users} users, {self.attackers} attackers")
        for manager, manager_data in self._data.items():
            for key_i, (key, val) in enumerate(manager_data["Y"].items()):
                max_y_limit = 0
                for m in self._data.values():
                    if max(m["Y"][key]) > max_y_limit:
                        max_y_limit = max(m["Y"][key])
                axs[key_i].set_ylim(-1, max_y_limit + max_y_limit // 10)
                axs[key_i].set(xlabel="Round num", ylabel=key)

        return fig, axs
