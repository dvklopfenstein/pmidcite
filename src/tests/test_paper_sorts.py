#!/usr/bin/env python3
"""Test various sorts of papers"""
# TBD Add assertions

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"


from tests.icite import ICiteTester

def test_paper_sort():
    """Test various sorts of papers"""
    pmid = 22882545

    # Clean iCite files
    obj = ICiteTester()
    obj.rm_icitefiles()

    # iCite files are downloaded with the first call
    paper = obj.get_paper(pmid, do_prt=False)  # NIHiCitePaper
    all_cites = paper.cited_by.union(paper.cited_by_clin)

    print('\nDEFAULT SORT')
    for nih_entry in sorted(all_cites):
        print(nih_entry)

    print('\nSORT BY NIH PERCENTILE')
    for nih_entry in sorted(all_cites, key=lambda o: o.dct['nih_perc'], reverse=True):
        print(nih_entry)

    nih_entry = paper.pmid2icite[pmid]   # NIHiCiteEntry

    # Clean iCite files
    obj.rm_icitefiles()


if __name__ == '__main__':
    test_paper_sort()

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
