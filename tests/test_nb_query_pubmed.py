#!/usr/bin/env python3
"""Test notebook"""
# coding: utf-8
# pylint: disable=line-too-long,too-many-locals

# # Query PubMed
# You will need to either set your email, apikey, and tool in the `.pmidciterc` file. See the setup setion in the main ***pmidcite*** README.md

# In[1]:

from os import system
from pmidcite.cfg import Cfg
from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.icite.downloader import get_downloader


def test_query_pubmed_apikey1():
    """Test notebook that queries PubMed with free text"""
    cfg = Cfg(prt_fullname=False)

    # Instantiate a PubMed object
    pmobj = PubMed(
        email=cfg.get_email(),
        apikey=cfg.get_apikey(),
        tool=cfg.get_tool())

    _run(pmobj, force_download=False)
    #_run(pmobj, force_download=True)


def _run(pmobj, force_download):
    # Query PubMed, download PMIDs
    pubmed_query = 'Orcinus Orca Type D'
    pmids = pmobj.dnld_query_pmids(pubmed_query)
    print('', flush=True)
    print(f'TEST QUERY:            {pubmed_query}', flush=True)
    print(f'TEST PMIDS DOWNLOADED: {pmids}', flush=True)

    # Print NIH citation data for the papers
    dnldr = get_downloader()
    pmid2paper = dnldr.get_pmid2paper(pmids)
    for paper in pmid2paper.values():
        print(f'TEST PAPER: {paper}', flush=True)

    # Download the PubMed abstract for the newest paper
    paper_chosen = sorted(pmid2paper.values(), key=lambda o: o.icite.get_dict()['year'])[0]
    print(f'\nTEST CHOSEN: {paper_chosen}\n', flush=True)

    pmid2nt = pmobj.dnld_wr1_per_pmid([paper_chosen.pmid], force_download, dir_pubmed_txt=".")

    for pmid, data in pmid2nt.items():
        print('TEST PMID', pmid, data, flush=True)

    file_pubmed = f'./pubmed_{paper_chosen.pmid}.txt'
    system(f'cat {file_pubmed}')


if __name__ == '__main__':
    test_query_pubmed_apikey1()
    #test_query_pubmed_apikey0()

# Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved.
