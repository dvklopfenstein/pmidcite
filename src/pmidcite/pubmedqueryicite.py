"""Run PubMed user query and download PMIDs. Run iCite on PMIDs. Write text file."""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.cli.utils import wr_pmids
from pmidcite.icite.run import PmidCite


class PubMedQueryToICite:
    """Run PubMed user query and download PMIDs. Run iCite on PMIDs. Write text file."""

    def __init__(self, force_dnld, verbose=False):
        self.force_dnld = force_dnld
        self.verbose = verbose
        self.pmidcite = PmidCite()
        cfg = self.pmidcite.cfgparser
        self.pubmed = PubMed(
            email=cfg.get_email(),
            apikey=cfg.get_apikey(),
            tool=cfg.get_tool())

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
        self.wr_icite(fout_icite, pmids, self.force_dnld)

    def wr_icite(self, fout_icite, pmids, pmid2note=None):
        """Run PMIDs in iCite and print results into a file"""
        dnldr = self.pmidcite.get_icitedownloader(
            self.force_dnld, no_references=False, prt=None)
        pmid2ntpaper = dnldr.get_pmid2paper(pmids, self.verbose, pmid2note)
        dnldr.wr_papers(fout_icite, True, pmid2ntpaper)


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
