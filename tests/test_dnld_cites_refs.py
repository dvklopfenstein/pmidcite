#!/usr/bin/env python3
"""Test downloading a paper, paper + refs, paper + cites, paper + all"""

from os import system
from sys import stdout
from glob import glob
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader
from pmidcite.icite.entry import NIHiCiteEntry
from tests.icite import DIR_ICITE
from tests.icite import dir_icite_clobber

FORCE_DNLD = True


def test_dnld_cites_refs():
    """Test downloading a paper, paper + refs, paper + cites, paper + all"""

    pmid = 20640201
    dnldr_top = NIHiCiteDownloader(DIR_ICITE, FORCE_DNLD)
    _run("TEST(plain)", dnldr_top, pmid)

    _compare("TEST(cites)", pmid, NIHiCiteEntry.citekeys, "citations")
    _compare("TEST(refs)", pmid, NIHiCiteEntry.refkey, "references")
    _compare("TEST(all)", pmid, NIHiCiteEntry.associated_pmid_keys, "all")

    print('DIR_ICITE:', DIR_ICITE)


def _compare(test_name, pmid, entry_lst, desc):
    """Compare reporting refs/cites of a paper using set format vs. string format"""
    print(f"COMPARE: {entry_lst} {desc}")
    dir_icite_clobber(stdout)
    dnldr_set = NIHiCiteDownloader(DIR_ICITE, FORCE_DNLD, entry_lst)
    dnldr_txt = NIHiCiteDownloader(DIR_ICITE, FORCE_DNLD, desc)
    paper_set = _run(f"{test_name}-{','.join(entry_lst)}", dnldr_set, pmid)
    paper_txt = _run(f"{test_name}-{desc}", dnldr_txt, pmid)
    # pylint: disable=line-too-long
    assert len(paper_set.cited_by) == len(paper_txt.cited_by), \
        f'**FATAL {test_name} -- cited_by({len(paper_set.cited_by)} != {len(paper_txt.cited_by)}): {paper_set}'
    assert len(paper_set.cited_by_clin) == len(paper_txt.cited_by_clin), \
        f'**FATAL {test_name} -- cited_by_clin({len(paper_set.cited_by_clin)} != {len(paper_txt.cited_by_clin)}): {paper_set}'
    assert len(paper_set.references) == len(paper_txt.references), \
        f'**FATAL {test_name} -- references({len(paper_set.references)} != {len(paper_txt.references)}): {paper_set}'
    print(f'TEST PASSED: {desc}')

def _run(test_name, dnldr, pmid):
    """Download PMIDs"""
    system(f'rm -f {dnldr.dir_dnld}/p*.py')
    pmid2icitepaper = dnldr.get_pmid2paper({pmid}, pmid2note=None)

    # Get filenames (p{PMID}.py) downloaded from NIH's citation database
    globstr = f'{dnldr.dir_dnld}/p*.py'
    pmids_dnlded = glob(globstr)
    print(f'{len(pmids_dnlded)} NIH icites downloaded')
    ## print('{N} pmid2icitepaper for PMID({P}); {O} assc PMIDs'.format(
    ##     N=len(pmid2icitepaper),
    ##     P=pmid,
    ##     O=dnldr.details_cites_refs))
    paper = pmid2icitepaper[pmid]
    pmids_exp = _get_exp_pmids(dnldr, paper.icite.get_dict())
    ## print(pmids_exp)
    ## print(pmids_dnlded)
    assert len(pmids_exp) + 1 == len(pmids_dnlded), \
        f'{test_name} EXP({len(pmids_exp) + 1}) != ACT({len(pmids_dnlded)}) {dnldr.dir_dnld}'
    ## print(dnldr.details_cites_refs)
    ## print(paper.icite.get_dict())
    assert len(pmids_exp) + 1 == len(paper.pmid2icite)
    print(f'PMID({pmid}) has {len(paper.pmid2icite)} assc PMIDs by {dnldr.details_cites_refs}')
    print('')
    return paper

def _get_exp_pmids(dnldr, top_dct):
    """Get expected PMIDs (citations and references)"""
    pmids = set()
    for key in dnldr.details_cites_refs:
        ## print('EEEEEEEEEEEEE', top_dct[key])
        pmids.update(top_dct[key])
    return pmids


if __name__ == '__main__':
    test_dnld_cites_refs()

# Copyright (C) 2021-present, DV Klopfenstein, PhD. All rights reserved.
