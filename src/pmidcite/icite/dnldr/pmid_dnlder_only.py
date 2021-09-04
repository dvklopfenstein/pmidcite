"""Given a PubMed ID (PMID), download a list of publications which cite and reference it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from pmidcite.icite.dnldr.pmid_dnlder_base import NIHiCiteDownloaderBase
from pmidcite.icite.entry import NIHiCiteEntry


class NIHiCiteDownloaderOnly(NIHiCiteDownloaderBase):
    """Given a PubMed ID (PMID), download a list of publications which cite and reference it"""

    ##def __init__(self, details_cites_refs=None, nih_grouper=None):
    ##    super(NIHiCiteDownloaderOnly, self).__init__(details_cites_refs, nih_grouper)

    def get_icites(self, pmids):
        """Download NIH iCite data for requested PMIDs"""
        pmid2nihentry = {o.pmid: o for o in self._dnld_icites(pmids)}
        return [pmid2nihentry[pmid] for pmid in pmids if pmid in pmid2nihentry]

    def _dnld_icites(self, pmids):
        """Download a list of NIH citation data for PMIDs"""
        nihdicts = self.api.dnld_nihdicts(pmids)
        if nihdicts:
            s_get_group = self.nihgrouper.get_group
            return [NIHiCiteEntry(d, s_get_group(d['nih_percentile'])) for d in nihdicts]
        return []

    def get_icite(self, pmid):
        """Load or download NIH iCite data for requested PMID"""
        nih_dict = self.api.dnld_nihdict(pmid)
        if nih_dict:
            return NIHiCiteEntry(
                nih_dict,
                self.nihgrouper.get_group(nih_dict['nih_percentile']))
        return None


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
