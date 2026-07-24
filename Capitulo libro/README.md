# Chapter Project Scaffold

This project scaffold prepares the working structure requested in `codex_chapter_brief.md` for the UNAB book chapter on the Camino de Santiago and the Camino de Lengerke.

It includes:
- the folder structure required by the brief,
- CSV evidence matrices,
- chapter and notes templates,
- a Word generator that builds a submission-ready `.docx` in Arial 12 with single spacing,
- wrappers for the `sci-papers-downloder` skill and the `doc` rendering helper.

## Source inputs

The project is wired to these local inputs:
- `MEMORIA PFM LAURA JULIANA Para entregar.docx`
- `CALL-CHAPTERS-FACULTY-ECONOMICS-BUSINESS.pdf`
- `codex_chapter_brief.md`

## Call requirements already reflected in the generator

- Arial 12
- Single spacing
- Minimum 12 pages, maximum 18 pages
- Black-and-white tables inside the text
- APA 7 references
- Abstract max 250 words
- Keywords: 3 to 5
- Core sections: introduction, methodology, results and discussion, conclusions, references, author profiles

The call deadline in the PDF is `2026-04-10`.

## Project layout

- `config/` project metadata and Scopus query plans
- `draft/` chapter markdown source
- `evidence/` article and web evidence matrices
- `notes/` working notes for call alignment, thesis extraction, and evidence gaps
- `papers/` downloaded PDFs
- `output/doc/` generated Word documents
- `scripts/` runnable helpers
- `src/chapter_project/` reusable Python code

## Quick start

Generate the Word template:

```powershell
python scripts/generate_chapter_docx.py
```

Preview the generated `.docx` as page images if LibreOffice and Poppler are installed:

```powershell
python scripts/render_docx_preview.py
```

Inspect the literature acquisition commands first, then run them after setting credentials:

```powershell
python scripts/run_literature_batch.py --dry-run
python scripts/run_literature_batch.py
```

## Environment variables

Copy `.env.example` values into your shell or user environment:

- `ELSEVIER_API_KEY`
- `UNPAYWALL_EMAIL`
- `SCI_PAPERS_SKILL_DIR` (optional override)
- `DOC_SKILL_RENDER_SCRIPT` (optional override)

## Important limits

- The literature wrapper uses the local `sci-papers-downloder` skill scripts to search Scopus and download candidate PDFs.
- Q1 verification is still an auditable human step and must be recorded in `evidence/article_evidence_matrix.csv`.
- No downloader command is executed automatically during project creation.
- The current draft template stays in English to follow `codex_chapter_brief.md`. If the editors later require bilingual front matter, add Spanish `Resumen` and `Palabras clave` before submission.

