#!/usr/bin/env python3
"""Test for errors upon download for papers with huge numbers of citations"""

from timeit import default_timer
from pmidcite.icite.dnldr.pmid_dnlder_only import NIHiCiteDownloaderOnly
from tests.prt_hms import prt_hms


def test_missing_keys():
    """Test for errors upon download for papers with huge numbers of citations"""
    pmids = [
        30022098,  #   740   1  23 au[14](Klopfenstein) GOATOOLS
        10802651,  # 29685 130  32 au[20](Ashburner) Gene ontology
    ]
    details_cites_refs = {'cited_by_clin', 'cited_by', 'references'}

    ##dnldr = NIHiCiteDownloaderOnly(details_cites_refs='all')
    tic = default_timer()

    # Separate functions in NIHiCiteDownloaderOnly to gain access to nihdicts from NIH-OCC
    dldr = NIHiCiteDownloaderOnly(details_cites_refs)
    entries_all = []
    for pmid in pmids:
        if (entries_cur := _run_pmid(pmid, dldr)):
            entries_all.extend(entries_cur)
            prt_hms(tic, f"Downloaded {len(entries_cur):,} items for PMID({pmid})")
    assert not dldr.api.msgs, _get_errstr(dldr)
    prt_hms(tic, f"Downloaded {len(entries_all):,} TOTAL OF {len(pmids)} PMIDS")

def _run_pmid(pmid, dldr):
    pmids = [pmid]
    pmid2paper = dldr.get_pmid2paper(pmids)
    assert pmid2paper, 'FATAL: EXPECTED A NIHPaper TO BE CREATED FOR PMID({pmid})'
    assert pmid in pmid2paper
    #dldr.prt_papers(pmid2paper, prt=sys.stdout)
    return pmid2paper[pmid].pmid2icite.values()

def _get_errstr(dldr):
    txt = []
    for idx, err in enumerate(dldr.api.msgs):
        txt.append(f'ERROR {idx}) {err[:100]} ...')
    txt.append(f'{len(dldr.api.msgs)} TOTAL API ERRORS')
    return '\n'.join(txt)


if __name__ == '__main__':
    test_missing_keys()

# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
