"""Downloaded PubMed count data"""

DATE = '2020_01_10'

# 30,522,105 all                  all [sb]
#  1,817,560 all_ml0_pmc0         all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb]
#  1,815,524 all_ml0_pmc0b        all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd
# 28,704,545 ml1_pmc1             inprocess[sb] OR medline[sb] OR pubmed pmc[sb]
#    310,814 pub_init0            publisher[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook
#     76,964 pub_init1            publisher[sb] AND (pubstatusnihms OR pubstatuspmcsd OR pmcbook)
#    387,778 pub                  publisher[sb]
#     31,422 nihms_pub0           pubstatusnihms AND publisher[sb]
#     42,763 nihms_pub1           pubstatusnihms NOT publisher[sb]
#     74,185 nihms                pubstatusnihms
#     72,580 nihms_pmc1           pubstatusnihms AND pubmed pmc[sb]
#      1,605 nihms_pmc0           pubstatusnihms NOT pubmed pmc[sb]
#     23,278 pub_pmcsd            pubstatuspmcsd AND publisher[sb]
#     60,146 pmcsd                pubstatuspmcsd
#          0 pmcsd_and_nihms      pubstatuspmcsd AND pubstatusnihms
#     59,274 pmcsd_pmc1           pubstatuspmcsd AND pubmed pmc[sb]
#        872 pmcsd_pmc0           pubstatuspmcsd NOT pubmed pmc[sb]
#    557,189 inprocess_A_all      inprocess[sb]
#    420,679 inprocess_A_pmc0     inprocess[sb] NOT pubmed pmc[sb]
#    136,510 inprocess_A_pmc1     inprocess[sb] AND pubmed pmc[sb]
#    557,189 inprocess_ml0        inprocess[sb] NOT medline[sb]
#          0 inprocess_ml1        inprocess[sb] AND medline[sb]
# 27,016,854 medline_n_inprocess  medline[sb] OR inprocess[sb]
# 26,459,665 medline_all          medline[sb]
# 22,954,612 medline_pmc0         medline[sb] NOT pubmed pmc[sb]
#  3,505,053 medline_pmc1         medline[sb] AND pubmed pmc[sb]
#  5,329,254 pmc_all              pubmed pmc[sb]
#  5,255,867 pmc_all?             pubmed pmc[sb] AND (inprocess[sb] OR medline[sb] OR pubmednotmedline[sb])
#  3,641,563 pmc_m1               pubmed pmc[sb] AND (inprocess[sb] OR medline[sb])
#  1,687,691 pmc_m0               pubmed pmc[sb] NOT inprocess[sb] NOT medline[sb]
#  1,614,304 pmc_m0b              pubmed pmc[sb] AND pubmednotmedline[sb]
#     73,387 pmc_unknown          pubmed pmc[sb] NOT inprocess[sb] NOT medline[sb] NOT pubmednotmedline[sb]
#    762,137 au_all               author manuscript all[sb]
#    762,137 au_all1              author manuscript all[sb] AND all[sb]
#    666,598 au_ss                author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook
#     34,798 au_ss_m0             author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb]
#      9,082 au_ss_ml0            author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]
#      7,108 au_ss_pmconly        author manuscript[sb] AND pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]
#     69,494 au_nihms             author manuscript[sb] AND pubstatusnihms
#         12 au_pmcsd             author manuscript[sb] AND pubstatuspmcsd
#          0 au_pmcbook           author manuscript[sb] AND pmcbook
#    659,203 au_ml1               author manuscript[sb] AND (medline[sb] OR inprocess[sb])
#     76,901 au_ml0               author manuscript[sb] NOT medline[sb] NOT inprocess[sb]
#      3,438 au_ml0_pmc0          author manuscript[sb] NOT medline[sb] NOT inprocess[sb] NOT pubmed pmc[sb]
#     73,463 au_ml0_pmc1          author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb] NOT inprocess[sb]
#    633,453 au_m1                author manuscript[sb] AND medline[sb]
#     25,750 au_ip1               author manuscript[sb] AND inprocess[sb]
#    712,289 au_ml1_or_pmc1       author manuscript[sb] AND (medline[sb] OR pubmed pmc[sb])
#    625,444 au_ml1_and_pmc1      author manuscript[sb] AND medline[sb] AND pubmed pmc[sb]
#    630,817 au_ml1_and_pmc1_or_ip1 author manuscript[sb] AND (inprocess[sb] OR medline[sb] AND pubmed pmc[sb])
#    704,280 au_pmc1              author manuscript[sb] AND pubmed pmc[sb]
#      5,373 au_pmc1_ip1          author manuscript[sb] AND pubmed pmc[sb] AND inprocess[sb]
#     78,836 au_pmc1_ml0          author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb]
#     31,824 au_pmc0              author manuscript[sb] NOT pubmed pmc[sb]
#      8,009 au_embargo           author manuscript[sb] AND medline[sb] NOT pubmed pmc[sb]
#  3,117,473 pmnml_A              pubmednotmedline[sb]
#  3,117,473 pmnml_B              pubmednotmedline[sb] NOT medline[sb]
#  3,117,473 pmnml_C_ip0          pubmednotmedline[sb] NOT inprocess[sb]
#          0 pmnml_0_ip1          pubmednotmedline[sb] AND inprocess[sb]
#  1,614,304 pmnml_A_pmc1         pubmednotmedline[sb] AND pubmed pmc[sb]
#  1,503,169 pmnml_A_pmc0         pubmednotmedline[sb] NOT pubmed pmc[sb]
#     22,264 pmcbook_A            pmcbook
#     22,264 pmcbook_A_ml0        pmcbook NOT medline[sb]
#     22,264 pmcbook_A_pmc0       pmcbook NOT pubmed pmc[sb]

