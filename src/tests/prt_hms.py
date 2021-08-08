#!/usr/bin/env python3
"""Test that given, one PMID, all ref/cite PMIDs are downloaded"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import stdout
from datetime import timedelta
from timeit import default_timer


def prt_hms(tic, msg, prt=stdout):
    """Print elapsed time including Hours, Minutes, and seconds with a user message."""
    hms = str(timedelta(seconds=(default_timer()-tic)))
    prt.write("{HMS}: {MSG}\n".format(HMS=hms, MSG=msg))
    return default_timer()


# Copyright (C) 2021-present, DV Klopfenstein. All rights reserved.
