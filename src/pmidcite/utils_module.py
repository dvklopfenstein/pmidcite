"""Module helper"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import pkgutil
import importlib
import importlib.util


def import_var(modulestr, varname, log=sys.stdout, rpterr=True):
    """Return variable inside module."""
    mod = import_mod(modulestr, log)
    if mod is not None:
        var = getattr(mod, varname, None)
        if var is not None:
            return var
    if rpterr:
        _rpt_err(mod, varname, modulestr)
    return None

def _rpt_err(mod, varname, modulestr):
    if mod is None:
        raise Exception("MODULE({M}) NOT IMPORTED".format(M=modulestr))
    raise Exception("VAR({V}) NOT FOUND IN MOD({M})".format(V=varname, M=modulestr))

def import_mod(modulestr, log=None):
    """Import Python module"""
    if log is not None:
        log.write("  IMPORT {MOD}\n".format(MOD=modulestr))
    if pkgutil.find_loader(modulestr) is not None:
        return importlib.import_module(modulestr)
    if log is not None:
        log.write("  None   {MOD}\n".format(MOD=modulestr))
    return None

def load_modpy(fin_py):
    """Load NIH iCite information from Python modules"""
    try:
        spec = importlib.util.spec_from_file_location("module.name", fin_py)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except RuntimeError as inst:
        print('**ERROR: UNABLE TO READ: {PY}\nMSG: {M}'.format(PY=fin_py, M=str(inst)))
        return None


# Copyright (C) 2019-present DV Klopfensteinr,. All rights reserved.
