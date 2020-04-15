"""Holds NIH iCite data for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
# from pmidcite.utils_module import import_var
from pmidcite.utils_module import load_modpy
from pmidcite.icite.entry import NIHiCiteEntry


def sortby_year(obj):
    """Sort lists of iCite items"""
    return [-1*obj.dct['year'], -1*obj.dct['nih_percentile']]

def sortby_cite(obj):
    """Sort lists of iCite items"""
    return [-1*obj.dct['citation_count'], -1*obj.dct['year']]

def sortby_nih_sd(obj):
    """Sort lists of iCite items"""
    dct = obj.dct
    return [-1*dct['nih_sd'], -1*dct['year'], -1*dct['nih_perc'], -1*dct['citation_count']]


class NIHiCitePaper:
    """Holds NIH iCite data for one PubMed ID (PMID)"""

    sortby_dct = {
        'nih_sd': sortby_nih_sd,
        'cite': sortby_cite,
        'year': sortby_year,
    }

    # pylint: disable=too-many-instance-attributes
    def __init__(self, pmid, dirpy, header=None, note=None):
        self.pmid = pmid
        self.dirpy = dirpy
        self.hdr = header  # A header to print before a paper
        self.note = note   # A short note to print at end of cite line
        self.icite = NIHiCiteEntry(self.load_pmid(pmid))
        ## print('VVVVVVVVVVVVVVV', self.icite)
        self.cited_by = self.load_pmids(self.icite.dct['cited_by'])
        self.cited_by_clin = self.load_pmids(self.icite.dct['cited_by_clin'])
        self.references = self.load_pmids(self.icite.dct['references'])

    def str_line(self):
        """Return a string summarizing the the paper described herein"""
        txt = str(self.icite)
        return txt if not self.note else '{TXT} {NOTE}'.format(TXT=txt, NOTE=self.note)

    @staticmethod
    def prt_keys(prt=sys.stdout):
        """Print paper keys"""
        prt.write('  TOP: A user-requested paper\n')
        prt.write('  CIT: A paper that cited TOP\n')
        prt.write('  CLI: A clinical paper that cited TOP\n')
        prt.write('  REF: A clinical paper that cited TOP\n')

    def prt_summary(self, prt=sys.stdout, rpt_references=True, sortby_cites='nih_sd', sortby_refs=None):
        """Print summary of paper"""
        if self.hdr:
            prt.write('NAME: {NAME}\n'.format(NAME=self.hdr))
        prt.write('TOP {iCite}\n'.format(iCite=self.str_line()))
        # Citations by clinical papers
        if self.cited_by_clin:
            prt.write('Cited by {N} Clinical papers:\n'.format(N=len(self.cited_by_clin)))
        self.prt_list(self.cited_by_clin, 'CLI', prt, sortby_cites)
        # Citations 
        if self.cited_by:
            prt.write('{N} of {M} citations downloaded:\n'.format(
                N=len([1 for o in self.cited_by if o.dct['cited_by']]),
                M=self.icite.dct['citation_count']))
        self.prt_list(self.cited_by, 'CIT', prt, sortby_cites)
        # References
        if rpt_references and self.references:
            prt.write('{N} of {M} References downloaded:\n'.format(
                N=len(self.references),
                M=len(self.icite.dct['references'])))
            self.prt_list(self.references, 'REF', prt, sortby_refs)

    def get_sorted(self, icites, sortby=None):
        """Get citations or references, sorted"""
        if sortby in self.sortby_dct:
            sortby = self.sortby_dct[sortby]
        return sorted(icites, key=sortby)

    def prt_list(self, icites, desc, prt, sortby=None):
        """Print list of NIH iCites in summary format"""
        if sortby is not None:
            icites = self.get_sorted(icites, sortby)
        for icite in icites:
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
