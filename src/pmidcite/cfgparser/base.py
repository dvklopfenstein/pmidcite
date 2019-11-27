"""Manage a ConfigParser"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import configparser


# pylint: disable=useless-object-inheritance
class CfgParserBase(object):
    """Manage a ConfigParser"""

    def __init__(self, dfltcfgfile, dfltdct):
        self.cfgfile = self._init_cfgfilename(dfltcfgfile)
        self.cfgparser = self._init_cfgparser(dfltdct)

    def rd_rc(self):
        """Read a configuration file"""
        return self.cfgparser.read(self.cfgfile)

    @staticmethod
    def _init_cfgfilename(dfltcfgfile):
        """Get the configuration filename"""
        if 'PMIDCITECONF' in os.environ:
            cfgfile = os.environ['PMIDCITECONF']
            if os.path.exists(cfgfile):
                return cfgfile
        return dfltcfgfile

    def wr_rc(self, force=False):
        """Write a sample configuration with default values set"""
        if not os.path.exists(self.cfgfile) or force:
            with open(self.cfgfile, 'w') as prt:
                self.cfgparser.write(prt)
                print('  WROTE: {CFG}'.format(CFG=self.cfgfile))
                return True
        print('  EXISTS: {CFG} OVERWRITE WITH wr_rc(force=True)'.format(CFG=self.cfgfile))
        return False

    @staticmethod
    def _init_cfgparser(dfltdct_cfg):
        """Create a ConfigParser()"""
        config = configparser.ConfigParser()
        for section, dfltdct_cur in dfltdct_cfg.items():
            config[section] = dfltdct_cur
        return config


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
