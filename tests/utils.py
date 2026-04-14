"""Utilities"""

import os.path as op

from timeit import default_timer

from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader

from tests.icite import DIR_ICITE
from tests.icite import dir_icite_clobber
from tests.prt_hms import prt_hms

REPO = op.normpath(op.join(op.dirname(__file__), ".."))


def get_filename(fname):
    """Get absolute filename given a relative filename"""
    return op.join(REPO, fname)

def init_dnldr(force_dnld):
    """Initialize a NIH Downloader and tmp dir, src/tests/icite"""
    tic = default_timer()
    dir_icite_clobber(prt=None)
    dnldr = NIHiCiteDownloader(DIR_ICITE, force_dnld)
    tic = prt_hms(tic, "Initialize NIH citation downloader")
    return dnldr

def cat(fname):
    """Write the contents of a file to the screen if it exists"""
    if op.exists(fname):
        with open(fname, encoding='utf8') as ifstrm:
            for lnum, line in enumerate(ifstrm, 1):
                print(fname, lnum, line, end='')
    else:
        print('NO', fname)
