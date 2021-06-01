"""Run PubMed user query and download PMIDs. Run iCite on PMIDs. Write text file."""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
from collections import namedtuple
from pmidcite.cfg import get_cfgparser
from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.cli.utils import wr_pmids
from pmidcite.icite.run import PmidCite


class PubMedQueryToICite:
    """Run PubMed user query and download PMIDs. Run iCite on PMIDs. Write text file."""

    def __init__(self, force_dnld, verbose=True, pmid2note=None, prt_icitepy=None):
        self.force_dnld = force_dnld
        self.verbose = verbose
        self.pmid2note = {} if pmid2note is None else pmid2note
        # Setting prt_icitepy to sys.stdout causes messages: WROTE: ./icite/p31898878.py
        self.prt_icitepy = prt_icitepy
        self.pmidcite = PmidCite(get_cfgparser())
        cfg = self.pmidcite.cfgparser
        self.pubmed = PubMed(
            email=cfg.get_email(),
            apikey=cfg.get_apikey(),
            tool=cfg.get_tool())
        self._chk_dirs()

    def run(self, lst, dnld_idxs=None):
        """Give an list of tuples: Query PubMed for PMIDs. Download iCite, given PMIDs"""
        # Download PMIDs and NIH's iCite for only one PubMed query
        nts = self.get_nts_g_list(lst)
        if dnld_idxs is not None:
            for idx in dnld_idxs:
                ntd = nts[idx]
                self.querypubmed_runicite(ntd.filename, ntd.pubmed_query)
        # Download PMIDs and NIH's iCite for all PubMed queries
        else:
            for ntd in nts:
                ## print('QQQQQQQQQQQQQQQQ pmidcite/pubmedqueryicite.py', ntd.pubmed_query)
                self.querypubmed_runicite(ntd.filename, ntd.pubmed_query)

    def querypubmed_runicite(self, fout_pat, query):
        """Given a user query, return PMIDs. Then run NIH's iCite"""
        # 1) Query PubMed and download PMIDs
        pmids = self.pubmed.dnld_query_pmids(query)
        fout_pmids = os.path.join(self.get_dir_pmids(), fout_pat.format(PRE='pmids'))
        fout_icite = os.path.join(self.get_dir_icite(), fout_pat.format(PRE='icite'))
        # 2) Write PubMed PMIDs into a simple text file, one PMID per line
        if fout_pmids != fout_icite:
            if pmids:
                wr_pmids(fout_pmids, pmids)
            else:
                print('  0 PMIDs: NOT WRITING {TXT}'.format(TXT=fout_pmids))
        # 3) Run NIH's iCite on the PMIDs and write the results into a file
        if pmids:
            self.wr_icite(fout_icite, pmids)

    def get_dir_pmids(self):
        """Get directory to store lists of PMIDs"""
        return self.pmidcite.cfgparser.cfgparser['pmidcite']['dir_pmids']

    def get_dir_icite(self):
        """Get directory to store lists of PMIDs"""
        return self.pmidcite.cfgparser.cfgparser['pmidcite']['dir_icite']

    def wr_icite(self, fout_icite, pmids, grouperobj=None):
        """Run PMIDs in iCite and print results into a file"""
        # Get NIHiCiteDownloader object
        dnldr = self.pmidcite.get_icitedownloader(
            self.force_dnld,
            grouperobj,
            no_references=False,
            prt_icitepy=self.prt_icitepy)
        pmid2paper = dnldr.get_pmid2paper(pmids, self.verbose, self.pmid2note)
        dnldr.wr_papers(fout_icite, pmid2icitepaper=pmid2paper, force_overwrite=True)

    @staticmethod
    def get_nts_g_list(lst):
        """Turn a list iof tuple strings into a list of namedtuples"""
        nto = namedtuple('Nt', 'filename pubmed_query')
        return [nto._make(t) for t in lst]

    @staticmethod
    def get_index(argv):
        """Get the index of the pubmed query to run"""
        # If no argument was provided, run the last query in the list
        if len(argv) == 1:
            return [-1]
        if argv[1] == 'all':
            return None
        return [int(n) for n in argv[1:] if n.lstrip('-').isdigit()]

    def _chk_dirs(self):
        """Check output directories for existance"""
        not_exist = set()
        dct = self.pmidcite.cfgparser.cfgparser['pmidcite']
        if not os.path.exists(dct['dir_pmids']):
            not_exist.add(dct['dir_pmids'])
        if not os.path.exists(dct['dir_icite']):
            not_exist.add(dct['dir_icite'])
        if not_exist:
            for dirname in not_exist:
                print('**FATAL: NO DIR: {DIR}'.format(DIR=dirname))
            sys.exit(1)


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
