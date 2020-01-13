"""Downloaded PubMed count data"""

DATE = '2020_01_11'

# pylint: disable=line-too-long
# 30,527,422 all                  all [sb]
#  1,819,828 all_ml0_pmc0         all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb]
#  1,694,611 all_ml0_pmc0_free0   all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] NOT free full text[sb]
#    125,217 all_ml0_pmc0_free1   all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] AND free full text[sb]
#  1,817,769 all_ml0_pmc0b        all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd
#  1,503,281 all_ml0_pmc0d        all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd AND pubmednotmedline[sb]
#    314,488 all_ml0_pmc0c        all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pubmednotmedline[sb]
# 28,707,594 ml1_pmc1             inprocess[sb] OR medline[sb] OR pubmed pmc[sb]
#    311,051 pub_init0            publisher[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook
#     76,962 pub_init1            publisher[sb] AND (pubstatusnihms OR pubstatuspmcsd OR pmcbook)
#    388,013 pub                  publisher[sb]
#     31,420 nihms_pub0           pubstatusnihms AND publisher[sb]
#     42,782 nihms_pub1           pubstatusnihms NOT publisher[sb]
#     74,202 nihms                pubstatusnihms
#     72,580 nihms_pmc1           pubstatusnihms AND pubmed pmc[sb]
#      1,622 nihms_pmc0           pubstatusnihms NOT pubmed pmc[sb]
#     23,278 pub_pmcsd            pubstatuspmcsd AND publisher[sb]
#     60,153 pmcsd                pubstatuspmcsd
#          0 pmcsd_and_nihms      pubstatuspmcsd AND pubstatusnihms
#     59,274 pmcsd_pmc1           pubstatuspmcsd AND pubmed pmc[sb]
#        879 pmcsd_pmc0           pubstatuspmcsd NOT pubmed pmc[sb]
#    558,119 inprocess_A_all      inprocess[sb]
#    421,966 inprocess_A_pmc0     inprocess[sb] NOT pubmed pmc[sb]
#    136,153 inprocess_A_pmc1     inprocess[sb] AND pubmed pmc[sb]
#    558,119 inprocess_ml0        inprocess[sb] NOT medline[sb]
#          0 inprocess_ml1        inprocess[sb] AND medline[sb]
# 27,019,907 medline_n_inprocess  medline[sb] OR inprocess[sb]
# 26,461,788 medline_all          medline[sb]
# 22,956,376 medline_pmc0         medline[sb] NOT pubmed pmc[sb]
#  3,505,412 medline_pmc1         medline[sb] AND pubmed pmc[sb]
#  5,329,252 pmc_all              pubmed pmc[sb]
#  5,255,875 pmc_all?             pubmed pmc[sb] AND (inprocess[sb] OR medline[sb] OR pubmednotmedline[sb])
#  3,641,565 pmc_m1               pubmed pmc[sb] AND (inprocess[sb] OR medline[sb])
#  1,687,687 pmc_m0               pubmed pmc[sb] NOT inprocess[sb] NOT medline[sb]
#  1,614,310 pmc_m0b              pubmed pmc[sb] AND pubmednotmedline[sb]
#     73,377 pmc_unknown          pubmed pmc[sb] NOT inprocess[sb] NOT medline[sb] NOT pubmednotmedline[sb]
#    762,137 au_all               author manuscript all[sb]
#    762,137 au_all1              author manuscript all[sb] AND all[sb]
#    666,598 au_ss                author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook
#     34,746 au_ss_m0             author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb]
#      9,066 au_ss_ml0            author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]
#      7,106 au_ss_pmconly        author manuscript[sb] AND pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]
#     69,494 au_nihms             author manuscript[sb] AND pubstatusnihms
#         12 au_pmcsd             author manuscript[sb] AND pubstatuspmcsd
#          0 au_pmcbook           author manuscript[sb] AND pmcbook
#    659,219 au_ml1               author manuscript[sb] AND (medline[sb] OR inprocess[sb])
#     76,885 au_ml0               author manuscript[sb] NOT medline[sb] NOT inprocess[sb]
#      3,424 au_ml0_pmc0          author manuscript[sb] NOT medline[sb] NOT inprocess[sb] NOT pubmed pmc[sb]
#     73,461 au_ml0_pmc1          author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb] NOT inprocess[sb]
#    633,507 au_m1                author manuscript[sb] AND medline[sb]
#     25,712 au_ip1               author manuscript[sb] AND inprocess[sb]
#    712,329 au_ml1_or_pmc1       author manuscript[sb] AND (medline[sb] OR pubmed pmc[sb])
#    625,458 au_ml1_and_pmc1      author manuscript[sb] AND medline[sb] AND pubmed pmc[sb]
#    630,819 au_ml1_and_pmc1_or_ip1 author manuscript[sb] AND (inprocess[sb] OR medline[sb] AND pubmed pmc[sb])
#    704,280 au_pmc1              author manuscript[sb] AND pubmed pmc[sb]
#      5,361 au_pmc1_ip1          author manuscript[sb] AND pubmed pmc[sb] AND inprocess[sb]
#     78,822 au_pmc1_ml0          author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb]
#     31,824 au_pmc0              author manuscript[sb] NOT pubmed pmc[sb]
#      8,049 au_embargo           author manuscript[sb] AND medline[sb] NOT pubmed pmc[sb]
#  3,119,502 pmnml_A              pubmednotmedline[sb]
#  3,119,502 pmnml_B              pubmednotmedline[sb] NOT medline[sb]
#  1,505,192 pmnml_C              pubmednotmedline[sb] NOT pubmed pmc[sb]
#  1,505,192 pmnml_D              pubmednotmedline[sb] NOT pubmed pmc[sb] NOT pubstatusnihms[sb] NOT pubstatuspmcsd[sb]
#  3,119,502 pmnml_C_ip0          pubmednotmedline[sb] NOT inprocess[sb]
#          0 pmnml_0_ip1          pubmednotmedline[sb] AND inprocess[sb]
#  1,614,310 pmnml_A_pmc1         pubmednotmedline[sb] AND pubmed pmc[sb]
#  1,505,192 pmnml_A_pmc0         pubmednotmedline[sb] NOT pubmed pmc[sb]
#     22,264 pmcbook_A            pmcbook
#     22,264 pmcbook_A_ml0        pmcbook NOT medline[sb]
#     22,264 pmcbook_A_pmc0       pmcbook NOT pubmed pmc[sb]

