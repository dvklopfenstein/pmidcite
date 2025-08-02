"""Utilities"""

import os.path as op

REPO = op.normpath(op.join(op.dirname(__file__), ".."))

def get_filename(fname):
    """Get absolute filename given a relative filename"""
    return op.join(REPO, fname)
