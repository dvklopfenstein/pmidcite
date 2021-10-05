# [**PubMed**](https://pubmed.ncbi.nlm.nih.gov) **ID (PMID) Cite**

[![build](https://github.com/dvklopfenstein/pmidcite/actions/workflows/build.yml/badge.svg)](https://github.com/dvklopfenstein/pmidcite/actions/workflows/build.yml)
[![CodeQL](https://github.com/dvklopfenstein/pmidcite/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/dvklopfenstein/pmidcite/actions/workflows/codeql-analysis.yml)
[![Latest PyPI version](https://img.shields.io/pypi/v/pmidcite.svg)](https://pypi.org/project/pmidcite/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5172712.svg)](https://doi.org/10.5281/zenodo.5172712)

Augment a PubMed literature search by linking 
citation data from [**NIH's Open Citation Collection (NIH-OCC)**](https://icite.od.nih.gov)
for researcher-specified [**PubMed**](https://pubmed.ncbi.nlm.nih.gov) IDs (PMIDs)
using the command line.

#### This open-source project accompanies the *Research Synthesis Methods* paper:    
[**Commentary to Gusenbauer and Haddaway 2020: Evaluating Retrieval Qualities of PubMed and Google Scholar**](http://dx.doi.org/10.1002/jrsm.1456)    
Klopfenstein DV and Dampier W    
2020 | _Research Synthesis Methods_ | PMID: [33031632](https://pubmed.ncbi.nlm.nih.gov/33031632/) | DOI: [10.1002/jrsm.1456](http://dx.doi.org/10.1002/jrsm.1456) | [pdf](/doc/paper/JRSM_1456_iCite_main.pdf)    
dvklopfenstein@protonmail.com    

## Usage
* [**Download citation data for a research paper**](https://github.com/dvklopfenstein/pmidcite#download-citation-data-for-a-research-paper)
* [**Forward citation search**](https://github.com/dvklopfenstein/pmidcite#forward-citation-search)    
  AKA following a paper's *Cited by* links or *Forward snowballing*
* [**Backward citation search**](https://github.com/dvklopfenstein/pmidcite#backward-citation-search)    
  AKA following the links to a paper's references or *Backward snowballing*

## Download citation data for a research paper
```$ icite -H 26032263```    
* This paper (PMID 26032263) has `25` citations and `10` references.    
* This paper is performing well (`74`th percentile) compared to its peer papers.    
![Starting usage](images/pmidcite0.png)
The NIH percentile (`%`) is NIH's ranking of a paper among its [co-citation group](https://icite.od.nih.gov/user_guide?page_id=ug_overview).

The NIH percentile (`G`) grouping is part of this project and helps to
highlight the better performing papers in groups `2`, `3`, and `4` by
placing them at the front of a sorted list and the
lower performing papers in groups `0` or `1` at the back.

New papers appear at the beginning of a sorted list,
no matter how many citations they have to
better facilitate researchers in finding the latest discoveries.

## Forward citation search
Also known as following a paper's *Cited by* links or *Forward snowballing*    

```icite -H; icite 26032263 --load_citations | sort -k6 -r```    
or    
```icite -H; icite 26032263 -c | sort -k6 -r```    

## Backward citation search
Also known as following links to a paper's references or *Backward snowballing*    

```$ icite -H; icite 26032263 --load_references | sort -k6 -r```    
or    
```$ icite -H; icite 26032263 -r | sort -k6 -r```     


## Usage details

### Download citations for all papers returned from a PubMed search
Make a copy of `src/bin/dnld_pmids.py` and add your PubMed search to the end of the `queries` list.

There are two PubMed searches in this example:
  * `systematic review AND "how to"[TI]`
  * `Orcinus Orca Type D`

The PubMed search results are saved to specified filenames such as `systematic_review.txt` to be grepped and sorted.
```
def main():
    """Download PMIDs returned for a PubMed query. Write an iCite report for each PMID"""
    queries = [
        # Output filenames               PubMed query
        # -----------------              -----------------------------------
        ('systematic_review.txt',        'systematic review AND "how to"[TI]'),
        ('rarely_seen_killer_whale.txt', 'Orcinus Orca Type D'),
    ]

    obj = PubMedQueryToICite(force_dnld=True)
    dnld_idx = obj.get_index(sys.argv)
    obj.run(queries, dnld_idx)
```

To have better access to PubMed search results, 
get n NCBI API key using these instuctions:    
https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities


## PubMed vs Google Scholar
<p align="center">
<img src="images/Search_Features_GS_v_PubMed.png" alt="Google Scholar vs PubMed" width="600"/>
</p>

In 2013, Boeker et al. recommended that a scientific search interface contain five integrated search criteria. 
PubMed implements all five, while Google did not in 2013 or today.

Google's highly popular implementation of the forward citation search through their ubiquitous "Cited by N" links
is a "Better" experience than the PubMed's "forward citation search" implementation.

But if your research is in the health sciences and
you are amenable to consider working from the [command line](#command-line-interface-cli),
you can use PubMed in your browser plus
citation data downloaded from the NIH using the command-line  using *pmidcite*.
The NIH's citation data includes a paper's ranking among its co-citation network.


## What is in [**PubMed**](https://pubmed.ncbi.nlm.nih.gov)?  Take a [**quick tour**](https://www.nlm.nih.gov/pubs/techbull/ma20/brief/ma20_pubmed_essentials.html)
<img src="images/pubmed_content_2020_01_10.png" alt="PubMed Contents" width="850"/>

PubMed is a search interface and toolset used to access over 30.5 million article records from databases like:
* **MEDLINE**: a highly selective database started in the 1960s
* **PubMed Central (PMC)**: an open-access database for full-text papers that are free of cost
* Additional content like books and articles published before the 1960s


Copyright (C) 2019-present [pmidcite](https://dvklopfenstein.github.io/pmidcite/), DV Klopfenstein. All rights reserved.

<!--
  Title: PubMed ID (PMID) Cite
  Description: Augment your PubMed literature search with forward/backward citation chaining (snowballing) using NIH citation data
  Author: dvklopfenstein
  -->
<meta name='keywords' content='citation count, CitedBy, PubMed, PMID, forward citation, backward citation, forward snowball, backward snowball, literature review, citation downloader'>
