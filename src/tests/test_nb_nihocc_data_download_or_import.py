#!/usr/bin/env python3
"""Test notebook"""
# pylint: disable=line-too-long
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
# NOTE: The Python API always downloads data from the NIH-OCC, even if it has been requested before. See the notebook, *Download or import citation data from the NIH-OCC*.

# In[1]:


from os import mkdir
from os.path import exists
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader


def test_nihocc_data_download_or_import():
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
    dnldr = NIHiCiteDownloader(dir_icite, force_download)


    # ## 3) Download NIH-OCC data for one PMID
    #
    # Print the column headers first. Then print the citation data.

    # In[3]:


    nih_entry = dnldr.get_icite(22882545)

    print(nih_entry.hdr)
    print(nih_entry)


    # ## 4) Optionally, print the column header descriptions

    # In[4]:


    # nih_entry.prt_keys()


    # ## 5) Download NIH-OCC data for multiple PMIDs

    # In[5]:


    pmids = [31461780, 22882545, 20050301]
    nih_entries = dnldr.get_icites(pmids)
    # die # TBD WRONG OUTPUT

    for entry in nih_entries:
        print(entry)


    # ## 4) Print all the NIH-OCC data for one PMID

    # In[6]:


    for key, val in nih_entry.dct.items():
        print('{KEY:>27} {VAL}'.format(KEY=key, VAL=val))

if __name__ == '__main__':
    test_nihocc_data_download_or_import()


# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
