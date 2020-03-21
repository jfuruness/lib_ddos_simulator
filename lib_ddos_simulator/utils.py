#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains useful functions"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, a97gorbenko@gmail.com"
__status__ = "Development"


def split_list(list_to_split: list, size_of_chunk: int):
    """Splits a list into num_chunks"""

    chunks = []
    # https://stackoverflow.com/a/312464
    # NOTE: rounds down, could be a prob
    for i in range(0, len(list_to_split), size_of_chunk):
        # User chunk is the chunk Anna described
        chunks.append(list_to_split[i: i + size_of_chunk])
    return chunks
