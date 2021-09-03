#!/usr/bin/env python3
"""Test that given, one PMID, all ref/cite PMIDs are downloaded"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from timeit import default_timer
from time import sleep

from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader
from pmidcite.icite.dnldr.pmid_dnlder_only import NIHiCiteDownloaderOnly

from tests.icite import ICiteTester
from tests.prt_hms import prt_hms
from tests.prt_hms import str_hms


def test_print_paper():
    """Test that given, one PMID, all ref/cite PMIDs are downloaded"""
    pmid = 22882545

    # Clean iCite files

    obj = ICiteTester()
    obj.rm_icitefiles()

    # iCite files are downloaded with the first call
    dnldr = NIHiCiteDownloader(obj.dir_icite, force_download=False, details_cites_refs='all')
    tic = default_timer()
    pmid2paper0 = dnldr.get_pmid2paper([pmid])
    hms = str_hms(tic)
    paper0 = pmid2paper0[pmid]
    paper0.prt_summary()
    print('\nHMS {HMS}: All citation files downloaded from NIH and saved on disk'.format(HMS=hms))
    assert pmid in pmid2paper0
    f2mtime_dnld = obj.get_f2mtime(min_files=50)
    sleep(1)

    # iCite files are imported (NOT downloaded) with the second call
    dnldr = NIHiCiteDownloader(obj.dir_icite, force_download=False, details_cites_refs='all')
    tic = default_timer()
    pmid2paper1 = dnldr.get_pmid2paper([pmid])
    prt_hms(tic, 'All citation files loaded from local disk')
    assert pmid in pmid2paper1
    assert obj.get_f2mtime(min_files=50) == f2mtime_dnld, 'iCite FILES SHOULD NOT HAVE BE MODIFIED'

    # iCite files are imported (NOT downloaded) with the second call
    obj.rm_icitefiles()
    dnldr = NIHiCiteDownloaderOnly(details_cites_refs='all')
    tic = default_timer()
    pmid2paper2 = dnldr.get_pmid2paper([pmid])
    #### obj.get_paper(pmid, force_download=False)
    prt_hms(tic, 'All citation files downloaded from NIH and not saved on disk')
    assert pmid in pmid2paper2
    paper1 = pmid2paper2[pmid]
    assert len(paper0.cited_by) == len(paper1.cited_by)
    assert len(paper0.cited_by_clin) == len(paper1.cited_by_clin)
    assert len(paper0.references) == len(paper1.references)

    # Clean iCite files
    obj.rm_icitefiles()


if __name__ == '__main__':
    test_print_paper()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
