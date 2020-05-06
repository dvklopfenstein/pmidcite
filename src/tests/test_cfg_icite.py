#!/usr/bin/env python3
"""Test reading and writing configuration files"""

import os
from pmidcite.cfg import Cfg

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")


# pylint: disable=line-too-long
def test_cfg_icite():
    """Test writing and reading the configuration file"""
    # NIH iCite configuration file
    file_cfg = os.path.join(REPO, 'test_icite.cfg')

    os.system('rm -f {CFG}'.format(CFG=file_cfg))

    # Check that test configuration file was removed
    obj = Cfg()
    obj.set_cfg(file_cfg)
    assert not obj.rd_rc()

    # Write configuration file
    os.system('cat {CFG}'.format(CFG=file_cfg))
    assert obj.wr_rc()
    os.system('cat {CFG}'.format(CFG=file_cfg))
    assert os.path.exists(file_cfg)
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

def test_cfg_eutils():
    """Test writing and reading the configuration file"""
    # NIH iCite configuration file
    file_cfg = os.path.join(REPO, 'test_eutils.cfg')
    obj = Cfg()
    obj.set_cfg(file_cfg)

    # Write configuration file
    os.system('rm -f {CFG}'.format(CFG=file_cfg))
    assert obj.wr_rc()
    assert os.path.exists(file_cfg)
    assert not obj.wr_rc()

    # Read configuration file
    cfg = obj.rd_rc()
    assert next(iter(cfg)) == file_cfg
    assert obj.cfgparser['pmidcite']['email'] == Cfg.dfltdct['pmidcite']['email']
    assert obj.cfgparser['pmidcite']['apikey'] == Cfg.dfltdct['pmidcite']['apikey']
    assert obj.cfgparser['pmidcite']['tool'] == Cfg.dfltdct['pmidcite']['tool']


if __name__ == '__main__':
    test_cfg_icite()
    test_cfg_eutils()
