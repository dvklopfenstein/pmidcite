"""Plot the types of content and their amount in PubMed"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

import sys
import collections as cx
import itertools

from pmidcite.eutils.cmds.base import EntrezUtilities


# pylint: disable=line-too-long
class PubMedContents(EntrezUtilities):
    """Describe the percentage of various types of content in PubMed"""

    # https://pubmed.ncbi.nlm.nih.gov/help/#citation-status-subsets
    name2query = cx.OrderedDict([
        ('all', 'all [sb]'),
        ('all_ml0_pmc0', 'all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb]'),
        ('all_ml0_pmc0b', 'all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd'),
        ('ml1_pmc1', 'inprocess[sb] OR medline[sb] OR pubmed pmc[sb]'),
        # publisher[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT # pmcbook:
        #   1. Citations recently added to PubMed via electronic submission
        #   from a publisher, and are soon to proceed to the next stage,
        #   PubMed - in process (see below).
        #   2. Also for citations received
        #   before late 2003 if they are from journals not indexed for
        #   MEDLINE, or from a journal that was accepted for MEDLINE
        #   after the citations' publication date.
        #   NOTE: These citations bibliographic data have not been reviewed.
        ('pub_init0', 'publisher[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook'),
        ('pub_init1', 'publisher[sb] AND (pubstatusnihms OR pubstatuspmcsd OR pmcbook)'),
        ('pub', 'publisher[sb]'),
        # pubstatusnihms AND publisher[sb]:
        #   Author manuscripts submitted to PMC that fall under the NIH Public Access Policy.
        # https://www.ncbi.nlm.nih.gov/pmc/about/submission-methods/
        #   Some publishers will initiate the NIHMS deposit process for an author,
        #   but the author must complete two approval steps to load the PMC-ready version to PMC
        ('nihms_pub0', 'pubstatusnihms AND publisher[sb]'),
        ('nihms_pub1', 'pubstatusnihms NOT publisher[sb]'),
        ('nihms', 'pubstatusnihms'),
        ('nihms_pmc1', 'pubstatusnihms AND pubmed pmc[sb]'),
        ('nihms_pmc0', 'pubstatusnihms NOT pubmed pmc[sb]'),
        # pubstatuspmcsd AND publisher[sb]:
        #   Records for selective deposit articles in PMC.
        #   These are articles published in non-MEDLINE journals
        #   where the publisher has chosen to deposit in PMC
        #   only those articles that fall under the NIH Public Access Policy.
        ('pub_pmcsd', 'pubstatuspmcsd AND publisher[sb]'),
        ('pmcsd', 'pubstatuspmcsd'),
        ('pmcsd_and_nihms', 'pubstatuspmcsd AND pubstatusnihms'),  # DISJOINT
        ('pmcsd_pmc1', 'pubstatuspmcsd AND pubmed pmc[sb]'),
        ('pmcsd_pmc0', 'pubstatuspmcsd NOT pubmed pmc[sb]'),
        # inprocess[sb]:
        #   MeSH terms will be assigned if the subject of the article is within the scope of MEDLINE.
        ('inprocess_A_all', 'inprocess[sb]'),
        ('inprocess_A_pmc0', 'inprocess[sb] NOT pubmed pmc[sb]'),
        ('inprocess_A_pmc1', 'inprocess[sb] AND pubmed pmc[sb]'),
        ('inprocess_ml0', 'inprocess[sb] NOT medline[sb]'),
        ('inprocess_ml1', 'inprocess[sb] AND medline[sb]'),
        ('medline_n_inprocess', 'medline[sb] OR inprocess[sb]'),
        # medline[sb]:
        #   Citations that have been indexed with MeSH terms, Publication Types, Substance Names, etc.
        ('medline_all', 'medline[sb]'),
        ('medline_pmc0', 'medline[sb] NOT pubmed pmc[sb]'),
        ('medline_pmc1', 'medline[sb] AND pubmed pmc[sb]'),
        # pubmed pmc[sb]:
        #   Citations in PMC
        ('pmc_all', 'pubmed pmc[sb]'),
        #  5,323,939 pmc_all              pubmed pmc[sb]
        #    135,287 inprocess_A_pmc1     inprocess[sb] AND pubmed pmc[sb]
        #  3,503,057 medline_pmc1         medline[sb] AND pubmed pmc[sb]
        #  1,612,274 pmnml_A_pmc1         pubmednotmedline[sb] AND pubmed pmc[sb]
        ('pmc_all?', 'pubmed pmc[sb] AND (inprocess[sb] OR medline[sb] OR pubmednotmedline[sb])'),
        ('pmc_unknown', 'pubmed pmc[sb] NOT inprocess[sb] NOT medline[sb] NOT pubmednotmedline[sb]'),
        # https://www.ncbi.nlm.nih.gov/pmc/about/submission-methods/
        ('au_all', 'author manuscript all[sb]'),
        ('au_all1', 'author manuscript all[sb] AND all[sb]'),
        ('au_ss', 'author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook'),
        ('au_ss_m0', 'author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb]'),
        ('au_ss_ml0', 'author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]'),
        ('au_ss_pmconly', 'author manuscript[sb] AND pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]'),
        ('au_nihms', 'author manuscript[sb] AND pubstatusnihms'),
        ('au_pmcsd', 'author manuscript[sb] AND pubstatuspmcsd'),
        ('au_pmcbook', 'author manuscript[sb] AND pmcbook'),
        ('au_ml1', 'author manuscript[sb] AND (medline[sb] OR inprocess[sb])'),
        ('au_ml0', 'author manuscript[sb] NOT medline[sb] NOT inprocess[sb]'),
        ('au_ml0_pmc0', 'author manuscript[sb] NOT medline[sb] NOT inprocess[sb] NOT pubmed pmc[sb]'),
        ('au_ml0_pmc1', 'author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb] NOT inprocess[sb]'),
        ('au_m1', 'author manuscript[sb] AND medline[sb]'),
        ('au_ip1', 'author manuscript[sb] AND inprocess[sb]'),
        ('au_ml1_or_pmc1', 'author manuscript[sb] AND (medline[sb] OR pubmed pmc[sb])'),
        ('au_ml1_and_pmc1', 'author manuscript[sb] AND medline[sb] AND pubmed pmc[sb]'),
        ('au_ml1_and_pmc1_or_ip1', 'author manuscript[sb] AND (inprocess[sb] OR medline[sb] AND pubmed pmc[sb])'),
        ('au_pmc1', 'author manuscript[sb] AND pubmed pmc[sb]'),
        ('au_pmc1_ip1', 'author manuscript[sb] AND pubmed pmc[sb] AND inprocess[sb]'),
        ('au_pmc1_ml0', 'author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb]'),
        ('au_pmc0', 'author manuscript[sb] NOT pubmed pmc[sb]'),
        # 7,680 embargoed
        ('au_embargo', 'author manuscript[sb] AND medline[sb] NOT pubmed pmc[sb]'),
        # pubmednotmedline[sb]
        #   Citations that will not receive MEDLINE indexing because:
        #    * they are for articles in non-MEDLINE journals, or
        #    * they are for articles in MEDLINE journals but the articles are out of scope, or
        #    * they are from issues published prior to the date the journal was selected for indexing, or
        #    * citations to articles from journals that deposit their full text articles in PMC
        #      but have not yet been recommended for indexing in MEDLINE.
        ('pmnml_A', 'pubmednotmedline[sb]'),
        ('pmnml_B', 'pubmednotmedline[sb] NOT medline[sb]'),
        ('pmnml_C_ip0', 'pubmednotmedline[sb] NOT inprocess[sb]'),
        ('pmnml_0_ip1', 'pubmednotmedline[sb] AND inprocess[sb]'),
        ('pmnml_A_pmc1', 'pubmednotmedline[sb] AND pubmed pmc[sb]'),
        ('pmnml_A_pmc0', 'pubmednotmedline[sb] NOT pubmed pmc[sb]'),
        # pmcbook:
        #   Book and book chapter citations available on the NCBI Bookshelf.
        ('pmcbook_A', 'pmcbook'),
        ('pmcbook_A_ml0', 'pmcbook NOT medline[sb]'),
        ('pmcbook_A_pmc0', 'pmcbook NOT pubmed pmc[sb]'),
        ('pmcbook_A_pmc0', 'pmcbook NOT pubmed pmc[sb]'),
    ])

    arrow_p = {
        'color': 'k',
        'linewidth':0.4,
        'shape':'full',
        'length_includes_head':True,
        'head_width':.3,
        'head_length':400000,
        'overhang':0.0,
    }

    def __init__(self, email, apikey, tool):
        super(PubMedContents, self).__init__(email, apikey, tool)

    def dnld_content_counts(self):
        """Get the count of various types of content in PubMed"""
        name2cnt = {}
        for name, query in self.name2query.items():
            cnt = self.dnld_count(query)
            print(' {N:12,} {A:20} {Q}'.format(N=cnt, A=name, Q=query))
            name2cnt[name] = cnt
        # 2019/01/04 PubMed Query returns 30,500,360 results: all [sb]
        # 2019/01/04 PubMed Query returns  3,499,063 results: medline[sb] AND pubmed pmc[sb]
        # 2019/01/04 PubMed Query returns  3,636,767 results: medline[sb] OR inprocess[sb] AND pubmed pmc[sb]
        # 2019/01/04 PubMed Query returns  5,321,522 results: pubmed pmc[sb]
        # 2019/01/04 PubMed Query returns  3,499,063 results: pubmed pmc[sb] AND medline[sb]
        # 2019/01/04 PubMed Query returns    137,704 results: pubmed pmc[sb] AND inprocess[sb]
        # 2019/01/04 PubMed Query returns  3,636,767 results: pubmed pmc[sb] AND (inprocess[sb] OR medline[sb])
        # 2019/01/04 PubMed Query returns  1,229,362 results: pubmed pmc[sb] AND pubmednotmedline[sb]
        # 2019/01/04 PubMed Query returns  5,321,522 results: pubmed pmc[sb]

        # To search for the total number of citations in PubMed that are PubMed only citations
        # (pubmednotmedline[sb]-citations that will not receive MEDLINE indexing because
        #     * they are for articles in non-MEDLINE journals, or
        #     * they are for articles in MEDLINE journals but the articles are out of scope, or
        #     * they are from issues published prior to the date the journal was selected for indexing, or
        #     * citations to articles from journals that deposit their full text articles in PMC but have not yet been recommended for indexing in MEDLINE),
        #     * search for pubmednotmedline[sb] in the search box:
        #       pubmednotmedline[sb]
        # 2019/01/04 PubMed Query returns    422,513 results: inprocess[sb] NOT pubmed pmc[sb]
        # 2019/01/04 PubMed Query returns    137,704 results: inprocess[sb] AND pubmed pmc[sb]
        #%%% % PubMed Query: author manuscript[sb] AND pubmed pmc[sb]
        #%%% % PubMed Query: pubmed pmc[sb]
        # PubMed Query: pubmed pmc[sb] AND pubmednotmedline[sb]
        # PubMed Query: pubmed pmc[sb] AND pubmednotmedline[sb]
        # PubMed Query: author manuscript[sb] AND pubmed pmc[sb]
        return name2cnt

    def prt_content_counts(self, name2cnt, prt=sys.stdout):
        """Print the content typename and the count of that type"""
        for name, query in self.name2query.items():
            cnt = name2cnt[name]
            prt.write('    # {N:10,} {NAME:20} {Q}\n'.format(N=cnt, NAME=name, Q=query))

    def prt_content_cntdct(self, name2cnt, prt=sys.stdout):
        """Print the content typename and the count of that type"""
        # prt.write('    cnts = {\n')
        prt.write('    return {\n')
        for name in self.name2query:
            cnt = name2cnt[name]
            prt.write('        "{NAME}": {N},\n'.format(N=cnt, NAME=name))
        prt.write('    }\n')

    @staticmethod
    def _get_content_brokenbars(a2n, yval):
        """Transform the content counts to broken bar data"""
        par = {'edgecolor': 'black', 'linewidth':0.0, 'alpha':1.0}
        ml1 = a2n['medline_pmc0']
        ml2 = ml1 + a2n['inprocess_A_pmc0']  # PMC inprocess start
        ml3 = ml2 + a2n['inprocess_A_pmc1']  # PMC start
        ml4 = ml3 + a2n['medline_pmc1']
        # pylint: disable=bad-whitespace
        return [
            # All PubMed
            ## ([(0, a2n['all'])],                ( 0, 2), {'facecolors':'k', **par}),
            # MEDLINE
            ([(0, ml1)],                      (yval, 1.8), {'label':'MEDLINE', 'facecolors':'tab:blue', **par}),
            ([(ml1, a2n['inprocess_A_all'])], (yval, 1.8), {'label':'MEDLINE in process', 'facecolors':'tab:cyan', **par}),
            ([(ml3, a2n['medline_pmc1'])],    (yval, 1.8), {'facecolors':'tab:blue', **par}),
            # PMC
            ([(ml2, a2n['inprocess_A_pmc1'])], (yval-2, 1.8), {'facecolors':'tab:cyan', **par}),
            ([(ml3, a2n['medline_pmc1'])],     (yval-2, 1.8), {'facecolors':'tab:blue', **par}),
            ([(ml4, a2n['pmnml_A_pmc1'] + a2n['pmc_unknown'])], (yval-2, 1.8), {'label':'PMC Only', 'facecolors':'y', **par}),
            # Other
            ([(a2n['ml1_pmc1'], a2n['all_ml0_pmc0'])], (yval-4, 1.8), {'label':'Other', 'facecolors':'tab:orange', **par}),
        ]

    @staticmethod
    def chk_content_counts(a2n):
        """Check the content typename and the count of that type"""
        assert a2n['nihms_pub0'] + a2n['nihms_pub1'] == a2n['nihms']
        assert a2n['pmcsd_pmc0'] + a2n['pmcsd_pmc1'] == a2n['pmcsd']
        assert a2n['medline_pmc0'] + a2n['medline_pmc1'] == a2n['medline_all']
        #    557,390 inprocess_A_all      inprocess[sb]
        #    422,103 inprocess_A_pmc0     inprocess[sb] NOT pubmed pmc[sb]
        #    135,287 inprocess_A_pmc1     inprocess[sb] AND pubmed pmc[sb]
        #    557,390 inprocess_ml0        inprocess[sb] NOT medline[sb]
        #          0 inprocess_ml1        inprocess[sb] AND medline[sb]
        assert a2n['inprocess_A_all'] == a2n['inprocess_A_pmc0'] + a2n['inprocess_A_pmc1']
        # 30,514,237 all          all [sb]
        #  1,818,474 all_ml0_pmc0 all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb]
        # 28,695,763 ml1_pmc1     inprocess[sb] OR medline[sb] OR pubmed pmc[sb]
        assert a2n['all'] == a2n['all_ml0_pmc0'] + a2n['ml1_pmc1']
        #  3,116,339 pmnml_A              pubmednotmedline[sb]
        #  3,116,339 pmnml_B              pubmednotmedline[sb] NOT medline[sb]
        #  3,116,339 pmnml_C_ip0          pubmednotmedline[sb] NOT inprocess[sb]
        #          0 pmnml_0_ip1          pubmednotmedline[sb] AND inprocess[sb]
        #  1,612,274 pmnml_A_pmc1         pubmednotmedline[sb] AND pubmed pmc[sb]
        #  1,504,065 pmnml_A_pmc0         pubmednotmedline[sb] NOT pubmed pmc[sb]
        assert a2n['pmnml_A'] == a2n['pmnml_A_pmc1'] + a2n['pmnml_A_pmc0']
        #  5,323,939 pmc_all              pubmed pmc[sb]
        #    135,287 inprocess_A_pmc1     inprocess[sb] AND pubmed pmc[sb]
        #  3,503,057 medline_pmc1         medline[sb] AND pubmed pmc[sb]
        #  1,612,274 pmnml_A_pmc1         pubmednotmedline[sb] AND pubmed pmc[sb]
        pmc_notmedline = a2n['pmc_all'] - a2n['medline_pmc1'] - a2n['inprocess_A_pmc1']
        print('  {N:10,} of {M:10,} PMC (not MEDLINE)'.format(M=a2n['pmc_all'], N=pmc_notmedline))
        print(pmc_notmedline - a2n['pmnml_A_pmc1'])
        print('  {N:10,} of {M:10,} PubMed(not MEDLINE, PMC)'.format(
            N=a2n['all_ml0_pmc0'], M=a2n['all']))
        print('  {T:10,} = {A:10,} (MEDLINE OR PMC) + {B:10,} (not MEDLINE OR PMC)'.format(
            T=a2n['ml1_pmc1'] + a2n['all_ml0_pmc0'],
            A=a2n['ml1_pmc1'],
            B=a2n['all_ml0_pmc0']))
        total = a2n['all']
        au_all = a2n['au_all']
        print('  {N:10,} of {M:10,} {P:3.5f}% author ms'.format(N=au_all, M=total, P=100.0*au_all/total))
        print('  {T:10,} = {A:10,} (MEDLINE OR PMC) + {B:10,} (not MEDLINE OR PMC)'.format(
            T=a2n['ml1_pmc1'] + a2n['all_ml0_pmc0'],
            A=a2n['ml1_pmc1'],
            B=a2n['all_ml0_pmc0']))

    def dnld_count(self, query):
        """Searches an NCBI database for a user search term, returns NCBI IDs."""
        dct = self.run_eutilscmd('esearch', db='pubmed', term=query, rettype='count', retmode='json')
        if 'count' in dct:
            return int(dct['count'])
        return dct

    def _add_bounding_lines_all(self, xend, ymax):
        """Add bounding lines"""
        plt.plot((0, 0), (ymax-9, ymax+1), color='k', linewidth=0.4)        # LEFT  PubMed LINE
        plt.plot((xend, xend), (ymax-9, ymax+1), color='k', linewidth=0.4)  # RIGHT PubMed LINE
        plt.arrow(7200000, ymax, -7300000, 0, **self.arrow_p)
        plt.arrow(23800000, ymax, xend-23800000, 0, **self.arrow_p)
        txt = '~{N:4.1f} million (M) citations in PubMed'.format(N=round(xend/1000000.0, 1))
        plt.annotate(txt, (7400000, ymax-.5))

    def _add_bounding_lines_medline(self, xend, yval, xmax):
        """Add bounding lines"""
        plt.plot((xend, xend), (yval-5.7, yval+1), color='k', linewidth=0.4)   # BLUE-YELLOW DIVIDER
        plt.plot((xend, xend), (yval-11, yval-6.3), color='k', linewidth=0.4)  # BLUE-YELLOW DIVIDER
        plt.arrow(7200000, yval, -7300000, 0, **self.arrow_p)
        plt.arrow(18800000, yval, xend-18800000, 0, **self.arrow_p)
        txt = '~{N:4.1f}M ({P:4.1f}%) MEDLINE'.format(
            N=round(xend/1000000.0, 1), P=100.0*xend/xmax)
        plt.annotate(txt, (7400000, yval-.5))

    def _add_bounding_lines_pmc(self, a2n, yval, xmax):
        """Add bounding lines"""
        #   # PMC
        #   ([(ml2, a2n['inprocess_A_pmc1'])], (23, 1.8), {'facecolors':'tab:cyan', **par}),
        #   ([(ml3, a2n['medline_pmc1'])],     (23, 1.8), {'facecolors':'tab:blue', **par}),
        #   ([(ml4, a2n['pmnml_A_pmc1'] + a2n['pmc_unknown'])], (23, 1.8), {'facecolors':'y', **par}),
        pmc_x0 = a2n['medline_pmc0'] + a2n['inprocess_A_pmc0']
        pmc_all = a2n['pmc_all']
        pmc_xn = pmc_x0 + pmc_all
        plt.plot((pmc_x0, pmc_x0), (yval-1.7, yval+3), color='k', linewidth=0.4)  # UPPER CYAN DIVIDER
        plt.arrow(pmc_x0-6600000, yval, 6600000, 0, **self.arrow_p)
        plt.arrow(pmc_xn+1300000, yval, -1300000, 0, **self.arrow_p)
        txt = '~{N:5.1f}M ({P:3.1f}%) PMC'.format(N=round(pmc_all/1000000.0), P=100.0*pmc_all/xmax)
        plt.annotate(txt, (7400000, yval-.5))

    def _add_bounding_lines_other(self, other_sz, yval, xmax):
        """Add bounding lines"""
        xval = xmax - other_sz
        plt.plot((xval, xval), (yval-7, yval+3), color='k', linewidth=0.4)  # YELLOW-ORANGE DIVIDER
        plt.arrow(xval-11200000, yval, 11200000, 0, **self.arrow_p)
        plt.arrow(xmax+600000, yval, -600000, 0, **self.arrow_p)
        txt = '~{N:5.1f}M ({P:5.1f}%) Other'.format(N=round(other_sz/1000000.0), P=100.0*other_sz/xmax)
        plt.annotate(txt, (7400000, yval-.5))

    def _add_bounding_lines_pmc_100(self, a2n, yval):
        """Add bounding lines"""
        #   # PMC
        #   ([(ml2, a2n['inprocess_A_pmc1'])], (23, 1.8), {'facecolors':'tab:cyan', **par}),
        #   ([(ml3, a2n['medline_pmc1'])],     (23, 1.8), {'facecolors':'tab:blue', **par}),
        #   ([(ml4, a2n['pmnml_A_pmc1'] + a2n['pmc_unknown'])], (23, 1.8), {'facecolors':'y', **par}),
        pmc_all = a2n['pmc_all']
        pmc_ml1 = a2n['medline_pmc1'] + a2n['inprocess_A_pmc1']
        pmc_ml0 = pmc_all - pmc_ml1
        pmc_x0 = a2n['medline_pmc0'] + a2n['inprocess_A_pmc0']
        pmc_x1 = pmc_x0 + pmc_ml1
        pmc_xn = pmc_x0 + pmc_all
        plt.plot((pmc_x0, pmc_x0), (yval-5, yval+1.7), color='k', linewidth=0.4)  # LOWER CYAN DIVIDER
        # PMC AND MEDLINE
        plt.annotate('MEDLINE', (pmc_x0+pmc_ml1/2.0, yval-1.1), ha='center', va='center', fontsize=8)
        # PMC|MEDLINE
        plt.arrow(pmc_x0+900000, yval-2.3, -900000, 0, **self.arrow_p)
        plt.arrow(pmc_x1-900000, yval-2.3, 900000, 0, **self.arrow_p)
        plt.arrow(pmc_xn+700000, yval-2.3, -700000, 0, **self.arrow_p)
        txt_ml1 = '{P:2.0f}%'.format(P=round(100.0*pmc_ml1/pmc_all))
        plt.annotate(txt_ml1, (pmc_x0+pmc_ml1/2.0, yval-2.3), ha='center', va='center', fontsize=8)
        txt_ml0 = '{P:2.0f}%'.format(P=round(100.0*(pmc_all-pmc_ml1)/pmc_all))
        plt.annotate(txt_ml0, (pmc_x1 + pmc_ml0/2.0, yval-2.3), ha='center', va='center', fontsize=8)
        # PMC
        plt.arrow(pmc_x0+1600000, yval-4, -1600000, 0, **self.arrow_p)
        plt.arrow(pmc_xn-1600000, yval-4, 1600000, 0, **self.arrow_p)
        plt.annotate('PMC', (pmc_x0+pmc_all/2.0, yval-4), ha='center', va='center')

    def plt_content_counts(self, fout_png, a2n):
        """Plot pubmed content"""
        xmax = a2n['all']
        ymax = 14.5
        # Remove automatically-added 5% axes padding
        mpl.rcParams['axes.autolimit_mode'] = 'data'  # 'data' or 'round_numbers'
        mpl.rcParams['axes.xmargin'] = 0
        mpl.rcParams['axes.ymargin'] = 0
        # Get figure and axes with axes turned off and axes whitespace removed
        fig, axes = plt.subplots()
        fig.set_size_inches(6.4, 1.8)
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        axes.set_frame_on(False)
        axes.set_xlim(0, xmax+500000)
        axes.set_ylim(0, ymax+1)
        axes.grid(False)
        # Add horizontal bars for: PubMed, PMC, and other
        bbars = []
        for xvals, yval, dct in self._get_content_brokenbars(a2n, ymax-5):
            bbars.append(axes.broken_barh(xvals, yval, **dct))
        # Add Dimension lines
        self._add_bounding_lines_all(xmax, ymax)
        self._add_bounding_lines_medline(a2n['medline_n_inprocess'], ymax-2, xmax)
        self._add_bounding_lines_pmc(a2n, ymax-6, xmax)
        self._add_bounding_lines_other(a2n['all_ml0_pmc0'], ymax-8, xmax)
        self._add_bounding_lines_pmc_100(a2n, ymax-10)
        # Add legend
        axes.legend(loc='lower left', fontsize=8, ncol=2,
                    bbox_to_anchor=(0.015, 0.0), borderaxespad=0.1,
                    handletextpad=.2, columnspacing=1.0, labelspacing=.2)
        # Save figure
        plt.savefig(fout_png, bbox_inches='tight', pad_inched=0, dpi=300)
        print('  WROTE: {PNG}'.format(PNG=fout_png))


# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
