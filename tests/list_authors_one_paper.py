#!/usr/bin/env python
# coding: utf-8
"""Test notebook code: List the authors of a paper"""

from pmidcite.icite.downloader import get_downloader

def test_list_authors_one_paper():

    dnldr = get_downloader()

    # ### Download citation data from the NIH for a paper with PMID=30022098
    pmid = 30022098
    icitepaper = dnldr.get_icite(pmid)
    citedby = icitepaper.get('cited_by')
    citedby_clin = icitepaper.get('cited_by_clin')
    assert next(iter(citedby_clin)) in citedby
    assert set(citedby_clin).intersection(citedby) == set(citedby_clin)
    print(citedby.index(citedby_clin[0]))
    print(citedby[0])
    print(citedby_clin[0] in citedby)


    # ### Get the authors for a paper
    print(f"TITLE: {icitepaper.get('title')}")
    print('AUTHORS:')
    for idx, author in enumerate(icitepaper.get_authors(), 1):
        print(f'  {idx:2}) {author}')

    assert len(icitepaper.get_authors()) == 14


if __name__ == '__main__':
    test_list_authors_one_paper()


# Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved.
