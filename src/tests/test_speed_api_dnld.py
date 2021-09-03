#!/usr/bin/env python3
"""Test speed for download NIH citation data"""

from sys import getsizeof
from timeit import default_timer

from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader

from tests.icite import DIR_ICITE
from tests.icite import dir_icite_clobber
from tests.icite import dir_icite_wc_l
from tests.prt_hms import prt_hms
from tests.pmids_i3 import PMIDS


def test_dnld_speed():
    """Test speed for download NIH citation data"""
    force_dnld = True
    dnldr = _init_dnldr(force_dnld)

    num = 5000
    print('tests.pmids_i3 len(PMIDS)={}'.format(len(PMIDS)))
    pmids = PMIDS[:num]
    pmids = PMIDS
    # _dnld_icite_v_icites(dnldr, pmids)

    dir_icite_clobber()
    ## nihentries = dnldr.api.dnld_icites(pmids)
    ## nihentries = dnldr.get_pmid2paper(pmids)
    ## nihentries = dnldr.get_icites(pmids)
    tic = default_timer()
    nihdicts = dnldr.api.dnld_nihdicts(pmids)
    num_bytes = getsizeof(nihdicts)
    # pylint: disable=line-too-long
    print('{N} nihdicts: {BYTES:,} bytes, {MB:,} MB'.format(
        N=len(nihdicts),
        BYTES=num_bytes,
        MB=num_bytes/1000000.0))
    tic = prt_hms(tic, "Downloaded {N:,} items w/dnld_icites".format(N=len(nihdicts)))
    dir_icite_wc_l()

def _dnld_icite_v_icites(dnldr, pmids):
    dir_icite_clobber()
    num_pmids = len(pmids)
    tic = default_timer()
    for idx, pmid in enumerate(pmids, 1):
        if idx%10 == 0:
            print("Downloading item {N:,}".format(N=idx))
        dnldr.api.dnld_icite(pmid)  # NIHiCiteEntry
    tic = prt_hms(tic, "Downloaded {N} items w/dnld_icite".format(N=num_pmids))


def _init_dnldr(force_dnld):
    """Initialize a NIH Downloader and tmp dir, src/tests/icite"""
    tic = default_timer()
    dir_icite_clobber(prt=None)
    dnldr = NIHiCiteDownloader(DIR_ICITE, force_dnld)
    tic = prt_hms(tic, "Initialize NIH citation downloader")
    return dnldr


if __name__ == '__main__':
    test_dnld_speed()

# Copyright (C) 2021-present, DV Klopfenstein. All rights reserved.
