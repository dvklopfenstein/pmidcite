"""Download PubMed data to get PMID. Print NIH iCite summary using PMID.

     1) Download PubMed summary to get PMID, given DOI in bib entry
     2) Print PMID downloaded from PubMed and citekey from pubs
     3) Print NIH's iCite summary for each publication

"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
from PyBiocode.pubmed.dnld.wrpy_pmid import WrPyPMID
from pmidcite.eutils.cmds.base import EntrezUtilities


# pylint: disable=too-few-public-methods
class PubMedQuery:
    """Download PubMed text summary for PMID. Print NIH iCite summary using PMID"""

    doi_pat = '{DOI}[Location ID] OR {DOI}[Secondary Source ID] OR {DOI}[Article Identifier]'
    pmid_pat = '{PMID}[PMID]'

    def __init__(self):
        self.eutils = EntrezUtilities(log=None)

    def get_pubmed_dct(self, file_txt, **kws):
        """Download or load one PubMed text summary as a dict for one publication"""
        if os.path.exists(file_txt):
            return self._get_pmiddct(file_txt)
        if 'pmid' in kws:
            return self._dnld_pubmed_by_pmid(file_txt, kws['pmid'])
        if 'doi' in kws:
            return self._dnld_pubmed_by_doi(file_txt, kws['doi'])
        raise RuntimeError('UNKNOWN PubMed DATA: {KWS}'.format(str(kws)))

    def _dnld_pubmed_by_pmid(self, fout_txt, pmid):
        """Download & load one PubMed text summary as a dict for one publication"""
        if pmid is not None and pmid.isdigit():
            query = self.pmid_pat.format(PMID=pmid)
            return self._dnld_pubmed_by_query(fout_txt, query)
        print('PMID({PMID}) IS NOT VALID'.format(PMID=pmid))

    def _dnld_pubmed_by_doi(self, fout_txt, doi):
        """Download & load one PubMed text summary as a dict for one publication"""
        query = self.doi_pat.format(DOI=doi)
        return self._dnld_pubmed_by_query(fout_txt, query)

    def _dnld_pubmed_by_query(self, fout_txt, query):
        """Download & load one PubMed text summary as a dict for one publication"""
        print('QUERY: {Q}'.format(Q=query))
        dct = self.eutils.pubmed_query_fetch(query)
        txt = dct['TEXT']
        if txt is None:
            return None
        assert len(dct['RSP_QUERY']['idlist']) == 1, dct['RSP_QUERY']['idlist']
        with open(fout_txt, 'w') as prt:
            prt.write(dct['TEXT'])
            print('  WROTE: {TXT}'.format(TXT=fout_txt))
        return self._get_pmiddct(fout_txt)

    @staticmethod
    def _get_pmiddct(fin_txt):
        """Read PubMed text summary. Return PubMed dict, which contains PMID"""
        dct = WrPyPMID().get_pmid2info_g_text(fin_txt)
        assert len(dct) == 1, dct
        return list(dct.values())[0]


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
