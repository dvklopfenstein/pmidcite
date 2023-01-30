# PubMed ID (PMID) Cite

[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Python%20library%20to%20download%20pubmed%20citation%20counts%20and%20data,%20given%20a%20PMID&url=https://github.com/dvklopfenstein/pmidcite&via=dvklopfenstein&hashtags=pubmed,pmid,citations,pubmed2cite,writingtips,scientificwriting)
[![build](https://github.com/dvklopfenstein/pmidcite/actions/workflows/build.yml/badge.svg)](https://github.com/dvklopfenstein/pmidcite/actions/workflows/build.yml)
[![CodeQL](https://github.com/dvklopfenstein/pmidcite/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/dvklopfenstein/pmidcite/actions/workflows/codeql-analysis.yml)
[![Latest PyPI version](https://img.shields.io/pypi/v/pmidcite.svg)](https://pypi.org/project/pmidcite/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5172712.svg)](https://doi.org/10.5281/zenodo.5172712)

<p align="center"><img src="https://github.com/dvklopfenstein/pmidcite/raw/main/docs/images/pmidcite_citedby.png" alt="pmidcite summary" width="500"/></p>

Turbocharge a [**PubMed**](https://pubmed.ncbi.nlm.nih.gov) literature search in biomedicine, biochemistry, chemistry, behavioral science, and other life sciences by linking [**citation data**](https://icite.od.nih.gov) from the [**National Institutes of Health (NIH)**](https://www.nih.gov/) with [**PubMed**](https://pubmed.ncbi.nlm.nih.gov) IDs (PMIDs) using the command line rather than clicking and clicking and clicking on [**Google Scholar**](/doc/images/README_twitter.md) "*Cited by N*" links.

This open-source project is part of [**a peer-reviewed**](https://pubmed.ncbi.nlm.nih.gov/33031632) [**paper**](https://onlinelibrary.wiley.com/doi/10.1002/jrsm.1456) published in [***Research Synthesis Methods***](https://onlinelibrary.wiley.com/journal/17592887).
Please [**cite**](#how-to-cite) if you use *pmidcite* in your research or literature search.    

Contact: dvklopfenstein@protonmail.com     


# Table of Contents
* ***Quickstart on the*** [***command line***](https://github.com/dvklopfenstein/pmidcite/blob/main/README.md#command-line-interface-cli)
  * [**1) Download citation counts and data for a research paper**](https://github.com/dvklopfenstein/pmidcite#1-download-citation-counts-and-data-for-a-research-paper)
  * [**2) Forward citation search**](https://github.com/dvklopfenstein/pmidcite#2-forward-citation-search): following a paper's *Cited by* links or *Forward snowballing*
  * [**3) Backward citation search**](https://github.com/dvklopfenstein/pmidcite#3-backward-citation-search): following the links to a paper's references or *Backward snowballing*
  * [**4) Summarize a group of citations**](https://github.com/dvklopfenstein/pmidcite#4-summarize-a-group-of-citations)
  * [**5) Search PubMed from the command line**](https://github.com/dvklopfenstein/pmidcite/blob/main/README.md#5-download-citations-for-all-papers-returned-from-a-pubmed-search)
* ***Examples in Jupyter notebooks using the *pmidcite* Python library***
  * [**1) Download NIH-OCC citation data**](https://github.com/dvklopfenstein/pmidcite/blob/main/notebooks/NIHOCC_data_download_always.ipynb)
  * [**2) Download missing or load existing NIH-OCC citation data**](https://github.com/dvklopfenstein/pmidcite/blob/main/notebooks/NIHOCC_data_download_or_import.ipynb)
  * [**3) Print a paper's citation and reference data**](https://github.com/dvklopfenstein/pmidcite/blob/main/notebooks/print_paper_all_refs_cites.ipynb)
  * [**4) Sort NIH iCite entries**](https://github.com/dvklopfenstein/pmidcite/blob/main/notebooks/print_paper_sort_cites.ipynb)
  * [**5) Query PubMed**](https://github.com/dvklopfenstein/pmidcite/blob/main/notebooks/query_pubmed.ipynb)
* ***Installation & citation***:
  * [**Installation**](#installation)
  * [**Setup**](#setup)
  * [**Google Scholar vs. PubMed**](https://github.com/dvklopfenstein/pmidcite/blob/main/README.md#pubmed-vs-google-scholar)
    * [**What is in PubMed?**](https://github.com/dvklopfenstein/pmidcite/blob/main/README.md#what-is-in-pubmed--take-a-quick-tour)
  * [**How to Cite *pmidcite***](#how-to-cite)
  * [**Contributing**](#contributing
* [***References***](#references)

## 1) Download citation counts and data for a research paper
```$ icite -H 26032263```    
* This paper (PMID 26032263) has `25` citations, `10` references, and `4` authors.    
* This paper is performing well (`74`th percentile in column `%`) compared to its [peers](https://icite.od.nih.gov/user_guide?page_id=ug_overview).    
    
![Starting usage](https://github.com/dvklopfenstein/pmidcite/raw/main/docs/images/pmidcite0.png)
### NIH percentile
This paper is performing well (`74`th percentile) compared to its [peers](https://icite.od.nih.gov/user_guide?page_id=ug_overview) (column `%`).     

The NIH percentile grouping (column `G`) helps to
highlight the better performing papers in groups `2`, `3`, and `4` by
sorting the citing papers by group first, then publication year.

The sort places the lower performing papers in groups `0` or `1` at the back.

New papers appear at the beginning of a sorted list,
no matter how many citations they have to
better facilitate researchers in finding the latest discoveries.

The grouping of papers by NIH percentile grouping is a novel feature created by [dvklopfenstein](https://github.com/dvklopfenstein) for this project.

## 2) Forward citation search
<p align="left"><img src="https://github.com/dvklopfenstein/pmidcite/raw/main/docs/images/pmidcite_citedby_cit.png" alt="pmidcite summary" width="300"/></p>

Also known as following a paper's *Cited by* links or *Forward snowballing*    

```icite -H; icite 26032263 --load_citations | sort -k6 -r```    
or    
```icite -H; icite 26032263 -c | sort -k6 -r```    


## 3) Backward citation search
Also known as following links to a paper's references or *Backward snowballing*    
<p align="left"><img src="https://github.com/dvklopfenstein/pmidcite/raw/main/docs/images/pmidcite_citedby_ref.png" alt="pmidcite summary" width="300"/></p>

```$ icite -H; icite 26032263 --load_references | sort -k6 -r```    
or    
```$ icite -H; icite 26032263 -r | sort -k6 -r```     

## 4) Summarize a group of citations
* 4a) Examine a paper with PMID `30022098`. Print the column headers(`-H`):   
`icite -H 30022098`
* 4b) Download the details about each paper(`-c`) that cites `30022098` into a file(`-o goatools_cites.txt`):    
`icite 30022098 -c -o goatools_cites.txt`
* 4c) Summarize the overall performace of the 300+ citing papers contained in `goatools_cites.txt`    
`summarize_papers goatools_cites.txt -p TOP CIT CLI`

### 4a) Examine a paper with PMID `30022098`. Print the column headers(`-H`):
```
$ icite -H 30022098
COL 2        3  4       5 6 7        8  9  10 au[11](authors)
TYP PMID     RP HAMCc   % G YEAR   cit cli ref au[00](authors) title
TOP 30022098 R. .A..c 100 4 2018   318  1  23 au[14](D V Klopfenstein) GOATOOLS: A Python library for Gene Ontology analyses.
```

Paper with PMID `30022098` is cited by `318`(`cit`) other research papers and `1`(`cli`) clinical study. It has `23` references(`ref`).    

### 4b) Download the details about each paper(`-c`) that cites `30022098` into a file(`-o goatools_cites.txt`):
```
$ icite 30022098 -c -o goatools_cites.txt
```

The requested paper (PMID=`30022098`) is described in one one line in `goatools_cites.txt`:
```
$ grep TOP goatools_cites.txt
TOP 30022098 R. .A..c 100 4 2018   318  1  23 au[14](D V Klopfenstein) GOATOOLS: A Python library for Gene Ontology analyses.
```

The paper (PMID=`30022098`) is cited by 381(`CIT`) research papers plus 1(`CLI`) clinical study:
```
$ grep CIT goatools_cites.txt | wc -l
318

$ grep CLI goatools_cites.txt | wc -l
1
```

### 4c) Summarize all the papers in `goatools_cites.txt`
**NEW FUNCTIONALITY; INPUT REQUESTED: What would you like to see?** [Open an issue](https://github.com/dvklopfenstein/pmidcite/issues) to comment.   
```
$ summarize_papers goatools_cites.txt -p TOP CIT CLI
i=033.4% 4=003.4% 3=020.9% 2=021.9% 1=015.9% 0=004.4%   4 years:2018-2022   320 papers goatools_cites.txt
```

* Output is on one line so many files containing sets of PMIDs may be compared. TBD: Add multiline verbose option.
* The groups are from newest(`i`) to top-performing(`4`), great(`3`), very good(`2`), and overlooked(`1` and `0`)
* The percentages of papers in `goatools_citations.txt` in each group follow the group name


## 5) Download citations for all papers returned from a PubMed search
1. [Do a search in PubMed](#1-do-a-search-in-pubmed)
2. [Save all results into a file containing all PMIDs found by the search](#2-save-all-results-into-a-list-of-pmids)
3. [Download the list of PMIDs](#3-download-the-list-of-pmids)
4. [Run icite to analyze all the PMIDs](#4-run-icite-to-analyze-all-the-pmids)

### 1. Do a search in [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
<p align="center"><img src="https://github.com/dvklopfenstein/pmidcite/raw/main/doc/images/pubmed_HIV_AND_Me_srch.png" alt="pmidcite summary" width="800"/></p>   

### 2. Save all results into a list of PMIDs
<p align="center"><img src="https://github.com/dvklopfenstein/pmidcite/raw/main/doc/images/pubmed_HIV_AND_Me_save.png" alt="pmidcite summary" width="800"/></p>   

### 3. Download the list of PMIDs
<p align="center"><img src="https://github.com/dvklopfenstein/pmidcite/raw/main/doc/images/pubmed_HIV_AND_Me_dnld.png" alt="pmidcite summary" width="800"/></p>   

### 4. Run icite to analyze all the PMIDs
```
$ icite -i pmid-HIVANDDNAm-set.txt -o pmid-HIVANDDNAm-icite.txt
$ grep TOP pmid-HIVANDDNAm-icite.txt | sort -k6
```


## Command Line Interface (CLI)

A Command-Line Interface (CLI) can be preferable 
to a Graphical User Interface (GUI) because: 
* processing can be automated from a script
* time-consuming mouse clicking is reduced
* more data can be seen at once on a text screen
than in a browser, giving the researcher 
a better overall impression of the full set of information [[1]](#how-to-cite)

Researchers who use Linux or Mac already work from the command line.
Researchers who use Windows can get that Linux-like command line feeling
while still running native Windows programs by
downloading Cygwin from https://www.cygwin.com/ [[1]](#how-to-cite).


# PubMed vs Google Scholar
<p align="center">
<img src="https://github.com/dvklopfenstein/pmidcite/raw/main/docs/images/Search_Features_GS_v_PubMed.png" alt="Google Scholar vs PubMed" width="600"/>
</p>

In 2013, Boeker et al. [[6](#references)]
recommended that a scientific search interface contain five integrated search criteria. 
PubMed implements all five, while Google did not in 2013 or today.

Google's highly popular implementation of the forward citation search through their ubiquitous "Cited by N" links
is a "Better" experience than the PubMed's "forward citation search" implementation.

But if your research is in the health sciences and
you are amenable to working from the [command line](#command-line-interface-cli),
you can use PubMed in your browser plus
citation data downloaded from the NIH using the command-line  using *pmidcite*.
The NIH's citation data includes a paper's ranking among its co-citation network.


## What is in [PubMed](https://pubmed.ncbi.nlm.nih.gov)?  Take a [**quick tour**](https://www.nlm.nih.gov/pubs/techbull/ma20/brief/ma20_pubmed_essentials.html)
<img src="https://github.com/dvklopfenstein/pmidcite/raw/main/docs/images/pubmed_content_2020_01_10.png" alt="PubMed Contents" width="850"/>

PubMed is a search interface and toolset used to access over 30.5 million article records from databases such as:
* **MEDLINE**: a highly selective database started in the 1960s
* **PubMed Central (PMC)**: an open-access database for full-text papers that are free of cost
* Additional content such as books and articles published before the 1960s


## Installation
To install from [**PyPI**](https://pypi.org/project/pmidcite/)    
```$ pip3 install pmidcite```

To install locally
```
$ git clone https://github.com/dvklopfenstein/pmidcite.git
$ cd ./pmidcite
$ pip3 install .
```

## Setup
Save your literature search in a GitHub repo.

### 1. Add a [pmidcite init file](doc/example_cfg/.pmidciterc)
Add a .pmidciterc init file to a non-git managed directory, such as home (~)
```
$ icite --generate-rcfile | tee ~/.pmidciterc
[pmidcite]
email = myname@email.edu
# To download PubMed search results, get an NCBI API key here:
# https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities
apikey = MY_LONG_HEX_NCBI_API_KEY
tool = my_scripts
```
```
$ export PMIDCITECONF=~/.pmidciterc
```
Do not version manage the `.pmidciterc` using a tool such as GitHub because it
contains your personal email and your private NCBI API key.


### 2. NCBI E-Utils API key
To download PubMed abstracts and PubMed search results using NCBI's E-Utils,
get an NCBI API key using these instructions:    
https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities

Set the `apikey` value in the config file: `~/.pmidciterc`

# Contributing
See the [**contributing guide**](/docs/CONTRIBUTING.md) for detailed instructions on how to get started contributing to the **pmidcite** project.

# Contact
email: dvklopfenstein@protonmail.com    
https://orcid.org/0000-0003-0161-7603

## How to Cite
_If you use **pmidcite** in your research or literature search, please cite paper 1 (pmidcite) and paper 3 (NIH citation data)._      

_Please also consider reading and citing Gusenbauer's response (paper 2) about improving search for all during the information avalanche of these times:_

1. **The *pmidcite* paper:**    
[**Commentary to Gusenbauer and Haddaway 2020: Evaluating Retrieval Qualities of PubMed and Google Scholar**](http://dx.doi.org/10.1002/jrsm.1456)    
Klopfenstein DV and Dampier W    
2020 | _Research Synthesis Methods_ | PMID: [33031632](https://pubmed.ncbi.nlm.nih.gov/33031632/) | DOI: [10.1002/jrsm.1456](http://dx.doi.org/10.1002/jrsm.1456) | [pdf](/doc/paper/JRSM_1456_iCite_main.pdf)

2. **Gusenbauer's response to the *pmidcite* paper:**    
[**What every Researcher should know about Searching – Clarified Concepts, Search Advice, and an Agenda to improve Finding in Academia**](https://onlinelibrary.wiley.com/doi/10.1002/jrsm.1457)    
Gusenbauer M and Haddaway N    
2020 | _Research Synthesis Methods_ | PMID: [33031639](https://pubmed.ncbi.nlm.nih.gov/33031639/) | DOI: [10.1002/jrsm.1457](https://onlinelibrary.wiley.com/doi/10.1002/jrsm.1457) | [pdf](/doc/paper/jrsm.1457.pdf)

3. **The NIH citation data used by *pmidcite* -- Scientific Influence, Translation, and Citation counts:**     
[**The NIH Open Citation Collection: A public access, broad coverage resource**](https://pubmed.ncbi.nlm.nih.gov/31600197/)    
Hutchins BI ... Santangelo GM    
2019 | _PLoS Biology_ | PMID: [31600197](https://pubmed.ncbi.nlm.nih.gov/31600197) | DOI: [10.1371/journal.pbio.3000385](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000385)    

## References

_Please consider reading and citing the paper [4] which inspired the creation of **pmidcite** [1] and the authors' response to our paper [2]_:

4. [**Which Academic Search Systems are Suitable for Systematic Reviews or Meta-Analyses? Evaluating Retrieval Qualities of Google Scholar, PubMed and 26 other Resources**](https://pubmed.ncbi.nlm.nih.gov/31614060/)    
Gusenbauer M and Haddaway N    
2019 | _Research Synthesis Methods_ | PMID: [31614060](https://pubmed.ncbi.nlm.nih.gov/31614060) | DOI: [10.1002/jrsm.1378](https://onlinelibrary.wiley.com/doi/full/10.1002/jrsm.1378)

_Mentioned in this README are also these outstanding contributions_:

5. [**Relative Citation Ratio (RCR): A New Metric That Uses Citation Rates to Measure Influence at the Article Level**](https://pubmed.ncbi.nlm.nih.gov/27599104/)    
Hutchins BI, Xin Yuan, Anderson JM, and Santangelo, George M.    
2016 | _PLoS Biology_ | PMID: [27599104](https://pubmed.ncbi.nlm.nih.gov/27599104) | DOI: [10.1371/journal.pbio.1002541](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1002541)

6. [**Google Scholar as replacement for systematic literature searches: good relative recall and precision are not enough**](https://pubmed.ncbi.nlm.nih.gov/24160679/)    
Boeker M et al.    
2013 | BMC Medical Research Methodology | PMID: [24160679](https://pubmed.ncbi.nlm.nih.gov/24160679) | DOI: [10.1186/1471-2288-13-131](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-131)

7. [**Best Match: New relevance search for PubMed**](https://pubmed.ncbi.nlm.nih.gov/30153250/)    
Fiorini N ... Lu Zhiyong    
2018 | PLoS Biology | PMID: [30153250](https://pubmed.ncbi.nlm.nih.gov/30153250) | DOI: [10.1371/journal.pbio.2005343](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.2005343)    

## [PDFs](/doc/paper/JRSM_1456_iCite_main.pdf)
  * [**PMIDCITE Manuscript**](/doc/paper/JRSM_1456_iCite_main.pdf) with the original text box formatting
    * **Supplemental Material**
      * [S1. *pmidcite* information](/doc/paper/JRSM_1456_iCite_supp1_CitedByN.pdf)
      * [S2. Contents of PubMed](/doc/paper/JRSM_1456_iCite_supp2_PMcontents.pdf)
      * [S3. Screen shots Google Scholar taken Jan 2020](/doc/paper/JRSM_1456_iCite_supp3_GS.pdf)
  * [**Gusenbauer's Response**](/doc/paper/jrsm.1457.pdf)

## Contact
dvklopfenstein@protonmail.com    
https://orcid.org/0000-0003-0161-7603

Copyright (C) 2019-present [pmidcite](https://dvklopfenstein.github.io/pmidcite/), DV Klopfenstein, PhD. All rights reserved.
