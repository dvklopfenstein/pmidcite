"""Holds NIH iCite data for one PubMed ID (PMID)"""
# https://icite.od.nih.gov/api

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

from sys import stdout


class NIHiCiteEntry:
    """Holds NIH iCite data for one PubMed ID (PMID)"""

    fields = ['pmid', 'aart_type', 'aart_animal', 'nih_perc', 'nih_group', 'year',
              'num_cites_all', 'clin', 'references',
              'A', 'author1', 'title']

    pat_pre = ('{pmid:8} {aart_type:2} {aart_animal:5} '
               '{nih_perc:>3} {nih_group} {year:4} {num_cites_all:>5} {clin:>2} {references:>3} '
              )
    pat_str = pat_pre + 'au[{A:02}]({author1}) {title}'

    pat_md = ('{year}|{pmid:8}|{aart_type}|{aart_animal}|'
              '{num_cites_all:>5}|{clin:>4}|{references:>4}|'
              '{A:2}|{author1:16}|{title}'
             )

    pat_multiline = (
        '{pmid:8} PMID\n'
        '{year:4} Year published\n'
        '{aart_animal} Annotated with MeSH terms for: Human, Mouse, molecular/cellular\n'
        '{num_cites_all:>5} Number of total citations\n'
        '{clin:>4} Number of clinical papers which cited this paper\n'
        '{references:>4} Number of references\n'
        '{A:2} Number of authors\n'
        '{author1:16} First author\n'
        'TITLE: {title}'
    )

    citekeys = {'cited_by_clin', 'cited_by'}
    refkey = {'references',}
    associated_pmid_keys = citekeys.union(refkey)

    col_idx = pat_str.format(
        pmid='2',
        aart_type='3',
        aart_animal='4',
        nih_perc='5',
        nih_group='6',
        year='7',
        num_cites_all='8',
        clin='9',
        references='10',
        A=11,
        author1='authors',
        title='')

    hdr = pat_str.format(
        pmid='PMID',
        year='YEAR',
        aart_type='RP',
        aart_animal='HAMCc',
        nih_group='G',
        nih_perc='  %',
        num_cites_all='  cit',
        clin='cli',
        references='ref',
        A=0,
        author1='authors',
        title='title')

    def __init__(self, pmid=None, dct=None):
        self.pmid = pmid
        self.dct = dct

    def get_dict(self):
        """Gets a dict containing all member data.
           Use `get_dict` instead of accessing the dict directly.
           The dict data member is deprecated and will be replaced by a namedtuple
        """
        return self.dct

    @classmethod
    def from_jsondct(cls, icite_dct, nih_group_num):
        """Construct NIHiCiteEntry from jsondct downloaded from NIH using Entrez utils"""
        cls_dct = icite_dct
        cls_dct['nih_group'] = nih_group_num  # 0 - 5
        cls_dct['num_auth'] = len(lst) if (lst := icite_dct['authors']) else 0
        cit_clin = icite_dct['cited_by_clin']
        cited_by = icite_dct['cited_by']
        cls_dct['num_clin'] = len(cit_clin) if cit_clin else 0
        cls_dct['num_cite'] = len(cited_by) if cited_by else 0

        ##num_cites_all = len(set(cls_dct['cited_by_clin']).union(cls_dct['cited_by']))
        all_citing_pmids = cls._get_cites_all(cit_clin, cited_by)
        cls_dct['all_citing_pmids'] = all_citing_pmids
        num_cites_all = len(all_citing_pmids) if all_citing_pmids is not None else 0
        cls_dct['num_cites_all'] = num_cites_all

        nih_perc = icite_dct['nih_percentile']
        cls_dct['nih_perc'] = round(nih_perc) if nih_perc is not None else 110 + num_cites_all
        cls_dct['num_refs'] = len(icite_dct['references'])
        return cls(icite_dct['pmid'], cls_dct)

    @classmethod
    def _get_cites_all(cls, cit_clin, cited_by):
        if cit_clin is not None and cited_by is not None:
            return set(cit_clin).union(cited_by)
        if cit_clin is None and cited_by is not None:
            return cited_by
        if cit_clin is not None and cited_by is None:
            return cit_clin
        return None

    def get(self, attrname):
        """Get the value of attrname. Use this rather than the deprecated dct data member"""
        if attrname in self.dct:
            return self.dct[attrname]
        return None

    def get_attrnames(self):
        """Get a list of attribute names"""
        return list(self.dct.keys())

    def get_authors(self):
        """Get the list of authors from NIH's iCite for this paper"""
        return self.dct.get('authors')

    ####def get_au1_lastname(self):
    ####    """Get the last name of the first author"""
    ####    if (aus := self.dct['authors']):
    ####        return aus[0]['fullName']
    ####    return None

    def get_year(self):
        """Get the publication year"""
        return self.dct.get('year')

    def prt_cite_cnts(self):
        """Print cite counts. NIH's citation_count includes only cited_by, not cited_by_clin"""
        # pylint: disable=line-too-long
        # if self.dct['citation_count'] != len(set(self.dct['cited_by'])):
        # if self.dct['citation_count'] != len(set(self.dct['cited_by_clin']).union(self.dct['cited_by']))
        cited_by_clin = set(self.dct['cited_by_clin'])
        cited_by = set(self.dct['cited_by'])
        num_exp = len(cited_by_clin.union(cited_by))
        msg = ('**NOTE: {pmid:9}=pmid '
               '{citation_count:6,}=citation_count '
               '{num_clin:6,}=cited_by_clin '
               '{num_cite:6,}=cited_by;   '
               '{num_exp:6,}=cited_by_clin.union(cited_by)')
        print(msg.format(num_exp=num_exp, **self.dct))

    def prt_keys(self, prt=stdout):
        """Print paper keys, including header line"""
        prt.write(f'{self.line_fmt()}\n\n')
        self.prt_key_desc(prt)

    @staticmethod
    def line_fmt():
        """Return the format of the paper line"""
        return 'PubMedID RP HAMCc % G YEAR x y z au[A](First Author) Title of paper'

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
        prt.write('         %: NIH citation percentile rounded to an integer. -1 means "not determined" or TBD\n')
        prt.write('         G: NIH citation percentile group: 0=-3SD 1=-2SD 2=+/-1SD 3=+2SD 4=+3SD or i=TBD\n\n')
        prt.write('     YEAR/citations/references section:\n')
        prt.write('     ----------------------------------\n')
        prt.write('      YEAR: The year the article was published\n')
        prt.write('       cit: Total of all unique articles that have cited the paper, including clinical articles\n')
        prt.write('       cli: Number of unique clinical articles that have cited the paper\n')
        prt.write('       ref: Number of references\n')
        prt.write('     au[A]: A is the number of authors\n')

    def str_md(self):
        """Return one-line string describing NIH iCite entry"""
        return self._str(self.pat_md)

    def str_multiline(self):
        """Return multiline-line string describing NIH iCite entry"""
        return self._str(self.pat_multiline)

    def __str__(self):
        """Return one-line string describing NIH iCite entry"""
        return self._str(self.pat_str)

    def _str(self, pat):
        """Return one-line string describing NIH iCite entry"""
        dct = self.dct
        nih_group = dct['nih_group']
        nih_perc = dct['nih_perc']
        return pat.format(
            pmid=self.pmid,
            year=dct['year'],
            aart_type=self.get_aart_type(),
            aart_animal=self.get_aart_translation(),
            nih_group=str(nih_group) if nih_group != 5 else 'i',
            nih_perc=nih_perc if nih_perc <= 100 else ' -1',
            num_cites_all=dct['num_cites_all'],
            clin=dct['num_clin'],
            references=dct['num_refs'],
            A=dct['num_auth'],
            author1=dct['authors'][0]['lastName'] if dct['authors'] else '',
            title=dct['title'],
        )

    def get_assc_pmids(self, keys):
        """Get PMIDs associated with the given NIH iCite data"""
        pmids = set()
        s_dct = self.dct
        for assc_key in keys:
            if s_dct[assc_key]:
                pmids.update(s_dct[assc_key])
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
        prt.write(f'{self.str_dct()}\n')

    def str_dct(self):
        """Get a string describing object"""
        txt = []
        for key, val in self.dct.items():
            if isinstance(val, list):
                val = f"[{len(val)}] {', '.join(str(e) for e in val)}"
            txt.append(f'{key:27} {val}'.format(K=key, V=val))
        return '\n'.join(txt)

    def __lt__(self, rhs):
        """Default sort by PMID"""
        return self.pmid < rhs.pmid


# Copyright (C) 2019-present DV Klopfenstein, PhD. All rights reserved.
