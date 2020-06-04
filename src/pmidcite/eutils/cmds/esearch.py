"""Text query finds database UIDs for later use in ESummary, EFetch or ELink"""
# https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch

__copyright__ = "Copyright (C) 2020-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

import sys
from pmidcite.eutils.cmds.base import EntrezUtilities


class ESearch(EntrezUtilities):
    """Text query finds database UIDs for later use in ESummary, EFetch or ELink"""

    # https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
    exp_params = {
        # Required Parameters:
        'db',
        'term',
        # Optional Parameters - History Server
        'usehistory',
        'webenv',
        'querykey',
        # Optional Parameters – Retrieval
        'retstart',
        'retmax',
        'rettype',
        'retmode',
        'sort',
        'field',
        'idtype',
        # Optional Parameters – Dates
        'datetype',
        'reldate',
        'mindate',
        'maxdate',
    }
    pat = 'IDs/epost={P} IDs/efetch={F} querykey({Q} of {Qmax}) start({S})'


    def __init__(self, email, apikey, tool, prt=sys.stdout):
        super(ESearch, self).__init__(email, apikey, tool, prt)

    def esearch_ids(self, database, query, **return_params):
        """Get IDs using ESearch"""
        # Run query to find matching IDs. Get webenv for ID list
        rsp_0 = self.query(database, query, **return_params)
        idlist = list(rsp_0['idlist'])
        webenv = rsp_0['webenv']
        retmax = rsp_0['retmax']
        #self._prt_rsp(rsp_0, 0)
        num_iter = self._get_num_iterations(rsp_0['count'], rsp_0['retmax'])
        for querykey_cur in range(1, num_iter):
            rsp_i = self.query(
                database, query, WebEnv=webenv, retstart=querykey_cur*retmax, retmax=retmax)
            idlist.extend(rsp_i['idlist'])
            # self._prt_rsp(rsp_i, querykey_cur)
        print('{N} of {C} {DB} IDs FOR QUERY({Q})'.format(
            N=len(idlist), DB=database, C=rsp_0['count'], Q=query))
        ## print(len(set(idlist)))
        return idlist

    def query(self, database, query, **esearch):
        """Text query finds database UIDs for later use in ESummary, EFetch or ELink"""
        kws_exp = self.exp_params.difference({'db', 'term', 'rettype', 'usehistory', 'retmode'})
        kws_act = {k:v for k, v in esearch.items() if k in kws_exp}
        # Returns:
        #    count
        #    retmax
        #    retstart
        #    querykey
        #    webenv
        #    idlist
        #    translationset
        #    translationstack
        #    querytranslation
        dct = self.run_eutilscmd(
            'esearch',
            db=database,
            term=query,
            rettype='uilist',
            # retmax=esearch.get('retmax', 10),
            usehistory="y", # NCBI prefers we use history(QueryKey, WebEnv) for next acess
            retmode='json',
            **kws_act)
        if dct is not None and 'idlist' in dct and dct['idlist']:
            if database in {'pubmed',}:
                dct['idlist'] = [int(n) for n in dct['idlist']]
            for fldname in {'count', 'retmax'}:
                dct[fldname] = int(dct[fldname])
            return dct
        return None

    @staticmethod
    def _prt_rsp(rsp_dct, idx):
        """Print key-value pairs in a response dict"""
        for key, val in rsp_dct.items():
            if key == 'idlist':
                print('{I} FFFFFFFFFFFF {K:20} {V}'.format(I=idx, K=key, V=len(val)))
            elif key not in 'translationstack':
                print('{I} FFFFFFFFFFFF {K:20} {V}'.format(I=idx, K=key, V=val))


# Copyright (C) 2020-present, DV Klopfenstein. All rights reserved.
