#!/usr/bin/env python3
"""Test that given, one PMID, all ref/cite PMIDs are downloaded"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import stdout
from datetime import timedelta
from timeit import default_timer


def prt_hms(tic, msg, prt=stdout):
    """Print elapsed time including Hours, Minutes, and seconds with a user message."""
    prt.write("HMS {HMS}: {MSG}\n".format(HMS=str_hms(tic), MSG=msg))
    return default_timer()

def str_hms(tic):
    """Get string of elapsed time including Hours, Minutes, and seconds with a user message."""
    return str(timedelta(seconds=(default_timer()-tic)))


# Copyright (C) 2021-present, DV Klopfenstein. All rights reserved.
