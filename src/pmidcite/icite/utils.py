"""Small utilities used in the pmidcite project"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"


def split_list(iterable, len_sublists):
    """Split a long list into smaller lists"""
    # WAS: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # NOW: [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10,)]
    #
    # WAS: [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # NOW: [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    lst = list(iterable)
    mod = len(iterable)%len_sublists
    ret = list(zip(*[iter(lst)]*len_sublists))
    if mod != 0:
        ret.append(tuple(lst[-1*mod:]))
    return ret


# Copyright (C) 2021-present DV Klopfenstein. All rights reserved.
