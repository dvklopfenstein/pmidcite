# [PubMed](https://pubmed.ncbi.nlm.nih.gov) ID (PMID) Cite
Augment your literature search 
from the command-line to link 
citation data from [**NIH's iCite**](https://icite.od.nih.gov)
and [**PubMed**](https://pubmed.ncbi.nlm.nih.gov) IDs (PMIDs),
rather than clicking and clicking on
[**Google Scholar**](https://twitter.com/CT_Bergstrom/status/1170465764832231427)'s
*Cited by N* links.

## Examples
* [Examine one paper's citations and references]()
* [Examine iCite results on PMIDs returned from a PubMed Query]()

### Examine one paper's citations and references.
`icite 32260091 | sort -k1,1 -k6`

### Examine iCite results on PMIDs returned from a PubMed Query
#### Script contents
src/bin/dnld_pmids.py
#### Run script
src/bin/dnld_pmids.py
#### Examine iCite results on PMIDs returned from a PubMed Query
grep -w TOP ./log/icite/protfnc_antibodies.txt | sort -k6

## Take a [quick tour](https://www.nlm.nih.gov/pubs/techbull/ma20/brief/ma20_pubmed_essentials.html) of [PubMed](https://pubmed.ncbi.nlm.nih.gov) 


Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
