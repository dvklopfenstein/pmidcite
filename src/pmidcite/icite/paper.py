"""Holds NIH iCite data for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

from sys import stdout


def sortby_year(obj):
    """Sort lists of iCite items"""
    return [-1*obj.dct['year'], -1*obj.dct['nih_percentile']]

def sortby_cite(obj):
    """Sort lists of iCite items"""
    return [-1*obj.dct['citation_count'], -1*obj.dct['year']]

def sortby_nih_group(obj):
    """Sort lists of iCite items"""
    dct = obj.dct
    return [-1*dct['nih_group'], -1*dct['year'], -1*dct['nih_perc'],
            -1*dct['citation_count'] + -1*dct['num_clin'],
            -1*dct['num_refs'],
            -1*dct['pmid']]


# pylint: disable=too-many-instance-attributes
class NIHiCitePaper:
    """Holds NIH iCite data for one PubMed ID (PMID)"""

    sortby_dct = {
        'nih_group': sortby_nih_group,
        'cite': sortby_cite,
        'year': sortby_year,
    }

    def __init__(self, pmid, pmid2icite, header=None, pmid2note=None):
        self.pmid = pmid
        self.pmid2icite = pmid2icite
        ## print('PPPPPPPP NIHiCitePaper({}, len(pmid2icite)={})'.format(pmid, len(pmid2icite)))
        self.hdr = header  # A header to print before a paper
        # A short pmid2note to print at end of cite line
        self.pmid2note = {} if pmid2note is None else pmid2note
        self.icite = pmid2icite.get(pmid)
        # Sets of NIHiCiteEntrys
        self.cited_by = self._init_pmids('cited_by')
        self.cited_by_clin = self._init_pmids('cited_by_clin')
        self.references = self._init_pmids('references')

    def get_icite(self):
        """Get NIHiCiteEntry for this paper"""
        return self.pmid2icite[self.pmid]

    def get_authors(self):
        """Get authors for this paper"""
        return self.pmid2icite[self.pmid].get_authors()

    def str_line(self):
        """Return a string summarizing the the paper described herein"""
        txt = str(self.icite)
        if not self.pmid2note:
            return txt
        if self.pmid in self.pmid2note:
            return f'{txt} {self.pmid2note[self.pmid]}'
        return txt

    def prt_top(self, prt=stdout):
        """Print TOP paper"""
        prt.write(f'TOP {self.str_line()}\n')

    @staticmethod
    def prt_keys(prt=stdout):
        """Print paper keys"""
        prt.write('    TOP: The paper requested by the researcher\n')
        prt.write('    CIT: A paper that cited TOP\n')
        prt.write('    CLI: A clinical paper that cited TOP\n')
        prt.write("    REF: A paper referenced in the TOP paper's bibliography\n")

    def prt_summary(self, prt=stdout, sortby_cites='nih_group', sortby_refs='nih_group'):
        """Print summary of paper"""
        if self.hdr:
            prt.write(f'NAME: {self.hdr}\n')
        prt.write(f'TOP {self.str_line()}\n')
        # Citations by clinical papers
        if self.cited_by_clin:
            prt.write(f'Cited by {len(self.cited_by_clin)} Clinical papers:\n')
        self._prt_list(self.cited_by_clin, 'CLI', prt, sortby_cites)
        # Citations
        if self.cited_by:
            prt.write(f'{len(self.cited_by)} of {self.icite.dct["citation_count"]} '
                       'citations downloaded:\n')
        self._prt_list(self.cited_by, 'CIT', prt, sortby_cites)
        # References
        if self.references:
            prt.write(f'{len(self.references)} of {self.icite.dct["num_refs"]} '
                       'References downloaded:\n')
            self._prt_list(self.references, 'REF', prt, sortby_refs)

    def get_sorted(self, icites, sortby=None):
        """Get citations or references, sorted"""
        if sortby is None:
            return icites
        if sortby in self.sortby_dct:
            sortby = self.sortby_dct[sortby]
        return sorted(icites, key=sortby)

    def _prt_list(self, icites, desc, prt, sortby=None):
        """Print list of NIH iCites in summary format"""
        if sortby is not None:
            icites = self.get_sorted(icites, sortby)
        if self.pmid2note:
            s_pmid2note = self.pmid2note
            for icite in icites:
                if icite.pmid in s_pmid2note:
                    prt.write(f'{desc} {str(icite)} {s_pmid2note[icite.pmid]}\n')
                else:
                    prt.write('{desc} {str(icite.}\n')
            return
        for icite in icites:
            prt.write('{desc} {str(icite)}\n')

    def _init_pmids(self, name):
        """Load citation/reference PMIDs, if the 'top' paper has NIH iCite data"""
        if self.icite is None:
            return []
        s_pmid2icite = self.pmid2icite
        return set(s_pmid2icite[pmid] for pmid in self.icite.dct[name] if pmid in s_pmid2icite)

    def __str__(self):
        """Get the line containing data downloaded from NIH iCite for only the featured paper"""
        return self.str_line()


# Copyright (C) 2019-present DV Klopfenstein, PhD. All rights reserved.
