"""Print PMC information"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"


def _prt_a2n(a2n):
    """Print PMC information"""
    tot = a2n['ml1_pmc1'] + a2n['all_ml0_pmc0']
    vala = a2n['ml1_pmc1']
    valb = a2n['all_ml0_pmc0']
    print(f'  {tot:10,} = {vala:10,} (MEDLINE OR PMC) + {valb:10,} (not MEDLINE OR PMC)')
    total = a2n['all']
    au_all = a2n['au_all']
    print(f'  {au_all:10,} of {total:10,} {100.0*au_all/total:3.5f}% author ms')
    print(f'  {tot:10,} = {vala:10,} (MEDLINE OR PMC) + {valb:10,} (not MEDLINE OR PMC)')

def chk_content_counts(a2n):
    """Check the content typename and the count of that type"""
    ##a2n = self.name2cnt
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
    print(f'  {pmc_notmedline:10,} of {a2n["pmc_all"]:10,} PMC (not MEDLINE)')
    print(pmc_notmedline - a2n['pmnml_A_pmc1'])
    print(f'  {a2n["all_ml0_pmc0"]:10,} of {a2n["all"]:10,} PubMed(not MEDLINE, PMC)')

    _prt_a2n(a2n)
    ####print('  {T:10,} = {A:10,} (MEDLINE OR PMC) + {B:10,} (not MEDLINE OR PMC)'.format(
    ####    T=a2n['ml1_pmc1'] + a2n['all_ml0_pmc0'],
    ####    A=a2n['ml1_pmc1'],
    ####    B=a2n['all_ml0_pmc0']))
    ####total = a2n['all']
    ####au_all = a2n['au_all']
    ####print(f'  {au_all:10,} of {total:10,} {100.0*au_all/total:3.5f}% author ms')
    ####print('  {T:10,} = {A:10,} (MEDLINE OR PMC) + {B:10,} (not MEDLINE OR PMC)'.format(
    ####    T=a2n['ml1_pmc1'] + a2n['all_ml0_pmc0'],
    ####    A=a2n['ml1_pmc1'],
    ####    B=a2n['all_ml0_pmc0']))


# Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved.
