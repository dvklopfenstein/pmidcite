#!/usr/bin/env python3
"""Test speed for download NIH citation data"""

import os
from sys import getsizeof
from sys import stdout
from pathlib import Path
import shutil
from timeit import default_timer

from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader
from pmidcite.icite.dnldr.pmid_dnlder_only import NIHiCiteDownloaderOnly

from tests.icite import DIR_ICITE
from tests.icite import dir_icite_wc_l
from tests.prt_hms import prt_hms
from tests.pmids_i3 import PMIDS
from tests.utils import cat


# pylint: disable=too-many-arguments,too-many-positional-arguments
def test_speed_dnld_load():
    """Test speed for download NIH citation data"""
    fout_log = 'test_speed_dnld_load.log'
    num = 5000
    force_wr = True
    ## pmids = PMIDS[:num]
    pmids = PMIDS  # Note: There are almost 90k PMIDs in this list
    # rm -rf {DIR_ICITE}; mkdir {DIR_ICITE}
    shutil.rmtree(DIR_ICITE, ignore_errors=True)
    Path(DIR_ICITE).mkdir(parents=True, exist_ok=True)

    with open(fout_log, 'w', encoding='utf-8') as log:
        dnldr_only = NIHiCiteDownloaderOnly()

        # SPEED TEST 1: DOWNLOAD citations but do not save temporary working files
        pmid2paper = _speed_test1(pmids, num, log, force_wr, dnldr_only)

        # SPEED TEST 2: DOWNLOAD citations and save into temporary working files
        _speed_test2(pmids, pmid2paper, num, log, force_wr, dnldr_only)

        # SPEED TEST 3: LOAD citations from temporary working files
        _speed_test3(pmids, pmid2paper, num, log, force_wr, dnldr_only)

        print(f'  WROTE: {fout_log}')
        cat(fout_log)


def _speed_test1(pmids, num, log, force_wr, dnldr_only):
    # SPEED TEST 1: DOWNLOAD citations but do not save temporary working files
    tic = default_timer()
    pmid2paper = _run_download(dnldr_only, pmids)
    msg = f"{len(pmid2paper):,} citations: Downloaded, but not saved"
    prt_hms(tic, msg, log)
    prt_hms(tic, msg, stdout)

    dnldr_only.wr_papers(f'dnldr_only_{num}.txt', pmid2paper, force_wr)

    # Create directory for temporary working files for citations
    # rm -rf {DIR_ICITE}; mkdir {DIR_ICITE}
    shutil.rmtree(DIR_ICITE, ignore_errors=True)
    return pmid2paper

def _speed_test2(pmids, pmid2paper, num, log, force_wr, dnldr_only):
    # SPEED TEST 2: DOWNLOAD citations and save into temporary working files
    os.makedirs(DIR_ICITE, exist_ok=True)
    dnldr_loader_f1 = NIHiCiteDownloader(DIR_ICITE, force_download=True)
    dnldr_only.wr_papers(f'dnldr_force_true_{num}.txt', pmid2paper, force_wr)
    print(f'\nICITE temporary working dir: {DIR_ICITE}')
    tic = default_timer()
    _run_download(dnldr_loader_f1, pmids)
    # pylint: disable=line-too-long
    msg = f"{len(pmid2paper):,} citations: Downloaded and saved into tmp files"
    prt_hms(tic, msg, log)
    prt_hms(tic, msg, stdout)

def _speed_test3(pmids, pmid2paper, num, log, force_wr, dnldr_only):
    # SPEED TEST 3: LOAD citations from temporary working files
    dnldr_loader_f0 = NIHiCiteDownloader(DIR_ICITE, force_download=False)
    dnldr_only.wr_papers(f'dnldr_force_false_{num}.txt', pmid2paper, force_wr)
    tic = default_timer()
    _run_download(dnldr_loader_f0, pmids)
    msg = f"{len(pmid2paper):,} citations: Loaded from tmp files"
    prt_hms(tic, msg, log)
    prt_hms(tic, msg, stdout)


def _run_download(dnldr, pmids):
    """Download citations"""

    print(f'tests.pmids_i3 len(PMIDS)={len(PMIDS)}')

    ## pmid2paper = dnldr.api.dnld_icites(pmids)
    ## pmid2paper = dnldr.get_pmid2paper(pmids)
    ## pmid2paper = dnldr.get_icites(pmids)
    ## pmid2paper = dnldr.get_icites(pmids)
    pmid2paper = dnldr.get_pmid2paper(pmids)
    num_bytes = getsizeof(pmid2paper)
    # pylint: disable=line-too-long
    print(f'{len(pmid2paper):,} pmid2paper: {num_bytes:,} bytes, {num_bytes/1000000.0:,} MB')
    dir_icite_wc_l()
    print('')
    return pmid2paper


if __name__ == '__main__':
    test_speed_dnld_load()

# Copyright (C) 2021-present, DV Klopfenstein, PhD. All rights reserved.
