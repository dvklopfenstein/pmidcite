"""Holds NIH iCite data for one PubMed ID (PMID)"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys


class NIHiCiteEntry:
    """Holds NIH iCite data for one PubMed ID (PMID)"""

    pat_str = ('{year} {pmid:8} {aart_type} {aart_animal} '
               '{citation_count:5} {clin:2} {references:3} '
               'au[{A:02}]({author1}) {title}'
              )
    pat_md = ('{year}|{pmid:8}|{aart_type}|{aart_animal}|'
              '{citation_count:>5}|{clin:>4}|{references:>4}|'
              '{A:2}|{author1:16}|{title}'
             )

    associated_pmids = {'cited_by_clin', 'cited_by', 'references'}

    def __init__(self, icite_dct):
        self.dct = icite_dct

    @staticmethod
    def line_fmt():
        """Return the format of the paper line"""
        return 'YYYY NNNNNNNN RP HAMCc x y z au[A](First Author) Title of paper'

    @staticmethod
    def prt_keys(prt=sys.stdout):
        """Print paper keys"""
        # pylint: disable=line-too-long
        ## prt.write('NIH iCite line format:\n')
        ## prt.write('  YYYY NNNNNNNN RP HAMCc x y z au[A](First Author) Title of paper\n\n')
        ## prt.write('NIH iCite details:\n')
        prt.write('      YYYY: The year the article was published\n')
        prt.write('  NNNNNNNN: PubMed ID (PMID)\n\n')
        prt.write('         R: Is a research article\n')
        prt.write('         P: iCite has calculated an initial Relative Citation Ratio (RCR) for new papers\n\n')
        prt.write('         H: Has MeSH terms in the human category\n')
        prt.write('         A: Has MeSH terms in the animal category\n')
        prt.write('         M: Has MeSH terms in the molecular/cellular biology category\n')
        prt.write('         C: Is a clinical trial, study, or guideline\n')
        prt.write('         c: Is cited by a clinical trial, study, or guideline\n\n')
        prt.write('         x: Number of unique articles that have cited the paper\n')
        prt.write('         y: Number of unique clinical articles that have cited the paper\n')
        prt.write('         z: Number of references\n\n')
        prt.write('     au[A]: A is the number of authors\n')

    def str_md(self):
        """Return one-line string describing NIH iCite entry"""
        return self._str(self.pat_md)

    def __str__(self):
        """Return one-line string describing NIH iCite entry"""
        return self._str(self.pat_str)

    def _str(self, pat):
        """Return one-line string describing NIH iCite entry"""
        dct = self.dct
        return pat.format(
            pmid=dct['pmid'],
            year=dct['year'],
            aart_type=self.get_aart_type(),
            aart_animal=self.get_aart_translation(),
            citation_count=dct['citation_count'],
            clin=len(dct['cited_by_clin']),
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
        lst.append('P' if dct['provisional'] else '.')
        return ''.join(lst)

    def get_aart_translation(self):
        """Get succinct ASCII art for concise info display"""
        lst = []
        dct = self.dct
        lst.append('H' if dct['human'] != 0.0 else '.')
        lst.append('A' if dct['animal'] != 0.0 else '.')
        lst.append('M' if dct['molecular_cellular'] != 0.0 else '.')
        lst.append('C' if dct['is_clinical'] else '.')
        lst.append('c' if dct['cited_by_clin'] else '.')
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
