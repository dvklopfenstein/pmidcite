"""Given a PubMed ID (PMID), return a list of publications which cite it"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from os.path import join
from os.path import exists
from importlib.util import spec_from_file_location
from importlib.util import module_from_spec

from pmidcite.icite.entry import NIHiCiteEntry


class NIHiCiteLoader:
    """Load iCite citations that are stored as a dict in a Python module"""

    icitepypat = 'p{PMID}.py'

    def __init__(self, dir_icitepy):
        self.dir_dnld = dir_icitepy  # e.g., ./icite

    def load_icites(self, pmids, prt=sys.stdout):
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
            prt.write('{N:5,} of {P:5,} PMIDs have iCite entries\n'.format(
                N=len(icites), P=len(pmids)))
        return icites

    @staticmethod
    def load_icite(file_pmid):
        """Load NIH iCite information from Python modules"""
        if exists(file_pmid):
            spec = spec_from_file_location("module.name", file_pmid)
            mod = module_from_spec(spec)
            spec.loader.exec_module(mod)
            return NIHiCiteEntry(mod.ICITE)
        return None


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
