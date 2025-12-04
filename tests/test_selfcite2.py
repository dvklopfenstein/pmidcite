#!/usr/bin/env python3
"""Test getting all authors for a bunch of papers"""

from pmidcite.cfg import Cfg
from pmidcite.icite.downloader import get_downloader

def test_selfcite():
    """Test getting all authors for a bunch of papers"""
    pmid = 33031639

    cfg = Cfg(check=False)
    groupobj = cfg.get_nihgrouper()
    dnldr = get_downloader(groupobj)

    # Get PMID and pmidcite.icite.paper.NIHiCitePaper
    icitepaper = dnldr.get_icite(pmid)
    print(icitepaper)
    ## for pmid, icitepaper in pmid2icitepaper.items():
    ##     for author in icitepaper.get_authors():
    ##         print(f'PAPER: {pmid:8} {author}')

    ## # Even simpler:
    ## # Get pmidcite.icite.paper.NIHiCiteEntry for each PMID in the references
    ## for icitepaper in dnldr.get_icites(ref_pmids):
    ##     for author in icitepaper.get_authors():
    ##         print(f'iCite: {icitepaper.pmid:8} {author}')


if __name__ == '__main__':
    test_selfcite()
