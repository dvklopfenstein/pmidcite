"""Higher-level PubMed Record handling"""

__copyright__ = 'Copyright (C) 2020-present, DV Klopfenstein, PhD. All rights reserved'
__author__ = 'DV Klopfenstein, PhD'

# https://pubmed.ncbi.nlm.nih.gov/22750224/?format=pubmed
# https://pubmed.ncbi.nlm.nih.gov/help/#pubmed-format     PubMed Format tags

# pylint: disable=line-too-long

# Tag            |Name            |Description
# AB            |Abstract            |English language abstract taken directly from the published article
# AD            |Affiliation            |Author or corporate author addresses
# AID            |Article Identifier            |Article ID values supplied by the publisher may include the pii (controlled publisher identifier), doi (digital object identifier), or book accession
# AU            |Author            |Authors
# AUID            |Author Identifier            |Unique identifier associated with an author, corporate author, or investigator name
# BTI            |Book Title            |Book Title
# CI            |Copyright Information            |Copyright statement provided by the publisher
# CIN            |Comment In            |Reference containing a comment about the article
# CN            |Corporate Author            |Corporate author or group names with authorship responsibility
# COI            |Conflict of Interest            |Conflict of interest statement
# CON            |Comment On            |Reference upon which the article comments
# CP            |Chapter            |Book chapter
# CRDT            |Create Date            |The date the citation record was first created
# CRF            |Corrected and republished from            |Final, correct version of an article
# CRI            |Corrected and republished in            |Original article that was republished in corrected form
# CTDT            |Contribution Date            |Book contribution date
# CTI            |Collection Title            |Collection Title
# DCOM            |Completion Date            |NLM internal processing completion date
# DDIN            |Dataset described in            |Citation for the primary article resulting from a dataset
# DRIN            |Dataset use reported in            |Citation for an article that uses a dataset from another scientific article
# DEP            |Date of Electronic Publication            |Electronic publication date
# DP            |Publication Date            |The date the article was published
# DRDT            |Date Revised            |Book Revision Date
# ECF            |Expression of Concern For            |Reference containing an expression of concern for an article
# ECI            |Expression of Concern In            |Cites the original article for which there is an expression of concern
# EDAT            |Entry Date            |The date the citation was added to PubMed; the date is set to the publication date if added more than 1 year after the date published
# EFR            |Erratum For            |Cites the original article for which there is a published erratum; as of 2016, partial retractions are considered errata
# EIN            |Erratum In            |Cites a published erratum to the article
# ED            |Editor            |Book editors
# EN            |Edition            |Book edition
# FAU            |Full Author Name            |Full author names
# FED            |Full Editor Name            |Full editor names
# FIR            |Full Investigator Name            |Full investigator or collaborator names
# FPS            |Full Personal Name as Subject            |Full Personal Name of the subject of the article
# GN            |General Note            |Supplemental or descriptive information related to the document
# GR            |Grants and Funding            |Grant numbers, contract numbers, and intramural research identifiers associated with a publication
# GS            |Gene Symbol            |Abbreviated gene names (used 1991 through 1996)
# IP            |Issue            |The number of the issue, part, or supplement of the journal in which the article was published
# IR            |Investigator            |Investigator or collaborator
# IRAD            |Investigator Affiliation            |Investigator or collaborator addresses
# IS            |ISSN            |International Standard Serial Number of the journal
# ISBN            |ISBN            |International Standard Book Number
# JID            |NLM Unique ID            |Unique journal ID in the NLM catalog of books, journals, and audiovisuals
# JT            |Full Journal Title            |Full journal title from NLM cataloging data
# LA            |Language            |The language in which the article was published
# LID            |Location ID            |The pii or doi that serves the role of pagination
# LR            |Modification Date            |Citation last revision date
# MH            |MeSH Terms            |NLM Medical Subject Headings (MeSH) controlled vocabulary
# MHDA            |MeSH Date            |The date MeSH terms were added to the citation. The MeSH date is the same as the Entrez date until MeSH are added
# MID            |Manuscript Identifier            |Identifier assigned to an author manuscript submitted to the NIH Manuscript Submission System
# NM            |Substance Name            |Supplementary Concept Record (SCR) data
# OAB            |Other Abstract            |Abstract supplied by an NLM collaborating organization
# OABL            |Other Abstract Language            |Language of an abstract available from the publisher
# OCI            |Other Copyright Information            |Copyright owner
# OID            |Other ID            |Identification numbers provided by organizations supplying citation data
# ORI            |Original Report In            |Cites the original article associated with the patient summary
# OT            |Other Term            |Non-MeSH subject terms (keywords) either assigned by an organization identified by the Other Term Owner, or generated by the author and submitted by the publisher
# OTO            |Other Term Owner            |Organization that may have provided the Other Term data
# OWN            |Owner            |Organization acronym that supplied citation data
# PB            |Publisher            |Publishers of Books & Documents citations
# PG            |Pagination            |The full pagination of the article
# PHST|Publication History Status Date|Publisher supplied dates regarding the article publishing process and PubMed date stamps:
# PHST|Publication History Status Date|received: manuscript received for review
# PHST|Publication History Status Date|revised: manuscript revised by publisher or author
# PHST|Publication History Status Date|accepted: manuscript accepted for publication
# PHST|Publication History Status Date|aheadofprint: published electronically prior to final publication
# PHST|Publication History Status Date|entrez: PubMed Create Date [crdt]
# PHST|Publication History Status Date|pubmed: PubMed Entry Date [edat]
# PHST|Publication History Status Date|medline: PubMed MeSH Date [mhda]
# PL            |Place of Publication            |Journal's (country only) or book’s place of publication
# PMC            |PubMed Central Identifier            |Unique identifier for the cited article in PubMed Central (PMC)
# PMCR            |PMC Release            |Availability of PMC article
# PMID            |PubMed Unique Identifier            |Unique number assigned to each PubMed citation
# PS            |Personal Name as Subject            |Individual is the subject of the article
# PST            |Publication Status            |Publication status
# PT            |Publication Type            |The type of material the article represents
# RF            |Number of References            |Number of bibliographic references for Review articles
# RIN            |Retraction In            |Retraction of the article
# RN            |EC/RN Number            |Includes chemical, protocol or disease terms. May also include a number assigned by the Enzyme Commission or by the Chemical Abstracts Service.
# ROF            |Retraction Of            |Article being retracted
# RPF            |Republished From            |Article being cited has been republished or reprinted in either full or abridged form from another source
# RPI            |Republished In            |Article being cited also appears in another source in either full or abridged form
# RRI            |Retracted and Republished In            |Final, republished version of an article
# RRF            |Retracted and Republished From            |Original article that was retracted and republished
# SB            |Subset            |Journal or citation subset values representing specialized topics
# SFM            |Space Flight Mission            |NASA-supplied data space flight/mission name and/or number
# SI            |Secondary Source ID            |Identifies secondary source databanks and accession numbers of molecular sequences discussed in articles
# SO            |Source            |Composite field containing bibliographic information
# SPIN            |Summary For Patients In            |Cites a patient summary article
# STAT            |Status Tag            |Used for internal processing at NLM
# TA            |Journal Title Abbreviation            |Standard journal title abbreviation
# TI            |Title            |The title of the article
# TT            |Transliterated Title            |Title of the article originally published in a non-English language, in that language
# UIN            |Update In            |Update to the article
# UOF            |Update Of            |The article being updated
# VI            |Volume            |Volume number of the journal
# VTI            |Volume Title            |Book Volume Title

# Copyright (C) 2020-present, DV Klopfenstein, PhD. All rights reserved
