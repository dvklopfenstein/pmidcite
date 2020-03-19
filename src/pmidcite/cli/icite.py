"""Manage args for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
import argparse

from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.icite.run import PmidCite


class NIHiCiteCli:
    """Manage args for NIH iCite run for one PubMed ID (PMID)"""

    def __init__(self):
        self.pmidcite = PmidCite()
        cfgparser = self.pmidcite.cfgparser
        self.dir_pmid_py = cfgparser.cfgparser['pmidcite']['dir_pmid_py']
        self.dir_pubmed = cfgparser.cfgparser['pmidcite']['dir_pubmed_txt']
        self.pubmed = PubMed(
            email=cfgparser.get_email(),
            apikey=cfgparser.get_apikey(),
            tool=cfgparser.get_tool())

    @staticmethod
    def get_argparser():
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
        parser.add_argument(
            'pmids', metavar='PMID', type=int, nargs='*',
            help='PubMed IDs (PMIDs)')
        parser.add_argument(
            '-i', '--infile', nargs='*',
            help='Read PMIDs from a file containing one PMID per line.')
        parser.add_argument(
            '-a', '--append_outfile',
            help='Append current citation report to an ASCII text file. Create if needed.')
        parser.add_argument(
            '-k', '--print_keys', action='store_true',
            help='Print the keys describing the abbreviations.')
        parser.add_argument(
            '-o', '--outfile',
            help='Write current citeation report to an ASCII text file.')
        parser.add_argument(
            '-f', '--force_write', action='store_true',
            help='if an existing outfile file exists, overwrite it.')
        parser.add_argument(
            '-D', '--force_download', action='store_true',
            help='Download PMID iCite information to a Python file, over-writing if necessary.')
        parser.add_argument(
            '-R', '--no_references', action='store_true',
            help='Print the list of citations, but not the list of references.')
        parser.add_argument(
            '-s', '--succinct', action='store_true',
            help="Print one line for each PMID provided by user. Don't add lines per cite or ref.")
        parser.add_argument(
            '-q', '--quiet', action='store_true',
            help='Quiet mode; Do not echo the paper report to screen.')
        parser.add_argument(
            '-p', '--pubmed', action='store_true',
            help='Download PubMed entry containing title, abstract, authors, journal, MeSH, etc.')
        parser.add_argument(
            '--md', action='store_true',
            help='Print using markdown table format.')
        parser.add_argument(
            '--generate-rcfile', action='store_true',
            help='Generate a sample configuration file according to the '
                 'current configuration.')
        return parser

    def cli(self):
        """Run iCite/PubMed using command-line interface"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        pmids = self.run_icite(args, argparser)
        if args.pubmed:
            pmid_nt_list = self.pubmed.get_pmid_nt_list(pmids, args.force_download, self.dir_pubmed)
            self.pubmed.dnld_wr1_per_pmid(pmid_nt_list)

    def run_icite(self, args, argparser, pmid2note=None):
        """Run iCite/PubMed"""
        print('ICITE ARGS: ../pmidcite/src/pmidcite/cli/icite.py', args)
        # Print rcfile initialization file
        if args.generate_rcfile:
            self.pmidcite.prt_rcfile(sys.stdout)
            return []
        # Get user-specified PMIDs
        pmids = self.get_pmids(args.pmids, args.infile)
        if not pmids and not args.print_keys:
            argparser.print_help()
            return pmids
        return self._run_icite(pmids, args, pmid2note)

    def _run_icite(self, pmids, args, pmid2note):
        """Print papers, including citation counts"""
        loader = self.pmidcite.get_iciteloader(args.force_download, args.no_references, args.quiet)
        if args.print_keys:
            loader.prt_keys()
        outfile = self._get_outfile(args)
        mode, force_write = self._get_mode_force(args)
        prt_verbose = not args.succinct
        pmid2ntpaper = loader.get_pmid2paper(pmids, prt_verbose, pmid2note)
        if outfile is None:
            loader.prt_papers(pmid2ntpaper, prt=sys.stdout, prt_assc_pmids=prt_verbose)
        else:
            if not args.quiet:
                loader.prt_papers(pmid2ntpaper, prt=sys.stdout, prt_assc_pmids=prt_verbose)
            loader.wr_papers(outfile, force_write, pmid2ntpaper, mode)
        return pmids

    def get_pmids(self, pmid_list, fin_pmids):
        """Get PMIDs from the command line or from a file"""
        if not pmid_list and not fin_pmids:
            return []
        pmids = list(pmid_list)
        if fin_pmids:
            for fin in fin_pmids:
                if os.path.exists(fin):
                    pmids.extend(self.pmidcite.read_pmids(fin))
                else:
                    print('  MISSING: {FILE}'.format(FILE=fin))
        return pmids

    @staticmethod
    def _get_mode_force(args):
        """Given arguments, return outfile"""
        # if '-o', only over-write existing file if explicitly requested
        if args.outfile is not None:
            return 'w', args.force_write
        # if '-a', always append given file or create the file if needed
        if args.append_outfile is not None:
            return 'a', True
        return 'w', True

    @staticmethod
    def _get_outfile(args):
        """Given arguments, return outfile"""
        if args.outfile is not None:
            return args.outfile
        if args.append_outfile is not None:
            return args.append_outfile
        return None


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
