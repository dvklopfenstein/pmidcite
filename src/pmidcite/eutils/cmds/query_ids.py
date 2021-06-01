"""Text query finds database UIDs for later use in ESummary, EFetch or ELink"""
# https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch

__copyright__ = "Copyright (C) 2020-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

import sys
from pmidcite.eutils.cmds.base import EntrezUtilities


class QueryIDs(EntrezUtilities):
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

    def __init__(self, email, apikey, tool, prt=sys.stdout):
        super(QueryIDs, self).__init__(email, apikey, tool, prt)

    def dnld_query_ids(self, query, database, num_ids_p_epost=10):
        """Searches a NCBI database for a user query, writes resulting entries into one file."""
        rsp_dct = self.get_query_rsp(query, database, num_ids_p_epost)
        return self.get_ids(rsp_dct, query, database, num_ids_p_epost)

    def get_query_rsp(self, query, database, num_ids_p_epost=10):
        """Searches a NCBI database for a user query, writes resulting entries into one file."""
        # 1) Query PubMed/Protein/etc. Get first N (num_ids_p_epost) of the total PMIDs
        rsp_dct = self.query(database, query, retmax=num_ids_p_epost)
        if rsp_dct is None:
            if self.log:
                self.log.write('No {DB} entries found: {Q}\n'.format(DB=database, Q=query))
                self.log.flush()
            return []
        if rsp_dct and self.log:
            self.log.write('{N:6,} IDs FOR {DB} QUERY({Q})\n'.format(
                DB=database, N=rsp_dct['count'], Q=query))
            self.log.flush()
        return rsp_dct

    def get_ids(self, rsp_dct, query, database, num_ids_p_epost=10):
        """Download PMIDs, N (num_ids_p_epost) at a time"""
        ## print('WWWWWWWWWWWWWWWWWWWWW pmidcite/eutils/cmds/query_ids.py', rsp_dct)
        if not rsp_dct:
            return []
        ids = list(rsp_dct['idlist'])
        kws_p = {
            'webenv': rsp_dct['webenv'],
            'querykey': rsp_dct['querykey'],
            'retmax': num_ids_p_epost,
        }
        tot_ids = rsp_dct['count']
        ## print('WWWWWWWWWWWWWWWWWWWWWWWW', kws_p)
        for retnum in range(1, self._get_num_querykeys(num_ids_p_epost, tot_ids)):
            rsp_dct = self.query(database, query, retstart=num_ids_p_epost*retnum, **kws_p)
            if rsp_dct:
                ids.extend(rsp_dct['idlist'])
        assert tot_ids == len(set(ids)), 'PMIDS EXP({E}) ACT({A})'.format(
            E=tot_ids, A=len(set(ids)))
        return ids

    @staticmethod
    def _get_num_querykeys(num_ids_p_epost, num_pmids):
        """Get the number of querykeys necessary to process all PMIDs"""
        num_querykeys = num_pmids//num_ids_p_epost
        if num_pmids%num_ids_p_epost != 0:
            num_querykeys += 1
        return num_querykeys

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


# Copyright (C) 2020-present, DV Klopfenstein. All rights reserved.
