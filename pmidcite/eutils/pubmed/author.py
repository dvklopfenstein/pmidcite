"""Author object."""

__author__ = 'DV Klopfenstein, PhD'
__copyright__ = "Copyright (C) 2019-present DV Klopfenstein, PhD. All rights reserved."


class Author:
    """Hold list of Authors."""

    def __init__(self, full_author_name, aut=None, ads=None):
        self.fau = full_author_name
        self.aut = aut
        self.ads = [] if ads is None else ads

    def __str__(self):
        lst = [f"\nFAU: {self.fau}", f"AU:  {self.aut}"]
        for affil in self.ads:
            lst.append(f"AD:  {affil}")
        return "\n".join(lst)

    def __eq__(self, lhs):
        return self.fau == lhs.fau and self.aut == lhs.aut and self.ads == lhs.ads


# Copyright (C) 2019-present DV Klopfenstein, PhD.  All rights reserved.
