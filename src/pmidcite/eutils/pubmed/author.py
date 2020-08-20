"""Author object."""

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2019-present DV Klopfenstein. All rights reserved."


class Author(object):
  """Hold list of Authors."""

  # pylint: disable=invalid-name
  def __init__(self, full_author_name):
    self.fau = full_author_name
    self.au = None
    self.ads = []

  def __str__(self):
    lst = ["\nFAU: {AU}".format(AU=self.fau), "AU:  {AU}".format(AU=self.au)]
    for affil in self.ads:
      lst.append("AD:  {AD}".format(AD=affil))
    return "\n".join(lst)


# Copyright (C) 2019-present DV Klopfenstein.  All rights reserved.
