"""Run PubMed user query and download PMIDs. Run iCite on PMIDs. Write text file."""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from pmidcite.cfg import get_cfgparser
from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.cli.utils import wr_pmids
from pmidcite.icite.downloader import get_downloader


class PubMedQueryToICite:
    """Run PubMed user query and download PMIDs. Run iCite on PMIDs. Write text file."""

    def __init__(self, force_dnld, verbose=True, pmid2note=None):
        self.force_dnld = force_dnld
        self.verbose = verbose
        self.pmid2note = {} if pmid2note is None else pmid2note
        self.cfg = get_cfgparser()
        self.pubmed = PubMed(
            email=self.cfg.get_email(),
            apikey=self.cfg.get_apikey(),
            tool=self.cfg.get_tool())

    def run(self, fout_query, dnld_idxs=None):
        """Give an list of tuples: Query PubMed for PMIDs. Download iCite, given PMIDs"""
        # Download PMIDs and NIH's iCite for only one PubMed query
        nts = self.get_nts_g_list(fout_query)
        if dnld_idxs is not None:
            for idx in dnld_idxs:
                ntd = nts[idx]
                self._querypubmed_runicite(ntd.filename, ntd.pubmed_query)
        # Download PMIDs and NIH's iCite for all PubMed queries
        else:
            for ntd in nts:
                self._querypubmed_runicite(ntd.filename, ntd.pubmed_query)

    def _querypubmed_runicite(self, filename, query):
        """Given a user query, return PMIDs. Then run NIH's iCite"""
        # 1) Query PubMed and download PMIDs
        pmids = self.pubmed.dnld_query_pmids(query)
        fout_pmids = self.cfg.get_fullname_pmids(filename)
        fout_icite = self.cfg.get_fullname_icite(filename)
        # 2) Write PubMed PMIDs into a simple text file, one PMID per line
        if fout_pmids != fout_icite:
            if pmids:
                wr_pmids(fout_pmids, pmids)
            else:
                print('  0 PMIDs: NOT WRITING {TXT}'.format(TXT=fout_pmids))
        # 3) Run NIH's iCite on the PMIDs and write the results into a file
        if pmids:
            self._wr_icite(fout_icite, pmids)

    def _wr_icite(self, fout_icite, pmids):
        """Run PMIDs in iCite and print results into a file"""
        cfg = self.cfg
        dnldr = get_downloader(
            details_cites_refs=None,
            nih_grouper=cfg.get_nihgrouper(),
            dir_icite_py=cfg.get_dir_icite_py(),
            force_download=self.force_dnld)
        pmid2paper = dnldr.get_pmid2paper(pmids, self.pmid2note)
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


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
