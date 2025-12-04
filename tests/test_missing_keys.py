#!/usr/bin/env python3
"""Test speed for download NIH citation data"""

from timeit import default_timer
from pmidcite.icite.api import NIHiCiteAPI
from pmidcite.icite.nih_grouper import NihGrouper
from pmidcite.icite.entry import NIHiCiteEntry
from pmidcite.icite.paper import NIHiCitePaper
from tests.prt_hms import prt_hms

# NIH-OCC does not document which fields may be missing
#   Currently believe that commented out fields are always present
NIH_FIELDS_ALWAYS = {
    "pmid",
    "is_clinical",
    "molecular_cellular",
    "human",
    "animal",
    "_id",
}

NIH_FIELDS = [
    #"_id",
    "authors",
    "doi",
    "pmid",
    "title",
    #"animal",
    "apt",
    #"human",
    "citedByPmidsByYear",
    "citedByClinicalArticle",
    "year",
    "journal",
    "is_research_article",
    "citation_count",
    "field_citation_rate",
    "expected_citations_per_year",
    "citations_per_year",
    "relative_citation_ratio",
    "nih_percentile",
    #"molecular_cellular",
    "x_coord",
    "y_coord",
    #"is_clinical",
    "cited_by_clin",
    "cited_by",
    "references",
    "provisional",
]


def test_missing_keys():
    """Test speed for download NIH citation data"""
    pmids = [
        30022098,  #   740   1  23 au[14](Klopfenstein) GOATOOLS
        #10802651,  # 29685 130  32 au[20](Ashburner) Gene ontology
    ]

    tic = default_timer()
    # Separate functions in NIHiCiteDownloaderOnly to gain access to nihdicts from NIH-OCC
    api = NIHiCiteAPI()
    grpr = NihGrouper()
    for pmid in pmids:
        _run_pmid(pmid, api, grpr)
    tic = prt_hms(tic, f"Downloaded {len(pmids):,} items w/dnld_icites")

def _run_pmid(pmid, api, grpr):
    nihdicts = api.dnld_nihdicts([pmid])
    assert len(nihdicts) == 1
    _prt_dcts(nihdicts)
    nihdct = nihdicts[0]
    print('\nTEST PRINTING NIH DICT AS DOWNLOADED BY `api`:')
    _run_nihdct(pmid, nihdct, grpr)
    for fld in NIH_FIELDS:
        if fld not in NIH_FIELDS_ALWAYS and fld in nihdct:
            print(f'\nTEST RM FLD({fld}):')
            nihcp = nihdct.copy()
            del nihcp[fld]
            _run_nihdct(pmid, nihcp, grpr)

def _run_nihdct(pmid, nihdct, grpr):
    nih_perc = nihdct.get('nih_percentile')
    grp_num = grpr.get_group(nih_perc)
    entry = NIHiCiteEntry.from_jsondct(nihdct, grp_num)
    paper = NIHiCitePaper(pmid, {pmid:entry})
    print(paper)



def _prt_dcts(dcts):
    for dct in dcts:
        _prt_dct(dct)

def _prt_dct(dct):
    for key, val in dct.items():
        ##print(f'    "{key}",')
        if key not in {'cited_by', 'citedByPmidsByYear'}:
            print(f'{key:27}: {val}')
        else:
            print(f'{key}[{len(val)}]')


if __name__ == '__main__':
    test_missing_keys()

# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
