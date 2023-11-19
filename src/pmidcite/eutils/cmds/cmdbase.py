"""Fetch items and write"""

__author__ = 'DV Klopfenstein, PhD'
__copyright__ = "Copyright (C) 2016-present DV Klopfenstein, PhD. All rights reserved."
__license__ = "GPL"

from pmidcite.cfg import Cfg
from pmidcite.eutils.cmds.base import EntrezUtilities


class CommandBase(EntrezUtilities):
    """Fetch and write text"""

    def __init__(self, retmax=10000, rettype='medline', retmode='text', batch_size=100):
        cfg = Cfg()
        super().__init__(cfg.get_email(), cfg.get_apikey(), cfg.get_tool())
        self.batch_size = batch_size
        self.retmax = retmax
        self.rettype = rettype
        self.retmode = retmode
        ## print(f'CommandBase: retmax({retmax}) retmode({retmode}) rettype({rettype})')


# Copyright (C) 2016-present DV Klopfenstein, PhD. All rights reserved.
