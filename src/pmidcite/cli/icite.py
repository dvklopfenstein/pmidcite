"""Manage args for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

## import os
import sys
import argparse

from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.icite.run import PmidCite
from pmidcite.cli.utils import get_outfile
from pmidcite.cli.utils import get_pmids


class NIHiCiteCli:
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
        dir_pmid_py = self.pmidcite.cfgparser.cfgparser['pmidcite']['dir_pmid_py']
        dir_pubmed_txt = self.pmidcite.cfgparser.cfgparser['pmidcite']['dir_pubmed_txt']
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
            help='Write current citation report to an ASCII text file.')
        parser.add_argument(
            '-f', '--force_write', action='store_true',
            help='if an existing outfile file exists, overwrite it.')
        parser.add_argument(
            '-D', '--force_download', action='store_true',
            help='Download PMID iCite information to a Python file, over-writing if necessary.')
        parser.add_argument(
            '--dir_pmid_py', default=dir_pmid_py,
            help='Write PMID iCite information into directory (default={D})'.format(D=dir_pmid_py))
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
            '--dir_pubmed_txt', default=dir_pubmed_txt,
            help='Write PubMed entry into directory (default={D})'.format(D=dir_pubmed_txt))
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
        self.pmidcite.dir_pmid_py = args.dir_pmid_py
        dnldr = self.get_icite_downloader(args.force_download, args.no_references)
        pmids = get_pmids(args.pmids, args.infile)
        pmid2icitepaper = dnldr.get_pmid2paper(pmids, not args.no_references, None)
        self.run_icite(pmid2icitepaper, dnldr, args, argparser)
        # pylint:disable=line-too-long
        if args.pubmed:
            pmid_nt_list = self.pubmed.get_pmid_nt_list(pmids, args.force_download, args.dir_pubmed_txt)
            self.pubmed.dnld_wr1_per_pmid(pmid_nt_list)

    def run_icite(self, pmid2icitepaper, dnldr, args, argparser, pmid2note=None):
        """Run iCite/PubMed"""
        print('ICITE ARGS: ../pmidcite/src/pmidcite/cli/icite.py', args)
        # Print rcfile initialization file
        if args.generate_rcfile:
            self.pmidcite.prt_rcfile(sys.stdout)
        # Get user-specified PMIDs
        if not pmid2icitepaper and not args.print_keys:
            argparser.print_help()
            self._prt_infiles(args.infile)
        self._run_icite(pmid2icitepaper, args, pmid2note, dnldr)

    @staticmethod
    def _prt_infiles(infiles):
        """Print input files"""
        if infiles:
            for fin in infiles:
                print('**ERROR: NO PMIDs found in: {F}'.format(F=fin))

    @staticmethod
    def _run_icite(pmid2icitepaper, args, pmid2note, dnldr):
        """Print papers, including citation counts"""
        if args.print_keys:
            dnldr.prt_keys()
        dct = get_outfile(args.outfile, args.append_outfile, args.force_write)
        prt_verbose = not args.succinct
        if dct['outfile'] is None:
            dnldr.prt_papers(pmid2icitepaper, prt=sys.stdout, prt_assc_pmids=prt_verbose, pmid2note=pmid2note)
        else:
            if not args.quiet:
                dnldr.prt_papers(pmid2icitepaper, prt=sys.stdout, prt_assc_pmids=prt_verbose)
            # pylint: disable=line-too-long
            dnldr.wr_papers(dct['outfile'], dct['force_write'], pmid2icitepaper, dct['mode'], pmid2note)

    def get_icite_downloader(self, force_download, no_references):
        """Get iCite downloader"""
        return self.pmidcite.get_icitedownloader(force_download, no_references, prt=None)

    #def _get_pmid2icitepaper(self, pmids, args):
    #    """Get pmid2icitepaper"""
    #    dnldr = self.pmidcite.get_icitedownloader(args.force_download, args.no_references, prt=None)
    #    if args.print_keys:
    #        dnldr.prt_keys()
    #    dct = get_outfile(args.outfile, args.append_outfile, args.force_write)
    #    prt_verbose = not args.succinct
    #    return dnldr.get_pmid2paper(pmids, not args.no_references, pmid2note)


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
