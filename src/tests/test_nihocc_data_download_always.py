#!/usr/bin/env python
"""Test notebook"""
# coding: utf-8

# # Download citation data from NIH-OCC
# Nation Institute of Health's Open Citation Collection (NIH-OCC)
#
# ## 1) Load Python interface to NIH-OCC's API
# One NIH entry per PubMed ID (PMID) will be downloaded to the directory, `./icite`.
#
# It is not advisable to add these files to a repo or revision manage them because the number of
# files will multitudinous. So ensure `./icite` is listed in the `.gitignore` file.
#
# NOTE: The Python API always downloads data from the NIH-OCC, even if it has been requested before.
# See the notebook, *Download or import citation data from the NIH-OCC*.

# In[1]:

import sys
from pmidcite.icite.api import NIHiCiteAPI
#### from pmidcite.icite.nih_grouper import NihGrouper


def test_nihocc_data_download_always():
    """Test notebook"""
    # prt=None will suppress the "WROTE: ./icite/p22882545.py" messages
    
    #### grpr = NihGrouper()
    api = NIHiCiteAPI('./icite', prt=sys.stdout)


    # ## 2) Download NIH-OCC data for one PMID
    #
    # Print the column headers first. Then print the citation data.

    # In[ ]:


    nih_entry = api.dnld_icite(22882545)

    print(nih_entry.hdr)
    print(nih_entry)


    # ## 3) Print the key to the column headers

    # In[ ]:


    nih_entry.prt_keys()


    # ## 3) Download NIH-OCC data for multiple PMIDs

    # In[ ]:


    pmids = [31461780, 22882545, 20050301]
    nih_entries = api.dnld_icites(pmids)

    for entry in nih_entries:
        print(entry)


    # ## 4) Print all the NIH-OCC data for one PMID

    # In[ ]:


    for key, val in nih_entry.dct.items():
        print('{KEY:>27} {VAL}'.format(KEY=key, VAL=val))

if __name__ == '__main__':
    test_nihocc_data_download_always()


# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
