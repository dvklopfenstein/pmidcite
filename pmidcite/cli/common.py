"""Code used by more than one module"""

__copyright__ = "Copyright (C) 2019, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"



def _add_force_write(parser):
    parser.add_argument(
        '-f', '--force_write', action='store_true',
        help='if an existing outfile file exists, overwrite it.')

def _add_force_download(parser):
    parser.add_argument(
        '-D', '--force_download', action='store_true',
        help='Download PMID iCite information to a Python file, over-writing if necessary.')

def _add_pmids(parser):
    parser.add_argument(
        'pmids', metavar='PMID', type=int, nargs='*',
        help='PubMed IDs (PMIDs)')

def _add_infile(parser):
    parser.add_argument(
        '-i', '--infile', nargs='*',
        help='Read PMIDs from a file containing one PMID per line.')

ADD_ARG = {
    'pmids':          _add_pmids,
    'infile':         _add_infile,
    'force_write':    _add_force_write,
    'force_download': _add_force_download,
}

def add_args(parser, args):
    """Add arguments to a parser"""
    for arg in args:
        if arg in ADD_ARG:
            ADD_ARG[arg](parser)



# Copyright (C) 2019, DV Klopfenstein, PhD. All rights reserved."
