---
title: 'pmidcite: get citations for a PubMed paper from the command line'
tags:
  - pubmed
  - command-line-tool
  - citation-downloader
  - citation
  - literature-review
  - systematic-review
  - google-scholar
authors:
  - name: DV Klopfenstein
    orcid: 0000-0003-0161-7603
    corresponding: true
    affiliation: "1"
affiliations:
  - name: Department of Microbiology and Immunology, Drexel University College of Medicine, Philadelphia, PA, United States
    index: 1
date:  5 January 2026
bibliography: paper.bib
repository: https://github.com/dvklopfenstein/pmidcite
archive_doi: 10.5281/zenodo.5172713
---
<!-- https://github.com/openjournals/joss-reviews -->

# Summary
<!-- Viewing citation counts for a paper is a common task when performing a literature search. -->
Google Scholar and PubMed are the most popular free search engines
for literature searches in the fields of biomedicine and health. <!--
-->
With Google Scholar being the most common starting point when performing a literature search---in
large part due to their "Cited by N" link found next to every paper summary,
where "N" is the number of citations. <!--
which appears in the summary for each paper returned from a search query
where "N" is the number of citing papers. 
The "Cited by" link contains the number of papers and articles citing a single paper.
Clicking on the "Cited by" link provides researchers with the ability to quickly view a list of citing papers
and those papers' citation counts.
-->
For all of PubMed's easy-to-use and powerful literature search features,
it lacks the "Cited by N" link,
resulting in Google Scholar the tempting first choice. <!--
-->
However, scientists using Google Scholar as their primary system for literature searches may be unacquainted
with research that details five key criteria for scientific literature tools. <!--
-->
Using this list to compare Google Scholar and PubMed,
I found profound differences which tremendously favored PubMed;
except for PubMed's lack of "Cited by N" feature.  <!--
-->
Here I present a method which augments PubMed searches
with functionality similar to
that offered by Google Scholar's "Cited by N" link. <!--
-->
The pmidcite method is
designed to improve upon the Google Scholar experience
when working from the command-line or
when scripting
while doing a literature search for papers reposited into PubMed.

<!-- using a paper or set of papers that are reposited into PubMed,
a resource which is aimed to help scientists perform work that
improves health for both individuals and people all over the world.
PubMed contains millions and millions of citations
from the biomedicine and health fields,
and related disciplines such as
life sciences, behavioral sciances, chemical, sciences, and bioengineering. 
-->


<!-- A scientist traces the evolution of a research question by
performing forward and backward snowballing and 
carrying out database searches. 
-->
<!-- Forward snowballing begins with studying the citation list of a chosen paper to find additional papers of interest.
The researcher then selects papers from the citation list for further review by
investigating the citation lists of all the newly selected papers,
thus building a larger and larger snowball of information from which to synthesize knowledge.
Backward snowballing uses lists of references rather than citations.[@Wohlin_2014] 
-->
<!-- Database searches add new papers to a literature search using free-text entered by the researcher into a search bar. 
-->


<!-- PubMed was developed and is maintained by
the National Center for Biotechnology Information (NCBI), at
the U.S. National Library of Medicine (NLM),
located at the National Institutes of Health (NIH).[@sayers2025database] 
-->
<!-- Citation counts and other data is downloaded by pmidcite from the NIH Open Citation Collection.[@Hutchins_2019]    -->


# Statement of need
The development of pmidcite was driven by the need to rapidly sift through
hundreds or thousands of papers in a literature search by following both
citations, also known as forward snowballing, or
references (backward snowballing) from the command line.
<!-- -->
While Google Scholar (GS) is primarily accessible through a 
graphical user interface (GUI),
there are application programming interfaces (APIs)
available written by users.[@cholewiak2021]
However, GS blocks the download of citations 
without issuing any warnings that the results have been truncated.

Additionally, GS, lacks five of the six crucial elements
as defined by Boeker et al
necessary for the creation of solid scientific evidence 
useing high quality systematic and exploratory literature searches.

Almost immediately after Gehanno et al wrote a paper
concluding that GS alone could be used for systematic reviews,
which was based on exclusively using look-up searches 
rather the typical exploratory or the more rigorous systematic searches,
Giustini and Boulos slapped back with a paper titled,
"Google Scholar is not enough to be used alone for systematic reviews"

<!-- A scientist traces the evolution of a research question by 
trace the evolution of a research question
performing forward and backward snowballing and 
carrying out database searches. 
-->

<!--
The development of pmidcite was driven by the need to generate large-scale datasets of drug-like peptide SMILES strings for pretraining transformer-based models to predict membrane permeation from chemical structure [@feller2025peptide]. Built on the core concepts from the CycloPs [@duffy2011cyclops] method for FASTA-to-SMILES conversion, pmidcite has evolved into a stand-alone resource to support peptide-focused machine learning pipelines and peptide design workflows. While several bioinformatics toolkits exist for chemical representation and cheminformatics workflows [@ChemAxon; @o2011open; @landrum2013rdkit; @OEChem; @cock2009biopython];, many face limitations such as proprietary licensing and lack in ability to interpret or encode noncanonical amino acids (NCAAs). These constraints limit high-throughput application of sequence generation and conversion, especially for drug-like peptides containing diverse stereochemistries. In, addition, there are several python tools that focus on structure generation and cyclization [@tien2013peptidebuilder; @yang2025cyclicpeptide], however, these are not able to incorporate all necessary modifications. I used pmidcite to build a dataset of 10M peptides with NCAAs, backbone modifications, and cyclizations for pretraining a chemical language model [@feller2025peptide]. To support the community, have made pmidcite available as an open source package on PyPI, offering both command-line tools and Python functions for seamless integration into larger workflows.
-->