CNTS = {
    "all": 30527422,
    "all_ml0_pmc0": 1819828,
    "all_ml0_pmc0_free0": 1694611,
    "all_ml0_pmc0_free1": 125217,
    "all_ml0_pmc0b": 1817769,
    "all_ml0_pmc0d": 1503281,
    "all_ml0_pmc0c": 314488,
    "ml1_pmc1": 28707594,
    "pub_init0": 311051,
    "pub_init1": 76962,
    "pub": 388013,
    "nihms_pub0": 31420,
    "nihms_pub1": 42782,
    "nihms": 74202,
    "nihms_pmc1": 72580,
    "nihms_pmc0": 1622,
    "pub_pmcsd": 23278,
    "pmcsd": 60153,
    "pmcsd_and_nihms": 0,
    "pmcsd_pmc1": 59274,
    "pmcsd_pmc0": 879,
    "inprocess_A_all": 558119,
    "inprocess_A_pmc0": 421966,
    "inprocess_A_pmc1": 136153,
    "inprocess_ml0": 558119,
    "inprocess_ml1": 0,
    "medline_n_inprocess": 27019907,
    "medline_all": 26461788,
    "medline_pmc0": 22956376,
    "medline_pmc1": 3505412,
    "pmc_all": 5329252,
    "pmc_all?": 5255875,
    "pmc_m1": 3641565,
    "pmc_m0": 1687687,
    "pmc_m0b": 1614310,
    "pmc_unknown": 73377,
    "au_all": 762137,
    "au_all1": 762137,
    "au_ss": 666598,
    "au_ss_m0": 34746,
    "au_ss_ml0": 9066,
    "au_ss_pmconly": 7106,
    "au_nihms": 69494,
    "au_pmcsd": 12,
    "au_pmcbook": 0,
    "au_ml1": 659219,
    "au_ml0": 76885,
    "au_ml0_pmc0": 3424,
    "au_ml0_pmc1": 73461,
    "au_m1": 633507,
    "au_ip1": 25712,
    "au_ml1_or_pmc1": 712329,
    "au_ml1_and_pmc1": 625458,
    "au_ml1_and_pmc1_or_ip1": 630819,
    "au_pmc1": 704280,
    "au_pmc1_ip1": 5361,
    "au_pmc1_ml0": 78822,
    "au_pmc0": 31824,
    "au_embargo": 8049,
    "pmnml_A": 3119502,
    "pmnml_B": 3119502,
    "pmnml_C": 1505192,
    "pmnml_D": 1505192,
    "pmnml_C_ip0": 3119502,
    "pmnml_0_ip1": 0,
    "pmnml_A_pmc1": 1614310,
    "pmnml_A_pmc0": 1505192,
    "pmcbook_A": 22264,
    "pmcbook_A_ml0": 22264,
    "pmcbook_A_pmc0": 22264,
}
