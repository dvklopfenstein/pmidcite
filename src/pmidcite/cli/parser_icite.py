"""Manage args for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import argparse

from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.pmid_loader import NIHiCiteLoader
from pmidcite.cfgparser.icite import NIHiCiteCfg


class NIHiCiteArgs:
    """Manage args for NIH iCite run for one PubMed ID (PMID)"""

    def __init__(self):
        self.cfgparser = NIHiCiteCfg()

    def get_argparser(self):
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        self.cfgparser.rd_rc()
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
        parser.add_argument(
            'pmids', metavar='PMID', type=int, nargs='*',
            help='PubMed IDs (PMIDs)')
        parser.add_argument(
            '--dir_pmid_py', default=self.cfgparser.cfgparser['DEFAULT']['dir_pmid_py'],
            help='Directory for PMID iCite data stored in Python modules')
        parser.add_argument(
            '--dir_pmid_txt', default=self.cfgparser.cfgparser['DEFAULT']['dir_pmid_txt'],
            help='Directory for PMID data, including the abstract stored in a text file')
        parser.add_argument(
            '-o', '--outfile', default='pmidcite.txt',
            help='Write report to a ASCII text file')
        parser.add_argument(
            '-f', '--force_download', action='store_true',
            help='Download PMID iCite information to a file')
        parser.add_argument(
            '-r', '--references', action='store_true',
            help='Print references as well as citations')
        parser.add_argument(
            '--generate-rcfile', action='store_true',
            help='Generate a sample configuration file according to the '
                 'current configuration.')
        return parser

    def run(self):
        """Run the argparser"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        if args.generate_rcfile:
            self.cfgparser.wr_rc()
            return
        print(args)
        print(args.pmids)
        kws = {}  # TBD
        api = NIHiCiteAPI(args.dir_pmid_py, **kws)
        loader = NIHiCiteLoader(args.force_download, args.references, api)
        print('NIHiCiteArgs WWWWWWWWWWWWWWWW', kws)
        if args.outfile in {'None', 'False', 'none', 'false'}:
            loader.run_icite_pmids(args.pmids, prtout=sys.stdout)
        else:
            loader.wr_out(args.outfile, args.pmids)


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
