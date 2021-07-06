"""Manage pmidcite Configuration"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from os import environ
from os.path import exists
from os.path import basename
from sys import stdout
from sys import argv
import configparser

from pmidcite.icite.nih_grouper import NihGrouper


# pylint: disable=useless-object-inheritance
class Cfg(object):
    """Manage pmidcite Configuration"""

    envvar = 'PMIDCITECONF'
    dfltcfgfile = '.pmidciterc'

    dfltdct = {
        'pmidcite' : {
            # Information downloaded from NIH iCite stored in a Python module
            'dir_icite_py': '.',

            # Used by PubMedQueryToICite:
            # Directory for files containing PMIDs downloaded from PubMed
            'dir_pmids': '.',
            # Run NIH's iCite on a set of PMIDs and store results in a file
            'dir_icite': '.',

            # NIH Group divisions
            'group1_min': '2.1',
            'group2_min': '15.7',
            'group3_min': '83.9',
            'group4_min': '97.5',

            # Entrez utilities
            'email': 'name@university.edu',
            # https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/
            'apikey': 'LONG_HEX_NCBI_API_KEY',
            'tool': 'scripts',

            # Directory for abstracts downloaded from PubMed
            'dir_pubmed_txt': '.',
        },
    }

    def __init__(self, check=True, prt=stdout, prt_fullname=True):
        self.cfgfile = self._init_cfgfilename()
        self.cfgparser = self._get_dflt_cfgparser()
        if check:
            self._run_chk(prt, prt_fullname)

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

    def get_dir_icite(self):
        """Get the name of the directory containg PubMed entry text files"""
        return self.cfgparser['pmidcite']['dir_icite']

    def get_nihgrouper(self):
        """Get an NIH Grouper with default values from the cfg file"""
        cfg = self.cfgparser['pmidcite']
        return NihGrouper(
            float(cfg['group1_min']),
            float(cfg['group2_min']),
            float(cfg['group3_min']),
            float(cfg['group4_min']))

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

    def rd_rc(self, prt=stdout, prt_fullname=True):
        """Read a configuration file"""
        if exists(self.cfgfile):
            if prt:
                cfgfile = self.cfgfile if prt_fullname else basename(self.cfgfile)
                prt.write('  READ: {CFG}\n'.format(CFG=cfgfile))
        # Returns a list containing configuration file names
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
        cfgfile = environ[self.envvar] if self.envvar in environ else self.cfgfile
        msg = ('E-Utils CONFIG FILE NOT FOUND: {CFG}\n'
               'Generate {CFG} with:\n    '
               "$ python3 -c 'from pmidcite.cfg import Cfg; Cfg(check=False).wr_rc(force=True)'\n"
               'To ensure your API key is not made public, add {CFG} to the .gitignore')
        raise RuntimeError(msg.format(CFG=cfgfile))

    def _get_dflt_cfgparser(self):
        """Create a ConfigParser() filled with the default key-value"""
        config = configparser.ConfigParser()
        for section, dfltdct_cur in self.dfltdct.items():
            ## print('KEY-VAL: {} {}'.format(section, dfltdct_cur))
            config[section] = dfltdct_cur
        return config

    def prt_rcfile_dflt(self, prt=stdout):
        """Print default rcfile"""
        cfgparser = self._get_dflt_cfgparser()
        cfgparser.write(prt)

    def _init_cfgfilename(self):
        """Get the configuration filename"""
        if self.envvar in environ:
            cfgfile = environ[self.envvar]
            if exists(cfgfile):
                return cfgfile
            print('**WARNING: NO pmidcite CONFIG FILE FOUND AT {ENVVAR}={F}'.format(
                F=cfgfile, ENVVAR=self.envvar))
        if not exists(self.dfltcfgfile):
            print('**WARNING: NO pmidcite CONFIG FILE FOUND: {F}'.format(
                F=self.dfltcfgfile))
        return self.dfltcfgfile


def get_cfgparser(prt=stdout):
    """Init cfg parser"""
    cfgparser = Cfg(check=False, prt=prt)
    cfgparser.rd_rc(prt=prt)
    return cfgparser


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
