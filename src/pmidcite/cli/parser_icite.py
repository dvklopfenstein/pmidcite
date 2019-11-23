"""Manage args for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import argparse
import configparser

from pmidcite.api import NIHiCiteAPI


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
            help='PubMed IDs (PMIDs)')
        parser.add_argument(
            '--dir_pmid_py', default=self.cfgparser['DEFAULT']['dir_pmid_py'],
            help='Directory for PMID iCite data stored in Python modules')
        parser.add_argument(
            '--dir_pmid_txt', default=self.cfgparser['DEFAULT']['dir_pmid_txt'],
            help='Directory for PMID data, including the abstract stored in a text file')
        parser.add_argument(
            '-o', '--outfile', default='p{PMID}.txt',
            help='Write report to a ASCII text file')
        parser.add_argument(
            '-f', '--force_download', action='store_true',
            help='Download PMID iCite information to a file')
        parser.add_argument(
            '--generate-rcfile', action='store_true',
            help='Generate a sample configuration file according to the '
                 'current configuration.')
        return parser

    @staticmethod
    def run_icite(pmids, dir_dnld, outfile, **kws):
        """Run NIH's iCite"""
        #for pmid in args.pmids:
        api = NIHiCiteAPI(kws['force_download'], dir_dnld, prt=sys.stdout, **kws)
        print('WWWWWWWWWWWWWWWW', kws)
        if outfile in {'None', 'False', 'none', 'false'}:
            api.run_icite_pmids(pmids, prtout=sys.stdout)
        elif '{PMID}' in outfile:
            if len(pmids) == 1:
                fout_txt = outfile.format(PMID=pmids[0])
                api.wr_out(fout_txt, pmids)
            else:
                fout_txt = 'pmidcite.txt'
                api.wr_out(fout_txt, pmids)
        else:
            api.wr_out(outfile, pmids)

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
        self.run_icite(args.pmids, args.dir_pmid_py, args.outfile, **kws)

    @staticmethod
    def _init_cfgparser():
        """Create a ConfigParser()"""
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'dir_pmid_py': '.',
            'dir_pmid_txt': '.',
        }
        # config['PMIDs'] = {
        # }
        return config

    def wr_rc(self):
        """Write a sample configuration"""
        with open(self.cfgfile, 'w') as prt:
            self.cfgparser.write(prt)
            print('  WROTE: {CFG}'.format(CFG=self.cfgfile))


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
