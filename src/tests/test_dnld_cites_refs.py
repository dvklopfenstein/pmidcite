#!/usr/bin/env python3
"""Test downloading a paper, paper + refs, paper + cites, paper + all"""

from os import system
from glob import glob
from pmidcite.icite.nih_grouper import NihGrouper
from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader
from pmidcite.icite.entry import NIHiCiteEntry
from tests.icite import DIR_ICITE


def test_dnld_cites_refs():
    """Test downloading a paper, paper + refs, paper + cites, paper + all"""
    force_dnld = True
    nihgrouper = NihGrouper()
    api = NIHiCiteAPI(nihgrouper, dirpy_dnld=DIR_ICITE)

    pmid = 20640201
    dnldr_top = NIHiCiteDownloader(force_dnld, api)
    _run(dnldr_top, pmid)

    dnldr_cites = NIHiCiteDownloader(force_dnld, api, NIHiCiteEntry.citekeys)
    _run(dnldr_cites, pmid)

    dnldr_refs = NIHiCiteDownloader(force_dnld, api, NIHiCiteEntry.refkey)
    _run(dnldr_refs, pmid)

    dnldr_all = NIHiCiteDownloader(force_dnld, api, NIHiCiteEntry.associated_pmid_keys)
    _run(dnldr_all, pmid)
    print('DIR_ICITE:', DIR_ICITE)


def _run(dnldr, pmid):
    """Download PMIDs"""
    system('rm -f {DIR}/p*.py'.format(DIR=dnldr.dir_dnld))
    pmid2icitepaper = dnldr.get_pmid2paper({pmid}, pmid2note=None)

    # Get filenames (p{PMID}.py) downloaded from NIH's citation database
    globstr = '{DIR}/p*.py'.format(DIR=dnldr.dir_dnld)
    pmids_dnlded = glob(globstr)
    print('{N} NIH icites downloaded'.format(N=len(pmids_dnlded)))
    ## print('{N} pmid2icitepaper for PMID({P}); {O} assc PMIDs'.format(
    ##     N=len(pmid2icitepaper),
    ##     P=pmid,
    ##     O=dnldr.details_cites_refs))
    paper = pmid2icitepaper[pmid]
    pmids_exp = _get_exp_pmids(dnldr, paper.icite.dct)
    ## print(pmids_exp)
    ## print(pmids_dnlded)
    assert len(pmids_exp) + 1 == len(pmids_dnlded)
    ## print(dnldr.details_cites_refs)
    ## print(paper.icite.dct)
    assert len(pmids_exp) + 1 == len(paper.pmid2icite)
    print('PMID({PMID}) has {N} assc PMIDs by {KEYS}'.format(
        PMID=pmid,
        N=len(paper.pmid2icite),
        KEYS=dnldr.details_cites_refs))
    print('')

def _get_exp_pmids(dnldr, top_dct):
    """Get expected PMIDs (citations and references)"""
    pmids = set()
    for key in dnldr.details_cites_refs:
        ## print('EEEEEEEEEEEEE', top_dct[key])
        pmids.update(top_dct[key])
    return pmids


if __name__ == '__main__':
    test_dnld_cites_refs()

# Copyright (C) 2021-present, DV Klopfenstein. All rights reserved.
