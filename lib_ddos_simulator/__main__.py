#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file runs the simulations with cmd line arguments"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from argparse import ArgumentParser
from sys import argv

from .ddos_simulator import DDOS_Simulator
from .sieve_manager import Sieve_Manager
from .protag_manager import Protag_Manager
from .utils import config_logging

def main():
    """Runs simulations with command line arguments"""

    parser = ArgumentParser(description="Runs a DDOS simulation")
    parser.add_argument("--num_users", type=int, dest="num_users", default=1000)
    parser.add_argument("--num_attackers", type=int, dest="num_attackers", default=10)
    parser.add_argument("--num_buckets", type=int, dest="num_buckets", default=100)
    parser.add_argument("--threshold", type=int, dest="threshold", default=10)
    parser.add_argument("--rounds", type=int, dest="rounds", default=20)
    parser.add_argument("--debug", dest="debug", default=False, action='store_true')
    parser.add_argument("--animate", dest="animate", default=False, action='store_true')

    args = parser.parse_args()
    if args.debug:
        config_logging(DEBUG)

    if args.animate:
        DDOS_Simulator(24,  # number of users
                       4,  # number of attackers
                       8,  # number of buckets
                       10,  # Threshold
                       Sieve_Manager.runnable_managers).run(10, animate=True)
    else:
        DDOS_Simulator(int(args.num_users),
                       int(args.num_attackers),
                       int(args.num_buckets),
                       int(args.threshold),
                       Sieve_Manager.runnable_managers + [Protag_Manager]).run(int(args.rounds))
