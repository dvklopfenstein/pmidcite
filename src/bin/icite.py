#!/usr/bin/env python3
"""Given a PubMed ID (PMID), return a list of citing publications"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from pmidcite.cli.parser_icite import get_argparser
from pmidcite.api import NIHiCiteAPI
from pmidcite.paper import NIHiCitePaper


def main(pmid=30022098, force_dnld=False):
    """Print lists of pubs in formation"""
    argparser = get_argparser()
    args = argparser.parse_args()
    print(args)
    print(args.pmids)

    for pmid in args.pmids:
        api = NIHiCiteAPI(force_dnld, 'src/nihcite/pmids', 'nihcite.pmids')

        icites = api.run_icite(pmid)
        print('{N} NIH iCite items'.format(N=len(icites)))

        paper = NIHiCitePaper(pmid, moddir='nihcite.pmids', prt=None)
        paper.prt_summary(sys.stdout, 'cite')

def _get_args():
    """Get arguments, if provided"""

if __name__ == '__main__':
    main(sys.argv[1:])

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
