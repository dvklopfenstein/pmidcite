#!/usr/bin/env python3
"""Given a user query, query PubMed and return PMIDs. Then run NIH's iCite on the PMIDs"""

__copyright__ = "Copyright (C) 2020-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from os import system
from os.path import join
from os.path import exists

from pmidcite.pubmedqueryicite import PubMedQueryToICite

from tests.icite import DIR_REPO


def main():
    """Download PMIDs returned for a PubMed query. Write an iCite report for each PMID"""
    # pylint: disable=bad-whitespace,line-too-long
    queries = [
        # Output filenames         PubMed query
        # -----------------       -----------------------------------
        ('SMILES_review.txt',     'Simplified molecular-input line-entry system AND (review[Filter])'),
    ]
    filename = join(DIR_REPO, queries[-1][0])

    # By default, only the last entry in the list is run.
    # This allows you to build a history of searches,
    # but not run all of them every time.
    #
    # To re-run all entries in the list:
    #   $ src/bin/dnld_pmids.py all
    #
    # To run the first query:
    #   $ src/bin/dnld_pmids.py 0
    #
    # To run the second to last query:
    #   $ src/bin/dnld_pmids.py -2
    #
    system('rm -f {}'.format(filename))
    assert not exists(filename)
    obj = PubMedQueryToICite(force_dnld=True, prt_icitepy=None)
    obj.cfg.set_dir_pmids(DIR_REPO)
    obj.cfg.set_dir_icite(DIR_REPO)
    dnld_idx = obj.get_index(sys.argv)
    obj.run(queries, dnld_idx)
    assert exists(filename)
    print('**PASSED: DIR=repo\n')

    system('rm -f {}'.format(filename))
    assert not exists(filename)
    obj.cfg.set_dir_pmids(None)
    obj.cfg.set_dir_icite(None)
    obj.run(queries, dnld_idx)
    print('**PASSED: DIR=None\n')

    system('rm -f {}'.format(filename))
    assert not exists(filename)
    obj.cfg.set_dir_pmids('.')
    obj.cfg.set_dir_icite('.')
    obj.run(queries, dnld_idx)
    print("**PASSED: DIR='.'\n")


if __name__ == '__main__':
    main()

# Copyright (C) 2020-present DV Klopfenstein. All rights reserved.
