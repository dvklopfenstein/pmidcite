"""Given a PubMed ID (PMID), return a list of publications which cite it"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from sys import stdout
from os.path import join
from os.path import exists
from importlib.util import spec_from_file_location
from importlib.util import module_from_spec

from pmidcite.icite.entry import NIHiCiteEntry


class NIHiCiteLoader:
    """Load iCite citations that are stored as a dict in a Python module"""

    def __init__(self, nih_grouper, dir_icitepy, icitepypat='p{PMID}.py', prt=stdout):
        self.nih_grouper = nih_grouper
        self.dir_dnld = dir_icitepy  # e.g., ./icite
        self.icitepypat = icitepypat
        self.prt = prt

    def load_icites(self, pmids):
        """Load multiple NIH iCite data from Python modules"""
        if not pmids:
            return []
        icites = []
        s_icitepat = self.icitepypat
        s_load_icite = self.load_icite
        for pmid in pmids:
            file_pmid = join(self.dir_dnld, s_icitepat.format(PMID=pmid))
            iciteobj = s_load_icite(file_pmid)
            if iciteobj is not None:
                icites.append(iciteobj)
        if self.prt:
            self.prt.write('{N:5,} of {P:5,} PMIDs have iCite entries\n'.format(
                N=len(icites), P=len(pmids)))
        return icites

    def load_icite_mods_all(self, pmids_top):
        """Load iCite all connected NIHiCiteEntry"""
        icites_top = self.load_icites(pmids_top)
        pmids_top = set(o.dct['pmid'] for o in icites_top)
        pmids_linked = self._get_pmids_linked(icites_top)
        icites_linked = self.load_icites(pmids_linked.difference(pmids_top))
        return icites_top + icites_linked

    def get_file_pmid(self, pmid):
        """Get the name of the icite file for one PMID"""
        return join(self.dir_dnld, self.icitepypat.format(PMID=pmid))

    def load_icite(self, file_pmid):
        """Load NIH iCite information from Python modules"""
        if exists(file_pmid):
            spec = spec_from_file_location("module.name", file_pmid)
            mod = module_from_spec(spec)
            spec.loader.exec_module(mod)
            return NIHiCiteEntry(mod.ICITE, self.nih_grouper.get_group(mod.ICITE['nih_percentile']))
        return None

    def load_pmid(self, pmid):
        """Get NIHiCiteEntry for a PMID"""
        fin_py = self.get_file_pmid(pmid)
        return self.load_icite(fin_py)

    @staticmethod
    def _get_pmids_linked(icites_top):
        """Get PMID hextrings linked to given hex strings"""
        pmidstrs_linked = set()
        flds = ['cited_by', 'cited_by_clin', 'references']
        for obj in icites_top:
            for fld in flds:
                for pmid in obj.dct[fld]:
                    pmidstrs_linked.add(pmid)
        return pmidstrs_linked


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
