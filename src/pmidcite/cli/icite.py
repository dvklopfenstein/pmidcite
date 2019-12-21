"""Manage args for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
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
        print(self.cfgparser.cfgfile)
        parser.add_argument(
            'pmids', metavar='PMID', type=int, nargs='*',
            help='PubMed IDs (PMIDs)')
        parser.add_argument(
            '-i', '--infile', nargs='*',
            help='Read PMIDs from a file containing one PMID per line')
        parser.add_argument(
            '-a', '--outfile_append',
            help='Append current citation report to an ASCII text file. Create if needed.')
        parser.add_argument(
            '-o', '--outfile',
            help='Write current citeation report to an ASCII text file')
        parser.add_argument(
            '-f', '--force_download', action='store_true',
            help='Download PMID iCite information to a Python file')
        parser.add_argument(
            '-R', '--no_references', action='store_true',
            help='Print the list of citations, but not the list of references')
        parser.add_argument(
            '-q', '--quiet', action='store_true',
            help='Quiet mode; Do not echo the paper report to screen')
        parser.add_argument(
            '--generate-rcfile', action='store_true',
            help='Generate a sample configuration file according to the '
                 'current configuration.')
        parser.add_argument(
            '--dir_pmid_py', default=self.cfgparser.cfgparser['DEFAULT']['dir_pmid_py'],
            help='Directory for PMID iCite data stored in Python modules')
        parser.add_argument(
            '--dir_pmid_txt', default=self.cfgparser.cfgparser['DEFAULT']['dir_pmid_txt'],
            help='Directory for PMID data, including the abstract stored in a text file')
        return parser

    def run(self):
        """Run the argparser"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        print(args)
        if args.generate_rcfile:
            self.cfgparser.wr_rc()
            return
        pmids = self._get_pmids(args)
        if not pmids:
            argparser.print_help()
            return
        kws = {}  # TBD NIHiCiteArgs
        log = None if args.quiet else sys.stdout
        api = NIHiCiteAPI(args.dir_pmid_py, log, **kws)
        loader = NIHiCiteLoader(args.force_download, api, not args.no_references)
        outfile = self._get_outfile(args)
        mode = self._get_mode(args)
        pmid2ntpaper = loader.run_icite_pmids(pmids)
        if outfile is None:
            loader.prt_papers(pmid2ntpaper, prt=sys.stdout)
        else:
            if not args.quiet:
                loader.prt_papers(pmid2ntpaper, prt=sys.stdout)
            loader.wr_papers(outfile, pmid2ntpaper, mode)

    def _get_pmids(self, args):
        """Get PMIDs from the command line or from a file"""
        if not args.pmids and not args.infile:
            return []
        pmids = list(args.pmids)
        if args.infile:
            for fin in args.infile:
                if os.path.exists(fin):
                    pmids.extend(self._read_pmids(fin))
                else:
                    print('  MISSING: {FILE}'.format(FILE=fin))
        return pmids


    @staticmethod
    def _read_pmids(fin):
        """Read PMIDs from a file. One PMID per line."""
        pmids = []
        with open(fin) as ifstrm:
            for line in ifstrm:
                line = line.strip()
                if line.isdigit():
                    pmids.append(int(line))
            print('  {N} PMIDs READ: {FILE}'.format(
                N=len(pmids), FILE=fin))
        return pmids

    @staticmethod
    def _get_mode(args):
        """Given arguments, return outfile"""
        if args.outfile is not None:
            return 'w'
        if args.outfile_append is not None:
            return 'a'
        return 'w'

    @staticmethod
    def _get_outfile(args):
        """Given arguments, return outfile"""
        if args.outfile is not None:
            return args.outfile
        if args.outfile_append is not None:
            return args.outfile_append
        return None


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
