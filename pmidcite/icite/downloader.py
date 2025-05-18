"""Get a Dowloader/Loader or Downloader-Only"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader
from pmidcite.icite.dnldr.pmid_dnlder_only import NIHiCiteDownloaderOnly


def get_downloader(
        nih_grouper=None,
        force_download=True,
        details_cites_refs=None,
        dir_icite_py=None):
    """Get a Dowloader/Loader or Downloader-Only"""
    if not dir_icite_py or dir_icite_py == 'None':
        return NIHiCiteDownloaderOnly(details_cites_refs, nih_grouper)
    return NIHiCiteDownloader(
        dir_icite_py,
        force_download,
        details_cites_refs,
        nih_grouper)


# Copyright (C) 2021-present DV Klopfenstein, PhD. All rights reserved.
