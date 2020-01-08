"""Plot the types of content and their amount in PubMed"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from pmidcite.eutils.cmds.base import EntrezUtilities


# pylint: disable=line-too-long
class PubMedContents(EntrezUtilities):
    """Describe the percentage of various types of content in PubMed"""

    # https://pubmed.ncbi.nlm.nih.gov/help/#citation-status-subsets
    name2query = cx.OrderedDict([
        ('all', 'all [sb]'),
        ('all_ml0_pmc0', 'all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb]'),
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
        ('inprocess_all', 'inprocess[sb]'),
        ('inprocess_pmc0', 'inprocess[sb] NOT pubmed pmc[sb]'),
        ('inprocess_pmc1', 'inprocess[sb] AND pubmed pmc[sb]'),
        ('medline_inprocess', 'medline[sb] OR inprocess[sb]'),
        # medline[sb]:
        #   Citations that have been indexed with MeSH terms, Publication Types, Substance Names, etc.
        ('medline_all', 'medline[sb]'),
        ('medline_pmc0', 'medline[sb] NOT pubmed pmc[sb]'),
        ('medline_pmc1', 'medline[sb] AND pubmed pmc[sb]'),
        # pubmed pmc[sb]:
        #   Citations in PMC
        ('pmc_all', 'pubmed pmc[sb]'),
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
        ('pm_ml0', 'pubmednotmedline[sb]'),
        ('pm_ml0b', 'pubmednotmedline[sb] NOT medline[sb]'),
        ('pm_ml0_ip1', 'pubmednotmedline[sb] AND inprocess[sb]'),
        ('pm_ml0_ip0', 'pubmednotmedline[sb] NOT inprocess[sb]'),
        ('pm_ml0_pmc1', 'pubmednotmedline[sb] AND pubmed pmc[sb]'),
        ('pm_ml0_pmc0', 'pubmednotmedline[sb] NOT pubmed pmc[sb]'),
        # pmcbook:
        #   Book and book chapter citations available on the NCBI Bookshelf.
        ('pmcbook', 'pmcbook'),
        ('pmcbook_ml0', 'pmcbook NOT medline[sb]'),
        ('pmcbook_pmc0', 'pmcbook NOT pubmed pmc[sb]'),
    ])

    arrow_p = {
        'linewidth':0.4,
        'shape':'full',
        'length_includes_head':True,
        'head_width':.5,
        'head_length':400000,
        'overhang':1.0
    }

    def __init__(self, email, apikey, tool):
        super(PubMedContents, self).__init__(email, apikey, tool)

    def dnld_content_counts(self):
        """Get the count of various types of content in PubMed"""
        name2cnt = {}
        for name, query in self.name2query.items():
            name2cnt[name] = self.dnld_count(query)
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
        for name in self.name2query():
            cnt = name2cnt[name]
            prt.write('        "{NAME}": {N},\n'.format(N=cnt, NAME=name))
        prt.write('    }\n')

    @staticmethod
    def chk_content_counts(a2n):
        """Check the content typename and the count of that type"""
        assert a2n['nihms_pub0'] + a2n['nihms_pub1'] == a2n['nihms']
        assert a2n['pmcsd_pmc0'] + a2n['pmcsd_pmc1'] == a2n['pmcsd']
        assert a2n['medline_pmc0'] + a2n['medline_pmc1'] == a2n['medline_all']
        assert a2n['inprocess_pmc0'] + a2n['inprocess_pmc1'] == a2n['inprocess_all']
        assert a2n['ml1_pmc1'] + a2n['all_ml0_pmc0'] == a2n['all']
        pmc_notmedline = a2n['pmc_all'] - a2n['medline_pmc1'] - a2n['inprocess_pmc1']
        print('  {N:10,} of {M:10,} PMC (not MEDLINE)'.format(M=a2n['pmc_all'], N=pmc_notmedline))
        print(pmc_notmedline - a2n['pm_ml0_pmc1'])
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

    def plt_content_counts(self, fout_png, a2n):
        """Plot pubmed content"""
        fig, axes = plt.subplots()
        for xvals, yval, dct in self._get_content_brokenbars(a2n):
            axes.broken_barh(xvals, yval, **dct)
        axes.set_ylim(0, 35)
        xmax = a2n['all']
        self._add_bounding_lines_all(xmax, 2)
        self._add_bounding_lines_medline(a2n['medline_inprocess'], 4, xmax)
        self._add_bounding_lines_inprocess(a2n, 6, xmax)
        self._add_bounding_lines_pmc(a2n, 10, xmax)
        ## axes.set_xlim(0, 200)
        ## axes.set_xlabel('seconds since start')
        ## axes.set_yticks([15, 25])
        ## axes.set_yticklabels(['All', 'MEDLINE'])
        axes.grid(False)
        ## axes.annotate('race interrupted', (61, 25),
        ##             xytext=(0.8, 0.9), textcoords='axes fraction',
        ##             arrowprops=dict(facecolor='black', shrink=0.05),
        ##             fontsize=16,
        ##             horizontalalignment='right', verticalalignment='top')
        plt.savefig(fout_png, bbox_inches='tight', pad_inched=0, dpi=200)
        print('  WROTE: {PNG}'.format(PNG=fout_png))

    def _add_bounding_lines_pmc(self, a2n, yval, xmax):
        """Add bounding lines"""
        pmc_x0 = a2n['medline_pmc0'] + a2n['inprocess_pmc0']
        pmc_all = a2n['pmc_all'] - a2n['inprocess_pmc1']
        plt.plot((pmc_x0, pmc_x0), (yval-1, yval+30), color='k', linewidth=0.4)
        plt.plot((pmc_x0+pmc_all, pmc_x0+pmc_all), (yval-1, yval+30), color='k', linewidth=0.4)
        # plt.arrow(7200000, yval, -7300000, 0, **self.arrow_p)
        # txt = '~{N:4.1f} million ({P:4.1f}%) MEDLINE'.format(
        #     N=round(xend/1000000.0, 1), P=100.0*xend/xmax)
        # plt.annotate(txt, (7400000, yval-.5))
        # plt.arrow(22500000, yval, xend-22500000, 0, **self.arrow_p)

    def _add_bounding_lines_all(self, xend, yval):
        """Add bounding lines"""
        plt.axvline(x=0, color='k', linewidth=0.4)
        plt.axvline(x=xend, color='k', linewidth=0.4)
        plt.arrow(7200000, yval, -7300000, 0, **self.arrow_p)
        txt = '~{N:4.1f} million citations in PubMed'.format(
            N=round(xend/1000000.0, 1))
        plt.annotate(txt, (7400000, yval-.5))
        plt.arrow(23500000, yval, xend-23500000, 0, **self.arrow_p)

    def _add_bounding_lines_medline(self, xend, yval, xmax):
        """Add bounding lines"""
        plt.plot((xend, xend), (yval-1, yval+2.8), color='k', linewidth=0.4)
        plt.arrow(7200000, yval, -7300000, 0, **self.arrow_p)
        txt = '~{N:4.1f} million ({P:4.1f}%) MEDLINE'.format(
            N=round(xend/1000000.0, 1), P=100.0*xend/xmax)
        plt.annotate(txt, (7400000, yval-.5))
        plt.arrow(22500000, yval, xend-22500000, 0, **self.arrow_p)

    def _add_bounding_lines_inprocess(self, a2n, yval, xmax):
        """Add bounding lines"""
        xip = a2n['inprocess_all']
        xp0 = a2n['medline_pmc0']
        xp1 = xp0 + xip
        plt.plot((xp0, xp0), (yval-1, yval+.8), color='k', linewidth=0.4)
        plt.plot((xp1, xp1), (yval-1, yval+.8), color='k', linewidth=0.4)
        plt.arrow(xp0-2000000, yval, 2000000, 0, **self.arrow_p)
        plt.arrow(xp1+2000000, yval, -2000000, 0, **self.arrow_p)
        txt = '~{N:3.0f}k ({P:3.1f}%) in process'.format(
            N=round(xip/1000.0), P=100.0*xip/xmax)
        plt.annotate(txt, (9000000, yval-.5))

    @staticmethod
    def _get_content_brokenbars(a2n):
        """Transform the content counts to broken bar data"""
        par = {'edgecolor': 'black', 'linewidth':0.0, 'alpha':1.0}
        ml1 = a2n['medline_pmc0']
        ml2 = ml1 + a2n['inprocess_pmc0']
        ml3 = ml2 + a2n['inprocess_pmc1']
        ml4 = ml3 + a2n['medline_pmc1']
        # pylint: disable=bad-whitespace
        return [
            # All PubMed
            ## ([(0, a2n['all'])],                ( 0, 2), {'facecolors':'k', **par}),
            # MEDLINE
            ([(0, ml1)],                       ( 7, 1.8), {'facecolors':'tab:blue', **par}),
            ([(ml1, a2n['inprocess_all'])],    ( 7, 1.8), {'facecolors':'tab:cyan', **par}),
            # ([(ml1, a2n['inprocess_pmc0'])], ( 7, 1.8), {'facecolors':'tab:orange', **par}),
            # ([(ml2, a2n['inprocess_pmc1'])], ( 7, 1.8), {'facecolors':'tab:green', **par}),
            ([(ml3, a2n['medline_pmc1'])],     ( 7, 1.8), {'facecolors':'tab:blue', **par}),
            # PMC
            ([(ml2, a2n['inprocess_pmc1'])],   ( 9, 1.8), {'facecolors':'tab:cyan', **par}),
            ([(ml3, a2n['medline_pmc1'])],     ( 9, 1.8), {'facecolors':'tab:blue', **par}),
            ([(ml4, a2n['pm_ml0_pmc1'])],      ( 9, 1.8), {'facecolors':'y', **par}),
            # Full PMC to compare against brokenbar PMC
            # ([(ml2, a2n['pmc_all'])],          (15, 2), {'facecolors':'tab:cyan', **par}),
            #
            ([(a2n['ml1_pmc1'], a2n['all_ml0_pmc0'])],  (11, 1.8), {'facecolors':'tab:orange', **par}),
            # ([(ml2, a2n['inprocess_pmc1'])],   (10, 2), {'facecolors':'tab:cyan', **par}),
            # ([(ml3, a2n['inprocess_pmc1'])],   (10, 2), {'facecolors':'tab:cyan', **par}),
            ## ([(110, 30), (150, 10)], (10, 9), {'facecolors':'tab:blue'}),
            ## ([(10, 50), (100, 20), (130, 10)], (20, 9), {'facecolors':('tab:orange', 'tab:green', 'tab:red')}),
        ]


# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
