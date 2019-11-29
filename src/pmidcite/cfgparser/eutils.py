"""Manage configuration for NIH iCite run for one PubMed ID (PMID)"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
from pmidcite.cfgparser.base import CfgParserBase


class EUtilsCfg(CfgParserBase):
    """Manage configuration for Entrez Utilities"""

    dfltdct = {
        'DEFAULT' : {
            'email': 'name@email.edu',
            # https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/
            'apikey': 'long_hex_digit',
            'tool': 'scripts',
        },
    }

    def __init__(self, cfgfile='.eutilsrc', chk=True):
        super(EUtilsCfg, self).__init__(cfgfile, self.dfltdct)
        if chk:
            self._run_chk()

    def _run_chk(self):
        if not self.rd_rc():
            self._err_notfound()
        dflt = self.cfgparser['DEFAULT']
        self._chk_email(dflt)
        self._chk_apikey(dflt)

    def _chk_email(self, loaded):
        """Check to see that user has added their email"""
        if loaded['email'] == self.dfltdct['DEFAULT']['email']:
            raise RuntimeError('SET EMAIL IN {CFG}'.format(CFG=self.cfgfile))

    def _chk_apikey(self, loaded):
        """Check to see that user has added a NCBI API key"""
        try:
            int(loaded['apikey'], 16)
        except ValueError:
            msg = ('SET API KEY IN {CFG}\n'
                   'Get an NCBI API key to run the E-utilities:\n'
                   'https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/'
                   'new-api-keys-for-the-e-utilities\n'
                   'To ensure your API key is not made public, add {CFG} to the .gitignore')
            raise RuntimeError(msg.format(CFG=self.cfgfile))

    def _err_notfound(self):
        """Report the config file was not found"""
        msg = ('E-Utils CONFIG FILE NOT FOUND: {CFG}\n'
               'Generate {CFG} with:\n    '
               "python3 -c 'from pmidcite.cfgparser.eutils "
               "import EUtilsCfg; EUtilsCfg().wr_rc()'\n"
               'To ensure your API key is not made public, add {CFG} to the .gitignore')
        raise RuntimeError(msg.format(CFG=self.cfgfile))

    def get_email(self):
        """Get email"""
        return self.cfgparser['DEFAULT']['email']

    def get_apikey(self):
        """Get API Key"""
        return self.cfgparser['DEFAULT']['apikey']

    def get_tool(self):
        """Get tool name"""
        return self.cfgparser['DEFAULT']['tool']

    @staticmethod
    def _init_cfgfilename(dfltcfgfile):
        """Get the configuration filename"""
        if 'PMIDCITECONF' in os.environ:
            cfgfile = os.environ['PMIDCITECONF']
            if os.path.exists(cfgfile):
                return cfgfile
        return dfltcfgfile

# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
