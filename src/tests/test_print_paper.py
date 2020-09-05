#!/usr/bin/env python3
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
from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader


def test_print_paper():
    """Test that given, one PMID, all ref/cite PMIDs are downloaded"""
    dir_icite = join(dirname(abspath(__file__)), "./icite")
    obj = Tester(dir_icite)

    pmid = 22882545

    # Clean iCite files
    obj.rm_icitefiles()

    # iCite files are downloaded with the first call
    obj.run(pmid, force_download=False)
    f2mtime = obj.get_f2mtime()
    assert len(f2mtime) >= 50, 'iCite FILES NOT DOWNLOADED'

    # iCite files are imported (NOT downloaded) with the second call
    obj.run(pmid, force_download=False)
    assert obj.get_f2mtime() == f2mtime, 'iCite FILES SHOULD NOT HAVE BE MODIFIED'


class Tester:
    """Test that given, one PMID, all ref/cite PMIDs are downloaded"""

    def __init__(self, dir_icite):
        self.api = NIHiCiteAPI(dir_icite, prt=sys.stdout)
        self.icite_files = join(dir_icite, '*.py')

    def rm_icitefiles(self):
        """Remove downloaded NIH-OCC iCite files"""
        system('rm {PY}'.format(PY=self.icite_files))
        assert not list(glob(self.icite_files)), 'BAD INITIAL CLEAN UP'

    def run(self, pmid, force_download):
        """Run one download"""
        dnldr = NIHiCiteDownloader(force_download, self.api)
        pmids = [pmid]
        pmid2paper = dnldr.get_pmid2paper(pmids)
        assert pmid in pmid2paper
        paper = pmid2paper[pmid]
        paper.prt_summary()

    def get_f2mtime(self):
        """Get mofification times of globbed files"""
        return {getmtime(fin) for fin in glob(self.icite_files)}


if __name__ == '__main__':
    test_print_paper()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
