#!/usr/bin/env python3
"""Test reading and writing configuration files"""

import os
from pmidcite.cfgparser.icite import NIHiCiteCfg
from pmidcite.cfgparser.eutils import EUtilsCfg

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")


# pylint: disable=line-too-long
def test_cfg_icite():
    """Test writing and reading the configuration file"""
    # NIH iCite configuration file
    obj = NIHiCiteCfg()
    file_cfg = os.path.join(REPO, 'test_icite.cfg')
    obj.cfgfile = file_cfg

    # Write configuration file
    os.system('rm -f {CFG}'.format(CFG=file_cfg))
    print(obj.rd_rc())
    assert obj.wr_rc()
    assert os.path.exists(file_cfg)
    assert not obj.wr_rc()

    # Read configuration file
    cfg = obj.rd_rc()
    assert next(iter(cfg)) == file_cfg

    assert obj.cfgparser['DEFAULT']['dir_pmid_py'] == NIHiCiteCfg.dfltdct['DEFAULT']['dir_pmid_py']
    assert obj.cfgparser['DEFAULT']['dir_pmid_txt'] == NIHiCiteCfg.dfltdct['DEFAULT']['dir_pmid_txt']

def test_cfg_eutils():
    """Test writing and reading the configuration file"""
    # NIH iCite configuration file
    file_cfg = os.path.join(REPO, 'test_eutils.cfg')
    obj = EUtilsCfg(file_cfg, chk=False)

    # Write configuration file
    os.system('rm -f {CFG}'.format(CFG=file_cfg))
    assert obj.wr_rc()
    assert os.path.exists(file_cfg)
    assert not obj.wr_rc()

    # Read configuration file
    cfg = obj.rd_rc()
    assert next(iter(cfg)) == file_cfg
    assert obj.cfgparser['DEFAULT']['email'] == EUtilsCfg.dfltdct['DEFAULT']['email']
    assert obj.cfgparser['DEFAULT']['apikey'] == EUtilsCfg.dfltdct['DEFAULT']['apikey']
    assert obj.cfgparser['DEFAULT']['tool'] == EUtilsCfg.dfltdct['DEFAULT']['tool']


if __name__ == '__main__':
    test_cfg_icite()
    test_cfg_eutils()
