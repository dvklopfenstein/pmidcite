"""Holds NIH iCite data for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from PyBiocode.Utils.module_helper import import_var
from pmidcite.icite import NIHiCite


class NIHiCitePaper:
    """Holds NIH iCite data for one PubMed ID (PMID)"""

    def __init__(self, pmid, moddir, prt=sys.stdout):
        self.moddir = moddir
        self.icite = NIHiCite(self.load_pmid(pmid, prt))
        self.cited_by = self.load_pmids(self.icite.dct['cited_by'], prt)
        self.cited_by_clin = self.load_pmids(self.icite.dct['cited_by_clin'], prt)
        self.references = self.load_pmids(self.icite.dct['references'], prt)

    def prt_summary(self, prt=sys.stdout, sortby=None):
        """Print summary of paper"""
        prt.write('TOP {iCite}\n'.format(iCite=str(self.icite)))
        if self.cited_by:
            prt.write('{N} of {M} citations have citations:\n'.format(
                N=len([1 for o in self.cited_by if o.dct['cited_by']]),
                M=self.icite.dct['citation_count']))
        self.prt_list(self.cited_by, 'CIT', prt, sortby)
        if self.cited_by_clin:
            prt.write('{N} Cited by Clinical papers:\n'.format(N=len(self.cited_by_clin)))
        self.prt_list(self.cited_by_clin, 'CLI', prt, sortby)
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

    def prt_list(self, icites, desc, prt, sortby=None):
        """Print list of NIH iCites in summary format"""
        sortby = self._get_sortby(sortby)
        for icite in sorted(icites, key=sortby):
            prt.write('{DESC} {iCite}\n'.format(DESC=desc, iCite=str(icite)))

    def load_pmid(self, pmid, prt=sys.stdout):
        """Load NIH iCite data for one PMID from a Python module"""
        modstr = '{MODDIR}.p{PMID}'.format(MODDIR=self.moddir, PMID=pmid)
        return import_var(modstr, 'ICITE', prt)

    def load_pmids(self, pmids, prt):
        """Load NIH iCite data for many PMID from a Python module"""
        if not pmids:
            return []
        load_pmid = self.load_pmid
        return [NIHiCite(load_pmid(p, prt)) for p in pmids]


# Copyright (C) 2019-present DV Klopfensteinr,. All rights reserved.
