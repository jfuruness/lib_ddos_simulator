#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the Combination_Grapher to graph ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from copy import deepcopy
import os

from statistics import mean, variance
from math import sqrt
from multiprocessing import cpu_count
from pathos.multiprocessing import ProcessingPool
import random
import json

from ..base_grapher import Base_Grapher

from ..attackers import Attacker
# Done this way to avoid circular imports
from ..ddos_simulators import ddos_simulator
from ..managers import Manager
from ..utils import Log_Levels


class Combo_Data_Generator(Base_Grapher):
    """Compares managers against each other

    Plots total utility over all rounds on the Y axis
    Plots % of users that are attackers on the X axis
    """

    def run(self,
            percent_attackers_list=[x / 100 for x in range(1, 92, 5)],
            managers=Manager.paper_managers,
            attackers=Attacker.paper_attackers,
            # Note that for range, last number is not included
            num_buckets=1,
            # Note that this is the users per bucket, not total users
            users_per_bucket=10,
            num_rounds=2,
            trials=2):
        """Runs in parallel every possible scenario

        Looks complicated, but no real way to simplify it
        so deal with it"""

        p = ProcessingPool(nodes=cpu_count())
        full_args = [[percent_attackers_list] * trials,
                     [attackers] * trials,
                     [num_buckets] * trials,
                     [users_per_bucket] * trials,
                     [num_rounds] * trials,
                     [managers] * trials,
                     list(range(trials)),
                     [trials] * trials]

        # If we are debugging, no multiprocessing
        # https://stackoverflow.com/a/1987484/8903959
        # https://stackoverflow.com/a/58866220/8903959
        if self.debug or "PYTEST_CURRENT_TEST" in os.environ:
            results = []
            for trial_num in range(trials):
                args = [x[trial_num] for x in full_args]
                results.append(self.get_combo_data(*args))
        else:
            # Doesn't make sense to do tqdm here since they finish all at once
            results = p.map(self.get_combo_data, *full_args)
            p.close()
            p.join()
            p.clear()
        # Get rid of carriage returns
        print()
        return self._aggregate_results(results,
                                       managers,
                                       attackers,
                                       percent_attackers_list)

    def get_combo_data(self,
                       percent_attackers_list,
                       attackers,
                       num_buckets,
                       users_per_bucket,
                       num_rounds,
                       managers,
                       trial_num,
                       total_trials):
        """Gets data for graphing and graphs it"""

        # Done so that trials are different
        # JF 2022 - idk why I did this before. It makes no sense
        # and resulted in a massive bottleneck (97% of runtime under pypy)
        # random.seed(str(percent_attackers_list)
        #             + str(attackers)
        #             + str(managers)
        #             + str(trial_num))

        ddos_sim_cls = deepcopy(ddos_simulator.DDOS_Simulator)
        attackers = deepcopy(attackers)
        managers = deepcopy(managers)

        scenario_data = {manager: {attacker: {"X": [],
                                              "HARM": [],
                                              "PERCENT_GOOD_NOT_SERVICED": [],
                                              "BUCKET_BOUND": [],
                                              "TOTAL_BUCKETS": [],
                                              "AVG_BUCKETS": [],
                                              "UTILITY": []}
                                   for attacker in attackers}
                         for manager in managers}

        for i, attacker in enumerate(attackers):
            self.print_progress(i,
                                len(attackers),
                                trial_num,
                                total_trials)
            for manager in managers:
                manager_data = scenario_data[manager][attacker]
                for percent_attackers in percent_attackers_list:
                    manager_data["X"].append(percent_attackers * 100)
                    # Get the utility for one trial and append
                    (harm,
                     percent_good_not_serviced,
                     bucket_bound,
                     utility,
                     total_buckets,
                     avg_buckets) = self.run_scenario(attacker,
                                                  num_buckets,
                                                  users_per_bucket,
                                                  num_rounds,
                                                  percent_attackers,
                                                  manager)
                    manager_data["HARM"].append(harm)
                    manager_data["PERCENT_GOOD_NOT_SERVICED"].append(percent_good_not_serviced)
                    manager_data["BUCKET_BOUND"].append(bucket_bound)
                    manager_data["UTILITY"].append(utility)
                    manager_data["TOTAL_BUCKETS"].append(total_buckets)
                    manager_data["AVG_BUCKETS"].append(avg_buckets)
        return scenario_data

    def run_scenario(self,
                     attacker_cls,
                     num_buckets,
                     users_per_bucket,
                     num_rounds,
                     percent_attackers,
                     manager_cls):
        """Runs a trial for simulation"""

        users = num_buckets * users_per_bucket
        attackers = int(users * percent_attackers)
        good_users = users - attackers
        sim = ddos_simulator.DDOS_Simulator(good_users,
                                            attackers,
                                            num_buckets,
                                            [manager_cls],
                                            debug=self.debug,
                                            graph_dir=self.graph_dir,
                                            tikz=self.tikz,
                                            save=self.save,
                                            attacker_cls=attacker_cls)
        # dict of {manager: {utility: final utility, harm: final harm}}
        outcome_dict = sim.run(num_rounds, graph_trials=False)
        attrs = [
            "harm",
            "percent_good_not_serviced",
            "bucket_bound",
            "utility",
            "total_buckets",
            "average_buckets"
        ]
        return [outcome_dict[manager_cls][x] for x in attrs]

    def print_progress(self, atk_num, atk_total, trial_num, trial_total):
        #if trial_num % 500 == 0:
        print(f"{atk_num + 1}/{atk_total} attackers, "
              f"{trial_num + 1}/{trial_total} trials    \r")

    def _aggregate_results(self, results, managers, attackers, percents):
        """Aggregates results and returns them"""

        # Results are the in format:
        # {Manager: {Attacker: {X: [], HARM: [], UTILITY: []}}}
        agg_results = {}
        for manager_cls in managers:
            agg_results[manager_cls] = {}
            for attacker_cls in attackers:
                # YES, I know these should all be enums.
                agg_results[manager_cls][attacker_cls] = {"X": [],
                                                          "HARM": [],
                                                          "HARM_YERR": [],
                                                          "PERCENT_GOOD_NOT_SERVICED": [],
                                                          "PERCENT_GOOD_NOT_SERVICED_YERR": [],
                                                          "BUCKET_BOUND": [],
                                                          "BUCKET_BOUND_YERR": [],
                                                          "TOTAL_BUCKETS": [],
                                                          "TOTAL_BUCKETS_YERR": [],
                                                          "AVG_BUCKETS": [],
                                                          "AVG_BUCKETS_YERR": [],
                                                          "UTILITY": [],
                                                          "UTILITY_YERR": []}
                cur_agg_data = agg_results[manager_cls][attacker_cls]
                for i, percent in enumerate(percents):
                    cur_agg_data["X"].append(percent)
                    # Get all the raw data
                    raw_harm = []
                    raw_percent_good_not_serviced = []
                    raw_bucket_bound = []
                    raw_total_buckets = []
                    raw_avg_buckets = []
                    raw_utility = []
                    for result in results:
                        cur_result_data = result[manager_cls][attacker_cls]
                        raw_harm.append(cur_result_data["HARM"][i])
                        raw_percent_good_not_serviced.append(cur_result_data["PERCENT_GOOD_NOT_SERVICED"][i])
                        raw_bucket_bound.append(cur_result_data["BUCKET_BOUND"][i])
                        raw_total_buckets.append(cur_result_data["TOTAL_BUCKETS"][i])
                        raw_avg_buckets.append(cur_result_data["AVG_BUCKETS"][i])
                        raw_utility.append(cur_result_data["UTILITY"][i])
                    # Take the average of the raw data and append
                    cur_agg_data["HARM"].append(mean(raw_harm))
                    cur_agg_data["PERCENT_GOOD_NOT_SERVICED"].append(mean(raw_percent_good_not_serviced))
                    cur_agg_data["BUCKET_BOUND"].append(mean(raw_bucket_bound))
                    cur_agg_data["TOTAL_BUCKETS"].append(mean(raw_total_buckets))
                    cur_agg_data["AVG_BUCKETS"].append(mean(raw_avg_buckets))
                    cur_agg_data["UTILITY"].append(mean(raw_utility))
                    # error bar data and append
                    cur_agg_data["HARM_YERR"].append(self._error_bar(raw_harm))
                    cur_agg_data["PERCENT_GOOD_NOT_SERVICED_YERR"].append(self._error_bar(raw_percent_good_not_serviced))
                    cur_agg_data["BUCKET_BOUND_YERR"].append(self._error_bar(raw_bucket_bound))
                    cur_agg_data["TOTAL_BUCKETS_YERR"].append(self._error_bar(raw_total_buckets))
                    cur_agg_data["AVG_BUCKETS_YERR"].append(self._error_bar(raw_avg_buckets))
                    utility_y_err = self._error_bar(raw_utility)
                    cur_agg_data["UTILITY_YERR"].append(utility_y_err)
        return agg_results

    def _error_bar(self, values: list):
        return 1.645 * 2 * (sqrt(variance(values)) / sqrt(len(values)))
