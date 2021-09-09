#!/usr/bin/env python3
"""Test the icite command-line options"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from os import system
from os.path import join
from sys import argv
import filecmp

from pmidcite.cli.icite import NIHiCiteCli  # get_argparser
from pmidcite.cfg import get_cfgparser
from tests.icite import mk_dir
from tests.icite import DIR_ICITE
from tests.icite import DIR_REPO
from tests.icite import DIR_TEST
from tests.args_dflt import ARGS

# DDDDDDDDDDDDDDDDDDDDDDDDDD
# !!!!!!!!!!!!!!!!!!!!!!!!!!


def test_cli_icite():
    """Test the icite command-line options"""
    args = ARGS
    print(args)

    # icite
    # pylint: disable=protected-access
    obj = NIHiCiteCli(get_cfgparser())
    argparser = obj.get_argparser()
    obj._run(args, argparser)

    # icite 29129787 29628312
    # icite 29129787 29628312 -H
    # icite 29129787 29628312 -O; wc -l 29129787.txt; wc -l 29628312.txt
    # icite 29129787 29628312 -O -H; wc -l 29129787.txt; wc -l 29628312.txt
    # icite 29129787 29628312 -O -H -c; wc -l 29129787.txt; wc -l 29628312.txt
    # icite 29129787 29628312 -O -H -r; wc -l 29129787.txt; wc -l 29628312.txt

    # icite 29129787 29628312 -O -H -v; wc -l 29129787.txt; wc -l 29628312.txt
    mk_dir(DIR_ICITE, rmdir=True)
    print('SET FROM TEST')

    # WROTE: /cygdrive/c/Users/note2/Data/git/pmidcite/src/tests/./icite/29129787.txt
    # WROTE: /cygdrive/c/Users/note2/Data/git/pmidcite/src/tests/./icite/29628312.txt
    system('icite 29129787 29628312 -O -H -v --dir_icite {}'.format(DIR_ICITE))

    # WROTE: /cygdrive/c/Users/note2/Data/git/pmidcite/29129787.txt
    # WROTE: /cygdrive/c/Users/note2/Data/git/pmidcite/29628312.txt
    system('icite 29129787 29628312 -O -H -v --dir_icite {}'.format(DIR_REPO))

    assert filecmp.cmp(join(DIR_REPO, '29129787.txt'), join(DIR_ICITE, '29129787.txt'))
    assert filecmp.cmp(join(DIR_REPO, '29628312.txt'), join(DIR_ICITE, '29628312.txt'))

    # icite 29129787 29628312 -O -H
    # WROTE: /cygdrive/c/Users/note2/Data/git/pmidcite/29129787.txt
    system('icite 29129787 -O -H --dir_icite {}'.format(DIR_REPO))
    assert not filecmp.cmp(join(DIR_REPO, '29129787.txt'), join(DIR_ICITE, '29129787.txt'))
    print('**PASSED')

def _get_args_dflt(obj, argparser):
    """Get icite default args"""
    # pylint: disable=protected-access
    args = obj._get_args(argparser)
    print(args)
    for argname in dir(args):
        if argname[:1] != '_':
            print('{:15} {}'.format(argname, getattr(args, argname)))
    return args

def _wr_args():
    """Write an args object"""
    fout_py = join(DIR_TEST, 'args_dflt.py')
    obj = NIHiCiteCli(get_cfgparser())
    argparser = obj.get_argparser()
    args = _get_args_dflt(obj, argparser)
    print(args)
    with open(fout_py, 'w') as prt:
        prt.write('"""Default icite arguments"""\n\n')
        prt.write('from argparse import Namespace\n\n')
        prt.write('# pylint: disable=line-too-long\n')
        prt.write('ARGS = {}\n'.format(args))
        print('  WROTE: {ARGS}\n'.format(ARGS=fout_py))



# O               False
# append_outfile  None
# outfile         None

# force_download  False
# force_write     False
# infile          None
# md              False

# verbose         False
# load_citations  False
# load_references False
# no_references   False

# pmids           []
# pubmed          False



# dir_icite       None
# dir_icite_py    None
# dir_pubmed_txt  None

# min1            2.1
# min2            15.7
# min3            70.0
# min4            97.5

# generate_rcfile False
# print_header    False
# print_keys      False


if __name__ == '__main__':
    if len(argv) != 1:
        _wr_args()
    else:
        test_cli_icite()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
