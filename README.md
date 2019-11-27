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
 * No bulk export for results
 * Results can only be exported into reference management software 20 at a time
 * Unknown size of database
 * [Google's Disclaimer](https://www.google.com/intl/en/scholar/about.html): Google does not warrant that the information is complete or accurate
 * Crawler-based search engines function differently than bibliographic databases which have a curated entries


### References

1. Gusenbauer, Michael and Haddaway, Neal R.    
   "Which Academic Search Systems are Suitable for Systematic Reviewsor Meta-Analyses? Evaluating Retrieval Qualities of Google Scholar, PubMed and 26 other Resources"    
    Research Synthesis Methods (2019)

2. Boeker, Martin et al.
   "Google Scholar as replacement for systematic literature searches: good relative recall and precision are not enough" 
   BMC Medical Research Methodology (2013)


Copyright (C) 2019-present, DV Klopfenstein. All rights reserved.
