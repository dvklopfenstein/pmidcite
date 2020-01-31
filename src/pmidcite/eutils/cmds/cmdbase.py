"""Fetch items and write"""

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2016-present DV Klopfenstein. All rights reserved."
__license__ = "GPL"

from pmidcite.cfg import Cfg
from pmidcite.eutils.cmds.base import EntrezUtilities


#### class EntrezCommands(EntrezUtilities):
class CommandBase(EntrezUtilities):
    """Fetch and write text"""

    def __init__(self, retmax=10000, rettype='medline', retmode='text', batch_size=100, **kws):
        kws_base = {k:v for k, v in kws.items() if k in EntrezUtilities.exp_kws}
        cfg = Cfg()
        super(CommandBase, self).__init__(
            cfg.get_email(), cfg.get_apikey(), cfg.get_tool(), **kws_base)
        self.batch_size = batch_size
        self.retmax = retmax
        self.rettype = rettype
        self.retmode = retmode


# Copyright (C) 2016-present DV Klopfenstein. All rights reserved.
