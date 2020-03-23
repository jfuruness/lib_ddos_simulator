#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains useful functions"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"


import logging

def split_list(list_to_split: list, num_chunks: int):
    """Splits a list into num_chunks"""

    chunks = []

    size_of_chunk = len(list_to_split) // num_chunks
    
    # This number is the index of the list from which
    # Items can no longer be divided evenly
    split_number = size_of_chunk * num_chunks
    perfectly_dividable_list = list_to_split[:split_number]

    remainder_list = list_to_split[split_number:]
    

    # https://stackoverflow.com/a/312464
    # NOTE: rounds down, could be a prob
    for i in range(0, len(perfectly_dividable_list), size_of_chunk):
        # User chunk is the chunk Anna described
        chunks.append(list_to_split[i: i + size_of_chunk])

    assert len(remainder_list) < len(chunks), "see comment below. Math wrong"
    # We can do a for loop here because by the mathematical definition
    # The remainder list will not be longer than num chunky monkeys
    for i, val in enumerate(remainder_list):
        # Add the remainder to the chunks
        chunks[i].append(val)
    return chunks

def config_logging(level):
    """Configures logging"""

    if len(logging.root.handlers) <= 0:
        logging.root.handlers = []
        logging.basicConfig(level=level,
                            format='%(asctime)s-%(levelname)s: %(message)s',
                            handlers=[logging.StreamHandler()])

        logging.captureWarnings(True)
