"""Manage args for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import stdout
import argparse

from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.cfgini import prt_rcfile
from pmidcite.cli.utils import get_outfile
from pmidcite.cli.utils import get_pmids
from pmidcite.cli.entry_keyset import get_details_cites_refs
from pmidcite.icite.nih_grouper import NihGrouper
from pmidcite.icite.downloader import get_downloader
from pmidcite.icite.downloader import prt_hdr
from pmidcite.icite.downloader import prt_keys


class NIHiCiteCli:
    """Manage args for NIH iCite run for one PubMed ID (PMID)"""

    def __init__(self, cfg):
        self.cfg = cfg
        self.pubmed = PubMed(
            email=cfg.get_email(),
            apikey=cfg.get_apikey(),
            tool=cfg.get_tool())

    def get_argparser(self):
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        parser = argparse.ArgumentParser(
            description="Run NIH's iCite given PubMed IDs",
            add_help=False)
        cfg = self.cfg
        dflt_dir_icite_py = cfg.get_dir_icite_py()
        dflt_dir_icite = cfg.get_dir_icite()
        dflt_dir_pubmed_txt = cfg.get_dir_pubmed_txt()
        # https://docs.python.org/3/library/argparse.html
        # https://docs.python.org/3/library/argparse.html#action
        # - PMIDs ----------------------------------------------------------------------------
        parser.add_argument(
            '-h', '--help', action='store_true',
            help='print this help message and exit (also --help)')
        parser.add_argument(
            'pmids', metavar='PMID', type=int, nargs='*',
            help='PubMed IDs (PMIDs)')
        parser.add_argument(
            '-i', '--infile', nargs='*',
            help='Read PMIDs from a file containing one PMID per line.')
        # - help -----------------------------------------------------------------------------
        parser.add_argument(
            '-H', '--print_header', action='store_true',
            help='Print column headings on one line.')
        parser.add_argument(
            '-k', '--print_keys', action='store_true',
            help='Print the keys describing the abbreviations.')
        # - verbosity ------------------------------------------------------------------------
        parser.add_argument(
            '-v', '--verbose', action='store_true', default=False,
            help='Load and print a descriptive list of citations and references for each paper.')
        parser.add_argument(
            '-c', '--load_citations', action='store_true', default=False,
            help='Load and print a descriptive list of citations for each paper.')
        parser.add_argument(
            '-r', '--load_references', action='store_true', default=False,
            help='Load and print a descriptive list of references for each paper.')
        # pylint: disable=line-too-long
        parser.add_argument(
            '-R', '--no_references', action='store_true',
            help='(DEPRECATED) Do not load or print a descriptive list of references. DEPRECATED -- Use instead: -c -r')
        # - output ---------------------------------------------------------------------------
        parser.add_argument(
            '-a', '--append_outfile',
            help='Append current citation report to an ASCII text file. Create if needed.')
        parser.add_argument(
            '-o', '--outfile',
            help='Write current citation report to an ASCII text file.')
        parser.add_argument(
            '-O', action='store_true',
            help="Write each PMIDs' iCite report with citations/references to <dir_icite>/PMID.txt")
        parser.add_argument(
            '-f', '--force_write', action='store_true',
            help='if an existing outfile file exists, overwrite it.')
        parser.add_argument(
            '-D', '--force_download', action='store_true',
            help='Download PMID iCite information to a Python file, over-writing if necessary.')
        # - abstracts -------------------------------------------------------------------------
        parser.add_argument(
            '-p', '--pubmed', action='store_true',
            help='Download PubMed entry containing title, abstract, authors, journal, MeSH, etc.')
        self.cfg.get_nihgrouper().add_arguments(parser)
        # - directories ----------------------------------------------------------------------
        # pylint: disable=line-too-long
        parser.add_argument(
            '--dir_icite_py', default=dflt_dir_icite_py,
            help='Write PMID iCite information into directory which contains temporary working files (default={D})'.format(
                D=dflt_dir_icite_py))
        parser.add_argument(
            '--dir_icite', default=dflt_dir_icite,
            help='Write PMID icite reports into directory (default={D})'.format(D=dflt_dir_icite))
        parser.add_argument(
            '--dir_pubmed_txt', default=dflt_dir_pubmed_txt,
            help='Write PubMed entry into directory (default={D})'.format(D=dflt_dir_pubmed_txt))
        # ------------------------------------------------------------------------------------
        parser.add_argument(
            '--md', action='store_true',
            help='Print using markdown table format.')
        # - initialization -------------------------------------------------------------------
        parser.add_argument(
            '--generate-rcfile', action='store_true',
            help='Generate a sample configuration file according to the '
                 'current configuration.')
        parser.add_argument(
            '--print-rcfile', action='store_true',
            help='Print the location of the pmidcite configuration file')
        return parser

    def cli(self):
        """Run iCite/PubMed using command-line interface"""
        argparser = self.get_argparser()
        args = self._get_args(argparser)
        ## print('ICITE ARGS ../pmidcite/src/pmidcite/cli/icite.py', args)
        self._run(args, argparser)

    def _run(self, args, argparser):
        """Run iCite/PubMed using command-line interface"""
        if args.help:
            argparser.print_help()
            print('\nHelp message printed because: -h or --help == True')
            exit()
        self.prt_info(args)
        # Get a list of researcher-specified PMIDs
        pmids = get_pmids(args.pmids, args.infile)
        if pmids:
            if len(pmids) > 10:
                print('PROCESSING {N:,} PMIDs'.format(N=len(pmids)))
            dnldr = self._get_downloader(args)
            pmid2icitepaper = dnldr.get_pmid2paper(pmids, None)
            ## print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX pmid2icitepaper', pmid2icitepaper)
            self.run_icite(pmid2icitepaper, dnldr, args, argparser)
            if args.pubmed:
                self.pubmed.dnld_wr1_per_pmid(pmids, args.force_download, args.dir_pubmed_txt)
        # pylint: disable=line-too-long
        elif not (args.generate_rcfile or args.print_keys or args.print_header or args.print_rcfile):
            argparser.print_help(stdout)

    def prt_info(self, args):
        """Print helpful information"""
        # If writing to a file, don't write to stdout
        if args.O or args.append_outfile or args.outfile:
            return
        # Print rcfile initialization file
        if args.print_rcfile:
            self.cfg.prt_cfgfile()
        if args.generate_rcfile:
            prt_rcfile(stdout)
        self._prt_keys_n_hdr(stdout, args.print_keys, args.print_header)

    @staticmethod
    def _prt_keys_n_hdr(prt, print_keys, print_header):
        # Print the keys and/or the header
        if print_keys:
            prt_keys(prt)
        if print_header:
            prt_hdr(prt)

    @staticmethod
    def _get_downloader(args):
        """Get the downloader"""
        details_cites_refs = get_details_cites_refs(
            args.verbose,
            args.load_citations,
            args.load_references,
            args.no_references)
        groupobj = NihGrouper(args.min1, args.min2, args.min3, args.min4)
        return get_downloader(
            details_cites_refs,
            groupobj,
            args.dir_icite_py,
            args.force_download)

    def _get_args(self, argparser):
        """Get args"""
        args = argparser.parse_args()
        self.cfg.set_dir_icite_py(args.dir_icite_py)
        self.cfg.set_dir_icite(args.dir_icite)
        # append_outfile:
        #   * Append TOP, CIT, CLI, and REF into file if it is not already present
        #   * Print TOP to the screen
        if args.append_outfile:
            args.load_citations = True
            args.load_references = True
        return args

    # pylint: disable=too-many-arguments
    def run_icite(self, pmid2icitepaper_all, dnldr, args, argparser):
        """Run iCite/PubMed"""
        pmid2icitepaper_cur = self.run_icite_pre(pmid2icitepaper_all, args, argparser)
        if not pmid2icitepaper_cur:
            dnldr.prt_api_msgs()
            return
        # Write the report with citations and references for each PMID into its own file
        if args.O:
            self._wr_papers(pmid2icitepaper_cur, dnldr, args.print_header)
        # Write the succinct report each PMID to the screen
        else:
            self.run_icite_wr(pmid2icitepaper_cur, args, dnldr)

    def run_icite_pre(self, pmid2icitepaper_all, args, argparser):
        """Run iCite/PubMed"""
        ## print('ALL', pmid2icitepaper_all)
        if not pmid2icitepaper_all and not args.print_keys and not args.print_header:
            argparser.print_help()
            self._prt_infiles(args.infile)
        pmid2icitepaper_cur = {p: o for p, o in pmid2icitepaper_all.items() if o is not None}
        if not pmid2icitepaper_cur:
            # pylint: disable=line-too-long
            self._prt_no_icite(set(pmid2icitepaper_all.keys()).difference(pmid2icitepaper_cur.keys()))
            return {}
        return pmid2icitepaper_cur

    @staticmethod
    def _prt_infiles(infiles):
        """Print input files"""
        if infiles:
            for fin in infiles:
                print('**ERROR: NO PMIDs found in: {F}'.format(F=fin))

    @staticmethod
    def run_icite_wr(pmid2icitepaper, args, dnldr):
        """Print papers, including citation counts"""
        dct = get_outfile(args.outfile, args.append_outfile, args.force_write)
        if dct['outfile'] is None and not args.O:
            dnldr.prt_papers(pmid2icitepaper, prt=stdout)
        else:
            if args.verbose:
                dnldr.prt_papers(pmid2icitepaper, prt=stdout)
            elif args.append_outfile:
                # Print TOP to stdout if append_outfile
                for icitepaper in pmid2icitepaper.values():
                    icitepaper.prt_top(prt=stdout)
            if dct['outfile'] is not None:
                dnldr.wr_papers(dct['outfile'], pmid2icitepaper, dct['force_write'], dct['mode'])

    def _wr_papers(self, pmid2icitepaper, dnldr, print_header):
        """Write one icite report per PMID into dir_icite/PMID.txt"""
        for pmid, paper in pmid2icitepaper.items():
            fout_txt = self.cfg.get_fullname_icite('{PMID}.txt'.format(PMID=pmid))
            with open(fout_txt, 'w') as prt:
                if print_header:
                    prt_hdr(prt)
                dnldr.prt_papers({pmid:paper}, prt)
                print('  WROTE: {TXT}'.format(TXT=fout_txt))

    @staticmethod
    def _prt_no_icite(pmids):
        if not pmids:
            return
        print('**NOTE: No NIH iCite papers found for: {Ps}'.format(
            Ps=' '.join(str(p) for p in pmids)))


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
