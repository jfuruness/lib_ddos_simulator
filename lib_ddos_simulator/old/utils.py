#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains useful functions"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"


from enum import Enum
import sys


def split_list(list_to_split: list, num_chunks: int):
    """Splits a list into num_chunks"""

    chunks = []
    err_msg = "You have more users than you have buckets"
    assert len(list_to_split) >= num_chunks, err_msg

    size_of_chunk = len(list_to_split) // num_chunks
    size_of_uneven_chunk = size_of_chunk + 1

    # An uneven chunk means due to remainder it needs one more
    uneven_chunks = len(list_to_split) - size_of_chunk * num_chunks

    # NOTE Now size of chunk is plus one because this includes remainder chunks

    # https://stackoverflow.com/a/312464
    # NOTE: rounds down, could be a prob
    for i in range(0,
                   size_of_uneven_chunk * uneven_chunks,
                   size_of_uneven_chunk):
        # User chunk is plus one since you this is from remainder
        chunks.append(list_to_split[i: i + size_of_uneven_chunk])

    # Now this is for non remainder chunks, ones that split evenly
    for i in range(size_of_uneven_chunk * uneven_chunks,
                   len(list_to_split),
                   size_of_chunk):
        # User chunk is plus one since you this is from remainder
        chunks.append(list_to_split[i: i + size_of_chunk])

    return chunks

class Log_Levels(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    def __eq__(self, other):
        if isinstance(other, Log_Levels):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            return False
