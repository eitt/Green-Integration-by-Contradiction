# EJAtlas LNG Database

This folder contains a reproducible extract of LNG-related conflicts from the Environmental Justice Atlas (EJAtlas), plus verification outputs, a methodology note, and article-ready figures.

## What is included

- A full EJAtlas API pull for the `LNG` search query.
- A curated core subset for the comparative article framing:
  - 13 European cases
  - 6 US East Coast cases, marked as provisional where the title is broader than strict LNG
  - 2 Algeria cases
  - 1 UAE case
  - 4 Russia cases

## Files

- `data/raw/ejatlas_lng_cases.json`: raw API response with one row per case.
- `data/processed/ejatlas_lng_database.csv`: coded case database.
- `data/processed/ejatlas_lng_empirical_table.csv`: compact empirical table aligned to the article variables.
- `data/processed/ejatlas_lng_core_26.csv`: curated core subset.
- `data/processed/ejatlas_lng_map_verification.csv`: verification of map-listed places against the live EJAtlas pull.
- `data/processed/ejatlas_lng_workbook.xlsx`: multi-sheet Excel workbook with the main outputs.
- `data/processed/full_database.xlsx`: single-sheet Excel export of the full coded database.
- `data/processed/empirical_table.xlsx`: single-sheet Excel export of the empirical table.
- `data/processed/core_26.xlsx`: single-sheet Excel export of the core subset.
- `data/processed/map_verification.xlsx`: single-sheet Excel export of the verification table.
- `data/processed/core_case_relation_edges.csv`: weighted edge list for the relational case graph.
- `data/processed/ejatlas_lng_summary.json`: quick counts and coverage notes.
- `data/processed/methodology_case_selection.md`: draft methods section for Leonardo.
- `scripts/build_lng_database.js`: scraper and coder.
- `scripts/generate_lng_figures.py`: Python figure generator.
- `scripts/export_lng_excel.py`: Excel export script.
- `scripts/generate_relational_figures.py`: relational network and world-map figure generator.
- `scripts/generate_interactive_relation_network.py`: standalone interactive HTML for the core-case relation network.
- `figures/`: output charts for the empirical section.

## Notes on consistency

- The EJAtlas API search for `LNG` returns 105 cases. That is slightly broader than the 99-case figure mentioned in the article draft, so the database keeps the full API pull and flags the comparative core subset separately.
- The US cases are classified by coast using geography:
  - East Coast
  - Gulf Coast
  - West Coast
  - Alaska
  - Mixed or unclear
- The UAE case appears in EJAtlas as Abu Dhabi, not Dubai. I keep it in the core subset as the UAE case and add a note in the database.
- The database distinguishes:
  - `core_article_flag`
  - `core_article_group`
  - `us_coast_bucket`
  - `link_to_eu`
  - `evidence_quality`

## Rebuild

Run the scraper script from this folder with Node.js:

```bash
node scripts/build_lng_database.js
```

Then generate the figures with Python:

```bash
python scripts/generate_lng_figures.py
```

Generate relational figures and the weighted edge table:

```bash
python scripts/generate_relational_figures.py
```

Generate the standalone interactive HTML network:

```bash
python scripts/generate_interactive_relation_network.py
```

Then export the tables to Excel:

```bash
python scripts/export_lng_excel.py
```
