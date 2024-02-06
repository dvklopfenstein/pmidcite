#!/usr/bin/env python3
"""Test self-citing functions"""

from pmidcite.cfg import Cfg
from pmidcite.icite.entry import NIHiCiteEntry
#from pmidcite.cli.entry_keyset import get_details_cites_refs
from pmidcite.icite.downloader import get_downloader

def test_selfcite():
    """Test self-citing functions"""
    authors = [
        'Nasserdine Papa Mze',
        'Cécile Fernand-Laurent',
        'Solen Daugabel',
        'Olfa Zanzouri',
        'Stéphanie Marque Juillet',
    ]
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

    cfg = Cfg()

    details_cites_refs = set(NIHiCiteEntry.associated_pmid_keys)
    print(f'details_cites_refs: {details_cites_refs}')

    groupobj = cfg.get_nihgrouper()
    print(groupobj)

    dnldr = get_downloader(
        None,     # {'references', 'cited_by', 'cited_by_clin'}
        groupobj
    )
        #cfg.dir_icite_py,
        #args.force_download)
    print(dnldr)

    pmid2icitepaper = dnldr.get_pmid2paper(ref_pmids, None)
    # Get PMID and pmidcite.icite.paper.NIHiCitePaper
    # TODO: Improve researcher experience here
    for pmid, icitepaper in pmid2icitepaper.items():
        entry = icitepaper.get_icite()
        authors = entry.dct['authors']
        print(entry)
        for author in authors:
            print(f'{pmid:8} {author}')

    print()
    print(entry.dct.keys())


if __name__ == '__main__':
    test_selfcite()
