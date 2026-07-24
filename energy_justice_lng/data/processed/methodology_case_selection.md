# Methodology and Case Selection from the LNG Conflict Map

## Overview

The LNG conflict map was treated as a starting point rather than a finished dataset. To build a reproducible empirical database, all cases were re-verified against the live EJAtlas API on July 9, 2026. The query strategy began with the public EJAtlas search endpoint for `LNG`, after which each returned case was checked through its case-detail endpoint and recoded into a structured comparative table.

The live EJAtlas API returned 105 LNG-tagged cases globally. This is broader than the 99-case figure referenced in the draft text, which suggests that the map, the platform, or the article draft are not perfectly synchronized. For transparency, the full live pull is preserved as the master dataset, while a separate curated subset of 26 cases is marked as the core comparative sample used for the article.

## Coding strategy

Each case was coded using EJAtlas metadata together with rule-based recoding of the case title, headline, description, actors, impacts, and mobilization fields. The coding table standardizes the following variables: case name, country, region or city, infrastructure type, supply-chain role, link to EU supply, main impacts, conflict category, affected groups, main actors, status, evidence quality, and relevance to the core argument.

The coding strategy distinguishes between direct LNG cases and broader gas or environmental-justice cases. In the live July 9, 2026 pull, 59 cases were coded as direct LNG cases and 46 as broader gas or LNG-linked cases. This distinction matters because some conflicts included in the LNG search are not strictly terminals or liquefaction projects, but pipelines, ports, storage sites, or wider gas conflicts that become relevant through their connection to LNG supply chains.

To clarify comparative relevance, the dataset also distinguishes among direct EU-linked cases, indirect EU-linked cases, and broader contextual cases. 20 cases were coded as directly connected to EU LNG import diversification, while 77 were retained only as broader contextual environmental-justice cases.

## Case selection logic

The core article subset was organized around the supply chain most relevant to Europe's diversification strategy: European import and regasification sites, Russian Arctic export infrastructure, selected US export-side conflicts, Algerian export-side conflicts, and one UAE contextual comparison. This produces the following verified core sample: 13 European cases, 6 US East Coast provisional cases, 4 Russia cases, 2 Algeria cases, and 1 UAE case.

The US cases required special verification because the map brief mixes East Coast, Gulf Coast, and inland Texas locations. The database therefore adds a separate `us_coast_bucket` field to distinguish East Coast, Gulf Coast, West Coast, Alaska, and mixed or unclear cases. This helps separate cases directly relevant to Atlantic export routes to Europe from broader US fossil-fuel conflicts.

## Dynamic-map verification

Because EJAtlas is dynamic, all map references were checked against the live platform rather than assumed to be stable. The verification exercise shows that some listed geographies correspond cleanly to current LNG cases, while others do not. In particular, the current live LNG pull does not yield clean country-level LNG matches for the map items San Diego, San Antonio, Austin, Libya. In those cases, the evidence suggests either a contextual linkage, a broader gas conflict, or a mismatch between the map snapshot and the current EJAtlas index.

This matters substantively. Algeria remains strong enough for the core article because its cases are directly tied to EU gas supply and export infrastructure. Egypt is better treated as a contextual case with direct EU relevance. Pakistan, Tunisia, and UAE are better treated as contextual rather than core cases. Israel and Libya do not appear as standalone live LNG cases in the current EJAtlas pull, although Israel appears indirectly through regional gas and export routes discussed in related cases.

## Why this coding matters

Transforming the map into a coded dataset makes it possible to compare LNG conflicts systematically across importing, exporting, and transit sites. That step is necessary for analyzing how EU diversification reshapes environmental burdens, how energy-security narratives justify infrastructure expansion, and how procedural injustice, health risks, Indigenous dispossession, and coastal degradation recur across different segments of the LNG supply chain.
