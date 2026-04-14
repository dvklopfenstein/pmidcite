#!/usr/bin/env python3
"""Test that given, one PMID, all ref/cite PMIDs are downloaded"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

import os
import os.path as op
import shutil
from os import system
from pathlib import Path
from glob import glob
from sys import stdout
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader

DIR_TEST = op.dirname(op.abspath(__file__))
DIR_TESTDATA = op.join(DIR_TEST, "data")
DIR_ICITE = op.abspath(op.join(DIR_TEST, "./icite"))
DIR_REPO = op.abspath(op.join(DIR_TEST, ".."))
DL = os.environ.get('DLCYG')


def get_dnld_files(glob_pattern):
    """Get the filenames of downloaded files matching the researcher's glob pattern"""
    return glob(op.join(DL, glob_pattern))

def get_filename_test(basename):
    """Get the full filename of a test file, basename"""
    return op.join(DIR_TEST, basename)

def get_filename_testdata(basename):
    """Get the full filename of a test file, basename"""
    return op.join(DIR_TESTDATA, basename)

def dir_icite_clobber(prt=stdout):
    """Create an empty dir, ./src/tests/icite, removing old contents if necessary"""
    shutil.rmtree(DIR_ICITE, ignore_errors=True)
    Path(DIR_ICITE).mkdir(parents=True, exist_ok=True)
    if prt:
        print('rm -rf', DIR_ICITE)

def dir_icite_wc_l(prt=stdout):
    """Print count of p{PMID}.py files in dir ./src/tests/icite"""
    # pylint: disable=consider-using-f-string
    cmd = r'find {DIR} -name \*.py | wc -l'.format(DIR=DIR_ICITE)
    system(cmd)
    if prt:
        prt.write(f"{cmd}\n")

def mk_dir(dir_name, rmdir=False):
    """Get the directory where data downloaded from NIH-OCC are stored"""
    if rmdir:
        shutil.rmtree(dir_name, ignore_errors=True)
    if not op.exists(dir_name):
        os.mkdir(dir_name)
        print(f'**CREATED DIR: {op.abspath(dir_name)}')
    return dir_name


class ICiteTester:
    """Test that given, one PMID, all ref/cite PMIDs are downloaded"""

    def __init__(self):
        self.dir_icite = mk_dir(DIR_ICITE)
        self.icite_files = op.join(self.dir_icite, '*.py')

    def rm_icitefiles(self):
        """Remove downloaded NIH-OCC iCite files"""
        for fname in list(glob(self.icite_files)):
            os.remove(fname)
        assert not list(glob(self.icite_files)), 'BAD INITIAL CLEAN UP'

    def get_paper(self, pmid, force_download=False, do_prt=True):
        """Run one download"""
        dnldr = NIHiCiteDownloader(self.dir_icite, force_download, details_cites_refs='all')
        pmids = [pmid]
        pmid2paper = dnldr.get_pmid2paper(pmids)
        assert pmid in pmid2paper
        paper = pmid2paper[pmid]
        if do_prt:
            paper.prt_summary()
        return paper

    def get_f2mtime(self, min_files):
        """Get mofification times of globbed files"""
        f2mtime = {fin:op.getmtime(fin) for fin in glob(self.icite_files)}
        assert len(f2mtime) >= min_files, \
            f'iCite FILES NOT DOWNLOADED {len(f2mtime)=} < min_files({min_files})'
        return f2mtime


# Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved.
