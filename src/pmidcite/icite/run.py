"""Run NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
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
        dnldr = NIHiCiteDownloader(
            self.dir_icite_py,
            force_download,
            details_cites_refs=None,
            nih_grouper=self.cfgparser.get_nihgrouper())
        pmid2ntpaper = dnldr.get_pmid2paper(pmids, pmid2note=None)
        dnldr.wr_papers(fout_icite, pmid2ntpaper, force_download, 'w')
        return pmids

    def prt_rcfile(self, prt=sys.stdout):
        """Print pmidcite rcfile"""
        self.cfgparser.prt_rcfile_dflt(prt)

    # pylint: disable=line-too-long
    def get_icitedownloader(self, force_download, nih_grouper=None, details_cites_refs=None):
        """Create NIHiCiteDownloader"""
        if nih_grouper is None:
            nih_grouper = self.cfgparser.get_nihgrouper()
        # src/pmidcite/icite/entry.py NIHiCiteEntry {'cited_by_clin', 'cited_by', 'references'}
        return NIHiCiteDownloader(force_download, self.dir_icite_py, nih_grouper, details_cites_refs)


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
