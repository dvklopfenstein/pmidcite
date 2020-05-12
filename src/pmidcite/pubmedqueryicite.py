"""Run PubMed user query and download PMIDs. Run iCite on PMIDs. Write text file."""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
from collections import namedtuple
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
        self.pmidcite = PmidCite()
        cfg = self.pmidcite.cfgparser
        self.pubmed = PubMed(
            email=cfg.get_email(),
            apikey=cfg.get_apikey(),
            tool=cfg.get_tool())

    def run(self, lst, dnld_idx=None):
        """Give an list of tuples: Query PubMed for PMIDs. Download iCite, given PMIDs"""
        # Download PMIDs and NIH's iCite for only one PubMed query
        nts = self.get_nts_g_list(lst)
        if dnld_idx is not None:
            ntd = nts[dnld_idx]
            self.querypubmed_runicite(ntd.filename, ntd.pubmed_query)
        # Download PMIDs and NIH's iCite for all PubMed queries
        else:
            for ntd in nts:
                self.querypubmed_runicite(ntd.filename, ntd.pubmed_query)

    def querypubmed_runicite(self, fout_pat, query):
        """Given a user query, return PMIDs. Then run NIH's iCite"""
        # 1) Query PubMed and download PMIDs
        pmids = self.pubmed.dnld_query_pmids(query)
        dct = self.pmidcite.cfgparser.cfgparser['pmidcite']
        fout_pmids = os.path.join(dct['dir_pmids'], fout_pat.format(PRE='pmids'))
        fout_icite = os.path.join(dct['dir_icite'], fout_pat.format(PRE='icite'))
        # 2) Write PubMed PMIDs into a simple text file, one PMID per line
        if fout_pmids != fout_icite:
            wr_pmids(fout_pmids, pmids)
        # 3) Run NIH's iCite on the PMIDs and write the results into a file
        self.wr_icite(fout_icite, pmids)

    def wr_icite(self, fout_icite, pmids):
        """Run PMIDs in iCite and print results into a file"""
        # Get NIHiCiteDownloader object
        dnldr = self.pmidcite.get_icitedownloader(
            self.force_dnld, no_references=False, prt_icitepy=self.prt_icitepy)
        pmid2paper = dnldr.get_pmid2paper(pmids, self.verbose, self.pmid2note, prt=None)
        dnldr.wr_papers(fout_icite, force_overwrite=True, pmid2icitepaper=pmid2paper)

    @staticmethod
    def get_nts_g_list(lst):
        """Turn a list iof tuple strings into a list of namedtuples"""
        nto = namedtuple('Nt', 'filename pubmed_query')
        return [nto._make(t) for t in lst]


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
