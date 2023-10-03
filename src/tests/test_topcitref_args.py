#!/usr/bin/env python3
"""Test paper label args: TOP CIT CLI REF and aliases ALL CITS"""

from pmidcite.icite.top_cit_ref import TopCitRef

__copyright__ = "Copyright (C) 2022-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"


ADJ = TopCitRef().adjust_args

def test_topcitref_args():
    """Test paper label args: TOP CIT CLI REF and aliases ALL CITS"""
    # pylint: disable=bad-whitespace

    #     Arguments               Expected paper labels
    #    ----------------------  -------------------------------
    _chk(0, set(),                  None)
    _chk(1, {'ALL',},               {'TOP', 'CIT', 'CLI', 'REF'})
    _chk(2, {'CITS',},              {'CIT', 'CLI'})
    _chk(3, {'TOP', 'CITS',},       {'TOP', 'CIT', 'CLI'})
    _chk(4, {'TOP', 'CITS', 'REF'}, {'TOP', 'CIT', 'CLI', 'REF'})
    _chk(5, {'TOP', 'MOCK', 'REF'}, {'TOP', 'REF'})


def _chk(num, args, exp):
    """Check that args produces correct paper label cites"""
    act = ADJ(args)
    assert act == exp, f'TEST {num} ACT({act}) != EXP({exp}) WITH ARGS({args})'
    print(f'**PASSED TEST {num:2}: ARGS({args}) ADJUSTED TO {exp}')


if __name__ == '__main__':
    test_topcitref_args()

# Copyright (C) 2022-present, DV Klopfenstein, PhD. All rights reserved.
