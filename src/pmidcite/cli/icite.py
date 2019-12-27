"""Manage args for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
import argparse
import collections as cx

from pmidcite.eutils.cmds.efetch import EFetch
from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.pmid_loader import NIHiCiteLoader
from pmidcite.cfg import Cfg


class NIHiCiteCli:
    """Manage args for NIH iCite run for one PubMed ID (PMID)"""

    def __init__(self):
        self.cfgparser = self._init_cfgparser()
        self.dir_pmid_py = self.cfgparser.cfgparser['pmidcite']['dir_pmid_py']
        self.pubmed_dir = self.cfgparser.cfgparser['pmidcite']['dir_pubmed_txt']
        self.efetch = self._init_efetch()

    def _init_efetch(self):
        """Initialize EFetch for downloading PubMed entries"""
        kws = {
            'email':self.cfgparser.get_email(),
            'apikey':self.cfgparser.get_apikey(),
            'tool':self.cfgparser.get_tool()}
        return EFetch(
            retmax=10000,
            rettype='medline',
            retmode='text',
            batch_size=10,
            **kws)

    @staticmethod
    def _init_cfgparser():
        """Init cfg parser"""
        cfgparser = Cfg(chk=False)
        cfgparser.rd_rc()
        return cfgparser

    @staticmethod
    def get_argparser():
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
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
            '-s', '--succinct', action='store_true',
            help="Print one line for each PMID provided by user. Don't add lines per cite or ref")
        parser.add_argument(
            '-q', '--quiet', action='store_true',
            help='Quiet mode; Do not echo the paper report to screen')
        parser.add_argument(
            '-p', '--pubmed', action='store_true',
            help='Download PubMed entry containing title, abstract, authors, journal, MeSH, etc.')
        parser.add_argument(
            '-f', '--force_download', action='store_true',
            help='Download PMID iCite information to a Python file')
        parser.add_argument(
            '-R', '--no_references', action='store_true',
            help='Print the list of citations, but not the list of references')
        parser.add_argument(
            '--md', action='store_true',
            help='Print using markdown table format')
        parser.add_argument(
            '--generate-rcfile', action='store_true',
            help='Generate a sample configuration file according to the '
                 'current configuration.')
        #### parser.add_argument(
        ####     '--dir_pmid_py', default=self.cfgparser.cfgparser['pmidcite']['dir_pmid_py'],
        ####     help='Directory for PMID iCite data stored in Python modules')
        #### parser.add_argument(
        ####     '--dir_pubmed_txt', default=self.cfgparser.cfgparser['pmidcite']['dir_pubmed_txt'],
        ####     help='Directory for PMID data, including the abstract stored in a text file')
        return parser

    def cli(self):
        """Run iCite/PubMed using command-line interface"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        pmids = self.run_icite(args, argparser)
        if args.pubmed:
            pmid_nt_list = self._get_pmid_nt_list(pmids, args.force_download)
            for ntd in pmid_nt_list:
                print('IIIIIIIIIIIIIIIIIIIII {PMID:12} {NT}'.format(PMID=ntd.PMID, NT=ntd))
            self._dnld_pubmed(pmid_nt_list)

    def _dnld_pubmed(self, pmid_nt_list):
        """Download and write PubMed entries, given PMIDs and assc info"""
        pmids = [nt.PMID for nt in pmid_nt_list]
        print('PMIDSSSSSSSSSSSSSSSSS', pmids)
        # post: {'querykey': 1, 'webenv': 'NCID_1_1510...}
        # Each PMID gets its own querykey (step=1)
        # post = self.efetch.epost('pubmed', pmids, step=1)
        post = {'querykey':3, 'webenv':'NCID_1_151249948_130.14.22.33_9001_1577434611_2126419517_0MetA0_S_MegaStore'}
        webenv = post['webenv']
        assert len(pmids) == post['querykey']
        for querykey, pmid in enumerate(pmids, 1):
            print('PPPPPPPPPPPPPPPPPPPP', querykey, pmid)
            self.efetch.efetch_and_write(sys.stdout, 'pubmed', webenv, querykey, 1)

    def run_icite(self, args, argparser):
        """Run iCite/PubMed"""
        print('ICITE ARGS: ../pmidcite/src/pmidcite/cli/icite.py', args)
        # Print rcfile initialization file
        if args.generate_rcfile:
            self.cfgparser.cfgparser.write(sys.stdout)
            return []
        # Get user-specified PMIDs
        pmids = self.get_pmids(args)
        if not pmids:
            argparser.print_help()
            return pmids
        kws = {}  # TBD NIHiCiteCli
        log = None if args.quiet else sys.stdout
        api = NIHiCiteAPI(self.dir_pmid_py, log, **kws)
        loader = NIHiCiteLoader(args.force_download, api, not args.no_references)
        outfile = self._get_outfile(args)
        mode = self._get_mode(args)
        prt_verbose = not args.succinct
        pmid2ntpaper = loader.get_pmid2paper(pmids, prt_verbose)
        if outfile is None:
            loader.prt_papers(pmid2ntpaper, prt=sys.stdout, prt_assc_pmids=prt_verbose)
        else:
            if not args.quiet:
                loader.prt_papers(pmid2ntpaper, prt=sys.stdout)
            loader.wr_papers(outfile, pmid2ntpaper, mode)
        return pmids

    ##def _wr_pubmed(self, pmids):
    def _get_pmid_nt_list(self, pmids, force_download):
        """Get list of PubMed entries: Title, abstract, authors, journal, MeSH"""
        nts = []
        ntobj = cx.namedtuple('Nt', 'PMID fout_pubmed fout_exists')
        for pmid in pmids:
            # Get filename, pPMID.txt
            fout_pubmed = os.path.join(self.pubmed_dir, 'p{PubMed}.txt'.format(PubMed=pmid))
            fout_exists = os.path.exists(fout_pubmed)
            if not fout_exists or force_download:
                ntd = ntobj(PMID=pmid, fout_pubmed=fout_pubmed, fout_exists=fout_exists)
                nts.append(ntd)
        return nts

    def get_pmids(self, args):
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
