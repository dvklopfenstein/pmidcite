"""Run NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader
from pmidcite.cli.utils import read_pmids


class PmidCite:
    """Run NIH iCite run for one PubMed ID (PMID)"""

    def __init__(self, cfgparser):
        self.cfgparser = cfgparser  # Cfg
        self.dir_icite = self.cfgparser.cfgparser['pmidcite']['dir_icite']  # ./log/icite
        self.dir_icite_py = self.cfgparser.cfgparser['pmidcite']['dir_icite_py']  # ./icite

    def run_pmid_file(self, fin_pmids, fout_icite, force_download):
        """Run iCite on list of PMIDs in a file"""
        pmids = read_pmids(fin_pmids)
        dnldr = self.get_icitedownloader(force_download)
        pmid2ntpaper = dnldr.get_pmid2paper(
            pmids, dnld_assc_pmids_do=False, pmid2note=None)
        dnldr.wr_papers(fout_icite, pmid2ntpaper, force_download, 'w')
        return pmids

    def prt_rcfile(self, prt=sys.stdout):
        """Print pmidcite rcfile"""
        self.cfgparser.prt_rcfile_dflt(prt)

    # pylint: disable=line-too-long
    def get_icitedownloader(self, force_download, nih_grouper=None, no_references=False, prt_icitepy=None):
        """Create NIHiCiteDownloader"""
        # Setting prt_icitepy to sys.stdout will cause: WROTE: ./icite/p10802651.py
        kws = {}  # TBD NIHiCiteCli
        if nih_grouper is None:
            nih_grouper = self.cfgparser.get_nihgrouper()
        api = NIHiCiteAPI(nih_grouper, self.dir_icite_py, prt_icitepy, **kws)
        return NIHiCiteDownloader(force_download, api, not no_references)


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
