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


from os import mkdir
from os.path import exists
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader
from pmidcite.icite.downloader import get_downloader

def test_print_paper_all_refs_cites():
    """Test notebook"""

    dir_icite = './icite'
    if not exists(dir_icite):
        mkdir(dir_icite)

    # ## 2) Load the NIH Downloader
    # The NIH downloader will use the API to download data from NIH if it is not stored locally or if the user has requested to always download and over-write the older citation file, allowing new citations to be seen.
    #
    # The NIH downloader will read already downloaded NIH-OCC data if it is available. This makes it possible to work offline using previously downloaded citation data.

    # In[2]:

    force_download = False
    dnldr = NIHiCiteDownloader(dir_icite, force_download, details_cites_refs="all")
    _run(dnldr)

    dnldr = get_downloader()
    _run(dnldr)


def _run(dnldr):
    """Print paper data"""
    # ## 3) Download NIH-OCC data for one PMID
    #
    # The first paper, `TOP`, is the requested paper. It is followed by a list of citations (`CIT`), then references (`REF`).
    pmid = 22882545
    paper = dnldr.get_paper(pmid)
    paper.prt_summary()


if __name__ == '__main__':
    test_print_paper_all_refs_cites()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
