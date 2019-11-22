"""Manage args for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import argparse
import configparser

from pmidcite.api import NIHiCiteAPI
from pmidcite.paper import NIHiCitePaper


class NIHiCiteArgs:
    """Manage args for NIH iCite run for one PubMed ID (PMID)"""

    cfgfile = '.pmidciterc'

    def __init__(self):
        self.cfgparser = self._init_cfgparser()

    def get_argparser(self):
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        self.cfgparser.read(self.cfgfile)
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
        parser.add_argument(
            'pmids', metavar='PMID', type=int, nargs='*',
            default=[30022098],
            help='PubMed IDs (PMIDs)')
        parser.add_argument(
            '-d', '--dir_pmids', default=self.cfgparser['DEFAULT']['dir_pmids'],
            help='Directory for PMID iCite data stored in Python modules')
        parser.add_argument(
            '-f', '--force_download', action='store_true',
            help='Download PMID iCite information to a file')
        parser.add_argument(
            '--generate-rcfile', action='store_true',
            help='Generate a sample configuration file according to the '
                 'current configuration.')
        return parser

    @staticmethod
    def run_icite(pmids, dir_dnld, **kws):
        """Run NIH's iCite"""
        #for pmid in args.pmids:
        api = NIHiCiteAPI(kws['force_download'], dir_dnld, prt=sys.stdout, **kws)
        for pmid in pmids:
            icites = api.run_icite(pmid)
            print('{N} NIH iCite items'.format(N=len(icites)))
            paper = NIHiCitePaper(pmid, dir_dnld, prt=None)
            paper.prt_summary(sys.stdout, 'cite')

    def run(self):
        """Run the argparser"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        if args.generate_rcfile:
            self.wr_rc()
            return
        print(args)
        print(args.pmids)
        kws = {
            'force_download': args.force_download,
        }
        self.run_icite(args.pmids, args.dir_pmids, **kws)

    @staticmethod
    def _init_cfgparser():
        """Create a ConfigParser()"""
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'dir_pmids': '.'
        }
        config['PMIDs'] = {
        }
        return config

    def wr_rc(self):
        """Write a sample configuration"""
        with open(self.cfgfile, 'w') as prt:
            self.cfgparser.write(prt)
            print('  WROTE: {CFG}'.format(CFG=self.cfgfile))


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
