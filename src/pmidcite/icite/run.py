"""Run NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from pmidcite.cfg import Cfg
from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.pmid_loader import NIHiCiteLoader


class PmidCite:
    """Run NIH iCite run for one PubMed ID (PMID)"""

    def __init__(self):
        self.cfgparser = self._init_cfgparser()  # Cfg
        self.dir_pmid_py = self.cfgparser.cfgparser['pmidcite']['dir_pmid_py']  # ./icite

    @staticmethod
    def _init_cfgparser():
        """Init cfg parser"""
        cfgparser = Cfg(chk=False)
        cfgparser.rd_rc()
        return cfgparser

    def run_pmid_file(self, fin_pmids, fout_icite, force_download):
        """Run iCite on list of PMIDs in a file"""
        pmids = self.read_pmids(fin_pmids)
        loader = self.get_iciteloader(force_download)
        pmid2ntpaper = loader.get_pmid2paper(pmids, dnld_assc_pmids=False)
        loader.wr_papers(fout_icite, force_download, pmid2ntpaper, 'w')
        return pmids

    def prt_rcfile(self, prt=sys.stdout):
        """Print pmidcite rcfile"""
        self.cfgparser.cfgparser.write(prt)

    def get_iciteloader(self, force_download, no_references=False, quiet=False):
        """Create NIHiCiteLoader"""
        kws = {}  # TBD NIHiCiteCli
        log = None if quiet else sys.stdout
        api = NIHiCiteAPI(self.dir_pmid_py, log, **kws)
        return NIHiCiteLoader(force_download, api, not no_references)

    @staticmethod
    def read_pmids(fin):
        """Read PMIDs from a file. One PMID per line."""
        pmids = []
        with open(fin) as ifstrm:
            for line in ifstrm:
                line = line.strip()
                if line.isdigit():
                    pmids.append(int(line))
            print('  {N} PMIDs READ: {FILE}'.format(
                N=len(pmids), FILE=fin))
        return pmids


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
