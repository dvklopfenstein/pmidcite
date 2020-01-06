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
    #     30,505,316 all               all [sb]
    #    311,374 pub_init          publisher[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook
    #    388,333 pub               publisher[sb]
    #     31,440 pub_author_ms     pubstatusnihms AND publisher[sb]
    #     31,440 pub_pmc           pubstatusnihms AND publisher[sb]
    #    561,614 inprocess_all     inprocess[sb]
    #    425,192 inprocess_pmc0    inprocess[sb] NOT pubmed pmc[sb]
    #    136,422 inprocess_pmc1    inprocess[sb] AND pubmed pmc[sb]
    # 27,003,672 medline_inprocess medline[sb] OR inprocess[sb]
    # 26,442,058 medline_all       medline[sb]
    # 22,942,582 medline_pmc0      medline[sb] NOT pubmed pmc[sb]
    #  3,499,476 medline_pmc1      medline[sb] AND pubmed pmc[sb]
    #  5,319,578 pmc_all           pubmed pmc[sb]
    #    761,237 au_all            author manuscript all[sb]
    #    632,627 au_ml1            author manuscript[sb] AND medline[sb]
    #    703,377 au_pmc1           author manuscript[sb] AND pubmed pmc[sb]
    #     31,814 au_pmc0           author manuscript[sb] NOT pubmed pmc[sb]
    #  3,113,311 pm_ml0            pubmednotmedline[sb]
    #  3,113,311 pm_ml0b           pubmednotmedline[sb] NOT medline[sb]
    #          0 pm_ml0_ip1        pubmednotmedline[sb] AND inprocess[sb]
    #  3,113,311 pm_ml0_ip0        pubmednotmedline[sb] NOT inprocess[sb]
    #  1,610,407 pm_ml0_pmc1       pubmednotmedline[sb] AND pubmed pmc[sb]
    #  1,502,904 pm_ml0_pmc0       pubmednotmedline[sb] NOT pubmed pmc[sb]
    #          0 pmcbook           pmcbook[sb]
    #          0 pmcbook_ml0       pmcbook[sb] NOT medline[sb]
    #          0 pmcbook_pmc0      pmcbook[sb] NOT pubmed pmc[sb]
    return {
        "all": 30505316,
        "pub_init": 311374,
        "pub": 388333,
        "pub_author_ms": 31440,
        "pub_pmc": 31440,
        "inprocess_all": 561614,
        "inprocess_pmc0": 425192,
        "inprocess_pmc1": 136422,
        "medline_inprocess": 27003672,
        "medline_all": 26442058,
        "medline_pmc0": 22942582,
        "medline_pmc1": 3499476,
        "pmc_all": 5319578,
        "au_all": 761237,
        "au_ml1": 632627,
        "au_pmc1": 703377,
        "au_pmc0": 31814,
        "pm_ml0": 3113311,
        "pm_ml0b": 3113311,
        "pm_ml0_ip1": 0,
        "pm_ml0_ip0": 3113311,
        "pm_ml0_pmc1": 1610407,
        "pm_ml0_pmc0": 1502904,
        "pmcbook": 0,
        "pmcbook_ml0": 0,
        "pmcbook_pmc0": 0,
    }


if __name__ == '__main__':
    main(len(sys.argv) != 1)

# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
