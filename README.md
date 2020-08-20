# [PubMed](https://pubmed.ncbi.nlm.nih.gov) ID (PMID) Cite
Augment your PubMed literature search 
from the command-line by linking
citation data from [**NIH's iCite**](https://icite.od.nih.gov)
with [**PubMed**](https://pubmed.ncbi.nlm.nih.gov) IDs (PMIDs),
rather than clicking and clicking and clicking on
[**Google Scholar**](https://twitter.com/CT_Bergstrom/status/1170465764832231427)'s
*Cited by N* links.

* [**_pmidcite_ Setup**](#setup)
* [**_pmidcite_ Documentation**](???)
* Take a [quick tour](https://www.nlm.nih.gov/pubs/techbull/ma20/brief/ma20_pubmed_essentials.html) of [PubMed](https://pubmed.ncbi.nlm.nih.gov) 


## To Cite

_If you use **pmidcite** in your literature search, please cite the following peer-reviewd Letter-to-the-Editor:

Klopfenstein DV and Dampier W [Commentary to Gusenbauer 2020: Evaluating Retrieval Qualitiesof 28 search tools](???)
_Research Synthesis Methods_ | 2020 | [DOI: 10.1038/??????????????????](???)

_and please cite the paper announcing NIH's iCite citation data_:

Hutchins B ... Santangelo G [The NIH Open Citation Collection: A public access, broad coverage resource](https://pubmed.ncbi.nlm.nih.gov/31600197/)    
_PLoS Biology_ | 2019 | [DOI: 10.1371/journal.pbio.3000385](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000385)    

_Please consider reading and citing the paper which inspired the creation of **pmidcite**_:

Gusenbauer M and Haddaway N [Which Academic Search Systems are Suitable for Systematic Reviews or Meta-Analyses? Evaluating Retrieval Qualities of Google Scholar, PubMed and 26 other Resources](https://pubmed.ncbi.nlm.nih.gov/31614060/)    
_Research Synthesis Methods_ | 2019 | [DOI:10.1002/jrsm.1378](https://onlinelibrary.wiley.com/doi/full/10.1002/jrsm.1378)



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
