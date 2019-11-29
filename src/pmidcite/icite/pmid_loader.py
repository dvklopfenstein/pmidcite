"""Given a PubMed ID (PMID), return a list of publications which cite it"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import os
#### import collections as cx
import importlib.util
#### import requests

from pmidcite.icite.entry import NIHiCiteEntry
from pmidcite.icite.paper import NIHiCitePaper


class NIHiCiteLoader:
    """Manage pubs notes files"""

    def __init__(self, force_dnld, api, rpt_references=False):
        self.rpt_references = rpt_references
        self.dnld_force = force_dnld
        self.dir_dnld = api.dir_dnld
        self.api = api

    def wr_papers(self, fout_txt, pmids, mode='w'):
        """Run iCite for user-provided PMIDs and write to a file"""
        pmids_new = pmids
        if mode == 'a':
            pmids_new = self._get_new_pmids(fout_txt, pmids)
        if pmids_new:
            with open(fout_txt, mode) as prt:
                self.run_icite_pmids(pmids_new, prtout=prt)
        print('  {WR}: {TXT}'.format(
            WR=self._msg_wrote(mode, pmids, pmids_new), TXT=fout_txt))

    @staticmethod
    def _msg_wrote(mode, pmids_req, pmids_new):
        """Get the 'WROTE' or 'APPENDED' message"""
        if mode == 'w':
            return '{N} WROTE'.format(N=len(pmids_req))
        if mode == 'a':
            if pmids_new:
                return '{N} of {M} APPENDED'.format(
                    N=len(pmids_new),
                    M=len(pmids_req))
            return '{N} of {M} FOUND'.format(
                N=len(pmids_new),
                M=len(pmids_req))
        raise RuntimeError('UNRECOGNIZED WRITE MODE({M})'.format(M=mode))

    def _get_new_pmids(self, pmidcite_txt, pmids):
        """Get PMIDs which are not already fully analyzed in pmidcite.txt"""
        if not os.path.exists(pmidcite_txt):
            return pmids
        pmids_old = self._get_old_pmids(pmidcite_txt)
        return [p for p in pmids if p not in pmids_old]

    @staticmethod
    def _get_old_pmids(pmidcite_txt):
        """Get PMIDs already found in pmidcite.txt"""
        pmids = set()
        with open(pmidcite_txt) as ifstrm:
            for line in ifstrm:
                if line[:4] == 'TOP ':
                    flds = line.split()
                    assert flds[2].isdigit(), flds
                    pmids.add(int(flds[2]))
        return pmids

    def wr_name2pmid(self, fout_txt, name2pmid):
        """Run iCite for user-provided PMIDs and write to a file"""
        with open(fout_txt, 'w') as prt:
            self.run_icite_name2pmid(name2pmid, prtout=prt)
            print('  WROTE: {TXT}'.format(TXT=fout_txt))

    def run_icite_name2pmid(self, name2pmid, prtout=sys.stdout):
        """Print summary for each user-specified PMID"""
        for name, pmid in name2pmid.items():
            self.run_icite_pmid(pmid, name, prtout)

    def run_icite_pmids(self, pmids, prtout=sys.stdout):
        """Print summary for each user-specified PMID"""
        for pmid in pmids:
            self.run_icite_pmid(pmid, prtout=prtout)

    def run_icite_pmid(self, pmid_top, name=None, prtout=sys.stdout):
        """Print summary for each user-specified PMID"""
        #### citedby = self.run_icite(pmid)
        citeobj_top = self.dnld_icite_pmid(pmid_top)
        if citeobj_top is None:
            print('No results found: {PMID} {NAME}'.format(PMID=pmid_top, NAME=name))
            prtout.write('No iCite results found: {PMID} {NAME}\n\n'.format(
                PMID=pmid_top, NAME=name if name is not None else ''))
            return
        self.dnld_assc_pmids(citeobj_top)
        paper = NIHiCitePaper(pmid_top, self.dir_dnld, name)
        paper.prt_summary(prtout, self.rpt_references, 'cite')
        prtout.write('\n')

    #### def run_icite(self, pmids):
    ####     """Load or download NIH iCite data for requested PMIDs"""
    ####     if isinstance(pmids, int):
    ####         iciteobj_top = self.dnld_icite_pmid(pmids)
    ####         print(iciteobj)
    ####         print('FFFFFFFFFFFFFFFF')
    ####         print(iciteobj)
    ####         return [self.dnld_assc_pmids(iciteobj_top)]
    ####     iciteobjs = []
    ####     for pmid in pmids:
    ####         iciteobj_top = self.dnld_icite_pmid(pmid)
    ####         if iciteobj_top is not None:
    ####             iciteobjs.append(self.dnld_assc_pmids(iciteobj))
    ####     return iciteobjs

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
        if os.path.exists(file_pmid):
            spec = importlib.util.spec_from_file_location("module.name", file_pmid)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return NIHiCiteEntry(mod.ICITE)
        return None

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
