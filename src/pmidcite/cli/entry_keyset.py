"""Read a file created by pmidcite and write simple text file of PMIDs"""

__copyright__ = "Copyright (C) 2021-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from pmidcite.icite.entry import NIHiCiteEntry


def get_details_cites_refs(verbose, load_citations, load_references, no_references):
    """Optionally download and print citations and/or references of a specified papers"""
    # If verbose, download and print all citations and references
    if verbose:
        details_cites_refs = set(NIHiCiteEntry.associated_pmid_keys)
        # TBD: obsolete no_references
        if no_references:
            details_cites_refs = details_cites_refs.difference(NIHiCiteEntry.refkey)
        return details_cites_refs
    details_cites_refs = set()
    if load_citations:
        details_cites_refs.update(NIHiCiteEntry.citekeys)
    if load_references:
        details_cites_refs.update(NIHiCiteEntry.refkey)
    # TBD: obsolete no_references
    if no_references:
        details_cites_refs = details_cites_refs.difference(NIHiCiteEntry.refkey)
    return details_cites_refs


# Copyright (C) 2021-present DV Klopfenstein. All rights reserved.
