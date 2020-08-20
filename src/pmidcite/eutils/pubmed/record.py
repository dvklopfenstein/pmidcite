"""Access data in a PubMed record"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"


class PubMedRecord:
    """Access data in a PubMed record"""

    def __init__(self, pubmed_dict):
        self.pmdct = pubmed_dict
        self.pmid = self.pmdct['PMID']
        self.doi = self._init_doi()

    def get_pmc(self):
        """Get the PubMed Central (PMC) ID, if it exists"""
        return self.pmdct.get('PMC')

    def get_bibtex(self, eprint=True):
        """Get bibtex fields and values for PMID and PMC"""
        # https://tex.stackexchange.com/questions/155532/biblatex-and-pubmed-pubmed-central-ids
        pmdct = self.pmdct
        pmid = pmdct['PMID']
        dct = {'pmid':pmid, 'doi':self.doi}
        if 'PMC' in pmdct:
            pmcid = pmdct['PMC']
            dct['pmcid'] = pmcid
            if eprint:
                dct['eprint'] = pmcid
                dct['eprinttype'] = 'pmcid'
            return dct
        if eprint:
            dct['eprint'] = pmid
            dct['eprinttype'] = 'pubmed'
        return dct

    def _init_doi(self):
        """Extract DOI from PubMed record"""
        dct = self.pmdct
        for aid in ['AID', 'LID']:
            if aid in dct:
                for typ, val in dct[aid].items():
                    if typ == 'doi':
                        return val
        return None


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
