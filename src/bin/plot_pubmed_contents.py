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
    print(date)
    fout_png = 'log/pubmed_content/pubmed_content_{DATE}.png'.format(DATE=date)
    fout_png = 'pubmed_content_{DATE}.png'.format(DATE=date)
    cfg = Cfg()
    obj = PubMedContents(cfg.get_email(), cfg.get_apikey(), cfg.get_tool())
    name2cnt = obj.dnld_content_counts() if dnld else _get_name2cnt()
    obj.prt_content_counts(name2cnt)
    if dnld:
        obj.prt_content_cntdct(name2cnt)
    obj.chk_content_counts(name2cnt)
    obj.plt_content_counts(fout_png, name2cnt)

def _get_name2cnt():
    """Return saved counts, rather than re-downloading"""
    # 2020_01_06:

    # 30,505,316 all                  all [sb]
    #  1,817,964 all_ml0_pmc0         all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb]
    # 28,687,352 ml1_pmc1             inprocess[sb] OR medline[sb] OR pubmed pmc[sb]
    #    311,374 pub_init0            publisher[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook
    #     76,959 pub_init1            publisher[sb] AND (pubstatusnihms OR pubstatuspmcsd OR pmcbook)
    #    388,333 pub                  publisher[sb]
    #     31,440 nihms_pub0           pubstatusnihms AND publisher[sb]
    #     42,673 nihms_pub1           pubstatusnihms NOT publisher[sb]
    #     74,113 nihms                pubstatusnihms
    #     72,467 nihms_pmc1           pubstatusnihms AND pubmed pmc[sb]
    #      1,646 nihms_pmc0           pubstatusnihms NOT pubmed pmc[sb]
    #     23,283 pub_pmcsd            pubstatuspmcsd AND publisher[sb]
    #     60,113 pmcsd                pubstatuspmcsd
    #          0 pmcsd_and_nihms      pubstatuspmcsd AND pubstatusnihms
    #     59,053 pmcsd_pmc1           pubstatuspmcsd AND pubmed pmc[sb]
    #      1,060 pmcsd_pmc0           pubstatuspmcsd NOT pubmed pmc[sb]
    #    561,614 inprocess_all        inprocess[sb]
    #    425,192 inprocess_pmc0       inprocess[sb] NOT pubmed pmc[sb]
    #    136,422 inprocess_pmc1       inprocess[sb] AND pubmed pmc[sb]
    # 27,003,672 medline_inprocess    medline[sb] OR inprocess[sb]
    # 26,442,058 medline_all          medline[sb]
    # 22,942,582 medline_pmc0         medline[sb] NOT pubmed pmc[sb]
    #  3,499,476 medline_pmc1         medline[sb] AND pubmed pmc[sb]
    #  5,319,578 pmc_all              pubmed pmc[sb]
    #    761,237 au_all               author manuscript all[sb]
    #    761,237 au_all1              author manuscript all[sb] AND all[sb]
    #    665,763 au_ss                author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook
    #     34,789 au_ss_m0             author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb]
    #      9,056 au_ss_ml0            author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]
    #      7,066 au_ss_pmconly        author manuscript[sb] AND pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]
    #     69,416 au_nihms             author manuscript[sb] AND pubstatusnihms
    #         12 au_pmcsd             author manuscript[sb] AND pubstatuspmcsd
    #          0 au_pmcbook           author manuscript[sb] AND pmcbook
    #    658,392 au_ml1               author manuscript[sb] AND (medline[sb] OR inprocess[sb])
    #     76,799 au_ml0               author manuscript[sb] NOT medline[sb] NOT inprocess[sb]
    #      3,490 au_ml0_pmc0          author manuscript[sb] NOT medline[sb] NOT inprocess[sb] NOT pubmed pmc[sb]
    #     73,309 au_ml0_pmc1          author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb] NOT inprocess[sb]
    #    632,627 au_m1                author manuscript[sb] AND medline[sb]
    #     25,765 au_ip1               author manuscript[sb] AND inprocess[sb]
    #    711,176 au_ml1_or_pmc1       author manuscript[sb] AND (medline[sb] OR pubmed pmc[sb])
    #    624,828 au_ml1_and_pmc1      author manuscript[sb] AND medline[sb] AND pubmed pmc[sb]
    #    630,068 au_ml1_and_pmc1_or_ip1 author manuscript[sb] AND (inprocess[sb] OR medline[sb] AND pubmed pmc[sb])
    #    703,377 au_pmc1              author manuscript[sb] AND pubmed pmc[sb]
    #      5,240 au_pmc1_ip1          author manuscript[sb] AND pubmed pmc[sb] AND inprocess[sb]
    #     78,549 au_pmc1_ml0          author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb]
    #     31,814 au_pmc0              author manuscript[sb] NOT pubmed pmc[sb]
    #      7,799 au_embargo           author manuscript[sb] AND medline[sb] NOT pubmed pmc[sb]
    #  3,113,311 pm_ml0               pubmednotmedline[sb]
    #  3,113,311 pm_ml0b              pubmednotmedline[sb] NOT medline[sb]
    #          0 pm_ml0_ip1           pubmednotmedline[sb] AND inprocess[sb]
    #  3,113,311 pm_ml0_ip0           pubmednotmedline[sb] NOT inprocess[sb]
    #  1,610,407 pm_ml0_pmc1          pubmednotmedline[sb] AND pubmed pmc[sb]
    #  1,502,904 pm_ml0_pmc0          pubmednotmedline[sb] NOT pubmed pmc[sb]
    #     22,236 pmcbook              pmcbook
    #     22,236 pmcbook_ml0          pmcbook NOT medline[sb]
    #     22,236 pmcbook_pmc0         pmcbook NOT pubmed pmc[sb]
    return {
        "all": 30505316,
        "all_ml0_pmc0": 1817964,
        "ml1_pmc1": 28687352,
        "pub_init0": 311374,
        "pub_init1": 76959,
        "pub": 388333,
        "nihms_pub0": 31440,
        "nihms_pub1": 42673,
        "nihms": 74113,
        "nihms_pmc1": 72467,
        "nihms_pmc0": 1646,
        "pub_pmcsd": 23283,
        "pmcsd": 60113,
        "pmcsd_and_nihms": 0,
        "pmcsd_pmc1": 59053,
        "pmcsd_pmc0": 1060,
        "inprocess_all": 561614,
        "inprocess_pmc0": 425192,
        "inprocess_pmc1": 136422,
        "medline_inprocess": 27003672,
        "medline_all": 26442058,
        "medline_pmc0": 22942582,
        "medline_pmc1": 3499476,
        "pmc_all": 5319578,
        "au_all": 761237,
        "au_all1": 761237,
        "au_ss": 665763,
        "au_ss_m0": 34789,
        "au_ss_ml0": 9056,
        "au_ss_pmconly": 7066,
        "au_nihms": 69416,
        "au_pmcsd": 12,
        "au_pmcbook": 0,
        "au_ml1": 658392,
        "au_ml0": 76799,
        "au_ml0_pmc0": 3490,
        "au_ml0_pmc1": 73309,
        "au_m1": 632627,
        "au_ip1": 25765,
        "au_ml1_or_pmc1": 711176,
        "au_ml1_and_pmc1": 624828,
        "au_ml1_and_pmc1_or_ip1": 630068,
        "au_pmc1": 703377,
        "au_pmc1_ip1": 5240,
        "au_pmc1_ml0": 78549,
        "au_pmc0": 31814,
        "au_embargo": 7799,
        "pm_ml0": 3113311,
        "pm_ml0b": 3113311,
        "pm_ml0_ip1": 0,
        "pm_ml0_ip0": 3113311,
        "pm_ml0_pmc1": 1610407,
        "pm_ml0_pmc0": 1502904,
        "pmcbook": 22236,
        "pmcbook_ml0": 22236,
        "pmcbook_pmc0": 22236,
    }


if __name__ == '__main__':
    main(len(sys.argv) != 1)

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
