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

class DataMgr:
    """Manage counts for various types of PubMed data"""

    ntobj = cx.namedtuple('Nt', 'count perc')

    def __init__(self, abc2count):
        self.a2n = abc2count
        # All of PubMed
        self.tot_pubmed = abc2count['all']
        # MEDLINE, PMC, and inprocess
        self.tot_pmc = abc2count['ml1_pmc1']

    def get_plot_data_pubmed(self):
        """Get data for the PubMed contents plot"""
        # pylint: disable=bad-whitespace
        name_data = []
        a2n = self.a2n
        # PubMed
        name_data.append(('PubMed',           self.get_nt_pubmed(a2n['all'])))
        # MEDLINE, PMC, and inprocess
        name_data.append(('PMC',             self.get_nt_pubmed(a2n['ml1_pmc1'])))
        # MEDLINE
        name_data.append(('MEDLINE_and_PMC', self.get_nt_pubmed(a2n['medline_n_inprocess'])))
        # PMC: All
        cnt_pmc                      = self.get_nt_pubmed(a2n['pmc_all'])
        # cnt_cur = a2n['inprocess_A_pmc1'] +
        # PMC: MEDLINE and in process to be MEDLINE
        return cx.OrderedDict(name_data)

    def get_nt_pubmed(self, cnt):
        """Return namedtuple with count and percentage data"""
        return self.ntobj(count=cnt, perc=100.0*(cnt/self.tot_pubmed))


# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
