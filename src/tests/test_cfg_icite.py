#!/usr/bin/env python3
"""Test reading and writing configuration files"""

from os import system
from os.path import join
from os.path import exists
from pmidcite.cfg import Cfg
from tests.icite import DIR_REPO


# pylint: disable=line-too-long
def test_cfg_icite():
    """Test writing and reading the configuration file"""
    # NIH iCite configuration file
    file_cfg = join(DIR_REPO, 'test_icite.cfg')

    system('rm -f {CFG}'.format(CFG=file_cfg))

    # Check that test configuration file was removed
    obj = Cfg(prt_fullname=False)
    obj.set_cfg(file_cfg)
    assert not obj.rd_rc()

    # Write configuration file
    system('cat {CFG}'.format(CFG=file_cfg))
    assert obj.wr_rc()
    system('cat {CFG}'.format(CFG=file_cfg))
    assert exists(file_cfg)
    assert not obj.wr_rc()

    # Read configuration file
    cfg = obj.rd_rc()
    print('cfg:', cfg)
    assert next(iter(cfg)) == file_cfg, 'UNEXPECTED FILENAME: EXP({E}) ACT({A})'.format(
        E=file_cfg, A=next(iter(cfg)))

    assert obj.cfgparser['pmidcite']['dir_icite_py'] == Cfg.dfltdct['pmidcite']['dir_icite_py'], \
        'dir_icite_py: EXP({E}) ACT({A})'.format(
            A=obj.cfgparser['pmidcite']['dir_icite_py'], E=Cfg.dfltdct['pmidcite']['dir_icite_py'])
    assert obj.cfgparser['pmidcite']['dir_pubmed_txt'] == Cfg.dfltdct['pmidcite']['dir_pubmed_txt']
    system('rm {CFG}'.format(CFG=file_cfg))

def test_cfg_eutils():
    """Test writing and reading the configuration file"""
    # NIH iCite configuration file
    file_cfg = join(DIR_REPO, 'test_eutils.cfg')
    obj = Cfg()
    obj.set_cfg(file_cfg)

    # Write configuration file
    system('rm -f {CFG}'.format(CFG=file_cfg))
    assert obj.wr_rc()
    assert exists(file_cfg)
    assert not obj.wr_rc()

    # Read configuration file
    cfg = obj.rd_rc()
    assert next(iter(cfg)) == file_cfg
    assert obj.cfgparser['pmidcite']['email'] == Cfg.dfltdct['pmidcite']['email']
    assert obj.cfgparser['pmidcite']['apikey'] == Cfg.dfltdct['pmidcite']['apikey']
    assert obj.cfgparser['pmidcite']['tool'] == Cfg.dfltdct['pmidcite']['tool']

    system('rm {CFG}'.format(CFG=file_cfg))

if __name__ == '__main__':
    test_cfg_icite()
    test_cfg_eutils()
