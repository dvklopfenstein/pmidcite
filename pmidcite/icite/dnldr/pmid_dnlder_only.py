"""Given a PubMed ID (PMID), download a list of publications which cite and reference it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019, DV Klopfenstein, PhD. All rights reserved"
__author__ = "DV Klopfenstein, PhD"

from pmidcite.icite.dnldr.pmid_dnlder_base import NIHiCiteDownloaderBase
from pmidcite.icite.entry import NIHiCiteEntry


class NIHiCiteDownloaderOnly(NIHiCiteDownloaderBase):
    """Given a PubMed ID (PMID), download a list of publications which cite and reference it"""

    ##def __init__(self, details_cites_refs=None, nih_grouper=None):
    ##    super(NIHiCiteDownloaderOnly, self).__init__(details_cites_refs, nih_grouper)

    def get_icites(self, pmids):
        """Download NIH iCite data for requested PMIDs"""
        ##print(f'DB DLLLLLLLLLLLLLLLL {len(pmids)} PMIDs')
        pmid2nihentry = {o.pmid: o for o in self._dnld_icites(pmids)}
        return [pmid2nihentry[pmid] for pmid in pmids if pmid in pmid2nihentry]

    def _dnld_icites(self, pmids):
        """Download a list of NIH citation data for PMIDs"""
        nihdicts = self.api.dnld_nihdicts(pmids)
        if nihdicts:
            ##print(f'DB NNNNNNNNNNNNNNNNNN {len(nihdicts)}')
            ##self._prt(nihdicts)
            s_get_group = self.nihgrouper.get_group
            s_from_jsondct = NIHiCiteEntry.from_jsondct
            return [s_from_jsondct(d, s_get_group(d.get('nih_percentile'))) for d in nihdicts]
        return []

    def get_icite(self, pmid):
        """Load or download NIH iCite data for requested PMID"""
        ##print(f'DOWNLOADER-ONLY: {pmid}')
        nih_dict = self.api.dnld_nihdict(pmid)
        if nih_dict:
            return NIHiCiteEntry.from_jsondct(
                nih_dict,
                self.nihgrouper.get_group(nih_dict.get('nih_percentile')))
        return None

    @staticmethod
    def _prt(nihdicts):
        print('FFFFFFF', len(nihdicts))
        for dct in nihdicts:
            print(f"\n{'-'*80}")
            for key, val in dct.items():
                print(f'{key:27} {val}')


# Copyright (C) 2019, DV Klopfenstein, PhD. All rights reserved
