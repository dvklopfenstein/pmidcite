"""Manage args for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import argparse

from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.icite.run import PmidCite
from pmidcite.cli.utils import get_pmids


class DnldPubMed:
    """Manage args for NIH iCite run for one PubMed ID (PMID)"""

    def __init__(self):
        self.pmidcite = PmidCite()
        cfgparser = self.pmidcite.cfgparser
        self.pubmed = PubMed(
            email=cfgparser.get_email(),
            apikey=cfgparser.get_apikey(),
            tool=cfgparser.get_tool())

    def get_argparser(self):
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
        dir_pubmed_txt = self.pmidcite.cfgparser.cfgparser['pmidcite']['dir_pubmed_txt']
        parser.add_argument(
            'pmids', metavar='PMID', type=int, nargs='*',
            help='PubMed IDs (PMIDs)')
        parser.add_argument(
            '-i', '--infile', nargs='*',
            help='Read PMIDs from a file containing one PMID per line.')
        ## parser.add_argument(
        ##     '-o', '--outfile',
        ##     help='Write current citation report to an ASCII text file.')
        ## parser.add_argument(
        ##     '-f', '--force_write', action='store_true',
        ##     help='if an existing outfile file exists, overwrite it.')
        parser.add_argument(
            '-D', '--force_download', action='store_true',
            help='Download PMID iCite information to a Python file, over-writing if necessary.')
        parser.add_argument(
            '--dir_pubmed_txt', default=dir_pubmed_txt,
            help='Write PubMed entry into directory (default={D})'.format(D=dir_pubmed_txt))
        return parser

    def cli(self):
        """Run iCite/PubMed using command-line interface"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        # 1) Get PMIDs
        pmids = self.run_icite(args, argparser)
        print('{N} PMIDs'.format(N=len(pmids)))
        # 2) Download PubMed entries.
        #    nt flds: PMID fout_pubmed fout_exists
        pmid_nt_list = self.pubmed.get_pmid_nt_list(pmids, args.force_download, args.dir_pubmed_txt)
        self.pubmed.dnld_wr1_per_pmid(pmid_nt_list)

    @staticmethod
    def run_icite(args, argparser):
        """Run iCite/PubMed"""
        print('DNLDPUBMED ARGS: ../pmidcite/src/pmidcite/cli/icite.py', args)
        # Get user-specified PMIDs
        pmids = get_pmids(args.pmids, args.infile)
        if not pmids:
            argparser.print_help()
        return pmids


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
