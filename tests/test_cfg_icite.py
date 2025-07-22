#!/usr/bin/env python3
"""Test cfg file documentation matches cfg init"""

from os import system
from os import stat
from os.path import join
from os.path import exists
from os.path import basename
from os.path import relpath
from sys import argv
import filecmp
from pmidcite.cfg import Cfg
from pmidcite.cfgini import wr_rcfile
from tests.icite import DIR_REPO


# pylint: disable=line-too-long
def test_cfg_desecriptive():
    """Test default cfg file that contains detailed comments"""
    file_cfg = join(DIR_REPO, 'test_icite.cfg')

    # Remove test configuration file and test that it does not exist
    system('rm -f {CFG}'.format(CFG=file_cfg))
    assert not exists(file_cfg)

    # Test that non-existing configuration file can not be read by Cfg
    obj = Cfg(prt_fullname=False)
    obj.set_cfg(file_cfg)
    assert not obj.rd_rc()

    # Write configuration file. Test that an exiting cfg file is not overwritten
    system('cat {CFG}'.format(CFG=file_cfg))
    assert wr_rcfile(file_cfg, force=False)
    system('cat {CFG}'.format(CFG=file_cfg))
    assert exists(file_cfg)
    assert not wr_rcfile(file_cfg, force=False)

    # Read configuration file, file_cfg
    cfg = obj.rd_rc()
    print('cfg:', cfg)
    assert next(iter(cfg)) == file_cfg, 'UNEXPECTED FILENAME: EXP({E}) ACT({A})'.format(
        E=file_cfg, A=next(iter(cfg)))

    # Test that the values for the new cfg file are the default values
    fin_base = basename(file_cfg)
    for key, actual in obj.cfgparser['pmidcite'].items():
        print('{}: {} {}'.format(fin_base, key, actual))
        expected = Cfg.dfltdct['pmidcite'][key]
        assert actual == expected, '{}: KEY({}) ACTUAL({}) != EXPECTED({})'.format(
            file_cfg, key, actual, expected)
    print(stat(file_cfg))
    system('rm {CFG}'.format(CFG=file_cfg))
    print('PASSED: cfg init with comments')


def test_cfg_example(update_example=False):
    """Test that the config file example is up-to-date"""
    fin_cfg = join(DIR_REPO, 'test_icite.cfg')
    fin_ex = join(DIR_REPO, 'doc/example_cfg/.pmidciterc')
    wr_rcfile(fin_cfg, force=True)
    wr_rcfile(fin_ex, force=update_example)
    # Compare the contents of the two files
    assert filecmp.cmp(fin_cfg, fin_ex, shallow=False), 'EXP({}) != ACT({})'.format(
        relpath(fin_ex), relpath(fin_cfg))
    system('rm {CFG}'.format(CFG=fin_cfg))
    print('PASSED: Cfg example matches cfg default')


def test_cfg_icite():
    """Test cfg file documentation matches cfg init"""
    # NIH iCite configuration file
    file_cfg = join(DIR_REPO, 'test_icite.cfg')

    # Remove test configuration file and test that it can no longer be read by Cfg
    system('rm -f {CFG}'.format(CFG=file_cfg))
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
    print('PASSED: cfg init with no comments')


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

    # Newly created cfg file should have default values for private data
    cfg = obj.rd_rc()
    assert next(iter(cfg)) == file_cfg
    assert obj.cfgparser['pmidcite']['email'] == Cfg.dfltdct['pmidcite']['email']
    assert obj.cfgparser['pmidcite']['apikey'] == Cfg.dfltdct['pmidcite']['apikey']
    assert obj.cfgparser['pmidcite']['tool'] == Cfg.dfltdct['pmidcite']['tool']

    system('rm {CFG}'.format(CFG=file_cfg))
    print('PASSED: cfg init private values are default')


if __name__ == '__main__':
    test_cfg_icite()
    test_cfg_eutils()
    test_cfg_desecriptive()
    test_cfg_example(len(argv) != 1)
