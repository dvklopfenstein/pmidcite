"""Download PubMed data to get PMID. Print NIH iCite summary using PMID.

     1) Download PubMed summary to get PMID, given DOI in bib entry
     2) Print PMID downloaded from PubMed and citekey from pubs
     3) Print NIH's iCite summary for each publication

"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
from pmidcite.eutils.pubmed.rdwr import PubMedRdWr
from pmidcite.eutils.pubmed.record import PubMedRecord
from pmidcite.eutils.cmds.pubmed import PubMed


# pylint: disable=too-few-public-methods
class PubMedQuery:
    """Download PubMed text summary for PMID. Print NIH iCite summary using PMID"""

    patterns = {
        'doi' : '{doi}[Location ID] OR {doi}[Secondary Source ID] OR {doi}[Article Identifier]',
        'pmid' : '{pmid}[PMID]',
    }

    def __init__(self, email, apikey, tool, prt=sys.stdout):
        self.pubmed = PubMed(email, apikey, tool, prt)
        self.pubmedrw = PubMedRdWr()

    def get_pubmed_g_doi(self, doi, prt=None):
        """Give a DOI, return PubMed record's text and Record object"""
        query = self.patterns['doi'].format(doi=doi)
        pubmed_txt = self.dnld_text_g_query(query)
        if pubmed_txt is not None:
            pmid2dct = self.get_pmid2dct_g_txt(pubmed_txt, prt)
            pmid2rec = {pmid:PubMedRecord(dct) for pmid, dct in pmid2dct.items()}
            return {'pubmed_text': pubmed_txt, 'pmid2rec':pmid2rec}
        return {}

    def get_pubmed_g_pmid(self, pmid, prt=None):
        """Give a DOI, return PubMed record's text and Record object"""
        query = self.patterns['pmid'].format(pmid=pmid)
        pubmed_txt = self.dnld_text_g_query(query)
        if pubmed_txt is not None:
            pmid2dct = self.get_pmid2dct_g_txt(pubmed_txt, prt)
            pmid2rec = {pmid:PubMedRecord(dct) for pmid, dct in pmid2dct.items()}
            return {'pubmed_text': pubmed_txt, 'pmid2rec':pmid2rec}
        return {}

    def get_prt(self):
        """Return the print stored in the E-Utils base"""
        return self.pubmed.log

    def get_pubmed_dct(self, file_txt, prt=None, **kws):
        """Download or load one PubMed text summary as a dict for one publication"""
        if os.path.exists(file_txt):
            return self._get_pmiddct(file_txt)
        for key in set(self.patterns).intersection(kws):
            query = self.patterns[key].format(**{key:kws[key]})
            pubmed_txt = self.dnld_text_g_query(query)
            if pubmed_txt is not None:
                self.wr_text(file_txt, pubmed_txt)
                return self.get_pmid2dct_g_txt(pubmed_txt, prt)
            print('**WARNING: NO RESULTS FOUND FOR: {Q}'.format(Q=query))
            return {}
        raise RuntimeError('UNKNOWN PubMed DATA: {KWS}'.format(KWS=str(kws)))

    def dnld_text_g_query(self, query):
        """Get PubMed text, given a PubMed query"""
        ## print('QUERY: {Q}'.format(Q=query))
        pmids = self.pubmed.dnld_query_pmids(query)
        if not pmids:
            return None
        efetch_idxs, efetch_params = self.pubmed.epost_ids(
            pmids, 'pubmed', 10, 10000, rettype='medline', retmode='text')
        txts = self.pubmed.dnld_texts(efetch_idxs, efetch_params)
        return '\n'.join(txts)

    def get_pmid2dct_g_txt(self, pubmed_txt, prt=None):
        """Given text containing downloaded PubMed records"""
        return self.pubmedrw.get_pmid2info_g_textblock(pubmed_txt, prt=prt)

    @staticmethod
    def wr_text(fout_txt, pubmed_txt):
        """Write PubMed record text into a file"""
        with open(fout_txt, 'w') as prt:
            prt.write(pubmed_txt)
            print('  WROTE: {TXT}'.format(TXT=fout_txt))

    def _get_pmiddct(self, fin_txt):
        """Read PubMed text summary. Return PubMed dict, which contains PMID"""
        dct = self.pubmedrw.get_pmid2info_g_text(fin_txt)
        assert len(dct) == 1, dct
        return list(dct.values())[0]


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
