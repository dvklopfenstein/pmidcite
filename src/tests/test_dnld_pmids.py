#!/usr/bin/env python3
"""Test downloading PMIDs"""

from pmidcite.cfg import Cfg
from pmidcite.eutils.cmds.base import EntrezUtilities
from tests.pmids import PMIDS


def test_dnld_pmids():
    """Test downloading PMIDs"""
    pmids1 = PMIDS[:97]
    cfg = Cfg()
    eutils = EntrezUtilities(cfg.get_email(), cfg.get_apikey(), cfg.get_tool())
    rsp_epost = eutils.epost('pubmed', pmids1, step=10)
    print(rsp_epost)
    #querykey_max = rsp_epost['querykey']
    webenv = rsp_epost['webenv']
    # querykey_max = 10
    # webenv = 'NCID_1_161316809_130.14.22.33_9001_1574883672_1613778891_0MetA0_S_MegaStore'

    querykey = 1
    rsp = eutils.run_eutilscmd(
        'efetch',
        db='pubmed',
        retstart=0,
        retmax=2,          # max: 10,000
        rettype='medline',
        retmode='text',
        webenv=webenv,
        query_key=querykey)
    print(rsp)


if __name__ == '__main__':
    test_dnld_pmids()
