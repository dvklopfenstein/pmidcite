# [PubMed](https://pubmed.ncbi.nlm.nih.gov) ID (PMID) Cite
Augment your literature search 
from the command-line to link 
citation data from [**NIH's iCite**](https://icite.od.nih.gov)
with [**PubMed**](https://pubmed.ncbi.nlm.nih.gov) IDs (PMIDs),
rather than clicking and clicking and clicking on
[**Google Scholar**](https://twitter.com/CT_Bergstrom/status/1170465764832231427)'s
*Cited by N* links.

* [**Setup**](#setup)

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


## Setup
Store your literature search in a GitHub repo.

### 1. Add a pmidcite init file
Add a .pmidciterc init file to a non-git managed directory, like home (~)
```
$ icite --generate-rcfile | tee ~/.pmidciterc
[pmidcite]
email = name@email.edu
apikey = long_hex_digit
tool = scripts
dir_icite_py = .
dir_pubmed_txt = .
dir_pmids = .
dir_icite = .
```

```
$ export PMIDCITECONF=~/.pmidciterc
```
You will want .pmidciterc to not be managed by GitHub because it
will contain your personal email and your own NCBI API key.

### 2. Add directories
Add directories which match those in ~/.pmidciterc:
```
$ mkdir [GIT_REPO_PATH]/icite
$ mkdir [GIT_REPO_PATH]/log
$ mkdir [GIT_REPO_PATH]/log/pubmed
$ mkdir [GIT_REPO_PATH]/log/pmids
$ mkdir [GIT_REPO_PATH]/log/icite
```

### 3. NCBI E-Utils API key
If you want to download PubMed abstracts and PubMed search results using NCBI's E-Utils,
get an NCBI API key by following instructions here:    
https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities

Set the `apikey` value in the config file: `~/.pmidciterc`



Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
