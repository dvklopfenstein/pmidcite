"""Given PMIDs, download PubMed records containing"""

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2016-present DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import os
import collections as cx
#### import sys
import re
from pmidcite.eutils.cmds.base import EntrezUtilities


class PubMed(EntrezUtilities):
    """Fetch and write text"""

    efetch_params = {
        'db': 'pubmed',
        'rettype': 'medline',
        'retmode': 'text',
    }
    pat = 'PMIDs/epost={P} PMIDs/efetch={F} querykey({Q} of {Qmax}) start({S})'

    def __init__(self, email, apikey, tool):
        super(PubMed, self).__init__(email, apikey, tool)

    def dnld_wr1_per_pmid(self, pmids, force_download=False, dir_pubmed="."):
        """Download and write file one PubMed entry per PMID"""
        pmid_nt_list = self._get_pmid_nt_list(pmids, force_download, dir_pubmed)
        for ntd in pmid_nt_list:
            print('IIIIIIIIIIIIIIIIIIIII {PMID:12} {NT}'.format(PMID=ntd.PMID, NT=ntd))

        # Run EPost
        pmids = [nt.PMID for nt in pmid_nt_list]
        epost_rsp = self.epost('pubmed', pmids, num_ids_p_epost=10)

        # Set EFetch params
        efetch_params = dict(self.efetch_params)
        efetch_params['webenv'] = epost_rsp['webenv']
        efetch_params['retmax'] = 1  # num_pmids_p_efetch

        # Run EFetches
        self._dnld_wr1_per_pmid(epost_rsp, efetch_params, pmids)

    def _dnld_wr1_per_pmid(self, epost_rsp, efetch_params, pmids):
        """Download and write PubMed entries, given PMIDs and assc info"""
        # pmids num_pmids_p_epost num_pmids_p_efetch  ->  num_efetches
        # ----- ----------------- ------------------      ------------
        #     5                 2                  3                 3
        #     5                 2                  1                 5
        querykey_max = epost_rsp['querykey']
        num_pmids_p_efetch = efetch_params['retmax']
        pat_val = {'P':epost_rsp['num_ids_p_epost'], 'F':num_pmids_p_efetch, 'Qmax':querykey_max}
        num_pmids = len(pmids)
        for querykey_cur, pmids_cur in enumerate(epost_rsp['qkey2ids'], 1):
            if querykey_cur == querykey_max:
                num_pmids_p_epost_cur = num_pmids%epost_rsp['num_ids_p_epost']
            for start in range(0, num_pmids_p_epost_cur, num_pmids_p_efetch):
                desc = self.pat.format(Q=querykey_cur, S=start, **pat_val)
                pmids_exp = pmids_cur[start:start+num_pmids_p_efetch]
                rsp_txt = self._run_efetch(start, querykey_cur, pmids_exp, desc, **efetch_params)
                if rsp_txt is not None:
                   pass 

    def _run_efetch(self, start, querykey, pmids_exp, desc, **params):
        """Get text from EFetch response"""
        rsp_dct = self.run_req('efetch', retstart=start, query_key=querykey, **params)
        rsp_txt = rsp_dct['data'].decode('utf-8')
        err_txt = self._chk_error_str(rsp_txt)
        if err_txt is not None:
            print('\nURL: {URL}\n{DESC}\n**ERROR: {ERR}'.format(
                ERR=err_txt, DESC=desc, URL=rsp_dct['url']))
            return None
        pmids_downloaded = [int(i) for i in re.findall(r'PMID-\s*(\d+)', rsp_txt)]
        print(desc, pmids_downloaded, pmids_exp)
        assert pmids_downloaded == pmids_exp, (desc, pmids_downloaded, pmids_exp)
        return rsp_txt

    @staticmethod
    def _get_str_post_fetch(num_pmids_p_epost, num_pmids_p_efetch, querykey, start):
        """Get a string summarizing current EPost and EFetch"""
        return 'PMIDs/epost={P} PMIDs/efetch={F} querykey({Q}) start({S})'.format(
            P=num_pmids_p_epost, F=num_pmids_p_efetch, Q=querykey, S=start)


    @staticmethod
    def _chk_error_str(text):
        """Check if data was correctly downloaded"""
        p0_err = text.find('<ERROR>')
        if p0_err < 0:
            return None
        msg = text[p0_err+7:]
        p1_err = msg.find('</ERROR>')
        return msg[:p1_err]

    @staticmethod
    def _get_pmid_nt_list(pmids, force_download, dir_pubmed):
        """Get list of PubMed entries: Title, abstract, authors, journal, MeSH"""
        nts = []
        ntobj = cx.namedtuple('Nt', 'PMID fout_pubmed fout_exists')
        for pmid in pmids:
            # Get filename, pPMID.txt
            fout_pubmed = os.path.join(dir_pubmed, 'p{PubMed}.txt'.format(PubMed=pmid))
            fout_exists = os.path.exists(fout_pubmed)
            if not fout_exists or force_download:
                ntd = ntobj(PMID=pmid, fout_pubmed=fout_pubmed, fout_exists=fout_exists)
                nts.append(ntd)
        return nts


# Copyright (C) 2016-present DV Klopfenstein. All rights reserved.
