"""Print NIH's iCite summary for each PubMed PMID"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.pmid_loader import NIHiCiteLoader
from pmidcite.cfgparser.icite import NIHiCiteCfg


# pylint: disable=too-few-public-methods
class NIHiCite:
    """Print NIH's iCite summary for each PubMed PMID"""

    def __init__(self):
        _cfg = self._init_cfg()
        self.dir_pmid_py = _cfg.cfgparser['DEFAULT']['dir_pmid_py']
        self.api = NIHiCiteAPI(self.dir_pmid_py)

    def run_icite_name2pmid(self, fout_txt, name2pmid, force_download=False):
        """Given PMIDs, return NIH iCite summary"""
        loader = NIHiCiteLoader(force_download, self.api, rpt_references=True)
        loader.wr_name2pmid(fout_txt, name2pmid)

    def run_icite_pmids(self, fout_txt, pmids, force_download=False):
        """Given PMIDs, return NIH iCite summary"""
        loader = NIHiCiteLoader(force_download, self.api, rpt_references=True)
        loader.wr_pmids(fout_txt, pmids)

    @staticmethod
    def _init_cfg():
        """Initialize iCite configuration"""
        cfg = NIHiCiteCfg()
        cfg.rd_rc()
        return cfg


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
