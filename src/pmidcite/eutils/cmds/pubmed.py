"""Given PMIDs, download PubMed records containing"""

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2016-present DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import os
import sys
import collections as cx
import re
from pmidcite.eutils.cmds.base import EntrezUtilities
from pkgbib.eutils.esearch import ESearch


class PubMed(EntrezUtilities):
    """Fetch and write text"""

    medline_text = {
        'rettype': 'medline',
        'retmode': 'text',
    }
    pat = 'PMIDs/epost={P} PMIDs/efetch={F} querykey({Q} of {Qmax}) start({S})'

    def __init__(self, email, apikey, tool):
        super(PubMed, self).__init__(email, apikey, tool)
        self.esearch = ESearch(email, apikey, tool)

    def dnld_query(self, fout_entrez, query, num_ids_p_epost=10, prt=sys.stdout):
        """Searches an PubMed for a user query, writes resulting entries into one file."""
        # 1) Query PubMed. Get first N (num_ids_p_epost) of the total PMIDs
        rsp_dct = self.esearch.query('pubmed', query, retmax=num_ids_p_epost)
        tot_pmids = rsp_dct['count']
        print('DDDDDDDDDDDDDDDDDDDDDDDDDDDD', rsp_dct)
        if rsp_dct and prt:
            prt.write('{N:5,} PMIDs FOR QUERY({Q})\n'.format(N=tot_pmids, Q=query))
        # 2) Set EFetch params
        efetch_params = dict(self.medline_text)
        efetch_params['webenv'] = rsp_dct['webenv']
        efetch_params['retmax'] = num_ids_p_epost  # num IDs epost == num IDs efetch
        qkey2ids = [None for _ in range(self._get_num_querykeys(num_ids_p_epost, tot_pmids))]
        qkey2ids[0] = rsp_dct['idlist']
        ef_dct = {
            'querykey': rsp_dct['querykey'],
            'num_ids_p_epost': num_ids_p_epost,
            'qkey2ids': qkey2ids,
        }
        # 3) Get number of times we run efetch
        efetch_idxs = self._get_efetch_indices(ef_dct, num_ids_p_epost, tot_pmids)
        for e in efetch_idxs:
            print('EEEEEEEEEEEEEEEEEEEEEEEE', e)
        self._dnld_wr_all(fout_entrez, efetch_idxs, efetch_params)

    def _dnld_wr_all(self, fout_pubmed, efetch_idxs, efetch_params):
        """Download and write all PMIDs PubMed text entries into one file"""
        if os.path.exists(fout_pubmed):
            os.system('rm {FILE}'.format(FILE=fout_pubmed))
        if not efetch_idxs:
            return
        for desc, start, pmids_exp, querykey_cur in efetch_idxs:
            rsp_txt = self._run_efetch(start, querykey_cur, pmids_exp, desc, **efetch_params)
            if rsp_txt is not None:
                with open(fout_pubmed, 'a') as prt:
                    prt.write(rsp_txt)
        print('  WROTE: {FILE}'.format(FILE=fout_pubmed))

    def _dnld_query(self, query):
        """Searches an NCBI database for a user search term, returns NCBI IDs."""
        dct = self.run_eutilscmd('esearch', db='pubmed', term=query, retmode='json')
        return dct

    @staticmethod
    def _get_num_querykeys(num_ids_p_epost, num_pmids):
        """Get the number of querykeys necessary to process all PMIDs"""
        num_querykeys = num_pmids//num_ids_p_epost
        if num_pmids%num_ids_p_epost != 0:
            num_querykeys += 1
        return num_querykeys

    def dnld_wr1_per_pmid(self, pmid_nt_list, num_ids_p_epost=10):
        """Download and write one PubMed text file entry per PMID"""
        # Get filenames to store PubMed entry information, one PMID per file
        # Use function, get_pmid_nt_list, to get nts w/flds: PMID fout_pubmed fout_exists
        if not pmid_nt_list:
            return
        # Run EPost
        pmids = [nt.PMID for nt in pmid_nt_list]
        # pylint: disable=line-too-long
        efetch_idxs, efetch_params = self.epost_ids(pmids, 'pubmed', num_ids_p_epost, 1, **self.medline_text)
        self._dnld_wr1_per_pmid(efetch_idxs, efetch_params, pmid_nt_list)

    def epost_ids(self, ids, database, num_ids_p_epost, retmax, **medline_text):
        """Post IDs using EPost"""
        epost_rsp = self.epost(database, ids, num_ids_p_epost=num_ids_p_epost)
        # Set EFetch params
        efetch_params = dict(medline_text)
        efetch_params['webenv'] = epost_rsp['webenv']
        efetch_params['retmax'] = retmax  # num_ids_p_efetch
        # Run EFetches
        efetch_idxs = self._get_efetch_indices(epost_rsp, retmax, len(ids))
        #efetch_idxs = self._get_efetch_indices(epost_rsp, retmax, epost_rsp['count'])
        return efetch_idxs, efetch_params

    def _dnld_wr1_per_pmid(self, efetch_idxs, efetch_params, pmid_nt_list):
        """Download and write one PMID PubMed entry into one text file"""
        pmid2nt = {nt.PMID:nt for nt in pmid_nt_list}
        for desc, start, pmids_exp, querykey_cur in efetch_idxs:
            rsp_txt = self._run_efetch(start, querykey_cur, pmids_exp, desc, **efetch_params)
            if rsp_txt is not None:
                assert len(pmids_exp) == 1
                ntd = pmid2nt[pmids_exp[0]]
                with open(ntd.fout_pubmed, 'w') as prt:
                    prt.write(rsp_txt)
                    print('  {WROTE}: {TXT}'.format(
                        WROTE='WROTE' if not ntd.fout_exists else 'UPDATED',
                        TXT=ntd.fout_pubmed))

    def _get_efetch_indices(self, epost_rsp, num_pmids_p_efetch, num_pmids):
        """Get EFetech list of: querykey_cur, pmids_cur, start"""
        # pmids num_pmids_p_epost num_pmids_p_efetch  ->  num_efetches
        # ----- ----------------- ------------------      ------------
        #     5                 2                  3                 3
        #     5                 2                  1                 5
        nts = []
        querykey_max = epost_rsp['querykey']
        num_pmids_p_epost_cur = epost_rsp['num_ids_p_epost']
        pat_val = {
            'P':epost_rsp['num_ids_p_epost'],
            'F':num_pmids_p_efetch,
            'Qmax':epost_rsp['querykey']}
        for querykey_cur, pmids_cur in enumerate(epost_rsp['qkey2ids'], 1):
            if querykey_cur == querykey_max:
                num_pmids_p_epost_cur = num_pmids%epost_rsp['num_ids_p_epost']
            for start in range(0, num_pmids_p_epost_cur, num_pmids_p_efetch):
                desc = self.pat.format(Q=querykey_cur, S=start, **pat_val)
                pmids_exp = pmids_cur[start:start+num_pmids_p_efetch] if pmids_cur is not None else None
                nts.append([desc, start, pmids_exp, querykey_cur])
        return nts

    def _run_efetch(self, start, querykey, pmids_exp, desc, **params):
        """Get text from EFetch response"""
        rsp_dct = self.run_req('efetch', retstart=start, query_key=querykey, db='pubmed', **params)
        if rsp_dct is None:
            print('\n{DESC}\n**ERROR: DATA is None'.format(DESC=desc))
            return None
        rsp_txt = rsp_dct['data'].decode('utf-8')
        err_txt = self._chk_error_str(rsp_txt)
        if err_txt is not None:
            print('\nURL: {URL}\n{DESC}\n**ERROR: {ERR}'.format(
                ERR=err_txt, DESC=desc, URL=rsp_dct['url']))
            return None
        pmids_downloaded = [int(i) for i in re.findall(r'PMID-\s*(\d+)', rsp_txt)]
        #print(desc, pmids_downloaded, pmids_exp)
        if pmids_exp:
            assert pmids_downloaded == pmids_exp, '{TXT}\nDESC: {DESC}\nDL[{D}]: {DL}\nEXP[{L}]: {EXP}'.format(
                TXT=rsp_txt, DESC=desc, D=len(pmids_downloaded),DL=pmids_downloaded, EXP=pmids_exp, L=len(pmids_exp))
        return rsp_txt

    @staticmethod
    def _get_str_post_fetch(num_pmids_p_epost, num_pmids_p_efetch, querykey, start):
        """Get a string summarizing current EPost and EFetch"""
        return 'IDs/epost={P} IDs/efetch={F} querykey({Q}) start({S})'.format(
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
    def get_pmid_nt_list(pmids, force_download, dir_pubmed):
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
            else:
                print('**NOTE: EXISTS: {PUBMED}'.format(PUBMED=fout_pubmed))
        return nts


# Copyright (C) 2016-present DV Klopfenstein. All rights reserved.
