"""Run PubMed user query and download PMIDs. Run iCite on PMIDs. Write text file."""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from collections import namedtuple
from pmidcite.cfg import get_cfgparser
from pmidcite.eutils.cmds.pubmed import PubMed
#### from pmidcite.cli.utils import wr_pmids
from pmidcite.icite.downloader import get_downloader


class PubMedQueryToICite:
    """Run PubMed user query and download PMIDs. Run iCite on PMIDs. Write text file."""

    def __init__(self, force_dnld, verbose=True, pmid2note=None):
        self.force_dnld = force_dnld
        self.verbose = verbose
        self.pmid2note = {} if pmid2note is None else pmid2note
        self.cfg = get_cfgparser()
        self.pubmed = PubMed(
            email=self.cfg.get_email(),
            apikey=self.cfg.get_apikey(),
            tool=self.cfg.get_tool())

    def run(self, fout_query, dnld_idxs=None):
        """Give an list of tuples: Query PubMed for PMIDs. Download iCite, given PMIDs"""
        # Download PMIDs and NIH's iCite for only one PubMed query
        nts = self.get_nts_g_list(fout_query)
        if dnld_idxs is not None:
            for idx in dnld_idxs:
                ntd = nts[idx]
                self.querypubmed_runicite(ntd.filename, ntd.pubmed_query)
        # Download PMIDs and NIH's iCite for all PubMed queries
        else:
            for ntd in nts:
                self.querypubmed_runicite(ntd.filename, ntd.pubmed_query)
        return nts

    def run_one(self, fout_query, dnld_idx):
        """Query PubMed for PMIDs. Download iCite, given PMIDs"""
        nts = self.get_nts_g_list(fout_query)
        ntd = nts[dnld_idx]
        return self.querypubmed_runicite(ntd.filename, ntd.pubmed_query)

    def querypubmed_runicite(self, filename, query, details_cites_refs=None):
        """Given a user query, return PMIDs. Then run NIH's iCite"""
        # 1) Query PubMed and download PMIDs
        #    Maximum PMIDs to download at a time is 100,000 (Default is 20):
        #        PMIDCITE uses usehistory='y', so can retrieve more than 100,000 PMIDs
        #        by incrementing the value of retstart for each 100k set of PMIDs
        #        https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
        pmids = self.pubmed.dnld_query_pmids(query, num_ids_p_epost=100000)
        ## print('PMIDCITE QQQQQQQQQQQQQQQQQ {N} PMIDs'.format(N=len(pmids)))
        ## fout_pmids = self.cfg.get_fullname_pmids(filename)
        fout_icite = self.cfg.get_fullname_icite(filename)
        ##### 2) Write PubMed PMIDs into a simple text file, one PMID per line
        ####if fout_pmids != fout_icite:
        ####    if pmids:
        ####        wr_pmids(fout_pmids, pmids)
        ####    else:
        ####        print('  0 PMIDs: NOT WRITING {TXT}'.format(TXT=fout_pmids))
        # 3) Run NIH's iCite on the PMIDs and write the results into a file
        if pmids:
            return self._wr_icite(fout_icite, pmids, details_cites_refs)
        return {}

    def _wr_icite(self, fout_icite, pmids, details_cites_refs):
        """Run PMIDs in iCite and print results into a file"""
        cfg = self.cfg
        dnldr = get_downloader(
            # all citations references
            details_cites_refs=details_cites_refs,
            nih_grouper=cfg.get_nihgrouper(),
            dir_icite_py=cfg.get_dir_icite_py(),
            force_download=self.force_dnld)
        ## print('PMIDCITE PPPPPPPPPPPPPPPPP dnldr.get_pmid2paper {N} PMIDs'.format(N=len(pmids)))
        pmid2paper = dnldr.get_pmid2paper(pmids, self.pmid2note)
        ## print('PMIDCITE PPPPPPPPPPPPPPPPP dnldr.wr_papers{N} PMIDs'.format(N=len(pmids)))
        dnldr.wr_papers(fout_icite, pmid2icitepaper=pmid2paper, force_overwrite=True)
        return pmid2paper

    def get_nts_g_list(self, lst):
        """Turn a list iof tuple strings into a list of namedtuples"""
        nto = namedtuple('Nt', 'filename fullname pubmed_query')
        return [nto._make([fname, self.cfg.get_fullname_icite(fname), qry]) for fname, qry in lst]

    @staticmethod
    def get_index(argv, queries=None):
        """Get the index of the pubmed query to run"""
        # If no argument was provided, run the last query in the list
        if len(argv) == 1:
            return [-1]
        if argv[1] == 'all' and queries is not None:
            return list(range(len(queries)))
        if 'h' in argv[1] and queries:
            for idx, item in enumerate(queries):
                print('{I:3} {E}'.format(I=idx, E=item))
            sys.exit(1)
        return [int(n) for n in argv[1:] if n.lstrip('-').isdigit()]


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
