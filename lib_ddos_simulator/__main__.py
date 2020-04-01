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
    parser.add_argument("--num_users", dest="num_users", default=1000)
    parser.add_argument("--num_attackers", dest="num_attackers", default=10)
    parser.add_argument("--num_buckets", dest="num_buckets", default=100)
    parser.add_argument("--threshold", dest="threshold", default=10)
    parser.add_argument("--rounds", dest="rounds", default=20)

    for i, arg in enumerate(argv):
        if "--debug" == arg.lower():
            config_logging(DEBUG)
            argv.pop(i)
            break


    args = parser.parse_args()

#    DDOS_Simulator(int(args.num_users),
#                   int(args.num_attackers),
#                   int(args.num_buckets),
#                   int(args.threshold),
#                   [Sieve_Manager, Protag_Manager]).run(int(args.rounds))

    # Now run fun graphing thing
    DDOS_Simulator(24,  # number of users
                   4,  # number of attackers
                   8,  # number of buckets
                   10,  # Threshold
                   Sieve_Manager.runnable_managers).run(10, animate=True)