CNTS = {
    "all": 30522105,
    "all_ml0_pmc0": 1817560,
    "all_ml0_pmc0b": 1815524,
    "ml1_pmc1": 28704545,
    "pub_init0": 310814,
    "pub_init1": 76964,
    "pub": 387778,
    "nihms_pub0": 31422,
    "nihms_pub1": 42763,
    "nihms": 74185,
    "nihms_pmc1": 72580,
    "nihms_pmc0": 1605,
    "pub_pmcsd": 23278,
    "pmcsd": 60146,
    "pmcsd_and_nihms": 0,
    "pmcsd_pmc1": 59274,
    "pmcsd_pmc0": 872,
    "inprocess_A_all": 557189,
    "inprocess_A_pmc0": 420679,
    "inprocess_A_pmc1": 136510,
    "inprocess_ml0": 557189,
    "inprocess_ml1": 0,
    "medline_n_inprocess": 27016854,
    "medline_all": 26459665,
    "medline_pmc0": 22954612,
    "medline_pmc1": 3505053,
    "pmc_all": 5329254,
    "pmc_all?": 5255867,
    "pmc_m1": 3641563,
    "pmc_m0": 1687691,
    "pmc_m0b": 1614304,
    "pmc_unknown": 73387,
    "au_all": 762137,
    "au_all1": 762137,
    "au_ss": 666598,
    "au_ss_m0": 34798,
    "au_ss_ml0": 9082,
    "au_ss_pmconly": 7108,
    "au_nihms": 69494,
    "au_pmcsd": 12,
    "au_pmcbook": 0,
    "au_ml1": 659203,
    "au_ml0": 76901,
    "au_ml0_pmc0": 3438,
    "au_ml0_pmc1": 73463,
    "au_m1": 633453,
    "au_ip1": 25750,
    "au_ml1_or_pmc1": 712289,
    "au_ml1_and_pmc1": 625444,
    "au_ml1_and_pmc1_or_ip1": 630817,
    "au_pmc1": 704280,
    "au_pmc1_ip1": 5373,
    "au_pmc1_ml0": 78836,
    "au_pmc0": 31824,
    "au_embargo": 8009,
    "pmnml_A": 3117473,
    "pmnml_B": 3117473,
    "pmnml_C_ip0": 3117473,
    "pmnml_0_ip1": 0,
    "pmnml_A_pmc1": 1614304,
    "pmnml_A_pmc0": 1503169,
    "pmcbook_A": 22264,
    "pmcbook_A_ml0": 22264,
    "pmcbook_A_pmc0": 22264,
}

