#!/usr/bin/env python3
"""Given a user query, query PubMed and return PMIDs. Then run NIH's iCite on the PMIDs"""

__copyright__ = "Copyright (C) 2020-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from pmidcite.pubmedqueryicite import PubMedQueryToICite


def main():
    """Download PMIDs returned from user queries. Write: ./log/pmids ./log/icite"""
    obj = PubMedQueryToICite(force_dnld=True)
    # pylint: disable=bad-whitespace
    lst = [
        # Output filenames   PubMed query
        # -----------------  -----------------------------------
        ('nih_icite.txt',    'NIH iCite'),
    ]
    # Default is to only run the last entry in the list
    # To run all entries in the list:
    #   $ src/bin/dnld_pmids.py dnld_all
    dnld_idx = -1 if len(sys.argv) == 1 else None
    obj.run(lst, dnld_idx)


if __name__ == '__main__':
    main()

# Copyright (C) 2020-present DV Klopfenstein. All rights reserved.
