#!/usr/bin/env python3
"""Test notebook"""
# coding: utf-8

# pylint: disable=line-too-long
# # Download citation data from NIH-OCC
# NIH-OCC: Nation Institute of Health's Open Citation Collection https://icite.od.nih.gov/
#
# ## 1) Load Python interface to NIH-OCC's API
# One NIH entry per PubMed ID (PMID) will be downloaded to the directory, `./icite`.
#
# It is not advisable to add these files to a repo or revision manage them because the number of files will multitudinous.
# So ensure `./icite` is listed in the `.gitignore` file.
#
# NOTE: The Python API always downloads data from the NIH-OCC, even if it has been requested before. The Python downloader, `NIHiCiteDownloader`, will load NIH-OCC data from a file if it exists, otherwise will download the data using the API.

# In[1]:


from pmidcite.icite.downloader import get_downloader
from pmidcite.icite.nih_grouper import NihGrouper

def test_print_paper_all_refs_cites():
    """Test notebook"""

    # ## 2) Load the NIH Downloader
    # The NIH downloader will use the API to download data from NIH if it is not stored locally or if the user has requested to always download and over-write the older citation file, allowing new citations to be seen.
    #
    # The NIH downloader will read already downloaded NIH-OCC data if it is available. This makes it possible to work offline using previously downloaded citation data.

    # In[2]:
    dnldr = get_downloader(details_cites_refs="citations")


    # ## 3) Download NIH-OCC data for one PMID
    #
    # The first paper, `TOP`, is the requested paper. It is followed by a list of citations (`CIT`), then references (`REF`).
    #
    # Citations are stored in two data members, `cited_by` and `cited_by_clin`. In this example, there are no clinical papers which cited the chosen paper. But we show how union can be used to merge the two sets.

    # In[3]:
    pmid = 22882545
    pmids = [pmid]
    pmid2paper = dnldr.get_pmid2paper(pmids)
    paper = pmid2paper[pmid]

    # set of NIHiCiteEntry
    all_cites = paper.cited_by.union(paper.cited_by_clin)
    ## print('AAAAAAAAAAAAAAAAAAAAAAAAA paper.cited_by', paper.cited_by)
    ## print('AAAAAAAAAAAAAAAAAAAAAAAAA paper.cited_by_clin', paper.cited_by_clin)
    ## print('AAAAAAAAAAAAAAAAAAAAAAAAA all_cites', all_cites)


    print('4) Default sort of NIHiCiteEntry objects is by PMIDs')
    # In[4]:
    for nih_entry in sorted(all_cites):
        print(nih_entry)


    print('5) Sort by NIH percentile')
    # NIH entries that are too new to have been given a NIH percentile are set to 999 in *pmidcite*.
    #
    # It is important to highlight new papers.
    #
    # The 999 value makes the newest papers appear next to the papers having the highest NIH percentiles so the new papers are highlighted.

    # In[5]:
    for nih_entry in sorted(all_cites, key=lambda o: o.dct['nih_perc'], reverse=True):
        print(nih_entry)


    print('6) Sort by NIH group, then by year')
    # In[6]:
    nih_cites = sorted(all_cites, key=lambda o: [o.dct['nih_group'], o.dct['year']], reverse=True)
    for nih_entry in nih_cites:
        print(nih_entry)


    # ## 7) Print the keys which can be used for sorting
    # Pick out one NIH entry (NIHiCiteEntry object) and print available keys

    # In[7]:
    nih_entry = next(iter(nih_cites))
    print('\n{N} key-value pairs in an NIH entry:\n'.format(N=len(nih_entry.dct)))
    for key, value in nih_entry.dct.items():
        print("{KEY:>27} {VAL}".format(KEY=key, VAL=value))

    print('8) Expand NIH group `3` (well performing papers) to include NIH percentiles 50% or higher')
    grpr = NihGrouper(group3_min=50.0)
    dnldr = get_downloader(details_cites_refs="citations", nih_grouper=grpr)
    paper = dnldr.get_paper(22882545)
    for nihentry in sorted(paper.cited_by, key=lambda o: [o.dct['nih_group'], o.dct['year']], reverse=True):
        print(nihentry)


if __name__ == '__main__':
    test_print_paper_all_refs_cites()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
