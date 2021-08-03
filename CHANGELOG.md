# CHANGELOG

## Summary

* [**Unreleased**](#unreleased)
* [**Release 2021-08-03 v0.0.12**](#release-2021-08-03-v0012)
	Add new `icite` arguments, `-c` and `-r` for finer grain control for downloading NIH citation data
  [#3](https://github.com/dvklopfenstein/pmidcite/issues/3)
* [**Release 2021-07-12 v0.0.10**](#release-2021-07-12-v009)
  Updated notebooks to use new customizable paper grouping
  [#2]([#3](https://github.com/dvklopfenstein/pmidcite/issues/2)
* [**Release 2021-07-06 v0.0.8**](#release-2021-07-06-v008)
  Made grouping of paper's customizable
* [**Release 2020-12-03 v0.0.5**](#release-2020-12-03-v005)
  * The 1st citation count in icite line contains any clinical citations
* [**Release 2020-12-02 v0.0.4**](#release-2020-12-02-v004)
  * Added to Documentation in README
  * Added convenience get functions

## Details

### Unreleased

### Release 2021-08-03 v0.0.12
* NIH citation data is now downloaded for only researcher-specified PMIDs by default. [#3](https://github.com/dvklopfenstein/pmidcite/issues/3)
* To download NIH citation details for citations/references of a researcher-specified PMID, use the icite arguments:
  * -v (download NIH citation details for both citations and references of a researcher-specified PMID)
  * -c (download NIH citation details for the citations of a researcher-specified PMID)
  * -r (download NIH citation details for the references of a researcher-specified PMID)

### Release 2021-07-13 v0.0.10
* Add script, icite (like icite.py)

### Release 2021-07-12 v0.0.9
* Updated all notebooks to use the new customizable paper grouping using the NIH's co-citation network data [#2]([#3](https://github.com/dvklopfenstein/pmidcite/issues/2)

### Release 2021-07-16 v0.0.8
* Made grouping of papers customizable by the researcher
* Added image showing how to read the output of icite
![Starting usage](doc/images/pmidcite0.png)

### Release 2020-12-03 v0.0.5
* The 1st citation count in icite line contains any clinical citations

### Release 2020-12-02 v0.0.4
* Improved documentation in README
* Added notes about an external pmid2cite Web application
* Minor code improvements: Added get functions for researchers using pmidcite as a library


Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
