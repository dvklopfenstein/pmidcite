"""Holds NIH iCite data for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
# from pmidcite.utils_module import import_var
from pmidcite.utils_module import load_modpy
from pmidcite.icite.entry import NIHiCiteEntry


class NIHiCitePaper:
    """Holds NIH iCite data for one PubMed ID (PMID)"""

    def __init__(self, pmid, dirpy, name=None):
        self.pmid = pmid
        self.dirpy = dirpy
        self.name = name
        self.icite = NIHiCiteEntry(self.load_pmid(pmid))
        self.cited_by = self.load_pmids(self.icite.dct['cited_by'])
        self.cited_by_clin = self.load_pmids(self.icite.dct['cited_by_clin'])
        self.references = self.load_pmids(self.icite.dct['references'])

    def str_line(self):
        """Return a string summarizing the the paper described herein"""
        return str(self.icite)

    def prt_summary(self, prt=sys.stdout, rpt_references=True, sortby=None):
        """Print summary of paper"""
        if self.name:
            prt.write('NAME: {NAME}\n'.format(NAME=self.name))
        prt.write('TOP {iCite}\n'.format(iCite=self.str_line()))
        if self.cited_by:
            prt.write('{N} of {M} citations have citations:\n'.format(
                N=len([1 for o in self.cited_by if o.dct['cited_by']]),
                M=self.icite.dct['citation_count']))
        self.prt_list(self.cited_by, 'CIT', prt, sortby)
        if self.cited_by_clin:
            prt.write('{N} Cited by Clinical papers:\n'.format(N=len(self.cited_by_clin)))
        self.prt_list(self.cited_by_clin, 'CLI', prt, sortby)
        if rpt_references:
            prt.write('{N} References:\n'.format(N=len(self.references)))
            self.prt_list(self.references, 'REF', prt, sortby)

    @staticmethod
    def sortby_year(obj):
        """Sort lists of iCite items"""
        return [-1*obj.dct['year'], -1*obj.dct['citation_count']]

    @staticmethod
    def sortby_cite(obj):
        """Sort lists of iCite items"""
        return [-1*obj.dct['citation_count'], -1*obj.dct['year']]

    def _get_sortby(self, sortby):
        """Get a sorting function for NIH iCite objects"""
        if sortby is None:
            return self.sortby_year
        if isinstance(sortby, str):
            return self.sortby_year if sortby == 'year' else self.sortby_cite
        return sortby

    def get_sorted(self, icites, sortby=None):
        """Get citations or references, sorted"""
        sortby = self._get_sortby(sortby)
        return sorted(icites, key=sortby)

    def prt_list(self, icites, desc, prt, sortby=None):
        """Print list of NIH iCites in summary format"""
        for icite in self.get_sorted(icites, sortby):
            prt.write('{DESC} {iCite}\n'.format(DESC=desc, iCite=str(icite)))

    def load_pmid(self, pmid):
        """Load NIH iCite data for one PMID from a Python module"""
        fin_py = '{DIR}/p{PMID}.py'.format(DIR=self.dirpy, PMID=pmid)
        if os.path.exists(fin_py):
            mod = load_modpy(fin_py)
            return mod.ICITE
        return None
        ## modstr = '{MODDIR}.p{PMID}'.format(MODDIR=self.moddir, PMID=pmid)
        ## return import_var(modstr, 'ICITE', prt)

    def load_pmids(self, pmids):
        """Load NIH iCite data for many PMID from a Python module"""
        iciteobjs = []
        if not pmids:
            return iciteobjs
        load_pmid = self.load_pmid
        for pmid in pmids:
            mod_icite = load_pmid(pmid)
            if mod_icite is not None:
                iciteobjs.append(NIHiCiteEntry(mod_icite))
        return iciteobjs


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
