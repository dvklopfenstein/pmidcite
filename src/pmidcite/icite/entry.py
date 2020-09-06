"""Holds NIH iCite data for one PubMed ID (PMID)"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import stdout


class NIHiCiteEntry:
    """Holds NIH iCite data for one PubMed ID (PMID)"""

    pat_str = ('{pmid:8} {aart_type} {aart_animal} '
               '{nih_perc:3} {nih_sd} {year} {citation_count:5} {clin:2} {references:3} '
               'au[{A:02}]({author1}) {title}'
              )
    pat_md = ('{year}|{pmid:8}|{aart_type}|{aart_animal}|'
              '{citation_count:>5}|{clin:>4}|{references:>4}|'
              '{A:2}|{author1:16}|{title}'
             )

    associated_pmids = {'cited_by_clin', 'cited_by', 'references'}

    hdr = pat_str.format(
        pmid='PMID',
        year='YR',
        aart_type='RP',
        aart_animal='HAMCc',
        nih_sd='SD',
        nih_perc='  %',
        citation_count='  cit',
        clin='cli',
        references='ref',
        A=0,
        author1='authors',
        title='title')

    def __init__(self, icite_dct):
        self.pmid = icite_dct['pmid']
        self.dct = icite_dct
        nih_percentile = icite_dct['nih_percentile']
        self.dct['nih_sd'] = self._init_nih_sd(nih_percentile)
        self.dct['nih_perc'] = round(nih_percentile) if nih_percentile is not None else 999
        self.dct['num_auth'] = len(icite_dct['authors'])
        self.dct['num_clin'] = len(icite_dct['cited_by_clin'])
        self.dct['total_cites'] = icite_dct['citation_count'] + len(icite_dct['cited_by_clin'])
        self.dct['num_refs'] = len(icite_dct['references'])

    @staticmethod
    def _init_nih_sd(nih_percentile):
        """Assign group numbers to the NIH percentile values using the 68-95-99.7 rule"""
        # No NIH percentile yet assigned. This paper should be checked out.
        if nih_percentile is None:
            return 5
        #  2.1% -3 SD: Very low citation rate
        if nih_percentile < 2.1:
            return 0
        # 13.6% -2 SD: Low citation rate
        if nih_percentile < 15.7:
            return 1
        # 68.2% -1 SD to +1 SD: Average citation rate
        if nih_percentile < 83.9:
            return 2
        # 13.6% +2 SD: High citation rate
        if nih_percentile < 97.5:
            return 3
        #  2.1% +3 SD: Very high citation rate
        return 4

    def prt_keys(self, prt=stdout):
        """Print paper keys, including header line"""
        prt.write('{COLS}\n\n'.format(COLS=self.line_fmt()))
        self.prt_key_desc(prt)

    @staticmethod
    def line_fmt():
        """Return the format of the paper line"""
        return 'PubMedID RP HAMCc % SD YEAR x y z au[A](First Author) Title of paper'

    @staticmethod
    def prt_key_desc(prt=stdout):
        """Print paper key description"""
        # pylint: disable=line-too-long
        ## prt.write('NIH iCite line format:\n')
        ## prt.write('  YYYY NNNNNNNN RP HAMCc nih% x y z au[A](First Author) Title of paper\n\n')
        ## prt.write('NIH iCite details:\n')
        prt.write('  PubMedID: PubMed ID (PMID)\n\n')
        prt.write('     RP section:\n')
        prt.write('     ----------------------------------\n')
        prt.write('         R: Is a research article\n')
        prt.write('         P: iCite has calculated an initial Relative Citation Ratio (RCR) for new papers\n\n')
        prt.write('     HAMCc section:\n')
        prt.write('     ----------------------------------\n')
        prt.write('         H: Has MeSH terms in the human category\n')
        prt.write('         A: Has MeSH terms in the animal category\n')
        prt.write('         M: Has MeSH terms in the molecular/cellular biology category\n')
        prt.write('         C: Is a clinical trial, study, or guideline\n')
        prt.write('         c: Is cited by a clinical trial, study, or guideline\n\n')
        prt.write('     NIH section, based on Relative Citation Ratio (RCR):\n')
        prt.write('     ----------------------------------\n')
        prt.write('         %: NIH citation percentile rounded to an integer. 999 means "not determined" or TBD\n')
        prt.write('        SD: NIH citation percentile group: 0=-3SD 1=-2SD 2=+/-1SD 3=+2SD 4=+3SD or i=TBD\n\n')
        prt.write('     YEAR/citations/references section:\n')
        prt.write('     ----------------------------------\n')
        prt.write('      YEAR: The year the article was published\n')
        prt.write('         x: Number of unique articles that have cited the paper\n')
        prt.write('         y: Number of unique clinical articles that have cited the paper\n')
        prt.write('         z: Number of references\n')
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
        nih_sd = dct['nih_sd']
        return pat.format(
            pmid=self.pmid,
            year=dct['year'],
            aart_type=self.get_aart_type(),
            aart_animal=self.get_aart_translation(),
            nih_sd=str(nih_sd) if nih_sd != 5 else 'i',
            nih_perc=dct['nih_perc'],
            citation_count=dct['citation_count'],
            clin=dct['num_clin'],
            references=dct['num_refs'],
            A=dct['num_auth'],
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
        """Get succinct ASCII art for the translation information"""
        # Translation of basic sciene research into practical clinical applications
        # or 'bench-to-bedside'
        # https://www.ncbi.nlm.nih.gov/pubmed/23705970
        # https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000416
        lst = []
        dct = self.dct
        lst.append('H' if dct['human'] != 0.0 else '.')
        lst.append('A' if dct['animal'] != 0.0 else '.')
        lst.append('M' if dct['molecular_cellular'] != 0.0 else '.')
        lst.append('C' if dct['is_clinical'] else '.')
        lst.append('c' if dct['cited_by_clin'] else '.')
        return ''.join(lst)

    def prt_dct(self, prt=stdout):
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

    def __lt__(self, rhs):
        """Default sort by PMID"""
        return self.pmid < rhs.pmid


# Copyright (C) 2019-present DV Klopfensteinr,. All rights reserved.
