"""Run NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from pmidcite.cfg import Cfg
from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader
from pmidcite.cli.utils import read_pmids


class PmidCite:
    """Run NIH iCite run for one PubMed ID (PMID)"""

    def __init__(self):
        self.cfgparser = self._init_cfgparser()  # Cfg
        self.dir_icite_py = self.cfgparser.cfgparser['pmidcite']['dir_icite_py']  # ./icite

    @staticmethod
    def _init_cfgparser():
        """Init cfg parser"""
        cfgparser = Cfg(chk=False)
        cfgparser.rd_rc(prt=None)
        return cfgparser

    def run_pmid_file(self, fin_pmids, fout_icite, force_download):
        """Run iCite on list of PMIDs in a file"""
        pmids = read_pmids(fin_pmids)
        dnldr = self.get_icitedownloader(force_download)
        pmid2ntpaper = dnldr.get_pmid2paper(
            pmids, dnld_assc_pmids_do=False, pmid2note=None, prt=None)
        dnldr.wr_papers(fout_icite, force_download, pmid2ntpaper, 'w')
        return pmids

    def prt_rcfile(self, prt=sys.stdout):
        """Print pmidcite rcfile"""
        self.cfgparser.cfgparser.write(prt)

    def get_icitedownloader(self, force_download, no_references=False, prt_icitepy=None):
        """Create NIHiCiteDownloader"""
        # Setting prt_icitepy to sys.stdout will cause: WROTE: ./icite/p10802651.py
        kws = {}  # TBD NIHiCiteCli
        api = NIHiCiteAPI(self.dir_icite_py, prt_icitepy, **kws)
        return NIHiCiteDownloader(force_download, api, not no_references)


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
