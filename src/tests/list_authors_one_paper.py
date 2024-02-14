#!/usr/bin/env python
# coding: utf-8

# # List the authors of a paper
# ### Import the downloader to download NIH citations

# In[1]:


from pmidcite.icite.downloader import get_downloader

dnldr = get_downloader()


# ### Download citation data from the NIH for a paper with PMID=30022098

# In[2]:


pmid = 30022098
icitepaper = dnldr.get_icite(pmid)


# ### Get the authors for a paper

# In[3]:


for author in icitepaper.get_authors():
    print(f'{pmid:8} {author}')

assert len(icitepaper.get_authors()) == 14


# Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved.
