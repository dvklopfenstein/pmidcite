"""Manage pmidcite Configuration"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from os import environ
from os.path import exists
from os.path import basename
import sys
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

            # Information downloaded from NIH iCite stored in a Python module
            'dir_icite_py': '.',

            # Directory for abstracts downloaded from PubMed
            'dir_pubmed_txt': '.',

            # Used by PubMedQueryToICite:
            # Directory for files containing PMIDs downloaded from PubMed
            'dir_pmids': '.',
            # Run NIH's iCite on a set of PMIDs and store results in a file
            'dir_icite': '.',
        },
    }

    def __init__(self, chk=True, prt=sys.stdout, prt_fullname=True):
        self.cfgfile = self._init_cfgfilename()
        self.cfgparser = self._get_dflt_cfgparser()
        if chk:
            self._run_chk(prt, prt_fullname)

    def _run_chk(self, prt, prt_fullname):
        if not self.rd_rc(prt, prt_fullname):
            self._err_notfound()
        dflt = self.cfgparser['pmidcite']
        self._chk_email(dflt)
        self._chk_apikey(dflt)

    def set_cfg(self, cfgfile=None):
        """Set config file and initialize ConfigParser()"""
        self.cfgfile = self.dfltcfgfile if cfgfile is None else cfgfile
        self.cfgparser = self._get_dflt_cfgparser()
        return self.cfgparser.read(self.cfgfile)

    def rd_rc(self, prt=sys.stdout, prt_fullname=True):
        """Read a configuration file"""
        if exists(self.cfgfile):
            if prt:
                cfgfile = self.cfgfile if prt_fullname else basename(self.cfgfile)
                prt.write('  READ: {CFG}\n'.format(CFG=cfgfile))
        return self.cfgparser.read(self.cfgfile)

    def wr_rc(self, force=False):
        """Write a sample configuration with default values set"""
        if not exists(self.cfgfile) or force:
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
        cfgfile = environ['PMIDCITECONF'] if 'PMIDCITECONF' in environ else self.cfgfile
        msg = ('E-Utils CONFIG FILE NOT FOUND: {CFG}\n'
               'Generate {CFG} with:\n    '
               "$ python3 -c 'from pmidcite.cfg import Cfg; Cfg(chk=False).wr_rc(force=True)'\n"
               'To ensure your API key is not made public, add {CFG} to the .gitignore')
        raise RuntimeError(msg.format(CFG=cfgfile))

    def get_email(self):
        """Get email"""
        return self.cfgparser['pmidcite']['email']

    def get_apikey(self):
        """Get API Key"""
        return self.cfgparser['pmidcite']['apikey']

    def get_tool(self):
        """Get tool name"""
        return self.cfgparser['pmidcite']['tool']

    def get_dir_pubmed_txt(self):
        """Get the name of the directory containg PubMed entry text files"""
        return self.cfgparser['pmidcite']['dir_pubmed_txt']

    def get_dir_icite_py(self):
        """Get the name of the directory containg PubMed entry text files"""
        return self.cfgparser['pmidcite']['dir_icite_py']

    def _get_dflt_cfgparser(self):
        """Create a ConfigParser() filled with the default key-value"""
        config = configparser.ConfigParser()
        for section, dfltdct_cur in self.dfltdct.items():
            ## print('KEY-VAL: {} {}'.format(section, dfltdct_cur))
            config[section] = dfltdct_cur
        return config

    def _init_cfgfilename(self):
        """Get the configuration filename"""
        if 'PMIDCITECONF' in environ:
            cfgfile = environ['PMIDCITECONF']
            if exists(cfgfile):
                return cfgfile
            print('**WARNING: NO pmidcite CONFIG FILE FOUND AT PMIDCITECONF={F}'.format(
                F=cfgfile))
        if not exists(self.dfltcfgfile):
            print('**WARNING: NO pmidcite CONFIG FILE FOUND: {F}'.format(
                F=self.dfltcfgfile))
        return self.dfltcfgfile


def get_cfgparser(prt=sys.stdout):
    """Init cfg parser"""
    cfgparser = Cfg(chk=False, prt=prt)
    cfgparser.rd_rc(prt=prt)
    return cfgparser


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
