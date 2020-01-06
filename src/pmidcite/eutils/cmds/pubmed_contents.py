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
        # publisher[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT # pmcbook:
        #   Citations recently added to PubMed via electronic submission
        #   from a publisher, and are soon to proceed to the next stage,
        #   PubMed - in process (see below). Also for citations received
        #   before late 2003 if they are from journals not indexed for
        #   MEDLINE, or from a journal that was accepted for MEDLINE
        #   after the citations' publication date. These citations
        #   bibliographic data have not been reviewed.
        ('pub_init', 'publisher[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook'),
        ('pub', 'publisher[sb]'),
        # pubstatusnihms AND publisher[sb]:
        #   Author manuscripts submitted to PMC that fall under the NIH Public Access Policy.
        ('pub_author_ms', 'pubstatusnihms AND publisher[sb]'),
        # pubstatuspmcsd AND publisher[sb]:
        #   Records for selective deposit articles in PMC.
        #   These are articles published in non-MEDLINE journals
        #   where the publisher has chosen to deposit in PMC
        #   only those articles that fall under the NIH Public Access Policy.
        ('pub_pmc', 'pubstatusnihms AND publisher[sb]'),
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
        ('au_all', 'author manuscript all[sb]'),
        ('au_ml1', 'author manuscript[sb] AND medline[sb]'),
        ('au_pmc1', 'author manuscript[sb] AND pubmed pmc[sb]'),
        ('au_pmc0', 'author manuscript[sb] NOT pubmed pmc[sb]'),
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
        # pmcbook[sb]:
        #   Book and book chapter citations available on the NCBI Bookshelf.
        ('pmcbook', 'pmcbook[sb]'),
        ('pmcbook_ml0', 'pmcbook[sb] NOT medline[sb]'),
        ('pmcbook_pmc0', 'pmcbook[sb] NOT pubmed pmc[sb]'),
    ])

    arrow_p = {
        'linewidth':0.5,
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
            prt.write('  {N:10,} {NAME:20} {Q}\n'.format(N=cnt, NAME=name, Q=query))

    def prt_content_cntdct(self, name2cnt, prt=sys.stdout):
        """Print the content typename and the count of that type"""
        prt.write('    cnts = {\n')
        for name, query in self.name2query.items():
            cnt = name2cnt[name]
            prt.write('        "{NAME}": {N},\n'.format(N=cnt, NAME=name, Q=query))
        prt.write('    }\n')

    @staticmethod
    def chk_content_counts(a2n):
        """Check the content typename and the count of that type"""
        assert a2n['medline_pmc0'] + a2n['medline_pmc1'] == a2n['medline_all']
        assert a2n['inprocess_pmc0'] + a2n['inprocess_pmc1'] == a2n['inprocess_all']
        print('  {N:10,} PMC leftover'.format(N=a2n['pmc_all'] - a2n['medline_pmc1'] - a2n['inprocess_pmc1']))

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
        self._add_bounding_lines(a2n['all'], axes)
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

    def _add_bounding_lines(self, xend, axes):
        """Add bounding lines"""
        plt.axvline(x=0, color='k', linewidth=0.5)
        plt.axvline(x=xend, color='k', linewidth=0.5)
        plt.arrow(7200000, 2, -7300000, 0, **self.arrow_p)
        plt.annotate('~30.5 million citations in PubMed', (7400000, 1.5))
        plt.arrow(23500000, 2, xend-23500000, 0, **self.arrow_p)

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
            ([(0, ml1)],                       ( 5, 2), {'facecolors':'tab:blue', **par}),
            ([(ml1, a2n['inprocess_all'])],    ( 5, 2), {'facecolors':'tab:cyan', **par}),
            # ([(ml1, a2n['inprocess_pmc0'])], ( 5, 2), {'facecolors':'tab:orange', **par}),
            # ([(ml2, a2n['inprocess_pmc1'])], ( 5, 2), {'facecolors':'tab:green', **par}),
            ([(ml3, a2n['medline_pmc1'])],     ( 5, 2), {'facecolors':'tab:blue', **par}),
            # PMC
            ([(ml2, a2n['inprocess_pmc1'])],   (10, 2), {'facecolors':'tab:cyan', **par}),
            ([(ml3, a2n['medline_pmc1'])],     (10, 2), {'facecolors':'tab:blue', **par}),
            #
            ([(ml2, a2n['pmc_all'])],          (15, 2), {'facecolors':'tab:cyan', **par}),
            # ([(ml2, a2n['inprocess_pmc1'])],   (10, 2), {'facecolors':'tab:cyan', **par}),
            # ([(ml3, a2n['inprocess_pmc1'])],   (10, 2), {'facecolors':'tab:cyan', **par}),
            ## ([(110, 30), (150, 10)], (10, 9), {'facecolors':'tab:blue'}),
            ## ([(10, 50), (100, 20), (130, 10)], (20, 9), {'facecolors':('tab:orange', 'tab:green', 'tab:red')}),
        ]


# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
