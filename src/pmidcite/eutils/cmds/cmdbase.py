"""Run a NCBI E-Utils command that requires args, rettype and retmode"""
# pylint: disable=line-too-long
# https://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly

__author__ = 'DV Klopfenstein, PhD'
__copyright__ = "Copyright (C) 2016-present DV Klopfenstein, PhD. All rights reserved."
__license__ = "GPL"

from pmidcite.cfg import Cfg
from pmidcite.eutils.cmds.base import EntrezUtilities


class CommandBase(EntrezUtilities):
    """Run a NCBI E-Utils command that requires args, rettype and retmode"""

    def __init__(self, rettype='medline', retmode='text', batch_size=100, retmax=10000):
        cfg = Cfg()
        super().__init__(cfg.get_email(), cfg.get_apikey(), cfg.get_tool())
        self.batch_size = batch_size
        self.retmax = retmax
        self.rettype = rettype
        self.retmode = retmode
        ## print(f'CommandBase: retmax({retmax}) retmode({retmode}) rettype({rettype})')


# Copyright (C) 2016-present DV Klopfenstein, PhD. All rights reserved.
