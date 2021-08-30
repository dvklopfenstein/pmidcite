#!/usr/bin/env python3
"""Test speed for download NIH citation data"""

from os import system
from sys import getsizeof
from timeit import default_timer

from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader
from pmidcite.icite.pmid_dnlder_only import NIHiCiteDownloaderOnly

from tests.icite import DIR_ICITE
from tests.icite import dir_icite_wc_l
from tests.prt_hms import prt_hms
from tests.pmids_i3 import PMIDS


def test_dnld_speed():
    """Test speed for download NIH citation data"""
    num = 5000
    pmids = PMIDS[:num]
    #pmids = PMIDS

    # DOWNLOAD citations but do not save temporary working files
    dnldr_only = NIHiCiteDownloaderOnly()
    _run_download(dnldr_only, pmids)

    # Create directory for temporary working files for citations
    system('rm -rf {ICITE}; mkdir {ICITE}'.format(ICITE=DIR_ICITE))

    # DOWNLOAD citations and save into temporary working files
    dnldr_loader_f1 = NIHiCiteDownloader(DIR_ICITE, force_download=True)
    print('\nICITE temporary working dir: {ICITE}'.format(ICITE=DIR_ICITE))
    _run_download(dnldr_loader_f1, pmids)

    # LOAD citations from temporary working files
    dnldr_loader_f0 = NIHiCiteDownloader(DIR_ICITE, force_download=False)
    _run_download(dnldr_loader_f0, pmids)


def _run_download(dnldr, pmids):
    """Download citations"""

    print('tests.pmids_i3 len(PMIDS)={}'.format(len(PMIDS)))

    ## nihentries = dnldr.api.dnld_icites(pmids)
    ## nihentries = dnldr.get_pmid2paper(pmids)
    ## nihentries = dnldr.get_icites(pmids)
    tic = default_timer()
    nihdicts = dnldr.get_icites(pmids)
    num_bytes = getsizeof(nihdicts)
    # pylint: disable=line-too-long
    print('{N:,} nihdicts: {BYTES:,} bytes, {MB:,} MB'.format(N=len(nihdicts), BYTES=num_bytes, MB=num_bytes/1000000.0))
    tic = prt_hms(tic, "Downloaded {N:,} items w/dnld_icites".format(N=len(nihdicts)))
    dir_icite_wc_l()
    print('')


if __name__ == '__main__':
    test_dnld_speed()

# Copyright (C) 2021-present, DV Klopfenstein. All rights reserved.
