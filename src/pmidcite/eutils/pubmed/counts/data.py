"""Manage counts for various types of PubMed data"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx

# Notes from on non-MEDLINE citations accessible through PubMed:
#     McKeever, Liam et al.
#    "Demystifying the Search Button"
#     Journal of Parenteral and Enteral Nutrition (2015)
#
# Of the remaining 11.1%:
#     * 23.3% are in the process of becoming MEDLINE indexed,
#     * 15.3% have been submitted by the publisher and may become MEDLINE indexed in the future,
#     * 51.7% are available on PubMed but will not be indexed by MEDLINE, and
#     * 9.7% belong to an older version of MEDLINE

# pylint: disable=line-too-long
class DataMgr:
    """Manage counts for various types of PubMed data"""

    ntobj = cx.namedtuple('Nt', 'count perc')

    def __init__(self, abc2count):
        self.a2n = abc2count
        # All of PubMed
        self.tot_pubmed = abc2count['all']
        # MEDLINE, PMC, and inprocess
        self.tot_pmc = abc2count['ml1_pmc1']
        self.pltdata_pubmed = self._init_plot_data_pubmed()

    def _init_plot_data_pubmed(self):
        """Get data for the PubMed contents plot"""
        # pylint: disable=bad-whitespace
        name_data = []
        a2n = self.a2n
        #
        name_data.append(('PubMed',              self._get_nt_pubmed(a2n['all'])))
        name_data.append(('MEDLINE_and_PMC',     self._get_nt_pubmed(a2n['ml1_pmc1'])))
        name_data.append(('MEDLINE_n_inprocess', self._get_nt_pubmed(a2n['medline_n_inprocess'])))
        name_data.append(('PMC',                 self._get_nt_pubmed(a2n['pmc_all'])))
        name_data.append(('PMC_ml',              self._get_nt_pubmed(a2n['pmc_m1'])))
        name_data.append(('PMC_only',            self._get_nt_pubmed(a2n['pmc_m0'])))
        name_data.append(('other',               self._get_nt_pubmed(a2n['all_ml0_pmc0'])))
        #
        name_data.append(('ip',         self._get_nt_pubmed(a2n['inprocess_A_all'])))
        name_data.append(('ip_pmc0',    self._get_nt_pubmed(a2n['inprocess_A_pmc0'])))
        name_data.append(('ip_pmc1',    self._get_nt_pubmed(a2n['inprocess_A_pmc1'])))
        #
        name_data.append(('pmc_ip1',    self._get_nt_pubmed(a2n['inprocess_A_pmc1'])))
        name_data.append(('pmc_ml1',    self._get_nt_pubmed(a2n['medline_pmc1'])))
        name_data.append(('pmc_ml0',    self._get_nt_pubmed(a2n['pmc_m0'])))
        #
        name_data.append(('ml_pmc0',     self._get_nt_pubmed(a2n['medline_pmc0'])))
        name_data.append(('ml_pmc0_ip1', self._get_nt_pubmed(a2n['inprocess_A_pmc0'])))
        name_data.append(('ml_pmc1_ip1', self._get_nt_pubmed(a2n['inprocess_A_pmc1'])))
        name_data.append(('ml_pmc1',     self._get_nt_pubmed(a2n['medline_pmc1'])))
        dct = cx.OrderedDict(name_data)
        # Check that counts for the PubMed content figure add up
        #                             BLUE|CYAN|BROWN              + ORANGE
        assert dct['PubMed'].count == dct['MEDLINE_and_PMC'].count + dct['other'].count
        #                             BLUE|CYAN                        + BROWN                 + ORANGE
        assert dct['PubMed'].count == dct['MEDLINE_n_inprocess'].count + dct['PMC_only'].count + dct['other'].count
        #                             CYAN
        assert dct['ip'].count == dct['ip_pmc0'].count + dct['ip_pmc1'].count
        #                             CYAN                BLUE                   BROWN
        assert dct['PMC'].count == dct['pmc_ip1'].count + dct['pmc_ml1'].count + dct['pmc_ml0'].count
        #                                          BLUE                   CYAN                       CYAN                   BROWN
        assert dct['MEDLINE_n_inprocess'].count == dct['ml_pmc0'].count + dct['ml_pmc0_ip1'].count + dct['ml_pmc1_ip1'].count + dct['ml_pmc1'].count
        #                          CYAN|BLUE             BROWN
        assert dct['PMC'].count == dct['PMC_ml'].count + dct['PMC_only'].count
        return dct

    def _get_nt_pubmed(self, cnt):
        """Return namedtuple with count and percentage data"""
        return self.ntobj(count=cnt, perc=100.0*(cnt/self.tot_pubmed))

    def get_pubmed_xvals(self):
        """Get the colorbar data for the PubMed plot"""
        a2n = self.pltdata_pubmed
        xvals = [a2n['ml_pmc0'].count]                      # 0
        xvals.append(xvals[-1] + a2n['ml_pmc0_ip1'].count)  # 1
        xvals.append(xvals[-1] + a2n['ml_pmc1_ip1'].count)  # 2
        xvals.append(xvals[-1] + a2n['ml_pmc1'].count)      # 3
        xvals.append(xvals[-1] + a2n['PMC_only'].count)     # 4
        # print(a2n['PubMed'], xvals[-1] + a2n['other'].count)
        assert a2n['PubMed'].count == xvals[-1] + a2n['other'].count
        return xvals

    def get_pubmed_colorbars(self, yval):
        """Get the colorbar data for the PubMed plot"""
        par = {'edgecolor': 'black', 'linewidth':0.0, 'alpha':1.0}
        xvals = self.get_pubmed_xvals()
        a2n = self.pltdata_pubmed
        # pylint: disable=bad-whitespace
        # pylint: disable=line-too-long
        return [
            # All PubMed
            ## ([(0, a2n['all'])],                ( 0, 2), {'facecolors':'k', **par}),
            # MEDLINE
            ([(0,        a2n['ml_pmc0'].count)], (yval-1, 1.8), {'label':'MEDLINE', 'facecolors':'tab:blue', **par}),
            ([(xvals[0], a2n['ip'].count)],      (yval-1, 1.8), {'label':'MEDLINE in process', 'facecolors':'lawngreen', **par}),
            ([(xvals[2], a2n['ml_pmc1'].count)], (yval-1, 1.8), {'facecolors':'tab:blue', **par}),
            # PMC
            ([(xvals[1], a2n['pmc_ip1'].count)], (yval-3, 1.8), {'facecolors':'lawngreen', **par}),
            ([(xvals[2], a2n['pmc_ml1'].count)], (yval-3, 1.8), {'facecolors':'tab:blue', **par}),
            ([(xvals[3], a2n['pmc_ml0'].count)], (yval-3, 1.8), {'label':'PMC Only', 'facecolors':'brown', **par}),
            # Other
            ([(xvals[4], a2n['other'].count)],   (yval-7, 1.8), {'label':'Other', 'facecolors':'tab:orange', **par}),
        ]

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
