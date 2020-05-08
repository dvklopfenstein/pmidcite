"""Plot the types of content and their amount in PubMed"""

# To check whether a journal is indexed in MEDLINE and stored in PMC,
# search the NLM Catalog:
# 
#     https://www.ncbi.nlm.nih.gov/nlmcatalog
# 
# PMC also maintains a journals list, which is dynamic list, 
# that provides journal participation level information:
# 
#     https://www.ncbi.nlm.nih.gov/pmc/journals/
#
# Lidia Hutcherson
# LinkOut Development Team
# Information Engineering Branch
# National Center for Biotechnology Information
# US National Library of Medicine
# Linking to a World of Resources
# http://www.ncbi.nlm.nih.gov/projects/linkout/

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
import datetime
import collections as cx
from pmidcite.eutils.cmds.base import EntrezUtilities


# pylint: disable=line-too-long
class PubMedDnld(EntrezUtilities):
    """Describe the percentage of various types of content in PubMed"""

    # https://pubmed.ncbi.nlm.nih.gov/help/#citation-status-subsets
    name2query = cx.OrderedDict([
        ('all', 'all [sb]'),
        ('all_ml0_pmc0', 'all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb]'),
        ('all_ml0_pmc0_free0', 'all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] NOT free full text[sb]'),
        ('all_ml0_pmc0_free1', 'all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] AND free full text[sb]'),
        ('all_ml0_pmc0b', 'all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd'),
        # Categories include: "Online, ahead of print" and old articles/books, Reviews found in GeneReviews, etc.
        ('all_ml0_pmc0d', 'all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd AND pubmednotmedline[sb]'),
        ('all_ml0_pmc0c', 'all [sb] NOT inprocess[sb] NOT medline[sb] NOT pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pubmednotmedline[sb]'),
        ('ml1_pmc1', 'inprocess[sb] OR medline[sb] OR pubmed pmc[sb]'),
        # Over 2 million FREE-text articles in PubMed that are NOT in PMC
        ('pm1free_pmc0', 'free full text[sb] NOT loprovpmc[sb]'),
        # Over 2 million FREE-text articles in PubMed that are NOT in PMC
        ('ml1free_pmc0', 'free full text[sb] AND medline[sb] NOT pubmed pmc[sb]'),
        # publisher[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT # pmcbook:
        #   1. Citations recently added to PubMed via electronic submission
        #   from a publisher, and are soon to proceed to the next stage,
        #   PubMed - in process (see below).
        #   2. Also for citations received
        #   before late 2003 if they are from journals not indexed for
        #   MEDLINE, or from a journal that was accepted for MEDLINE
        #   after the citations' publication date.
        #   NOTE: These citations bibliographic data have not been reviewed.
        ('pub_init0', 'publisher[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook'),
        ('pub_init1', 'publisher[sb] AND (pubstatusnihms OR pubstatuspmcsd OR pmcbook)'),
        ('pub', 'publisher[sb]'),
        # pubstatusnihms AND publisher[sb]:
        #   Author manuscripts submitted to PMC that fall under the NIH Public Access Policy.
        # https://www.ncbi.nlm.nih.gov/pmc/about/submission-methods/
        #   Some publishers will initiate the NIHMS deposit process for an author,
        #   but the author must complete two approval steps to load the PMC-ready version to PMC
        ('nihms_pub0', 'pubstatusnihms AND publisher[sb]'),
        ('nihms_pub1', 'pubstatusnihms NOT publisher[sb]'),
        ('nihms', 'pubstatusnihms'),
        ('nihms_pmc1', 'pubstatusnihms AND pubmed pmc[sb]'),
        ('nihms_pmc0', 'pubstatusnihms NOT pubmed pmc[sb]'),
        # pubstatuspmcsd AND publisher[sb]:
        #   Records for selective deposit articles in PMC.
        #   These are articles published in non-MEDLINE journals
        #   where the publisher has chosen to deposit in PMC
        #   only those articles that fall under the NIH Public Access Policy.
        ('pub_pmcsd', 'pubstatuspmcsd AND publisher[sb]'),
        ('pmcsd', 'pubstatuspmcsd'),
        ('pmcsd_and_nihms', 'pubstatuspmcsd AND pubstatusnihms'),  # DISJOINT
        ('pmcsd_pmc1', 'pubstatuspmcsd AND pubmed pmc[sb]'),
        ('pmcsd_pmc0', 'pubstatuspmcsd NOT pubmed pmc[sb]'),
        # inprocess MEDLINE:  inprocess[sb]
        #   MeSH terms will be assigned if the subject of the article is within the scope of MEDLINE.
        ('inprocess_A_all', 'inprocess[sb]'),
        ('inprocess_A_pmc0', 'inprocess[sb] NOT pubmed pmc[sb]'),
        ('inprocess_A_pmc1', 'inprocess[sb] AND pubmed pmc[sb]'),
        ('inprocess_ml0', 'inprocess[sb] NOT medline[sb]'),
        ('inprocess_ml1', 'inprocess[sb] AND medline[sb]'),
        ('medline_n_inprocess', 'medline[sb] OR inprocess[sb]'),
        # medline[sb]:
        #   Citations that have been indexed with MeSH terms, Publication Types, Substance Names, etc.
        ('medline_all', 'medline[sb]'),
        ('medline_pmc0', 'medline[sb] NOT pubmed pmc[sb]'),
        ('medline_pmc1', 'medline[sb] AND pubmed pmc[sb]'),
        # pubmed pmc[sb]:
        #   Citations in PMC
        ('pmc_all', 'pubmed pmc[sb]'),
        #  5,323,939 pmc_all              pubmed pmc[sb]
        #    135,287 inprocess_A_pmc1     inprocess[sb] AND pubmed pmc[sb]
        #  3,503,057 medline_pmc1         medline[sb] AND pubmed pmc[sb]
        #  1,612,274 pmnml_A_pmc1         pubmednotmedline[sb] AND pubmed pmc[sb]
        ('pmc_all?', 'pubmed pmc[sb] AND (inprocess[sb] OR medline[sb] OR pubmednotmedline[sb])'),
        ('pmc_m1', 'pubmed pmc[sb] AND (inprocess[sb] OR medline[sb])'),
        ('pmc_m0', 'pubmed pmc[sb] NOT inprocess[sb] NOT medline[sb]'),
        ('pmc_m0b', 'pubmed pmc[sb] AND pubmednotmedline[sb]'),
        ('pmc_unknown', 'pubmed pmc[sb] NOT inprocess[sb] NOT medline[sb] NOT pubmednotmedline[sb]'),
        # https://www.ncbi.nlm.nih.gov/pmc/about/submission-methods/
        ('au_all', 'author manuscript all[sb]'),
        ('au_all1', 'author manuscript all[sb] AND all[sb]'),
        ('au_ss', 'author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook'),
        ('au_ss_m0', 'author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb]'),
        ('au_ss_ml0', 'author manuscript[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]'),
        ('au_ss_pmconly', 'author manuscript[sb] AND pubmed pmc[sb] NOT pubstatusnihms NOT pubstatuspmcsd NOT pmcbook NOT medline[sb] NOT inprocess[sb]'),
        ('au_nihms', 'author manuscript[sb] AND pubstatusnihms'),
        ('au_pmcsd', 'author manuscript[sb] AND pubstatuspmcsd'),
        ('au_pmcbook', 'author manuscript[sb] AND pmcbook'),
        ('au_ml1', 'author manuscript[sb] AND (medline[sb] OR inprocess[sb])'),
        ('au_ml0', 'author manuscript[sb] NOT medline[sb] NOT inprocess[sb]'),
        ('au_ml0_pmc0', 'author manuscript[sb] NOT medline[sb] NOT inprocess[sb] NOT pubmed pmc[sb]'),
        ('au_ml0_pmc1', 'author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb] NOT inprocess[sb]'),
        ('au_m1', 'author manuscript[sb] AND medline[sb]'),
        ('au_ip1', 'author manuscript[sb] AND inprocess[sb]'),
        ('au_ml1_or_pmc1', 'author manuscript[sb] AND (medline[sb] OR pubmed pmc[sb])'),
        ('au_ml1_and_pmc1', 'author manuscript[sb] AND medline[sb] AND pubmed pmc[sb]'),
        ('au_ml1_and_pmc1_or_ip1', 'author manuscript[sb] AND (inprocess[sb] OR medline[sb] AND pubmed pmc[sb])'),
        ('au_pmc1', 'author manuscript[sb] AND pubmed pmc[sb]'),
        ('au_pmc1_ip1', 'author manuscript[sb] AND pubmed pmc[sb] AND inprocess[sb]'),
        ('au_pmc1_ml0', 'author manuscript[sb] AND pubmed pmc[sb] NOT medline[sb]'),
        ('au_pmc0', 'author manuscript[sb] NOT pubmed pmc[sb]'),
        # 7,680 embargoed
        ('au_embargo', 'author manuscript[sb] AND medline[sb] NOT pubmed pmc[sb]'),
        # pubmednotmedline[sb]
        #   Citations that will not receive MEDLINE indexing because:
        #    * they are for articles in non-MEDLINE journals, or
        #    * they are for articles in MEDLINE journals but the articles are out of scope, or
        #    * they are from issues published prior to the date the journal was selected for indexing, or
        #    * citations to articles from journals that deposit their full text articles in PMC
        #      but have not yet been recommended for indexing in MEDLINE.
        ('pmnml_A', 'pubmednotmedline[sb]'),
        ('pmnml_B', 'pubmednotmedline[sb] NOT medline[sb]'),
        ('pmnml_C', 'pubmednotmedline[sb] NOT pubmed pmc[sb]'),
        ('pmnml_D', 'pubmednotmedline[sb] NOT pubmed pmc[sb] NOT pubstatusnihms[sb] NOT pubstatuspmcsd[sb]'),
        ('pmnml_C_ip0', 'pubmednotmedline[sb] NOT inprocess[sb]'),
        ('pmnml_0_ip1', 'pubmednotmedline[sb] AND inprocess[sb]'),
        ('pmnml_A_pmc1', 'pubmednotmedline[sb] AND pubmed pmc[sb]'),
        ('pmnml_A_pmc0', 'pubmednotmedline[sb] NOT pubmed pmc[sb]'),
        # pmcbook:
        #   Book and book chapter citations available on the NCBI Bookshelf.
        ('pmcbook_A', 'pmcbook'),
        ('pmcbook_A_ml0', 'pmcbook NOT medline[sb]'),
        ('pmcbook_A_pmc0', 'pmcbook NOT pubmed pmc[sb]'),
        ('pmcbook_A_pmc0', 'pmcbook NOT pubmed pmc[sb]'),
    ])

    def __init__(self, email, apikey, tool):
        super(PubMedDnld, self).__init__(email, apikey, tool)
        self.date = str(datetime.datetime.now().date()).replace('-', '_')

    def get_content_counts(self, file_py, force_dnld):
        """Read or download the PubMed content counts"""
        if not os.path.exists(file_py) or force_dnld:
            name2cnt = self.dnld_content_counts()
            self.wrpy_count_data(file_py, name2cnt)
            self.chk_content_counts(name2cnt)
            return name2cnt, self.date
        return self.load_count_data(file_py)

    @staticmethod
    def load_count_data(fin_py):
        """Load NIH iCite information from Python modules"""
        import importlib
        spec = importlib.util.spec_from_file_location("module.name", fin_py)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print('  READ: {PY}'.format(PY=fin_py))
        return mod.CNTS, mod.DATE

    def dnld_content_counts(self):
        """Get the count of various types of content in PubMed"""
        name2cnt = {}
        for name, query in self.name2query.items():
            cnt = self.dnld_count(query)
            print('  Downloaded {N:12,} {A:20} {Q}'.format(N=cnt, A=name, Q=query))
            name2cnt[name] = cnt
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

    def wrpy_count_data(self, fout_py, name2cnt):
        """Write PubMed count data into a Python module"""
        with open(fout_py, 'w') as prt:
            prt.write('"""Downloaded PubMed count data"""\n\n')
            prt.write("DATE = '{DATE}'\n\n".format(DATE=self.date))
            prt.write('# pylint: disable=line-too-long\n')
            self.prt_content_counts(name2cnt, prt)
            prt.write('\n')
            self.prt_content_cntdct(name2cnt, prt)
            print('  WROTE: {PY}'.format(PY=fout_py))

    def prt_content_counts(self, name2cnt, prt=sys.stdout):
        """Print the content typename and the count of that type"""
        for name, query in self.name2query.items():
            if name in name2cnt:
                cnt = name2cnt[name]
                prt.write('# {N:10,} {NAME:20} {Q}\n'.format(N=cnt, NAME=name, Q=query))

    def prt_content_cntdct(self, name2cnt, prt=sys.stdout):
        """Print the content typename and the count of that type"""
        prt.write('CNTS = {\n')
        for name in self.name2query:
            cnt = name2cnt[name]
            prt.write('    "{NAME}": {N},\n'.format(N=cnt, NAME=name))
        prt.write('}\n')

    @staticmethod
    def chk_content_counts(a2n):
        """Check the content typename and the count of that type"""
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
        print('  {N:10,} of {M:10,} PMC (not MEDLINE)'.format(M=a2n['pmc_all'], N=pmc_notmedline))
        print(pmc_notmedline - a2n['pmnml_A_pmc1'])
        print('  {N:10,} of {M:10,} PubMed(not MEDLINE, PMC)'.format(
            N=a2n['all_ml0_pmc0'], M=a2n['all']))
        print('  {T:10,} = {A:10,} (MEDLINE OR PMC) + {B:10,} (not MEDLINE OR PMC)'.format(
            T=a2n['ml1_pmc1'] + a2n['all_ml0_pmc0'],
            A=a2n['ml1_pmc1'],
            B=a2n['all_ml0_pmc0']))
        total = a2n['all']
        au_all = a2n['au_all']
        print('  {N:10,} of {M:10,} {P:3.5f}% author ms'.format(N=au_all, M=total, P=100.0*au_all/total))
        print('  {T:10,} = {A:10,} (MEDLINE OR PMC) + {B:10,} (not MEDLINE OR PMC)'.format(
            T=a2n['ml1_pmc1'] + a2n['all_ml0_pmc0'],
            A=a2n['ml1_pmc1'],
            B=a2n['all_ml0_pmc0']))

    def dnld_count(self, query):
        """Searches an NCBI database for a user search term, returns NCBI IDs."""
        dct = self.run_eutilscmd('esearch', db='pubmed', term=query, rettype='count', retmode='json')
        if 'count' in dct:
            return int(dct['count'])
        return dct


# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
