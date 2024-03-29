#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the Combination_Grapher to graph ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from copy import deepcopy
import os

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json

from ..base_grapher import Base_Grapher
from .combo_data_generator import Combo_Data_Generator

from ..attackers import Attacker


class Worst_Case_Attacker:
    """placeholder

    Later used to graph the worst case attacker graph"""
    pass


class Combination_Grapher(Base_Grapher):
    """Compares managers against each other

    Plots total utility over all rounds on the Y axis
    Plots % of users that are attackers on the X axis
    """

    y_vals = [
        "HARM",
        "PERCENT_GOOD_NOT_SERVICED",
        "BUCKET_BOUND",
        "UTILITY",
        "TOTAL_BUCKETS",
        "AVG_BUCKETS"
    ]

    def __init__(self, *args, **kwargs):
        super(Combination_Grapher, self).__init__(*args, **kwargs)
        self.second_legend = []

    def run(self, **kwargs):
        """Runs in parallel every possible scenario, then graphs

        Looks complicated, but no real way to simplify it
        sorry

        kwargs: See Combo_Data_Generator. They are the same there."""

        # Initializes graph path
        self.make_graph_dir(destroy=True)
        data = Combo_Data_Generator(**self.graph_kwargs).run(**kwargs)
        self._graph_normal_attackers(data, kwargs)
        self.graph_worst(data,
                         kwargs["managers"],
                         kwargs["attackers"],
                         kwargs["num_buckets"],
                         kwargs["users_per_bucket"],
                         kwargs["num_rounds"])

    def _graph_normal_attackers(self, data, kwargs):
        for attacker_cls in kwargs["attackers"]:
            for y_val in self.y_vals:
                self.graph_scenario(data,
                                    attacker_cls,
                                    y_val,
                                    kwargs["num_buckets"],
                                    kwargs["users_per_bucket"],
                                    kwargs["num_rounds"])

    def graph_worst(self,
                    data,
                    managers,
                    attackers,
                    num_buckets,
                    users_per_bucket,
                    num_rounds):
        for y_val in self.y_vals:
            worst_case_data = self.worst_case_data(managers,
                                                   deepcopy(data),
                                                   attackers,
                                                   y_val)
            self.graph_scenario(worst_case_data,
                                Worst_Case_Attacker,
                                y_val,
                                num_buckets,
                                users_per_bucket,
                                num_rounds,
                                write_json=True)

    def worst_case_data(self, managers, scenario_data, attackers, y_val):
        """Creates a json of worst case attacker data"""

        # Create json of worst case attackers
        worst_case_scenario_data = {
            manager: {
                Worst_Case_Attacker: {
                    "X": [],
                    y_val: [],
                    y_val + "_YERR": [],
                    "ATKS": []
                }
            }
            for manager in managers
        }

        for manager, manager_data in scenario_data.items():
            xs = manager_data[attackers[0]]["X"]
            for i, x in enumerate(xs):
                # should be changed to be abs max but whatevs
                if y_val in [
                    "HARM", "PERCENT_GOOD_NOT_SERVICED", "BUCKET_BOUND",
                    "TOTAL_BUCKETS", "AVG_BUCKETS"
                ]:
                    worst_case_y = -10000000000
                elif y_val == "UTILITY":
                    worst_case_y = 10000000000
                else:
                    assert False, "OG y not supported"
                worst_case_atk = None
                yerr = None
                for attacker in attackers:
                    if y_val in [
                        "HARM", "PERCENT_GOOD_NOT_SERVICED", "BUCKET_BOUND",
                        "TOTAL_BUCKETS", "AVG_BUCKETS"
                    ]:
                        cond = manager_data[attacker][y_val][i] > worst_case_y
                    elif y_val == "UTILITY":
                        cond = manager_data[attacker][y_val][i] < worst_case_y
                    else:
                        assert False, "y_val not supported"
                    # If there's a new worst case:
                    if cond:
                        worst_case_y = manager_data[attacker][y_val][i]
                        worst_case_atk = attacker
                        yerr = manager_data[attacker][y_val + "_YERR"][i]
                atk = Worst_Case_Attacker
                cur_data_point = worst_case_scenario_data[manager][atk]
                cur_data_point["X"].append(x * 100)
                cur_data_point[y_val].append(worst_case_y)
                cur_data_point[y_val + "_YERR"].append(yerr)
                cur_data_point["ATKS"].append(worst_case_atk.__name__)

        return worst_case_scenario_data

    def graph_scenario(self,
                       scenario_data,
                       attacker,
                       y_val: str,
                       num_buckets,
                       users_per_bucket,
                       num_rounds,
                       write_json=False):

        fig, axs, title = self._get_formatted_fig_axs(scenario_data,
                                                      num_buckets,
                                                      users_per_bucket,
                                                      num_rounds,
                                                      attacker,
                                                      y_val)
        for manager_i, manager in enumerate(scenario_data):
            self.populate_axs(axs,
                              scenario_data,
                              manager,
                              attacker,
                              manager_i,
                              y_val,
                              write_json=write_json)

        self.add_legend(axs)

        graph_dir = self.get_attacker_graph_dir(attacker)
        graph_path = os.path.join(graph_dir, y_val + f"_{title}.png")
        graph_path = graph_path.replace(":", "_").replace(",", "_")
        self.save_graph(graph_path, plt, fig=fig)

        if write_json:
            self.write_json(graph_path, scenario_data)

    def _get_formatted_fig_axs(self,
                               scenario_data,
                               num_buckets,
                               users_per_bucket,
                               num_rounds,
                               attacker,
                               y_val):
        """Creates and formats axes"""

        matplotlib.use("Agg")
        fig, axs = plt.subplots(figsize=(20, 10))
        plt.rcParams.update({"font.size": 18, "lines.markersize": 10})
        # Request NDSS 6/30/2023 for higher dpi
        fig.set_dpi(300)
        title = (f"Scenario: "
                 f"users: {users_per_bucket * num_buckets}, "
                 f"rounds: {num_rounds}, attacker_cls: {attacker.__name__} ")
        # fig.suptitle(title)

        # Request NDSS June 2023 change percent good not serviced to a decimal
        for _, manager_data in scenario_data.items():
            if y_val == "PERCENT_GOOD_NOT_SERVICED":
                vals = manager_data[attacker][y_val]
                # For some reason if we * 100 it multiplies by 10000?
                new_vals = [y * 10 for y in vals]
                manager_data[attacker][y_val] = new_vals

        # Gets maximum y value to set axis
        max_y_limit = 0
        for _, manager_data in scenario_data.items():
            if max(manager_data[attacker][y_val]) > max_y_limit:
                max_y_limit = max(manager_data[attacker][y_val])
        # Sets y limit
        # Request for NDSS June 2023, inclrease Y limit by 10%
        # UNLESS y_val is bucket bound or cost, which needs log scale
        # REVERTED 6/28/2023 because this was innaccurate
        # Brought back 6/30/2023 for percent good not serviced
        if y_val in ["PERCENT_GOOD_NOT_SERVICED", "AVG_BUCKETS"]:
            axs.set_yscale("log")
        else:
            axs.set_ylim(0, max_y_limit * 1.02)
        # Request for NDSS June 2023, set X limit to 0
        max_x_val = 0
        for _, manager_data in scenario_data.items():
            max_x_val = max(max_x_val, max(manager_data[attacker]["X"]))
        axs.set_xlim(0, max_x_val * 1.02)

        # Add labels to axis
        # Requested changes for NDSS June 2023
        # June 28 2023 - reverting this change. cost != bucket bound,
        # this was innaccurate
        # if y_val == "BUCKET_BOUND":
        #     y_val = "COST"
        #     # Request NDSS June 2023, Set Y scale to log
        #     axs.set_yscale("log")
        # Request NDSS June 2023 to change Y axis of this graph
        if y_val == "PERCENT_GOOD_NOT_SERVICED":
            y_val = "PERCENT HARMED"
        elif y_val == "AVG_BUCKETS":
            y_val = "COST"

        axs.set(xlabel="Percent Attackers", ylabel=y_val)

        return fig, axs, title

    def get_attacker_graph_dir(self, attacker_cls):
        graph_dir = os.path.join(self.graph_dir, attacker_cls.__name__)
        if not os.path.exists(graph_dir):
            os.makedirs(graph_dir)
        return graph_dir

    def populate_axs(self,
                     axs,
                     scenario_data,
                     manager,
                     attacker,
                     manager_i,
                     y_val: str,
                     write_json=False):
        """Plots error bar"""

        # Gets class attr name if it exists, if not, uses __name__
        name = getattr(manager, "name", manager.__name__)
        axs.errorbar(scenario_data[manager][attacker]["X"],  # X val
                     scenario_data[manager][attacker][y_val],  # Y value
                     yerr=scenario_data[manager][attacker][y_val + "_YERR"],
                     label=name,
                     ls=self.styles(index=manager_i, manager=manager),
                     # https://stackoverflow.com/a/26305286/8903959
                     marker=self.markers(index=manager_i, manager=manager),
                     color=self.colors(index=manager_i, manager=manager),
                     )
        # This means we are graphing worst case
        if write_json:
            self.overlay_scatter_plot(axs,
                                      scenario_data,
                                      manager,
                                      attacker,
                                      manager_i,
                                      y_val,
                                      write_json)

    def overlay_scatter_plot(self,
                             axs,
                             scenario_data,
                             manager,
                             attacker,
                             manager_i,
                             y_val: str,
                             write_json):
        """Overlays error bars with worst case attacker colors"""

        # Get list of colors
        # color_dict = self.get_worst_case_atk_color_dict()
        # colors = [color_dict[atk_name] for atk_name in
        #           scenario_data[manager][attacker]["ATKS"]]
        # No longer wanted
        # axs.scatter(scenario_data[manager][attacker]["X"],
        #            scenario_data[manager][attacker][y_val],
        #            c=colors,
        #            s=45,
        #            zorder=3,
        #            marker=self.markers(manager_i))

        # Sort worst case attacker by freq
        atk_freq_dict = {}
        for atk in scenario_data[manager][attacker]["ATKS"]:
            atk_freq_dict[atk] = atk_freq_dict.get(atk, 0) + 1
        atks = list(reversed(sorted(atk_freq_dict, key=atk_freq_dict.get)))

        self.second_legend.extend(atks)

    def get_worst_case_atk_color_dict(self):
        """Returns a dictionary of attacker to colors"""

        # https://matplotlib.org/3.1.1/gallery/color/named_colors.html
        colors = ["black", "dimgray", "lightcoral", "firebrick", "sienna",
                  "bisque", "gold", "olive", "lawngreen", "turquoise", "teal",
                  "deepskyblue", "midnightblue", "mediumpurple", "darkviolet",
                  "deeppink", "lightpink", "chocolate", "darkkhaki",
                  "powderblue"]

        new_colors_needed = len(Attacker.runnable_attackers) - len(colors)
        assert new_colors_needed <= 0, f"Add {new_colors_needed} more colors"
        return {attacker.__name__: colors[i]
                for i, attacker in enumerate(Attacker.runnable_attackers)}

    def add_legend(self, axs):
        """Adds legend. Potentially combine with grapher class"""

        # https://stackoverflow.com/a/4701285/8903959
        box = axs.get_position()
        axs.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        handles, labels = axs.get_legend_handles_labels()

        # Put a legend to the right of the current axis
        first = axs.legend(handles,
                           labels,
                           loc='center left',
                           bbox_to_anchor=(1, 0.5))

        # If we are adding a second legend for worst case attacker colors
        # Legacy code now. Amir changed his mind.
        if len(self.second_legend) > 0 and False:
            color_dict = self.get_worst_case_atk_color_dict()
            legend_elements = [mpatches.Patch(color=color_dict[atk], label=atk)
                               for atk in set(self.second_legend)]

            # https://riptutorial.com/matplotlib/example/32429/multiple-legends-on-the-same-axes
            # https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/custom_legends.html
            axs.legend(handles=legend_elements,
                       loc='upper right',
                       bbox_to_anchor=(1, 1))
            axs.add_artist(first)
            self.second_legend = []

    def write_json(self, graph_path, scenario_data):
        """Writes json file"""

        with open(graph_path.replace("png", "json"), "w") as f:
            data = {m.__name__: {atk.__name__: end_dict
                                 for atk, end_dict in m_data.items()}
                    for m, m_data in scenario_data.items()}
            json.dump(data, f)
