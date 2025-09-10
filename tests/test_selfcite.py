#!/usr/bin/env python3
"""Test getting all authors for a bunch of papers"""

from pmidcite.cfg import Cfg
from pmidcite.icite.downloader import get_downloader

def test_selfcite():
    """Test getting all authors for a bunch of papers"""
    #authors = [
    #    'Nasserdine Papa Mze',
    #    'Cécile Fernand-Laurent',
    #    'Solen Daugabel',
    #    'Olfa Zanzouri',
    #    'Stéphanie Marque Juillet',
    #]
    ref_pmids = [
        30753724, # TOP 30753724 H.M.c 40 2 2019    10  1  22 au[41](Lambert Assoumou)
        30517632, # TOP 30517632 H.M.. 21 2 2019     5  0  35 au[17](Paula C Aulicino)
         9527771, # TOP  9527771 H.M.c 97 3 1998   351 42  39 au[17](K Hertogs)
        15821401, # TOP 15821401 H.M.. 24 2 2005    20  0  12 au[07](Elizabeth Johnston)
        21628544, # TOP 21628544 H.M.. 26 2 2011    18  0  79 au[17](Jan Weber)
        28303602, # TOP 28303602 H.M.. 65 2 2018    21  0  29 au[05](Francesco Saladini)
        29207001, # TOP 29207001 H.M.. 76 2 2017    38  0  52 au[04](Natalia Stella-Ascariz)
        32344322, # TOP 32344322 H.M.. 44 2 2020     7  0  15 au[03](Shoshanna May)
        35269868, # TOP 35269868 H.M.. 59 2 2022     5  0  36 au[06](Maria Addolorata Bonifacio)
          843571, # TOP   843571 H...c -1 i 1977 34973 2577   8 au[02](J R Landis)
        30596682, # TOP 30596682 H.M.. 54 2 2018    17  0  20 au[06](Géraldine Dessilly)
        30682153, # TOP 30682153 ..M..  4 1 2019     1  0   1 au[06](Géraldine Dessilly) CORRECTION
    ]

    cfg = Cfg(check=False)
    groupobj = cfg.get_nihgrouper()
    dnldr = get_downloader(groupobj)

    # Get PMID and pmidcite.icite.paper.NIHiCitePaper
    pmid2icitepaper = dnldr.get_pmid2paper(ref_pmids, None)
    for pmid, icitepaper in pmid2icitepaper.items():
        for author in icitepaper.get_authors():
            print(f'PAPER: {pmid:8} {author}')

    # Even simpler:
    # Get pmidcite.icite.paper.NIHiCiteEntry for each PMID in the references
    for icitepaper in dnldr.get_icites(ref_pmids):
        for author in icitepaper.get_authors():
            print(f'iCite: {icitepaper.pmid:8} {author}')


if __name__ == '__main__':
    test_selfcite()
