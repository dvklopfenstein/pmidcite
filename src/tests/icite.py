#!/usr/bin/env python3
"""Test that given, one PMID, all ref/cite PMIDs are downloaded"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from os import system
from os import mkdir
from os import environ
from os.path import join
from os.path import dirname
from os.path import abspath
from os.path import relpath
from os.path import exists
from os.path import getmtime
from glob import glob
from sys import stdout
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader

DIR_TEST = dirname(abspath(__file__))
DIR_TESTDATA = join(DIR_TEST, "data")
DIR_ICITE = abspath(join(DIR_TEST, "./icite"))
DIR_REPO = abspath(join(DIR_TEST, "../.."))
DL = environ.get('DLCYG')

def get_dnld_files(glob_pattern):
    """Get the filenames of downloaded files matching the researcher's glob pattern"""
    return glob(join(DL, glob_pattern))

def get_filename_test(basename):
    """Get the full filename of a test file, basename"""
    return join(DIR_TEST, basename)

def get_filename_testdata(basename):
    """Get the full filename of a test file, basename"""
    return join(DIR_TESTDATA, basename)

def dir_icite_clobber(prt=stdout):
    """Create an empty dir, ./src/tests/icite, removing old contents if necessary"""
    cmd = 'rm -rf {ICITE}; mkdir {ICITE}'.format(ICITE=DIR_ICITE)
    system(cmd)
    if prt:
        prt.write("{}\n".format(cmd))

def dir_icite_wc_l(prt=stdout):
    """Print count of p{PMID}.py files in dir ./src/tests/icite"""
    cmd = r'find {DIR} -name \*.py | wc -l'.format(DIR=DIR_ICITE)
    system(cmd)
    if prt:
        prt.write("{}\n".format(cmd))

def mk_dir(dir_name, rmdir=False):
    """Get the directory where data downloaded from NIH-OCC are stored"""
    if rmdir:
        system('rm -rf {DIR}'.format(DIR=dir_name))
    if not exists(dir_name):
        mkdir(dir_name)
        print('**CREATED DIR: {D}'.format(D=relpath(dir_name)))
    return dir_name


class ICiteTester:
    """Test that given, one PMID, all ref/cite PMIDs are downloaded"""

    def __init__(self):
        self.dir_icite = mk_dir(DIR_ICITE)
        self.icite_files = join(self.dir_icite, '*.py')

    def rm_icitefiles(self):
        """Remove downloaded NIH-OCC iCite files"""
        if list(glob(self.icite_files)):
            system('rm {PY}'.format(PY=self.icite_files))
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
        f2mtime = {fin:getmtime(fin) for fin in glob(self.icite_files)}
        assert len(f2mtime) >= min_files, \
            'iCite FILES NOT DOWNLOADED len(f2mtime)={} < min_files({})'.format(
                len(f2mtime), min_files)
        return f2mtime



# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
