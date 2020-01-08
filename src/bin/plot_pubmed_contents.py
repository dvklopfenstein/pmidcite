#!/usr/bin/env python3
"""Plot the types of content and their amount in PubMed"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import datetime
from pmidcite.cfg import Cfg
from pmidcite.eutils.cmds.pubmed_contents import PubMedContents


def main(dnld=False):
    """Plot the types of content and their amount in PubMed"""
    date = str(datetime.datetime.now().date()).replace('-', '_')
    fout_png = 'log/pubmed_content/pubmed_content_{DATE}.png'.format(DATE=date)
    fout_png = 'pubmed_content_{DATE}.png'.format(DATE=date)
    cfg = Cfg()
    obj = PubMedContents(cfg.get_email(), cfg.get_apikey(), cfg.get_tool())
    name2cnt = obj.dnld_content_counts() if dnld else _get_name2cnt()
    print('    # {DATE}'.format(DATE=date))
    obj.prt_content_counts(name2cnt)
    if dnld:
        obj.prt_content_cntdct(name2cnt)
    obj.chk_content_counts(name2cnt)
    obj.plt_content_counts(fout_png, name2cnt)

def _get_name2cnt():
    """Return saved counts, rather than re-downloading"""
    # 2020_01_08:

    # 30,514,237 all                  all [sb]
    #  1,818,474 all_ml0_pmc0         all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb]
    # 28,695,763 ml1_pmc1             inprocess[sb] OR medline[sb] OR pubmed pmc[sb]
    #    310,768 pub_init0            publisher[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook
    #     76,962 pub_init1            publisher[sb] AND (pubstatusnihms OR pubstatuspmcsd OR pmcbook)
    #    387,730 pub                  publisher[sb]
    #     31,423 nihms_pub0           pubstatusnihms AND publisher[sb]
    #     42,740 nihms_pub1           pubstatusnihms NOT publisher[sb]
    #     74,163 nihms                pubstatusnihms
    #     72,518 nihms_pmc1           pubstatusnihms AND pubmed pmc[sb]
    #      1,645 nihms_pmc0           pubstatusnihms NOT pubmed pmc[sb]
    #     23,279 pub_pmcsd            pubstatuspmcsd AND publisher[sb]
    #     60,145 pmcsd                pubstatuspmcsd
    #          0 pmcsd_and_nihms      pubstatuspmcsd AND pubstatusnihms
    #     59,242 pmcsd_pmc1           pubstatuspmcsd AND pubmed pmc[sb]
    #        903 pmcsd_pmc0           pubstatuspmcsd NOT pubmed pmc[sb]
    #    557,390 inprocess_all        inprocess[sb]
    #    422,103 inprocess_pmc0       inprocess[sb] NOT pubmed pmc[sb]
    #    135,287 inprocess_pmc1       inprocess[sb] AND pubmed pmc[sb]
    #    557,390 inprocess_ml0        inprocess[sb] NOT medline[sb]
    #          0 inprocess_ml1        inprocess[sb] AND medline[sb]
    # 27,010,168 medline_n_inprocess  medline[sb] OR inprocess[sb]
    # 26,452,778 medline_all          medline[sb]
    # 22,949,721 medline_pmc0         medline[sb] NOT pubmed pmc[sb]
    #  3,503,057 medline_pmc1         medline[sb] AND pubmed pmc[sb]
    #  5,323,939 pmc_all              pubmed pmc[sb]
    #    761,655 au_all               author manuscript all[sb]
    #    761,655 au_all1              author manuscript all[sb] AND all[sb]
    #    666,187 au_ss                author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook
    #     34,760 au_ss_m0             author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb]
    #      9,046 au_ss_ml0            author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]
    #      7,084 au_ss_pmconly        author manuscript[sb] AND pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]
    #     69,433 au_nihms             author manuscript[sb] AND pubstatusnihms
    #         12 au_pmcsd             author manuscript[sb] AND pubstatuspmcsd
    #          0 au_pmcbook           author manuscript[sb] AND pmcbook
    #    658,826 au_ml1               author manuscript[sb] AND (medline[sb] OR inprocess[sb])
    #     76,806 au_ml0               author manuscript[sb] NOT medline[sb] NOT inprocess[sb]
    #      3,429 au_ml0_pmc0          author manuscript[sb] NOT medline[sb] NOT inprocess[sb] NOT pubmed pmc[sb]
    #     73,377 au_ml0_pmc1          author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb] NOT inprocess[sb]
    #    633,080 au_m1                author manuscript[sb] AND medline[sb]
    #     25,746 au_ip1               author manuscript[sb] AND inprocess[sb]
    #    711,761 au_ml1_or_pmc1       author manuscript[sb] AND (medline[sb] OR pubmed pmc[sb])
    #    625,179 au_ml1_and_pmc1      author manuscript[sb] AND medline[sb] AND pubmed pmc[sb]
    #    630,483 au_ml1_and_pmc1_or_ip1 author manuscript[sb] AND (inprocess[sb] OR medline[sb] AND pubmed pmc[sb])
    #    703,860 au_pmc1              author manuscript[sb] AND pubmed pmc[sb]
    #      5,304 au_pmc1_ip1          author manuscript[sb] AND pubmed pmc[sb] AND inprocess[sb]
    #     78,681 au_pmc1_ml0          author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb]
    #     31,772 au_pmc0              author manuscript[sb] NOT pubmed pmc[sb]
    #      7,901 au_embargo           author manuscript[sb] AND medline[sb] NOT pubmed pmc[sb]
    #  3,116,339 pmnml_A              pubmednotmedline[sb]
    #  3,116,339 pmnml_B              pubmednotmedline[sb] NOT medline[sb]
    #  3,116,339 pmnml_C_ip0          pubmednotmedline[sb] NOT inprocess[sb]
    #          0 pmnml_0_ip1          pubmednotmedline[sb] AND inprocess[sb]
    #  1,612,274 pmnml_A_pmc1         pubmednotmedline[sb] AND pubmed pmc[sb]
    #  1,504,065 pmnml_A_pmc0         pubmednotmedline[sb] NOT pubmed pmc[sb]
    #     22,260 pmcbook_A            pmcbook
    #     22,260 pmcbook_A_ml0        pmcbook NOT medline[sb]
    #     22,260 pmcbook_A_pmc0       pmcbook NOT pubmed pmc[sb]
    return {
        "all": 30514237,
        "all_ml0_pmc0": 1818474,
        "ml1_pmc1": 28695763,
        "pub_init0": 310768,
        "pub_init1": 76962,
        "pub": 387730,
        "nihms_pub0": 31423,
        "nihms_pub1": 42740,
        "nihms": 74163,
        "nihms_pmc1": 72518,
        "nihms_pmc0": 1645,
        "pub_pmcsd": 23279,
        "pmcsd": 60145,
        "pmcsd_and_nihms": 0,
        "pmcsd_pmc1": 59242,
        "pmcsd_pmc0": 903,
        "inprocess_all": 557390,
        "inprocess_pmc0": 422103,
        "inprocess_pmc1": 135287,
        "inprocess_ml0": 557390,
        "inprocess_ml1": 0,
        "medline_n_inprocess": 27010168,
        "medline_all": 26452778,
        "medline_pmc0": 22949721,
        "medline_pmc1": 3503057,
        "pmc_all": 5323939,
        "au_all": 761655,
        "au_all1": 761655,
        "au_ss": 666187,
        "au_ss_m0": 34760,
        "au_ss_ml0": 9046,
        "au_ss_pmconly": 7084,
        "au_nihms": 69433,
        "au_pmcsd": 12,
        "au_pmcbook": 0,
        "au_ml1": 658826,
        "au_ml0": 76806,
        "au_ml0_pmc0": 3429,
        "au_ml0_pmc1": 73377,
        "au_m1": 633080,
        "au_ip1": 25746,
        "au_ml1_or_pmc1": 711761,
        "au_ml1_and_pmc1": 625179,
        "au_ml1_and_pmc1_or_ip1": 630483,
        "au_pmc1": 703860,
        "au_pmc1_ip1": 5304,
        "au_pmc1_ml0": 78681,
        "au_pmc0": 31772,
        "au_embargo": 7901,
        "pmnml_A": 3116339,
        "pmnml_B": 3116339,
        "pmnml_C_ip0": 3116339,
        "pmnml_0_ip1": 0,
        "pmnml_A_pmc1": 1612274,
        "pmnml_A_pmc0": 1504065,
        "pmcbook_A": 22260,
        "pmcbook_A_ml0": 22260,
        "pmcbook_A_pmc0": 22260,
    }

if __name__ == '__main__':
    main(len(sys.argv) != 1)

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
