"""Read a file created by pmidcite and write simple text file of PMIDs"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
## import sys
import argparse

from pmidcite.cfg import get_cfgparser
## from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.icite.run import PmidCite
## from pmidcite.cli.utils import get_mode_force
from pmidcite.cli.utils import get_outfile
from pmidcite.cli.utils import mk_outname_pmids
from pmidcite.cli.utils import wr_pmids
from pmidcite.cli.utils import read_top_pmids


class ReadPmids:
    """Read a file created by pmidcite and write simple text file of PMIDs"""

    def __init__(self):
        self.pmidcite = PmidCite(get_cfgparser())

    @staticmethod
    def get_argparser():
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
        parser.add_argument(
            '-i', 'infile', nargs='*',
            help='Read PMIDs from a pmidcite output file.')
        parser.add_argument(
            '-o', '--outfile',
            help='Write current citation report to an ASCII text file.')
        parser.add_argument(
            '-f', '--force_write', action='store_true',
            help='if an existing outfile file exists, overwrite it.')
        ## parser.add_argument(
        ##     '-a', '--append_outfile',
        ##     help='Append current citation report to an ASCII text file. Create if needed.')
        return parser

    def cli(self):
        """Run iCite/PubMed using command-line interface"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        print('ARGS: ', args)
        pmids = self._read_pmids(args, argparser)
        # keys: outfile mode force_write
        ## dct = get_outfile(args.outfile, append_outfile, args.force_write)
        dct = get_outfile(args.outfile, None, args.force_write)
        outfile = self._get_outfile(args, dct)
        if outfile:
            wr_pmids(outfile, pmids)
        else:
            print(pmids)

    def _read_pmids(self, args, argparser):
        """Run iCite/PubMed"""
        ##print('ICITE ARGS: ../pmidcite/src/pmidcite/cli/icite.py', args)
        # Get user-specified PMIDs
        pmids = self.rd_pmidtxts(args.infile)
        if not pmids:
            argparser.print_help()
            return pmids
        return pmids

    @staticmethod
    def _get_outfile(args, dct):
        """Return outfile"""
        if dct['outfile']:
            return dct['outfile']
        if len(args.infile) == 1:
            return mk_outname_pmids(args.infile[0])
        return None

    @staticmethod
    def rd_pmidtxts(fins_pmidcite):
        """Get PMIDs from the command line or from a file"""
        pmids = []
        seen = set()
        if fins_pmidcite:
            for fin in fins_pmidcite:
                if os.path.exists(fin):
                    for pmid in read_top_pmids(fin):
                        if pmid not in seen:
                            pmids.append(pmid)
                            seen.add(pmid)
                else:
                    print('  MISSING: {FILE}'.format(FILE=fin))
        return pmids


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
