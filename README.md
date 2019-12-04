# PMID Cite
Traverse [**NIH iCite**](https://icite.od.nih.gov/) citations and references and download 
[**PubMed**](https://pubmed.ncbi.nlm.nih.gov/) summaries from the command line.

## How about Google Search?
Google Scholar was found to be inappropriate as principal search system [1][2] for peer-reviewed research papers due to:
 * The same query can produce different results at different times
 * Poor boolean search interface:
    * Not documented
    * A space ' ' is used to represent the logical AND
    * Nesting of subexpressions limited to one level
    * No history function
    * No clear access to booleans using Google's search expression builder
 * Queries are truncated to 256 characters without warning
    * Which may result in an increased number of false positive results
 * There are a maximum of 1000 results:
   * Displayed in steps of 20 per page.
   * Undocumented sort of full results, when not sorted by date
 * Unknown size of database
 * Crawler-based search engines function differently than bibliographic databases which have a curated entries


### References

1. Gusenbauer, Michael and Haddaway, Neal R.    
   "Which Academic Search Systems are Suitable for Systematic Reviewsor Meta-Analyses? Evaluating Retrieval Qualities of Google Scholar, PubMed and 26 other Resources"    
    Research Synthesis Methods (2019)

2. Boeker, Martin et al.
   "Google Scholar as replacement for systematic literature searches: good relative recall and precision are not enough" 
   BMC Medical Research Methodology (2013)

## Links to other PubMed tools

* [PubMed parser](https://github.com/titipata/pubmed_parser)
* [pymed](https://github.com/gijswobben/pymed)    
* [paper2remarkable](https://github.com/GjjvdBurg/paper2remarkable)
* [pubmed-lookup](https://github.com/mfcovington/pubmed-lookup)

Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
