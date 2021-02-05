"""Test that given, one PMID, all ref/cite PMIDs are downloaded"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from os.path import join
from os.path import dirname
from os.path import abspath
from os import system
from os.path import getmtime
from glob import glob
import sys
from pmidcite.icite.nih_grouper import NihGrouper
from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader

DIR_TEST = dirname(abspath(__file__))
DIR_ICITE = join(DIR_TEST, "./icite")
DIR_REPO = join(DIR_TEST, "../..")

class ICiteTester:
    """Test that given, one PMID, all ref/cite PMIDs are downloaded"""


    def __init__(self):
        self.dir_icite = DIR_ICITE
        nihgrouper = NihGrouper()
        self.api = NIHiCiteAPI(nihgrouper, self.dir_icite, prt=sys.stdout)
        self.icite_files = join(self.dir_icite, '*.py')

    def rm_icitefiles(self):
        """Remove downloaded NIH-OCC iCite files"""
        if list(glob(self.icite_files)):
            system('rm {PY}'.format(PY=self.icite_files))
        assert not list(glob(self.icite_files)), 'BAD INITIAL CLEAN UP'

    def get_paper(self, pmid, force_download=False, do_prt=True):
        """Run one download"""
        dnldr = NIHiCiteDownloader(force_download, self.api)
        pmids = [pmid]
        pmid2paper = dnldr.get_pmid2paper(pmids)
        assert pmid in pmid2paper
        paper = pmid2paper[pmid]
        if do_prt:
            paper.prt_summary()
        return paper

    def get_f2mtime(self, min_files):
        """Get mofification times of globbed files"""
        f2mtime = {getmtime(fin) for fin in glob(self.icite_files)}
        assert len(f2mtime) >= min_files, 'iCite FILES NOT DOWNLOADED'
        return f2mtime


# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
