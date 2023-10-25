"""Given PMIDs, download PubMed entries into a text file"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

import argparse

from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.cfg import Cfg
from pmidcite.cli.utils import get_pmids


class DnldPubMed:
    """Given PMIDs, download PubMed entries into a text file"""

    def __init__(self):
        cfg = Cfg()
        self.cfgdct = cfg.cfgparser
        self.pubmed = PubMed(email=cfg.get_email(), apikey=cfg.get_apikey(), tool=cfg.get_tool())

    def get_argparser(self):
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
        dir_pubmed_txt = self.cfgdct['pmidcite']['dir_pubmed_txt']
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
        ## parser.add_argument(
        ##     '-c', '--wordcloud_filename',
        ##     help='Output filename (i.e. pmids.png) for a word cloud plot for the given PMIDs')
        return parser

    def cli(self):
        """Run iCite/PubMed using command-line interface"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        # 1) Get PMIDs
        pmids = self._get_pmids(args, argparser)
        print('{N} PMIDs'.format(N=len(pmids)))
        # 2) Download PubMed entries.
        if pmids:
            self.pubmed.dnld_wr1_per_pmid(pmids, args.force_download, args.dir_pubmed_txt)

    @staticmethod
    def _get_pmids(args, argparser):
        """Extract PMIDs from required args and PMID files"""
        pmids = get_pmids(args.pmids, args.infile)
        if not pmids:
            argparser.print_help()
        return pmids


# Copyright (C) 2019-present DV Klopfenstein, PhD. All rights reserved.
