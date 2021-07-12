"""Text query finds database UIDs for later use in ESummary, EFetch or ELink"""
# https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch

__copyright__ = "Copyright (C) 2020-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

import os
import sys
import collections as cx
from pmidcite.eutils.cmds.base import EntrezUtilities
from pmidcite.eutils.cmds.query_ids import QueryIDs


class ESearch(EntrezUtilities):
    """Text query finds database UIDs for later use in ESummary, EFetch or ELink"""

    #### # https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
    #### exp_params = {
    ####     # Required Parameters:
    ####     'db',
    ####     'term',
    ####     # Optional Parameters - History Server
    ####     'usehistory',
    ####     'webenv',
    ####     'querykey',
    ####     # Optional Parameters – Retrieval
    ####     'retstart',
    ####     'retmax',
    ####     'rettype',
    ####     'retmode',
    ####     'sort',
    ####     'field',
    ####     'idtype',
    ####     # Optional Parameters – Dates
    ####     'datetype',
    ####     'reldate',
    ####     'mindate',
    ####     'maxdate',
    #### }
    #### pat = 'IDs/epost={P} IDs/efetch={F} querykey({Q} of {Qmax}) start({S})'


    def __init__(self, email, apikey, tool, prt=sys.stdout):
        super(ESearch, self).__init__(email, apikey, tool, prt)
        self.queryids = QueryIDs(email, apikey, tool, prt)

    def dnld_query_pmids(self, query, database, num_ids_p_epost=10):
        """Searches a NCBI database for a user query, writes resulting entries into one file."""
        return self.queryids.dnld_query_ids(query, database, num_ids_p_epost)
        #### # 1) Query PubMed/Protein/etc. Get first N (num_ids_p_epost) of the total PMIDs
        #### rsp_dct = self.query(database, query, retmax=num_ids_p_epost)
        #### if rsp_dct is None:
        ####     if self.log:
        ####         self.log.write('No {DB} entries found: {Q}\n'.format(DB=database, Q=query))
        ####         self.log.flush()
        ####     return []
        #### tot_ids = rsp_dct['count']
        #### ids = list(rsp_dct['idlist'])
        #### if rsp_dct and self.log:
        ####     self.log.write('{N:6,} IDs FOR {DB} QUERY({Q})\n'.format(DB=database, N=tot_ids, Q=query))
        ####     self.log.flush()
        #### # 2) Continue to download PMIDs, N (num_ids_p_epost) at a time
        #### kws_p = {
        ####     'webenv': rsp_dct['webenv'],
        ####     'querykey': rsp_dct['querykey'],
        ####     'retmax': num_ids_p_epost,
        #### }
        #### for retnum in range(1, self._get_num_querykeys(num_ids_p_epost, tot_ids)):
        ####     rsp_dct = self.query(database, query, retstart=num_ids_p_epost*retnum, **kws_p)
        ####     if rsp_dct:
        ####         ids.extend(rsp_dct['idlist'])
        #### assert tot_ids == len(set(ids)), 'PMIDS EXP({E}) ACT({A})'.format(
        ####     E=tot_ids, A=len(set(ids)))
        #### return ids

    def dnld_wr1_per_id(self, database, efetch_idxs, efetch_params, pmid_nt_list):
        """Download and write one PMID PubMed entry into one text file"""
        if not pmid_nt_list:
            return {}
        pmid2nt = {nt.PMID:nt for nt in pmid_nt_list}
        for desc, start, pmids_exp, querykey_cur in efetch_idxs:
            rsp_txt = self._run_efetch(
                database, start, querykey_cur, pmids_exp, desc, **efetch_params)
            if rsp_txt is not None:
                assert len(pmids_exp) == 1
                pmid = pmids_exp[0]
                if pmid in pmid2nt:
                    ntd = pmid2nt[pmid]
                    if ntd.download:
                        ## print('NNNNNNNNNNNNNNN', ntd)
                        with open(ntd.file_pubmed, 'w') as prt:
                            prt.write(rsp_txt)
                            print('  {WROTE}: {TXT}'.format(
                                WROTE='WROTE' if not ntd.file_exists else 'UPDATED',
                                TXT=ntd.file_pubmed))
                    else:
                        print('**WARNING: NOT DOWNLOADING: {PMID}'.format(PMID=pmid))
        return pmid2nt

    #### @staticmethod
    #### def _get_num_querykeys(num_ids_p_epost, num_pmids):
    ####     """Get the number of querykeys necessary to process all PMIDs"""
    ####     num_querykeys = num_pmids//num_ids_p_epost
    ####     if num_pmids%num_ids_p_epost != 0:
    ####         num_querykeys += 1
    ####     return num_querykeys

    def esearch_ids(self, database, query, **return_params):
        """Get IDs using ESearch"""
        # Run query to find matching IDs. Get webenv for ID list
        rsp_0 = self.queryids.query(database, query, **return_params)
        idlist = list(rsp_0['idlist'])
        webenv = rsp_0['webenv']
        retmax = rsp_0['retmax']
        #self._prt_rsp(rsp_0, 0)
        num_iter = self._get_num_iterations(rsp_0['count'], rsp_0['retmax'])
        for querykey_cur in range(1, num_iter):
            rsp_i = self.queryids.query(
                database, query, WebEnv=webenv, retstart=querykey_cur*retmax, retmax=retmax)
            idlist.extend(rsp_i['idlist'])
            # self._prt_rsp(rsp_i, querykey_cur)
        print('{N} of {C} {DB} IDs FOR QUERY({Q})'.format(
            N=len(idlist), DB=database, C=rsp_0['count'], Q=query))
        ## print(len(set(idlist)))
        return idlist

    #### def query(self, database, query, **esearch):
    ####     """Text query finds database UIDs for later use in ESummary, EFetch or ELink"""
    ####     kws_exp = self.exp_params.difference({'db', 'term', 'rettype', 'usehistory', 'retmode'})
    ####     kws_act = {k:v for k, v in esearch.items() if k in kws_exp}
    ####     # Returns:
    ####     #    count
    ####     #    retmax
    ####     #    retstart
    ####     #    querykey
    ####     #    webenv
    ####     #    idlist
    ####     #    translationset
    ####     #    translationstack
    ####     #    querytranslation
    ####     dct = self.run_eutilscmd(
    ####         'esearch',
    ####         db=database,
    ####         term=query,
    ####         rettype='uilist',
    ####         # retmax=esearch.get('retmax', 10),
    ####         usehistory="y", # NCBI prefers we use history(QueryKey, WebEnv) for next acess
    ####         retmode='json',
    ####         **kws_act)
    ####     if dct is not None and 'idlist' in dct and dct['idlist']:
    ####         if database in {'pubmed',}:
    ####             dct['idlist'] = [int(n) for n in dct['idlist']]
    ####         for fldname in {'count', 'retmax'}:
    ####             dct[fldname] = int(dct[fldname])
    ####         return dct
    ####     return None

    @staticmethod
    def _prt_rsp(rsp_dct, idx):
        """Print key-value pairs in a response dict"""
        for key, val in rsp_dct.items():
            if key == 'idlist':
                print('{I} FFFFFFFFFFFF {K:20} {V}'.format(I=idx, K=key, V=len(val)))
            elif key not in 'translationstack':
                print('{I} FFFFFFFFFFFF {K:20} {V}'.format(I=idx, K=key, V=val))

    @staticmethod
    def get_pmid_nt_list(ids, database, force_download, dir_pubmed, pmid2name=None):
        """Get list of database entries. PubMed ex: Title, abstract, authors, journal, MeSH"""
        nts = []
        ntobj = cx.namedtuple('Nt', 'PMID file_pubmed file_exists download')
        for id_val in ids:
            name = pmid2name[id_val] if pmid2name and id_val in pmid2name else id_val
            # Get filename, pubmed_PMID.txt
            file_db = os.path.join(dir_pubmed, '{DB}_{ID}.txt'.format(DB=database, ID=name))
            file_exists = os.path.exists(file_db)
            download = not file_exists or force_download
            ntd = ntobj(
                PMID=id_val,
                file_pubmed=file_db,
                file_exists=file_exists,
                download=download)
            nts.append(ntd)
            if not download:
                print('**NOTE: EXISTS: {TXT}'.format(TXT=file_db))
        return nts


# Copyright (C) 2020-present, DV Klopfenstein. All rights reserved.
