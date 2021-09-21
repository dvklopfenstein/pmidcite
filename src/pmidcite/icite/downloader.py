"""Get a Dowloader/Loader or Downloader-Only"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import stdout
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader
from pmidcite.icite.dnldr.pmid_dnlder_only import NIHiCiteDownloaderOnly


def get_downloader(
        details_cites_refs=None,
        nih_grouper=None,
        dir_icite_py=None,
        force_download=True):
    """Get a Dowloader/Loader or Downloader-Only"""
    if not dir_icite_py or dir_icite_py == 'None':
        return NIHiCiteDownloaderOnly(details_cites_refs, nih_grouper)
    return NIHiCiteDownloader(
        dir_icite_py,
        force_download,
        details_cites_refs,
        nih_grouper)

def prt_hdr(prt=stdout):
    """Print column headers in one line"""
    from pmidcite.icite.entry import NIHiCiteEntry
    prt.write('COL {HDR}\n'.format(HDR=NIHiCiteEntry.col_idx))
    prt.write('TYP {HDR}\n'.format(HDR=NIHiCiteEntry.hdr))

def prt_keys(prt=stdout):
    """Print paper keys"""
    from pmidcite.icite.entry import NIHiCiteEntry
    from pmidcite.icite.paper import NIHiCitePaper
    prt.write('\nKEYS TO PAPER LINE:\n')
    prt.write('    TYP {ICITE_FMT}\n'.format(ICITE_FMT=NIHiCiteEntry.line_fmt()))
    prt.write('\n')
    prt.write('TYPe of relationship to the user-requested paper (TYP):\n')
    NIHiCitePaper.prt_keys(prt)
    prt.write('\nNIH iCite details:\n\n')
    NIHiCiteEntry.prt_key_desc(prt)
    prt.write('\n')


# Copyright (C) 2021-present DV Klopfenstein. All rights reserved.
