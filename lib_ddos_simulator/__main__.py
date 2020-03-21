#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file runs the simulations with cmd line arguments"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, a97gorbenko@gmail.com"
__status__ = "Development"

from argparse import ArgumentParser
from .ddos_simulator import DDOS_Simulator
from .sieve_manager import Sieve_Manager
from .protag_manager import Protag_Manager

def main():
    """Runs simulations with command line arguments"""

    parser = ArgumentParser(description="Runs a DDOS simulation")
    parser.add_argument("--num_users", dest="num_users", default=1000)
    parser.add_argument("--num_attackers", dest="num_attackers", default=100)
    parser.add_argument("--num_buckets", dest="num_buckets", default=100)
    parser.add_argument("--threshold", dest="threshold", default=10)
    parser.add_argument("--rounds", dest="rounds", default=1000)


    args = parser.parse_args()
    for Manager_Class in [Sieve_Manager, Protag_Manager]:
        DDOS_Simulator(int(args.num_users),
                       int(args.num_attackers),
                       int(args.num_buckets),
                       int(args.threshold),
                       Manager_Class).run(int(args.rounds))
