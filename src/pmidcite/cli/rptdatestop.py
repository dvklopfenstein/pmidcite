"""Report the date each TOP line was added in an iCite report file"""

__copyright__ = "Copyright (C) 2020-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
import collections as cx
import re
from datetime import datetime
from subprocess import Popen
from subprocess import PIPE
from argparse import ArgumentParser


# pylint: disable=too-few-public-methods
class RptDatesTop:
    """Report the date each TOP line was added in an iCite report file"""
    # Dates are retrieved using: git blame -L 1,+1 lit.txt

    datecmp = re.compile(r' (\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')
    weekdays = ['M', 'T', 'W', 'X', 'F', 'S', 'U']

    def __init__(self):
        self.argparser = self._init_argparser()

    @staticmethod
    def _init_argparser():
        """Add args to link pubs and iCite/PubMed"""
        parser = ArgumentParser(
            description='Report the date each paper was appended to an iCite report')
        parser.add_argument(
            'iCite_files', type=str, nargs='+',
            help='an integer for the accumulator')
        return parser

    def cli(self):
        """Run iCite/PubMed/pubs"""
        # Arguments
        args = self.argparser.parse_args()
        ## print('ARGS iCite FILE DATE-REPORTER:', args.iCite_files)
        if args.iCite_files:
            nts = self._get_line_numbers_all(args.iCite_files)
            self._prt_nts(nts)
        else:
            print('**NOTE: Please provide a file created using icite')

    @staticmethod
    def _prt_nts(nts, prt=sys.stdout):
        """Print the date when each paper was added to the iCite file"""
        pat = '{D} {DATE} {LINE}'
        for ntd in nts:
            txt = pat.format(
                D=ntd.day,
                # https://docs.python.org/2/library/datetime.html
                DATE=ntd.dateobj.strftime('%Y-%m-%d'),
                LINE=ntd.line)
            prt.write(txt)

    def _get_line_numbers_all(self, icite_files, prt=sys.stdout):
        """Get the filename and line numbers for all iCite files"""
        nts_all = []
        for fin_icite in icite_files:
            nts_file = self._get_line_numbers_one(fin_icite, prt)
            if nts_file:
                nts_all += nts_file
        return nts_all

    def _get_line_numbers_one(self, icite_file, prt=sys.stdout):
        """Get the filename and line numbers for one iCite file"""
        if not os.path.exists(icite_file):
            return []
        nts = []
        nto = cx.namedtuple('Nt', 'day dateobj lnum line filename')
        with open(icite_file) as ifstrm:
            s_weekdays = self.weekdays
            s_get_date = self._get_date
            for lnum, line in enumerate(ifstrm, 1):
                if line[:4] == 'TOP ':
                    dateobj = s_get_date(lnum, icite_file)
                    if dateobj is not None:
                        ntd = nto(
                            day=s_weekdays[dateobj.weekday()],
                            dateobj=dateobj,
                            lnum=lnum,
                            line=line,
                            filename=icite_file)
                        print(ntd)
                        nts.append(ntd)
            if prt:
                prt.write('{N:6} TOP papers READ: {FIN}'.format(N=len(nts), FIN=icite_file))
        return nts

    def _get_date(self, lnum, filename):
        """Get the date the line was changed"""
        popenargs = ['git', 'blame', '-L', '{LNUM},+1'.format(LNUM=lnum), filename]
        ## print(' '.join(popenargs))
        blame, _ = Popen(popenargs, stdout=PIPE).communicate() # _ err
        blame = blame.decode("utf-8")
        mtch = self.datecmp.search(blame)
        if mtch:
            numbers = [int(n) for n in mtch.groups()]
            return datetime(*numbers)
            ## print(blame, self.weekdays[timestamp.weekday()], timestamp)
        return None


# Copyright (C) 2020-present DV Klopfenstein. All rights reserved.
