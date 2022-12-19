"""Summarize NIH citation data for requested papers from the commandline or in files"""

from sys import stdout
from argparse import ArgumentParser
from pmidcite.cli.utils import prt_loc_rcfile
from pmidcite.cli.utils import get_files_exists
from pmidcite.summarize_papers import SummarizePapers

__copyright__ = "Copyright (C) 2022-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"


class SummarizePapersCli:
    """Summarize NIH citation data for requested papers from the commandline or in files"""

    def __init__(self, cfg):
        self.cfg = cfg

    def get_argparser(self):
        """Argument parser for summarizing the citations on set(s) of papers"""
        parser = ArgumentParser(
            description="Summarize NIH's citation on a set(s) of papers",
            add_help=False)
        ##cfg = self.cfg
        # https://docs.python.org/3/library/argparse.html
        # https://docs.python.org/3/library/argparse.html#action
        # - PMIDs ----------------------------------------------------------------------------
        parser.add_argument(
            '-h', '--help', action='store_true',
            help='print this help message and exit (also --help)')
        parser.add_argument(
            'files', metavar='FILES', type=str, nargs='*',
            help='File(s) containing NIH citation data for numerous papers with PMIDs')
        ##parser.add_argument(
        ##    '-i', '--infile', nargs='*',
        ##    help='Files containing NIH citation data for numerous papers with PMIDs')
        ##parser.add_argument(
        ##    '-o', '--outfile',
        ##    help='Write current citation report to an ASCII text file.')
        ##parser.add_argument(
        ##    '-f', '--force_write', action='store_true',
        ##    help='if an existing outfile file exists, overwrite it.')

        self.cfg.get_nihgrouper().add_arguments(parser)
        ##parser.add_argument(
        ##    '--md', action='store_true',
        ##    help='Print using markdown table format.')
        parser.add_argument(
            '--print-rcfile', action='store_true',
            help='Print the location of the pmidcite configuration file (env var: PMIDCITECONF)')
        return parser


    def cli(self):
        """Run citation summary on a set(s) of PMIDs"""
        argparser = self.get_argparser()
        args = argparser.parse_args()
        print('ARGS CITE SUMMARY ../pmidcite/src/pmidcite/cli/summarize_papers.py', args)
        if args.print_rcfile:
            prt_loc_rcfile(self.cfg, stdout)
            return
        files = get_files_exists(args.files)
        if args.help or not files:
            argparser.print_help()
            print('\nHelp message printed because: -h or --help == True')
            return
        ##self._run(args, argparser)
        nih_grouper = self.cfg.get_nihgrouper()
        for filename in files:
            sumpap = SummarizePapers.from_file(filename, nih_grouper)
            print(sumpap.str_oneline())
        return


# Copyright (C) 2022-present, DV Klopfenstein, PhD. All rights reserved.
