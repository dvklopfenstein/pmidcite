#!/usr/bin/env python3
"""Given a user query, query PubMed and return PMIDs. Then run NIH's iCite on the PMIDs"""

__copyright__ = "Copyright (C) 2020-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

import sys
import os
import os.path as op
from pmidcite.pubmedqueryicite import PubMedQueryToICite


def main():
    """Download PMIDs returned for a PubMed query. Write an iCite report for each PMID"""
    queries = [
        # Output filenames               PubMed query
        # -----------------              -----------------------------------
        ('systematic_review.txt',        'systematic review AND "how to"[TI]'),
        ('rarely_seen_killer_whale.txt', 'Orcinus Orca Type D'),
    ]

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
    obj = PubMedQueryToICite(force_dnld=True)
    dnld_idx = obj.get_index(sys.argv, queries)

    nts_fout_query = obj.get_nts_g_list(queries)
    if dnld_idx == [-1]:
        qry = nts_fout_query[-1]
        cmd = f'grep TOP {op.relpath(qry.fullname)} | sort -k6'
        os.system(cmd)
        print(f'QRY: {qry.pubmed_query}')
        print(f'CMD: {cmd}')


if __name__ == '__main__':
    main()

# Copyright (C) 2020-present DV Klopfenstein, PhD. All rights reserved.
