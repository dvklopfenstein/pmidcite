#!/usr/bin/env python3
"""Given DOI, download PubMed data for PMID. Print NIH iCite summary

     1) Get user-specified PMIDs
     2) Download PubMed summary to get PMID, given DOI in bib entry
     3) Print PMID downloaded from PubMed and citekey from pubs

"""

__copyright__ = "Copyright (C) 2019-2020, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from pmidcite.eutils.pubmed import PubMedQuery


def main():
    """Print lists of pubs in formation"""

    # 1) Get user-specified PMIDs
    pmids = _get_pmids()
    foutpat_pubmed = 'log/pubmed/{PMID}.txt'

    # 2) Download PubMed summary to get PMID, given DOI in bib entry
    dcts = []
    for pmid in pmids:
        file_pubmed = foutpat_pubmed.format(PMID=pmid)
        dcts.append(PubMedQuery().get_pubmed_dct(file_pubmed, pmid=pmid))

    if dcts:
        # 3) Print PMID downloaded from PubMed and citekey from pubs
        print('PMID         Citekey')
        print('------------ -------')
        for dct in dcts:
            print('{PMID:12} {TITLE}'.format(PMID=dct['PMID'], TITLE=dct['TI']))


def _get_pmids():
    """Get PubMed PMID from user"""
    if len(sys.argv) == 1:
        print('Usage: dnld_pubmed_icite [PMID] ...')
        sys.exit()
    pmids = []
    for pmid in sys.argv[1:]:
        if pmid.isdigit():
            pmids.append(pmid)
        else:
            print('PMID({PMID}) IS NOT VALID'.format(PMID=pmid))
    return pmids


if __name__ == '__main__':
    main()

# Copyright (C) 2019-2020, DV Klopfenstein. All rights reserved.
