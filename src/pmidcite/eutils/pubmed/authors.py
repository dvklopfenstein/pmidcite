"""Hold list of Authors."""

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2019-present DV Klopfenstein. All rights reserved."

from pmidcite.eutils.pubmed.author import Author


class Authors(object):
  """Hold list of Authors."""

  flds = ['FAU', 'AU', 'AD']

  def __init__(self):
    self.authors = []
    self.ads = []  # Affiliations for the entire paper

  def get_match(self, mtch_fnc):
    """Find author which matches the search."""
    mtch_idxs = []
    for idx, auobj in enumerate(self.authors):
      if mtch_fnc(auobj):
        mtch_idxs.append(idx)
    return mtch_idxs
    #   auobj = pub['Authors'].get_au_order_desc(au_str)
    #   if au_str == aus[0]:
    #     desc2pub['1st'].append(pub)
    #   elif au_str == aus[-1]:
    #     desc2pub['Last'].append(pub)
    #   else:
    #     desc2pub['mid'].append(pub)

  def add_fld(self, fld, line, pmid):
    """Add an Author or add to the last Author."""
    if fld == 'FAU':  # 'Full Author Name' begins a new Author
      self.authors.append(Author(line))
      return
    # Author affiliation is for all authors on the paper
    if fld == 'AD' and not self.authors:
      self.ads.append(line)
      return
    assert self.authors, "{PMID} {F} {L}".format(PMID=pmid, F=fld, L=line)
    author = self.authors[-1]  # Get the last author
    if fld == 'AU':
      author.au = line
    elif fld == 'AD':
      author.ads.append(line)
    else:
      raise RuntimeError("UNEXPECTED Author FIELD({F})".format(F=fld))

  def __str__(self):
    return "\n".join([str(a) for a in self.authors])


# Copyright (C) 2019-present DV Klopfenstein.  All rights reserved.
