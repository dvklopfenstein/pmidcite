#!/usr/bin/env python3
"""Test notebook"""
# coding: utf-8
# pylint: disable=line-too-long

# # Query PubMed
# You will need to either set your email, apikey, and tool in the `.pmidciterc` file. See the setup setion in the main ***pmidcite*** README.md

# In[1]:


from pmidcite.cfg import Cfg
from pmidcite.eutils.cmds.pubmed import PubMed

def test_query_pubmed():
    """Test notebook"""
    cfg = Cfg(prt_fullname=False)


    # ## Instantiate a PubMed object

    # In[2]:


    pmobj = PubMed(
        email=cfg.get_email(),
        apikey=cfg.get_apikey(),
        tool=cfg.get_tool())


    # ## Query PubMed, download PMIDs

    # In[3]:


    pubmed_query = 'Orcinus Orca Type D'
    pmids = pmobj.dnld_query_pmids(pubmed_query)


    # ## Print NIH citation data for the papers

    # In[4]:


    from pmidcite.icite.api import NIHiCiteAPI
    from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader

    force_download = False
    api = NIHiCiteAPI(cfg.get_dir_icite_py())
    dnldr = NIHiCiteDownloader(force_download, api)
    pmid2paper = dnldr.get_pmid2paper(pmids)
    for paper in pmid2paper.values():
        print(paper)


    # ## Download the PubMed abstract
    # Download the PubMed abstract for the newest paper

    # In[5]:


    paper_chosen = sorted(pmid2paper.values(), key=lambda o: o.icite.dct['year'])[0]
    print(paper_chosen)


    # In[6]:


    pmobj.dnld_wr1_per_pmid([paper_chosen.pmid], force_download, dir_pubmed_txt=".")


    # In[7]:


    fpm = './pubmed_{PMID}.txt'.format(PMID=paper_chosen.pmid)
    get_ipython().system('cat $fpm')


if __name__ == '__main__':
    test_query_pubmed()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
