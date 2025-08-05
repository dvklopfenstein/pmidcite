"""Given PMIDs, download PubMed entries into a text file"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

import argparse

from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.cfg import Cfg
from pmidcite.cli.common import add_args
from pmidcite.cli.utils import get_pmids


class BasePubMed:
    """Given PMIDs, download PubMed entries into a text file"""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        cfg = Cfg()
        self.cfgdct = cfg.cfgparser
        self.pubmed = PubMed(email=cfg.get_email(), apikey=cfg.get_apikey(), tool=cfg.get_tool())


class DnldPubMed(BasePubMed):
    """Given PMIDs, download PubMed entries into a text file"""

    def get_argparser(self):
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
        dir_pubmed_txt = self.cfgdct['pmidcite']['dir_pubmed_txt']
        add_args(parser, ['pmids', 'infile', 'force_download'])
        parser.add_argument(
            '--dir_pubmed_txt', default=dir_pubmed_txt,
            help=f'Write PubMed entry into directory (default={dir_pubmed_txt})')
        return parser

    def cli(self):
        """Run iCite/PubMed using command-line interface"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        # 1) Get PMIDs
        pmids = self._get_pmids(args, argparser)
        print(f'{len(pmids)} PMIDs')
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


class QueryPubMed(BasePubMed):
    """Given PMIDs, download PubMed entries into a text file"""

    def get_argparser(self):
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
        dir_pubmed_txt = self.cfgdct['pmidcite']['dir_pubmed_txt']
        parser.add_argument(
            'query', metavar='query', type=str, nargs='*',
            help='PubMed query')
        parser.add_argument(
            '-p', '--pubmed', action='store_true',
            help='Download PubMed entry containing title, abstract, authors, journal, MeSH, etc.')
        parser.add_argument(
            '-f', '--force_download', action='store_true',
            help='Download PMID iCite information to a Python file, over-writing if necessary.')
        parser.add_argument(
            '--dir_pubmed_txt', default=dir_pubmed_txt,
            help=f'Write PubMed entry into directory (default={dir_pubmed_txt})')
        return parser

    def cli(self):
        """Run iCite/PubMed using command-line interface"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        if args.query:
            pmids = self._run_queries(args.query)
            if pmids:
                for pmid in pmids:
                    print(pmid)
                if args.pubmed:
                    self.pubmed.dnld_wr1_per_pmid(pmids, args.force_download, args.dir_pubmed_txt)

    def _run_queries(self, queries):
        """Run PubMed queries. Return PMIDs"""
        pmids_all = []
        for query in queries:
            pmids_cur = self.pubmed.dnld_query_pmids(query, 10)
            if pmids_cur:
                pmids_all.extend(pmids_cur)
        return pmids_all


# Copyright (C) 2019-present DV Klopfenstein, PhD. All rights reserved.
