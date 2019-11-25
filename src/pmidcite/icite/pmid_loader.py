"""Given a PubMed ID (PMID), return a list of publications which cite it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import os
#### import collections as cx
import importlib.util
#### import requests

from pmidcite.icite.icite import NIHiCite
from pmidcite.icite.paper import NIHiCitePaper


class NIHiCiteLoader:
    """Manage pubs notes files"""

    def __init__(self, force_dnld, rpt_references, api):
        self.rpt_references = rpt_references
        self.dnld_force = force_dnld
        self.dir_dnld = api.dir_dnld
        self.api = api
        #### self.kws = {k:v for k, v in kws.items() if k in self.opt_keys}

    def wr_out(self, fout_txt, pmids):
        """Run iCite for user-provided PMIDs and write to a file"""
        with open(fout_txt, 'w') as prt:
            self.run_icite_pmids(pmids, prtout=prt)
            print('  WROTE: {TXT}'.format(TXT=fout_txt))

    def run_icite_pmids(self, pmids, prtout=sys.stdout):
        """Print summary for each user-specified PMID"""
        for pmid in pmids:
            self.run_icite_pmid(pmid, prtout)

    def run_icite_pmid(self, pmid, prtout=sys.stdout):
        """Print summary for each user-specified PMID"""
        icites = self.run_icite(pmid)
        print('{N} NIH iCite PMIDs related to {PMID}'.format(
            N=len(icites), PMID=pmid))
        paper = NIHiCitePaper(pmid, self.dir_dnld)
        paper.prt_summary(prtout, self.rpt_references, 'cite')
        prtout.write('\n')

    def run_icite(self, pmids):
        """Load or download NIH iCite data for requested PMIDs"""
        if isinstance(pmids, int):
            iciteobj = self.dnld_icite_pmid(pmids)
            print(iciteobj)
            print('FFFFFFFFFFFFFFFF')
            print(iciteobj)
            return self.dnld_assc_pmids(iciteobj)
        raise RuntimeError('TBD IMPLEMENT')

    def dnld_assc_pmids(self, icite):
        """Download PMID iCite data for PMIDs associated with icite paper"""
        pmids_assc = icite.get_assc_pmids()
        ## print('AAAAAAAAAAAAAAAA')
        if not pmids_assc:
            return []
        ## print('BBBBBBBBBBBBBBBB')
        if self.dnld_force:
            return self.api.dnld_icites(pmids_assc)
        ## print('CCCCCCCCCCCCCCCC')
        pmids_missing = self._get_pmids_missing(pmids_assc)
        ## print('{N} PMIDs assc'.format(N=len(pmids_assc)))
        ## print('{N} PMIDs missing'.format(N=len(pmids_missing)))
        if pmids_missing:
            objs_missing = self.api.dnld_icites(pmids_missing)
            pmids_load = pmids_assc.difference(pmids_missing)
            objs_dnlded = self.load_icites(pmids_load)
            ## print('{N} PMIDs loaded'.format(N=len(pmids_load)))
            return objs_missing + objs_dnlded
        return self.load_icites(pmids_assc)
        ## print('DDDDDDDDDDDDDDDD')

    def load_icites(self, pmids):
        """Load multiple NIH iCite data from Python modules"""
        if not pmids:
            return []
        icites = []
        for pmid in pmids:
            file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dir_dnld, PMID=pmid)
            icites.append(self.load_icite(file_pmid))
        return icites

    @staticmethod
    def load_icite(file_pmid):
        """Load NIH iCite information from Python modules"""
        spec = importlib.util.spec_from_file_location("module.name", file_pmid)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return NIHiCite(mod.ICITE)

    def _get_pmids_missing(self, pmids_all):
        """Get PMIDs that have not yet been downloaded"""
        pmids_missing = set()
        for pmid_cur in pmids_all:
            file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dir_dnld, PMID=pmid_cur)
            if not os.path.exists(file_pmid):
                pmids_missing.add(pmid_cur)
        return pmids_missing

    def dnld_icite_pmid(self, pmid):
        """Download NIH iCite data for requested PMIDs"""
        file_pmid = '{DIR}/p{PMID}.py'.format(DIR=self.dir_dnld, PMID=pmid)
        if self.dnld_force or not os.path.exists(file_pmid):
            iciteobj = self.api.dnld_icite(pmid)
            if iciteobj is not None:
                return iciteobj
        return self.load_icite(file_pmid)


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