# Features
<!--
pmidcite offers five core command-line tools to support peptide sequence generation, conversion, modification, and analysis:

- **generate-peptides:**  
Generates random peptide sequences with customizable parameters; number of peptides, minimum and maximum length, percentage of unnatural amino acids, rate of D-stereochemistry, and cyclization types (randomly chosen). Currently accommodates over 100 unnatural amino acid residues described in SwissSidechain [@gfeller2012swisssidechain].  
**Input:** Settings and output filename.  
**Output:** FASTA file with expanded single character notation.

- **fasta2smi:**  
Converts peptide sequences from FASTA format (with the expanded set of NCAAs) into SMILES notation. Conducts cyclization reactions from notation in the FASTA header, supporting five types of cyclization reactions; disulfide bonded, head-to-tail, sidechain-to-sidechain, sidechain-to-head, and sidechain-to-tail.  
**Input:** Protein FASTA file. Optional FASTA header notation for cyclization reaction.  
**Output:** File in novel .pmidcite format that includes the single character amino acid representation, type of cyclization reaction, and the resulting SMILES string.

- **modify-smiles:**  
Applies N-methylation and PEGylation to existing SMILES strings. Rates of modification are defined by CLI arguments with peptides and sites randomly selected. Changes are recorded when input is in the .pmidcite format.  
**Input:** Text file with single SMILES per line or .pmidcite file.  
**Output:** Single SMILES per line or .pmidcite format (if input is .pmidcite).

- **smiles-props:**  
Computes molecular properties from SMILES strings including: molecular weight, TPSA, MolLogP, hydrogen donor/acceptor count, rotatable bond count, ring count, fraction Csp3, heavy atom count, formal charge, molecular formula, and compliance with Lipinski’s rules.  
**Input:** Text file with single SMILES per line or .pmidcite format.  
**Output:** Text file with JSON formatted dictionary of properties.

- **synthesis-check:**  
Synthetic feasibility of natural peptides including several forbidden motifs (N/Q at N-terminus, proline/glycine runs, DG/DP motifs, cysteine count, terminal P/C), a maximum length restriction, hydrophobicity check, and minimum charge distribution.  
**Input:** Protein FASTA file.  
**Output:** Protein FASTA file with modified header (PASS/FAIL).

For detailed usage instructions and options for each command, users can append the --help flag to any command (e.g., generate-peptides --help). This will provide guidance on the command’s functionality and available parameters.
-->


# State of the field
<!--
In the realm of peptide informatics, several tools have been recently developed to facilitate the analysis and representation of peptides, particularly those incorporating NCAAs and complex modifications including cyclization. Notably, pyPept [@ochoa2023pypept], PepFuNN [@ochoa2025pepfunn], and cyclicpeptide [@yang2025cyclicpeptide] have emerged as significant contributions in this area.

pyPept is a Python library that generates 2D and 3D representations of peptides. It converts sequences from formats like FASTA, HELM, or BILN into molecular graphs, enabling visualization and physicochemical property calculations. Notably, pyPept allows customization of monomer libraries to accommodate a wide range of peptide modifications. It also offers modules for rapid peptide conformer generation, incorporating user-defined or predicted secondary structure restraints, which is valuable for structural analyses.

PepFuNN is an open-source Python package designed to explore the chemical space of peptide libraries and conduct structure–activity relationship analyses. It includes modules for calculating physicochemical properties, assessing similarity using various peptide representations, clustering peptides based on molecular fingerprints or descriptors, and designing peptide libraries tailored to specific requirements. Additionally, PepFuNN provides tools for extracting matched pairs from experimental data, aiding in the identification of key mutations for subsequent design iterations.

The cyclicpeptide package provides a unified framework for converting between cyclic peptide sequences and structures, aligning cyclic peptides via graph methods, and analyzing their properties to support drug design. It supports multiple cyclization types and monomer libraries, validates its conversions on large cyclic peptide datasets with high accuracy and stability, and enables efficient cyclic peptide generation. By integrating these modular tools, it fills a gap in peptide informatics by facilitating standardized representations and transformations specifically for cyclic peptides, complementing existing tools focused more on linear peptides or structural analyses.

While these tools offer valuable capabilities, they are not specifically designed for the direct conversion of drug-like peptides into SMILES strings, a functionality central to the initial use-case for pmidcite of generating a large-scale database. Rather, these recent additions in the field focus on structural representation, analysis, and structure–activity relationship studies of peptides, complementing the sequence-to-SMILES conversion capabilities provided by pmidcite.
-->

# Code availability
The pmidcite package can be installed using pip, available on PyPI at https://pypi.org/project/pmidcite,
or bioconda, with the recipe available at https://bioconda.github.io/recipes/pmidcite/README.html.
The source code, including documentation and example notebooks, is openly available on GitHub at https://github.com/dvklopfenstein/pmidcite.


# Acknowledgements
I would like to thank Will Dampier, PhD for inspiring my creation of pmidcite.

# References
