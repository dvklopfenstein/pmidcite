"""Manage MeSH descriptors or qualifiers stored in Python modules."""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx
from pmidcite.eutils.pubmed.descriptors import UI2NT
from pmidcite.eutils.pubmed.qualifiers import NTS as nts_mesh_qual

class MeshTerms(object):
  """Manage MeSH descriptors or qualifiers stored in Python modules."""

  def __init__(self):
    # nt: MH MN UI;    Ex 'Abdomen', set(['A01.923.047']), 'D000005'
    self.mh2nt = {nt.MH:nt for nt in UI2NT.values()}
    # nt: SH QA QE MS; Ex 'agonists', 'AG', 'AGON', 'Used with ...
    self.sh2nt = {nt.SH:nt for nt in nts_mesh_qual}
    assert len(self.mh2nt) == len(UI2NT)
    assert len(self.sh2nt) == len(nts_mesh_qual)

  def mrg_starred_mesh(self, mhphrase2cnt): # phrase_list):
    """ *genetics & genetics -> *genetics."""
    phrase_new = cx.Counter()
    # Find all starred phrases. Remove '*' before storing.
    starred = set([w for w in mhphrase2cnt.keys() if w[:1] == '*'])
    for mesh_phrase, cnt in mhphrase2cnt.items():
      star, bare_phrase = self.get_star_phrase(mesh_phrase)
      if bare_phrase in starred:
        phrase_new["".join(["*", bare_phrase])] += cnt
      else:
        phrase_new[bare_phrase] += cnt
    return phrase_new 

  def get_star_phrase(self, phrase):
    """Return Corrected MeSH term."""
    return ['', phrase] if phrase[0]!='*' else ['*', phrase[1:]]

  def get_descqual2ctr(self, mh_vals):
    """Given MH raw strings, check strings include either MeSH descriptors or qualifiers."""
    # VAL Antineoplastic Agents, Phytogenic/administration & dosage
    # VAL Apoptosis/*drug effects
    mhtype2ctr = {'desc':cx.Counter(), 'qual':cx.Counter()}
    for mhline in mh_vals:
      for mhstr in mhline.split('/'):
        _, phrase = self.get_star_phrase(mhstr)
        is_mh = phrase in self.mh2nt
        is_sh = phrase in self.sh2nt
        if is_mh and not is_sh:
          mhtype2ctr['desc'][mhstr] += 1
        elif not is_mh and is_sh:
          mhtype2ctr['qual'][mhstr] += 1
        else:
          raise Exception("UNKNOWN VALUE({}) IN ({})".format(mhstr, mhline))
    return mhtype2ctr

  def chk_mhs(self, mh_vals):
    """Given MH raw strings, check strings include either MeSH descriptors or qualifiers."""
    # VAL Antineoplastic Agents, Phytogenic/administration & dosage
    # VAL Apoptosis/*drug effects
    for mhline in mh_vals:
      for mhstr in mhline.split('/'):
        star, phrase = self.get_star_phrase(mhstr)
        is_mh = phrase in self.mh2nt
        is_sh = phrase in self.sh2nt
        # assert is_mh != is_sh, "UNKNOWN VALUE({})".format(mhstr)
        if is_mh == is_sh:
            sys.stdout.write("MeSH CHECK-UNKNOWN VALUE({})\n".format(mhstr))


# Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
