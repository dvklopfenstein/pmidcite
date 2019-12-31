"""Manage pmidcite Configuration"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import configparser


# pylint: disable=useless-object-inheritance
class Cfg(object):
    """Manage pmidcite Configuration"""

    dfltcfgfile = '.pmidciterc'

    dfltdct = {
        'pmidcite' : {

            # Entrez utilities
            'email': 'name@email.edu',
            # https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/
            'apikey': 'long_hex_digit',
            'tool': 'scripts',
            'dir_pubmed_txt': '.',

            # NIH iCite
            'dir_pmid_py': '.',
        },
    }

    def __init__(self, chk=True):
        self.cfgfile = self._init_cfgfilename()
        self.cfgparser = self._get_cfgparser()
        if chk:
            self._run_chk()

    def _run_chk(self):
        if not self.rd_rc():
            self._err_notfound()
        dflt = self.cfgparser['pmidcite']
        self._chk_email(dflt)
        self._chk_apikey(dflt)

    def set_cfg(self, cfgfile=None):
        """Set config file and initialize ConfigParser()"""
        self.cfgfile = self.dfltcfgfile if cfgfile is None else cfgfile
        self.cfgparser = self._get_cfgparser()
        return self.cfgparser.read(self.cfgfile)

    def rd_rc(self):
        """Read a configuration file"""
        if os.path.exists(self.cfgfile):
            print('  READ: {CFG}'.format(CFG=self.cfgfile))
        return self.cfgparser.read(self.cfgfile)

    def wr_rc(self, force=False):
        """Write a sample configuration with default values set"""
        if not os.path.exists(self.cfgfile) or force:
            with open(self.cfgfile, 'w') as prt:
                self.cfgparser.write(prt)
                print('  WROTE: {CFG}'.format(CFG=self.cfgfile))
                return True
        print('  EXISTS: {CFG} OVERWRITE WITH wr_rc(force=True)'.format(CFG=self.cfgfile))
        return False

    def _chk_email(self, loaded):
        """Check to see that user has added their email"""
        if loaded['email'] == self.dfltdct['pmidcite']['email']:
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
               "$ python3 -c 'from pmidcite.cfg import Cfg; Cfg(chk=False).wr_rc(force=True)'\n"
               'To ensure your API key is not made public, add {CFG} to the .gitignore')
        raise RuntimeError(msg.format(CFG=self.cfgfile))

    def get_email(self):
        """Get email"""
        return self.cfgparser['pmidcite']['email']

    def get_apikey(self):
        """Get API Key"""
        return self.cfgparser['pmidcite']['apikey']

    def get_tool(self):
        """Get tool name"""
        return self.cfgparser['pmidcite']['tool']

    def _get_cfgparser(self):
        """Create a ConfigParser() filled with the default key-value"""
        config = configparser.ConfigParser()
        for section, dfltdct_cur in self.dfltdct.items():
            # print('KEY-VAL: {} {}'.format(section, dfltdct_cur))
            config[section] = dfltdct_cur
        return config

    def _init_cfgfilename(self):
        """Get the configuration filename"""
        if 'PMIDCITECONF' in os.environ:
            cfgfile = os.environ['PMIDCITECONF']
            if os.path.exists(cfgfile):
                return cfgfile
            print('**WARNING: NO pmidcite CONFIG FILE FOUND AT PMIDCITECONF={F}'.format(
                F=cfgfile))
        if not os.path.exists(self.dfltcfgfile):
            print('**WARNING: NO pmidcite CONFIG FILE FOUND: {F}'.format(
                F=self.dfltcfgfile))
        return self.dfltcfgfile


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.