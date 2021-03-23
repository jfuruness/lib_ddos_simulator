#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file runs the simulations with cmd line arguments"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from argparse import ArgumentParser
import os
from sys import argv

from .attackers import Basic_Attacker, Even_Turn_Attacker, Attacker
from .ddos_simulators import DDOS_Simulator
from .managers import Manager, Protag_Manager_Smart_Merge, Sieve_Manager_V0_S0, Sieve_Manager_V1_S0
from .utils import Log_Levels
from .graphers import Combination_Grapher

def main():
    """Runs simulations with command line arguments"""

    parser = ArgumentParser(description="Runs a DDOS simulation")
    parser.add_argument("--num_users", type=int, dest="num_users", default=21)
    parser.add_argument("--num_attackers", type=int, dest="num_attackers", default=9)
    parser.add_argument("--num_buckets", type=int, dest="num_buckets", default=3)
    parser.add_argument("--threshold", type=int, dest="threshold", default=10)
    parser.add_argument("--rounds", type=int, dest="rounds", default=7)
    parser.add_argument("--debug", dest="debug", default=False, action='store_true')
    parser.add_argument("--animate", dest="animate", default=False, action='store_true')
    parser.add_argument("--graph_combos", dest="graph_combos", default=False, action='store_true')
    parser.add_argument("--combination_grapher", dest="graph_combos", default=False, action='store_true')
    parser.add_argument("--tikz", dest="tikz", default=False, action="store_true")
    parser.add_argument("--save", dest="save", default=False, action="store_true")
    parser.add_argument("--high_res", dest="high_res", default=False, action="store_true")
    parser.add_argument("--trials", type=int, dest="trials", default=2)
    parser.add_argument("--graph_dir", type=str, dest="graph_dir", default=os.path.join("/tmp", "lib_ddos_simulator"))
    parser.add_argument("--api", dest="api", default=False, action="store_true")


    args = parser.parse_args()

    if args.animate:
        for atk_cls in [Basic_Attacker, Even_Turn_Attacker]:
            # NOTE: for optimal animations,
            # use 24, 4, 8, 10 for users, attackers, buckets, threshold
            DDOS_Simulator(args.num_users,  # number of users
                           args.num_attackers,  # number of attackers
                           args.num_buckets,  # number of buckets
                           Manager.runnable_managers,
                           graph_dir=args.graph_dir,
                           save=args.save,
                           debug=args.debug,
                           high_res=args.high_res,
                           attacker_cls=atk_cls).run(args.rounds,
                                                     animate=True,
                                                     graph_trials=False)
    elif args.graph_combos:
        #import cProfile, pstats, io

        def profile(fnc):
            
            """A decorator that uses cProfile to profile a function"""
            
            def inner(*args, **kwargs):
                
                pr = cProfile.Profile()
                pr.enable()
                retval = fnc(*args, **kwargs)
                pr.disable()
                s = io.StringIO()
                sortby = 'cumulative'
                ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
                ps.print_stats()
                print(s.getvalue())
                return retval

            return inner
        #@profile
        def graph(args):
            Combination_Grapher(debug=args.debug,
                            graph_dir=args.graph_dir,
                            tikz=args.tikz,
                            save=args.save,
                            high_res=args.high_res).run(
                                    percent_attackers_list=[x / 100 for x in
                                                            range(1, 52, 5)],
                                    managers=Manager.paper_managers,
                                    attackers=Attacker.paper_attackers,
                                    num_buckets=1,
                                    # Note that this is the users per bucket
                                    # Not total users
                                    users_per_bucket=1000,
                                    num_rounds=100,
                                    trials=2)
        graph(args)
        #from line_profiler import LineProfiler
        #print(LineProfiler(graph(args)).print_stats())

    else:
        DDOS_Simulator(args.num_users,
                       args.num_attackers,
                       args.num_buckets,
                       Manager.runnable_managers,
                       debug=args.debug,
                       graph_dir=args.graph_dir,
                       save=args.save,
                       tikz=args.tikz,
                       high_res=args.high_res).run(args.rounds)
