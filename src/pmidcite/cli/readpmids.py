"""Read a file created by pmidcite and write simple text file of PMIDs"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from os.path import exists
import argparse

from pmidcite.cfg import get_cfgparser

## from pmidcite.eutils.cmds.pubmed import PubMed
from pmidcite.cli.entry_keyset import get_details_cites_refs
## from pmidcite.cli.utils import get_mode_force
from pmidcite.cli.utils import get_outfile
from pmidcite.cli.utils import mk_outname_icite
## from pmidcite.cli.utils import wr_pmids
from pmidcite.cli.utils import read_pmids
## from pmidcite.cli.utils import read_top_pmids

from pmidcite.icite.run import PmidCite
from pmidcite.icite.nih_grouper import NihGrouper
from pmidcite.icite.pmid_dnlder import NIHiCiteDownloader


class ReadPmids:
    """Read a file created by pmidcite and write simple text file of PMIDs"""

    def __init__(self):
        self.pmidcite = PmidCite(get_cfgparser())

    def _get_argparser(self):
        """Argument parser for Python wrapper of NIH's iCite given PubMed IDs"""
        parser = argparse.ArgumentParser(description="Run NIH's iCite given PubMed IDs")
        parser.add_argument(
            'infile', nargs='*',
            help='Read PMIDs from a pmidcite output file.')
        self.pmidcite.cfgparser.get_nihgrouper().add_arguments(parser)
        parser.add_argument(
            '-f', '--force_write', action='store_true',
            help='if an existing outfile file exists, overwrite it.')
        parser.add_argument(
            '-D', '--force_download', action='store_true',
            help='Download PMID iCite information to a Python file, over-writing if necessary.')
        parser.add_argument(
            '-o', '--outfile',
            help='Write current citation report to an ASCII text file.')
        parser.add_argument(
            '-c', '--load_citations', action='store_true', default=False,
            help='Load and print the list of citations for each paper.')
        parser.add_argument(
            '-r', '--load_references', action='store_true', default=False,
            help='Load and print the list of references for each paper.')
        parser.add_argument(
            '-R', '--no_references', action='store_true',
            help='Print the list of citations, but not the list of references.')
        return parser

    def cli(self):
        """Run iCite/PubMed using command-line interface"""
        argparser = self._get_argparser()
        args = argparser.parse_args()
        ## print('ARGS: ', args)
        pmids = self._read_pmids(args, argparser)
        # keys: outfile mode force_write
        ## dct = get_outfile(args.outfile, append_outfile, args.force_write)
        dct = get_outfile(args.outfile, None, args.force_write)
        outfile = self._get_outfile(args, dct)
        if pmids:
            self._wr_icite(outfile, pmids, args)
        else:
            print('XXX', outfile, pmids)

    def _wr_icite(self, outfile, pmids, args):
        """Write an iCite report for the provided PMIDs"""
        grouperobj = NihGrouper(args.min1, args.min2, args.min3, args.min4)
        details_cites_refs = get_details_cites_refs(
            args.verbose,
            args.load_citations,
            args.load_references,
            args.no_references)
        dnldr = NIHiCiteDownloader(
            self.pmidcite.cfgparser.get_dir_icite_py(),
            args.force_download,
            details_cites_refs,
            grouperobj)
        pmid2icitepaper_all = dnldr.get_pmid2paper(pmids, None)
        pmid2icitepaper_cur = {p: o for p, o in pmid2icitepaper_all.items() if o is not None}
        if outfile is not None:
            dnldr.wr_papers(outfile, pmid2icitepaper_cur, args.force_write, 'w')

    def _read_pmids(self, args, argparser):
        """Read PMIDs from a file"""
        ##print('ICITE ARGS: ../pmidcite/src/pmidcite/cli/icite.py', args)
        # Get user-specified PMIDs
        pmids = self.rd_pmidtxts(args.infile)
        if not pmids:
            argparser.print_help()
            print('**WARNING: NO PMIDs FOUND')
            return pmids
        return pmids

    @staticmethod
    def _get_outfile(args, dct):
        """Return outfile"""
        if dct['outfile']:
            return dct['outfile']
        if len(args.infile) == 1:
            return mk_outname_icite(args.infile[0])
        return None

    @staticmethod
    def rd_pmidtxts(fins_pmidcite):
        """Get PMIDs from the command line or from a file"""
        pmids = []
        seen = set()
        if fins_pmidcite:
            for fin in fins_pmidcite:
                if exists(fin):
                    ## TBD: for pmid in read_top_pmids(fin):
                    for pmid in read_pmids(fin):
                        if pmid not in seen:
                            pmids.append(pmid)
                            seen.add(pmid)
                else:
                    print('  MISSING: {FILE}'.format(FILE=fin))
                if len(fins_pmidcite) != 1:
                    print('{N:6} PMIDs READ'.format(N=len(pmids)))
        return pmids


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
