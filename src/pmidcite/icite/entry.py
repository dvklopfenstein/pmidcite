"""Holds NIH iCite data for one PubMed ID (PMID)"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys


class NIHiCiteEntry:
    """Holds NIH iCite data for one PubMed ID (PMID)"""

    pat1 = ('{year} {pmid:8} {aart_type} {aart_animal} '
            '{citation_count:5} {clin:2} {references:3} '
            'au[{A:02}]({author1}) {title}'
           )

    associated_pmids = {'cited_by_clin', 'cited_by', 'references'}

    def __init__(self, icite_dct):
        self.dct = icite_dct

    def __str__(self):
        """Return one-line string describing NIH iCite entry"""
        dct = self.dct
        return self.pat1.format(
            pmid=dct['pmid'],
            year=dct['year'],
            aart_type=self.get_aart_type(),
            aart_animal=self.get_aart_animal(),
            clin=len(dct['cited_by_clin']),
            citation_count=dct['citation_count'],
            references=len(dct['references']),
            A=len(dct['authors']),
            author1=dct['authors'][0] if dct['authors'] else '',
            title=dct['title'],
        )

    def get_assc_pmids(self, keys=None):
        """Get PMIDs associated with the given NIH iCite data"""
        pmids = set()
        if keys is None:
            keys = self.associated_pmids
        for assc_key in keys:
            if self.dct[assc_key]:
                pmids.update(self.dct[assc_key])
        return pmids

    def get_aart_type(self):
        """Get succinct ASCII art for concise info display"""
        lst = []
        dct = self.dct
        lst.append('R' if dct['is_research_article'] else '.')
        lst.append('C' if dct['is_clinical'] else '.')
        lst.append('P' if dct['provisional'] else '.')
        return ''.join(lst)

    def get_aart_animal(self):
        """Get succinct ASCII art for concise info display"""
        lst = []
        dct = self.dct
        lst.append('H' if dct['human'] != 0.0 else '.')
        lst.append('A' if dct['animal'] != 0.0 else '.')
        lst.append('M' if dct['molecular_cellular'] != 0.0 else '.')
        return ''.join(lst)

    def prt_dct(self, prt=sys.stdout):
        """Print full NIH iCite dictionary"""
        prt.write('{STR}\n'.format(STR=self.str_dct()))

    def str_dct(self):
        """Get a string describing object"""
        txt = []
        for key, val in self.dct.items():
            if isinstance(val, list):
                val = '[{N}] {LST}'.format(N=len(val), LST=', '.join(str(e) for e in val))
            txt.append('{K:27} {V}'.format(K=key, V=val))
        return '\n'.join(txt)


# Copyright (C) 2019-present DV Klopfensteinr,. All rights reserved.
