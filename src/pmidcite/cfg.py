"""Manage pmidcite Configuration"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

from os import environ
from os import getcwd
from os.path import exists
from os.path import basename
from os.path import join
from os.path import abspath
from sys import stdout
import configparser

from pmidcite.icite.nih_grouper import NihGrouper


def get_cfgparser(prt=stdout):
    """Init cfg parser"""
    cfgparser = Cfg(check=False, prt=prt)
    cfgparser.rd_rc(prt=prt)
    return cfgparser

# pylint: disable=useless-object-inheritance
class Cfg(object):
    """Manage pmidcite Configuration"""

    envvar = 'PMIDCITECONF'
    dfltcfgfile = '.pmidciterc'

    dfltdct = {
        'pmidcite' : {
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

            # Information downloaded from NIH iCite stored in a Python module
            'dir_icite_py': 'None',

            # Directory for abstracts downloaded from PubMed
            'dir_pubmed_txt': 'None',

            # Used by PubMedQueryToICite:
            # Directory for files containing PMIDs downloaded from PubMed
            'dir_pmids': 'None',
            # Run NIH's iCite on a set of PMIDs and store results in a file
            'dir_icite': 'None',
        },
    }

    def __init__(self, check=True, prt=stdout, prt_fullname=True):
        self.cfgfile = self._init_cfgfilename(prt)
        self.cfgparser = self._get_dflt_cfgparser()
        if check:
            self._run_chk(prt, prt_fullname)

    def prt_cfgfile(self, prt=stdout):
        """Print information about the configuration file"""
        prt.write('  printenv {VAR} # value({VAL})\n'.format(
            VAR=self.envvar,
            VAL=environ[self.envvar]))
        prt.write('  CFG FILE: {CFG}\n'.format(
            CFG=abspath(self.cfgfile)))

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

    def get_fullname_pmids(self, filename):
        """get the name of the directory containg pubmed entry text files"""
        return self._get_fullname(filename, 'dir_pmids')

    def get_fullname_icite(self, filename):
        """get the name of the directory containg pubmed entry text files"""
        return self._get_fullname(filename, 'dir_icite')

    def _get_fullname(self, filename, dir_key):
        """Get the filename, including optionally the directory and filename"""
        dirname = self.cfgparser['pmidcite'][dir_key]
        if dirname is None or dirname == 'None':
            return filename
        if dirname is not None and exists(dirname):
            return join(dirname, filename)
        cwd = getcwd()
        print('**WARNING: DIR NOT EXIST {DIR_TYPE}({DIR_NAME}) RETURNING CWD({CWD})'.format(
            DIR_TYPE=dir_key, DIR_NAME=dirname, CWD=cwd))
        return join(cwd, filename)

    def set_dir_pubmed_txt(self, dirname):
        """Set the name of the directory containg PubMed entry text files"""
        self.cfgparser['pmidcite']['dir_pubmed_txt'] = self._get_dirname_str(dirname)

    def set_dir_icite_py(self, dirname):
        """Set the name of the directory containg PubMed entry text files"""
        self.cfgparser['pmidcite']['dir_icite_py'] = self._get_dirname_str(dirname)

    def set_dir_icite(self, dirname):
        """Set the name of the directory containg PubMed entry text files"""
        self.cfgparser['pmidcite']['dir_icite'] = self._get_dirname_str(dirname)

    def set_dir_pmids(self, dirname):
        """Set the name of the directory containg PubMed entry text files"""
        self.cfgparser['pmidcite']['dir_pmids'] = self._get_dirname_str(dirname)

    @staticmethod
    def _get_dirname_str(dirname):
        """Convert None to the str, "None", as needed by configparser"""
        return 'None' if dirname is None or dirname == 'None' else dirname

    def get_nihgrouper(self, min1=None, min2=None, min3=None, min4=None):
        """Get an NIH Grouper with default values from the cfg file"""
        cfg = self.cfgparser['pmidcite']
        return NihGrouper(
            float(cfg['group1_min'] if not min1 else min1),
            float(cfg['group2_min'] if not min2 else min2),
            float(cfg['group3_min'] if not min3 else min3),
            float(cfg['group4_min'] if not min4 else min4))

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
        if self.cfgfile is not None and exists(self.cfgfile):
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

    def _init_cfgfilename(self, prt=None):
        """Get the configuration filename"""
        if self.envvar in environ:
            cfgfile = environ[self.envvar]
            if exists(cfgfile):
                return cfgfile
            if prt:
                prt.write(f'**WARNING: NO pmidcite CONFIG FILE FOUND AT {self.envvar}={cfgfile}\n')
        if not exists(self.dfltcfgfile) and prt:
            prt.write(f'**WARNING: NO pmidcite CONFIG FILE FOUND: {self.dfltcfgfile}\n')
        return self.dfltcfgfile



# Copyright (C) 2019-present DV Klopfenstein, PhD. All rights reserved.
