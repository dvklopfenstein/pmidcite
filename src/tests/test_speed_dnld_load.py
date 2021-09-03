#!/usr/bin/env python3
"""Test speed for download NIH citation data"""

from os import system

from sys import getsizeof
from sys import stdout
from timeit import default_timer

from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader
from pmidcite.icite.dnldr.pmid_dnlder_only import NIHiCiteDownloaderOnly

from tests.icite import DIR_ICITE
from tests.icite import dir_icite_wc_l
from tests.prt_hms import prt_hms
from tests.pmids_i3 import PMIDS


def test_dnld_speed():
    """Test speed for download NIH citation data"""
    fout_log = 'test_speed_dnld_load.log'
    num = 5000
    force_wr = True
    ## pmids = PMIDS[:num]
    pmids = PMIDS
    system('rm -rf {ICITE}; mkdir {ICITE}'.format(ICITE=DIR_ICITE))

    with open(fout_log, 'w') as log:
        # SPEED TEST 1: DOWNLOAD citations but do not save temporary working files
        dnldr_only = NIHiCiteDownloaderOnly()

        tic = default_timer()
        pmid2paper = _run_download(dnldr_only, pmids)
        msg = "{N:,} citations: Downloaded, but not saved".format(N=len(pmid2paper))
        prt_hms(tic, msg, log)
        prt_hms(tic, msg, stdout)

        dnldr_only.wr_papers('dnldr_only_{N}.txt'.format(N=num), pmid2paper, force_wr)

        # Create directory for temporary working files for citations
        system('rm -rf {ICITE}; mkdir {ICITE}'.format(ICITE=DIR_ICITE))

        # SPEED TEST 2: DOWNLOAD citations and save into temporary working files
        dnldr_loader_f1 = NIHiCiteDownloader(DIR_ICITE, force_download=True)
        dnldr_only.wr_papers('dnldr_force_true_{N}.txt'.format(N=num), pmid2paper, force_wr)
        print('\nICITE temporary working dir: {ICITE}'.format(ICITE=DIR_ICITE))
        tic = default_timer()
        _run_download(dnldr_loader_f1, pmids)
        # pylint: disable=line-too-long
        msg = "{N:,} citations: Downloaded and saved into tmp files".format(N=len(pmid2paper))
        prt_hms(tic, msg, log)
        prt_hms(tic, msg, stdout)

        # SPEED TEST 3: LOAD citations from temporary working files
        dnldr_loader_f0 = NIHiCiteDownloader(DIR_ICITE, force_download=False)
        dnldr_only.wr_papers('dnldr_force_false_{N}.txt'.format(N=num), pmid2paper, force_wr)
        tic = default_timer()
        _run_download(dnldr_loader_f0, pmids)
        msg = "{N:,} citations: Loaded from tmp files".format(N=len(pmid2paper))
        prt_hms(tic, msg, log)
        prt_hms(tic, msg, stdout)
        print('  WROTE: {LOG}'.format(LOG=fout_log))
        system('cat {LOG}'.format(LOG=fout_log))


def _run_download(dnldr, pmids):
    """Download citations"""

    print('tests.pmids_i3 len(PMIDS)={}'.format(len(PMIDS)))

    ## pmid2paper = dnldr.api.dnld_icites(pmids)
    ## pmid2paper = dnldr.get_pmid2paper(pmids)
    ## pmid2paper = dnldr.get_icites(pmids)
    ## pmid2paper = dnldr.get_icites(pmids)
    pmid2paper = dnldr.get_pmid2paper(pmids)
    num_bytes = getsizeof(pmid2paper)
    # pylint: disable=line-too-long
    print('{N:,} pmid2paper: {BYTES:,} bytes, {MB:,} MB'.format(N=len(pmid2paper), BYTES=num_bytes, MB=num_bytes/1000000.0))
    dir_icite_wc_l()
    print('')
    return pmid2paper


if __name__ == '__main__':
    test_dnld_speed()

# Copyright (C) 2021-present, DV Klopfenstein. All rights reserved.
