"""Given PMIDs, download PubMed records containing"""

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2016-present DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import os
import sys
from pmidcite.eutils.cmds.base import EntrezUtilities
from pmidcite.eutils.cmds.esearch import ESearch


class PubMed(EntrezUtilities):
    """Fetch and write text"""

    medline_text = {
        'rettype': 'medline',
        'retmode': 'text',
    }
    pat = 'PMIDs/epost={P} PMIDs/efetch={F} querykey({Q} of {Qmax}) start({S})'

    def __init__(self, email, apikey, tool, prt=sys.stdout):
        super(PubMed, self).__init__(email, apikey, tool, prt)
        self.esearch = ESearch(email, apikey, tool, prt)

    def dnld_query_pmids(self, query, num_ids_p_epost=10):
        """Searches an PubMed for a user query, writes resulting entries into one file."""
        return self.esearch.dnld_query_pmids(query, 'pubmed', num_ids_p_epost)

    def _dnld_wr_all(self, fout_pubmed, efetch_idxs, efetch_params):
        """Download and write all PMIDs PubMed text entries into one file"""
        if os.path.exists(fout_pubmed):
            os.system('rm {FILE}'.format(FILE=fout_pubmed))
        if not efetch_idxs:
            return
        for desc, start, pmids_exp, querykey in efetch_idxs:
            rsp_txt = self._run_efetch('pubmed', start, querykey, pmids_exp, desc, **efetch_params)
            if rsp_txt is not None:
                with open(fout_pubmed, 'a') as prt:
                    prt.write(rsp_txt)
                    prt.flush()
        print('  WROTE: {FILE}'.format(FILE=fout_pubmed))

    def _dnld_query(self, query):
        """Searches an NCBI database for a user search term, returns NCBI IDs."""
        dct = self.run_eutilscmd('esearch', db='pubmed', term=query, retmode='json')
        return dct

    def dnld_wr1_per_pmid(self, pmids, force_download, dir_pubmed_txt, pmid2name=None):
        """Download and write one PubMed text file entry per PMID"""
        if not os.path.exists(dir_pubmed_txt):
            raise RuntimeError('**ERROR: NO OUTPUT DIR: {DIR}'.format(
                DIR=dir_pubmed_txt))
        pmid_nt_list = self.get_pmid_nt_list(pmids, force_download, dir_pubmed_txt, pmid2name)
        efetch_idxs, efetch_params = self.epost_ids(pmids, 'pubmed', 10, 1, **self.medline_text)
        return self.esearch.dnld_wr1_per_id('pubmed', efetch_idxs, efetch_params, pmid_nt_list)

    def dnld_texts(self, efetch_idxs, efetch_params):
        """Download and save one PMID PubMed entry into a text string"""
        txts = []
        for desc, start, pmids_exp, querykey in efetch_idxs:
            rsp_txt = self._run_efetch('pubmed', start, querykey, pmids_exp, desc, **efetch_params)
            txts.append(rsp_txt)
        return txts

    @staticmethod
    def _get_str_post_fetch(num_pmids_p_epost, num_pmids_p_efetch, querykey, start):
        """Get a string summarizing current EPost and EFetch"""
        return 'IDs/epost={P} IDs/efetch={F} querykey({Q}) start({S})'.format(
            P=num_pmids_p_epost, F=num_pmids_p_efetch, Q=querykey, S=start)

    def get_pmid_nt_list(self, pmids, force_download, dir_pubmed, pmid2name=None):
        """Get list of PubMed entries: Title, abstract, authors, journal, MeSH"""
        # [Nt(PMID=31614060, file_pubmed='./log/pubmed/pubmed_31614060.txt', file_exists=False)]
        return self.esearch.get_pmid_nt_list(pmids, 'pubmed', force_download, dir_pubmed, pmid2name)



# Copyright (C) 2016-present DV Klopfenstein. All rights reserved.
