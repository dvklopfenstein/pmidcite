#!/usr/bin/env python3
"""Test notebook"""
# coding: utf-8

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


import sys
from pmidcite.icite.api import NIHiCiteAPI

def print_paper_all_refs_cites():
    """Test notebook"""

    api = NIHiCiteAPI('./icite', prt=None)


    # ## 2) Load the NIH Downloader
    # The NIH downloader will use the API to download data from NIH if it is not stored locally or if the user has requested to always download and over-write the older citation file, allowing new citations to be seen.
    #
    # The NIH downloader will read already downloaded NIH-OCC data if it is available. This makes it possible to work offline using previously downloaded citation data.

    # In[2]:


    from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader

    force_download = False
    dnldr = NIHiCiteDownloader(force_download, api)


    # ## 3) Download NIH-OCC data for one PMID
    #
    # The first paper, `TOP`, is the requested paper. It is followed by a list of citations (`CIT`), then references (`REF`).

    # In[3]:


    pmids = [22882545]
    pmid2paper = dnldr.get_pmid2paper(pmids)

    for paper in pmid2paper.values():
        paper.prt_summary()


if __name__ == '__main__':
    print_paper_all_refs_cites()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
