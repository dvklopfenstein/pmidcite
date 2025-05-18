"""Get a Dowloader/Loader or Downloader-Only"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

from sys import stdout
from pmidcite.icite.entry import NIHiCiteEntry
from pmidcite.icite.paper import NIHiCitePaper


def prt_keys(prt=stdout):
    """Print paper keys"""
    prt.write('\nKEYS TO PAPER LINE:\n')
    prt.write(f'    TYP {NIHiCiteEntry.line_fmt()}\n')
    prt.write('\n')
    prt.write('TYPe of relationship to the user-requested paper (TYP):\n')
    NIHiCitePaper.prt_keys(prt)
    prt.write('\nNIH iCite details:\n\n')
    NIHiCiteEntry.prt_key_desc(prt)
    prt.write('\n')

def prt_hdr(prt=stdout):
    """Print column headers in one line"""
    prt.write(f'COL {NIHiCiteEntry.col_idx}\n')
    prt.write(f'TYP {NIHiCiteEntry.hdr}\n')


# Copyright (C) 2021-present DV Klopfenstein, PhD. All rights reserved.
