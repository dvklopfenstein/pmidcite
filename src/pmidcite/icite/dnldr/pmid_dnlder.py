"""Given a PubMed ID (PMID), download a list of publications which cite and reference it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from os.path import exists
from os.path import join

from pmidcite.icite.dnldr.pmid_dnlder_base import NIHiCiteDownloaderBase
from pmidcite.icite.dnldr.pmid_loader import NIHiCiteLoader
from pmidcite.icite.entry import NIHiCiteEntry


class NIHiCiteDownloader(NIHiCiteDownloaderBase):
    """Given a PubMed ID (PMID), download a list of publications which cite and reference it"""

    def __init__(self, dir_download, force_download, details_cites_refs=None, nih_grouper=None):
        super(NIHiCiteDownloader, self).__init__(details_cites_refs, nih_grouper)
        self.dnld_force = force_download
        self.dir_dnld = dir_download  # Recommended dir_icite_py: ./icite
        self.loader = NIHiCiteLoader(self.nihgrouper, dir_download, self.details_cites_refs)
        if not exists(dir_download):
            raise RuntimeError('**FATAL: NO DIRECTORY: {DIR}'.format(DIR=dir_download))

    def get_icites(self, pmids):
        """Download NIH iCite data for requested PMIDs"""
        # Python module filenames
        s_dir_dnld = self.dir_dnld
        pmid2py = {p:join(s_dir_dnld, 'p{PMID}.py'.format(PMID=p)) for p in pmids}
        if self.dnld_force:
            pmid2nihentry = {o.pmid: o for o in self._dnld_icites(pmid2py)}
            return [pmid2nihentry[pmid] for pmid in pmids if pmid in pmid2nihentry]
        # Separate PMIDs into those stored in Python modules and those not
        nihentries_all = []
        pmids_pyexist1 = set(pmid for pmid, py in pmid2py.items() if exists(py))
        pmids_pyexist0 = set(pmids).difference(pmids_pyexist1)
        if pmids_pyexist1:
            nihentries_loaded = self._load_icites(pmids_pyexist1, pmid2py)
            if nihentries_loaded:
                nihentries_all.extend(nihentries_loaded)
        if pmids_pyexist0:
            nihentries_all.extend(self._dnld_icites({p:pmid2py[p] for p in pmids_pyexist0}))
        # Return results sorted in the same order as input PMIDs
        pmid2nihentry = {o.pmid:o for o in nihentries_all}
        return [pmid2nihentry[pmid] for pmid in pmids if pmid in pmid2nihentry]

    def _dnld_icites(self, pmid2foutpy):
        """Download a list of NIH citation data for PMIDs"""
        nihdicts = self.api.dnld_nihdicts(pmid2foutpy.keys())
        if nihdicts:
            s_wrpy = self._wrpy
            for nih_dict in nihdicts:
                s_wrpy(pmid2foutpy[nih_dict['pmid']], nih_dict)
            s_get_group = self.nihgrouper.get_group
            return [NIHiCiteEntry(d, s_get_group(d['nih_percentile'])) for d in nihdicts]
        return []

    def get_icite(self, pmid):
        """Load or download NIH iCite data for requested PMID"""
        file_pmid = join(self.dir_dnld, 'p{PMID}.py'.format(PMID=pmid))
        if self.dnld_force or not exists(file_pmid):
            nih_dict = self.api.dnld_nihdict(pmid)
            if nih_dict:
                self._wrpy(file_pmid, nih_dict)
                return NIHiCiteEntry(
                    nih_dict,
                    self.nihgrouper.get_group(nih_dict['nih_percentile']))
        return self.loader.load_icite(file_pmid)  # NIHiCiteEntry

    # -------------------------------------------------------------------------------------
    def _get_pmids_missing(self, pmids_all):
        """Get PMIDs that have not yet been downloaded"""
        pmids_missing = set()
        for pmid_cur in pmids_all:
            file_pmid = join(self.dir_dnld, 'p{PMID}.py'.format(PMID=pmid_cur))
            if not exists(file_pmid):
                pmids_missing.add(pmid_cur)
        return pmids_missing

    def _wrpy(self, fout_py, dct, log=None):
        """Write NIH iCite to a Python module"""
        with open(fout_py, 'w') as prt:
            self.api.prt_dct(dct, prt)
            # Setting prt to sys.stdout -> WROTE: ./icite/p10802651.py
            if log:
                log.write('  WROTE: {PY}\n'.format(PY=fout_py))

    def _load_icites(self, pmids, pmid2py):
        """Load a list of NIH citation data for PMIDs"""
        nihentries_loaded = []
        s_load_icite = self.loader.load_icite
        num_exist = len(pmids)
        for idx, pmid in enumerate(pmids, 1):
            nihentries_loaded.append(s_load_icite(pmid2py[pmid]))
            if idx%1000 == 0:
                print('NIH citation data loaded: {N:,} of {M:,}'.format(N=idx, M=num_exist))
        ## nihentries_all.extend([s_load_icite(pmid2py[p]) for p in pmids_pyexist1])
        return nihentries_loaded


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
