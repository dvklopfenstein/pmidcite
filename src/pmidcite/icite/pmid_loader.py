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

    def __init__(self, nih_grouper, dir_icitepy, assc_pmid_keysset, icitepypat='p{PMID}.py'):
        self.nih_grouper = nih_grouper
        self.dir_dnld = dir_icitepy  # e.g., ./icite
        self.associated_pmid_keysset = assc_pmid_keysset
        self.icitepypat = icitepypat

    def load_icites(self, pmids, prt=stdout):
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
        if prt:
            num_icites = len(icites)
            num_pmids = len(pmids)
            if num_icites != num_pmids:
                prt.write('{N:5,} of {P:5,} PMIDs have iCite entries\n'.format(
                    N=num_icites,
                    P=num_pmids))
        return icites

    def load_icite_mods_all(self, pmids_top):
        """Load NIHiCiteEntry for the citations and references of PMIDs in pmids_top"""
        icites_top = self.load_icites(pmids_top)                             # [NIHiCiteEntry]
        pmids_top = set(o.dct['pmid'] for o in icites_top)
        pmids_linked = self._get_pmids_linked(icites_top)                    # [NIHiCiteEntry]
        icites_linked = self.load_icites(pmids_linked.difference(pmids_top)) # [NIHiCiteEntry]
        ## print('LLLLLLLLLL NIHiCiteLoader load_icite_mods_all icites_top', icites_top)
        ## print('LLLLLLLLLL NIHiCiteLoader load_icite_mods_all pmids_linked', len(pmids_linked))
        ## print('LLLLLLLLLL NIHiCiteLoader load_icite_mods_all icites_linked', len(icites_linked))
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
            ## print('LLLLLLLLLLLLL load_icite', file_pmid)
            return NIHiCiteEntry(mod.ICITE, self.nih_grouper.get_group(mod.ICITE['nih_percentile']))
        return None

    def load_pmid(self, pmid):
        """Get NIHiCiteEntry for a PMID"""
        fin_py = self.get_file_pmid(pmid)
        return self.load_icite(fin_py)

    def _get_pmids_linked(self, icites_top):
        """Get the PMIDs for the citations and references of top NIHiCiteEntry"""
        s_asscpmid_keys = self.associated_pmid_keysset
        return set(pmid for o in icites_top for f in s_asscpmid_keys for pmid in o.dct[f])
        ## pmids_linked = set()
        ## for obj in icites_top:
        ##     for fld in self.associated_pmid_keysset:
        ##         for pmid in obj.dct[fld]:
        ##             pmids_linked.add(pmid)
        ## return pmids_linked


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
