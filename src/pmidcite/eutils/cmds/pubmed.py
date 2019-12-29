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

    params = {
        'db': 'pubmed',
        'rettype': 'medline',
        'retmode': 'text',
    }

    def __init__(self, email, apikey, tool):
        super(PubMed, self).__init__(email, apikey, tool)

    def dnld_wr1_per_pmid(self, pmids, force_download=False, dir_pubmed="."):
        """Download and write file one PubMed entry per PMID"""
        pmid_nt_list = self._get_pmid_nt_list(pmids, force_download, dir_pubmed)
        for ntd in pmid_nt_list:
            print('IIIIIIIIIIIIIIIIIIIII {PMID:12} {NT}'.format(PMID=ntd.PMID, NT=ntd))
        self._dnld_pubmed(pmid_nt_list)

    # pmids num_pmids_p_epost num_pmids_p_efetch  ->  num_efetches
    # ----- ----------------- ------------------      ------------
    #     5                 2                  3                 3
    #     5                 2                  1                 5

    #def _dnld_pubmed(self, pmid_nt_list, num_pmids_p_efetch=1, num_pmids_p_epost=2):
    def _dnld_pubmed(self, pmid_nt_list, num_pmids_p_efetch=1, num_pmids_p_epost=2):
        """Download and write PubMed entries, given PMIDs and assc info"""
        # retstart=0&retmax=1&query_key=1
        # retstart=1&retmax=1&query_key=1
        # retstart=0&retmax=1&query_key=2
        # [30066183, 31196170, 30854042]
        pmids_all = [nt.PMID for nt in pmid_nt_list]
        num_pmids = len(pmids_all)
        # post: {'querykey': 1, 'webenv': 'NCID_1_1510..., '}

        # DEFN num_pmids_p_epost: number of PMIDs in each epost querykey
        post = self.epost('pubmed', pmids_all, step=num_pmids_p_epost)
        querykey_max = post['querykey']

        # post = {'querykey':3, 'webenv':'NCID_1_98788585_130.14.18.97_9001_1577436192_2019651544_0MetA0_S_MegaStore'}
        params = dict(self.params)
        params['webenv'] = post['webenv']
        params['retmax'] = num_pmids_p_efetch
        num_pmids_p_epost_cur = num_pmids_p_epost
        for querykey_cur, pmids_cur in enumerate(post['qkey2ids'], 1):
            if querykey_cur == querykey_max:
                num_pmids_p_epost_cur = num_pmids%num_pmids_p_epost
            print('QUERYKEY ----------- {N} PMIDs'.format(N=num_pmids), querykey_cur)
            for start in range(0, num_pmids_p_epost_cur, num_pmids_p_efetch):
                print('QUERYKEY({Q}) START({S}) ----------'.format(Q=querykey_cur, S=start))
                rsp_dct = self.run_req('efetch', retstart=start, query_key=querykey_cur, **params)
                rsp_dct['data'] = rsp_dct['data'].decode('utf-8')
                err_txt = self._chk_error_str(rsp_dct['data'])
                if err_txt is not None:
                    print('\nURL: {URL}\n\n**ERROR: {ERR}'.format(ERR=err_txt, URL=rsp_dct['url']))
                    return
                print('RRRRRRRRRRRRRRRRRRRRRRRRR', re.findall(r'(PMID-\s*\d+)', rsp_dct['data']))

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
