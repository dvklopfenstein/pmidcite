"""Manage configuration for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from pmidcite.cfgparser.base import CfgParserBase


class NIHiCiteCfg(CfgParserBase):
    """Manage configuration for NIH iCite run for one PubMed ID (PMID)"""

    dfltdct = {
        'DEFAULT' : {
            'dir_pmid_py': '.',
            'dir_pmid_txt': '.',
        },
    }

    def __init__(self, cfgfile='.pmidciterc'):
        super(NIHiCiteCfg, self).__init__(cfgfile, self.dfltdct)


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
