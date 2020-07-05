#!/usr/bin/env python3
"""Given a user query, query PubMed and return PMIDs. Then run NIH's iCite on the PMIDs"""

__copyright__ = "Copyright (C) 2020-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from pmidcite.pubmedqueryicite import PubMedQueryToICite


def main():
    """Download PMIDs returned from user queries. Write: ./log/pmids ./log/icite"""
    obj = PubMedQueryToICite(force_dnld=True, prt_icitepy=None)
    # pylint: disable=bad-whitespace
    queries = [
        # Output filenames      PubMed query
        # -----------------    -----------------------------------
        ('systematic_review.txt', 'systematic review AND "how to"[TI]')
    ]
    # Default is to only run the last entry in the list, index = -1
    #
    # To run all entries in the list:
    #   $ src/bin/dnld_pmids.py all
    #
    # To run the last query:
    #   $ src/bin/dnld_pmids.py -1
    #
    dnld_idx = obj.get_index(sys.argv)
    obj.run(queries, dnld_idx)


if __name__ == '__main__':
    main()

# Copyright (C) 2020-present DV Klopfenstein. All rights reserved.
