from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SUMMARY_GLOB = "*_download_summary.json"
FIELDNAMES = [
    "article_id",
    "apa_reference",
    "doi",
    "journal",
    "year",
    "scopus_q1_verified",
    "quartile_verification_source",
    "pdf_downloaded",
    "exact_phrase",
    "page_or_section",
    "theme_code",
    "why_it_matters_for_chapter",
    "target_chapter_section",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed the article evidence matrix from downloaded summary files."
    )
    parser.add_argument(
        "--evidence-dir",
        default="evidence",
        help="Directory containing *_download_summary.json files.",
    )
    parser.add_argument(
        "--matrix",
        default="evidence/article_evidence_matrix.csv",
        help="Target article evidence matrix CSV.",
    )
    return parser.parse_args()


def load_existing_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def build_article_id(cluster_name: str, index: int) -> str:
    return f"{cluster_name.upper()}_{index:03d}"


def collect_new_rows(evidence_dir: Path, existing_dois: set[str], start_index: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    sequence = start_index

    for summary_path in sorted(evidence_dir.glob(SUMMARY_GLOB)):
        cluster_name = summary_path.name.replace("_download_summary.json", "")
        payload = json.loads(summary_path.read_text(encoding="utf-8"))
        for result in payload.get("results", []):
            if result.get("status") != "downloaded":
                continue

            doi = (result.get("doi") or "").strip()
            if not doi or doi in existing_dois:
                continue

            title = (result.get("title") or "").strip()
            year = str(result.get("year") or "").strip()
            journal = (result.get("source") or "").strip()
            apa_reference = f"{title}. ({year}). {journal}. DOI: {doi}" if title and year and journal else title

            rows.append(
                {
                    "article_id": build_article_id(cluster_name, sequence),
                    "apa_reference": apa_reference,
                    "doi": doi,
                    "journal": journal,
                    "year": year,
                    "scopus_q1_verified": "",
                    "quartile_verification_source": "",
                    "pdf_downloaded": "Yes",
                    "exact_phrase": "",
                    "page_or_section": "",
                    "theme_code": "",
                    "why_it_matters_for_chapter": "",
                    "target_chapter_section": "",
                }
            )
            existing_dois.add(doi)
            sequence += 1

    return rows


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    evidence_dir = (ROOT_DIR / args.evidence_dir).resolve()
    matrix_path = (ROOT_DIR / args.matrix).resolve()

    existing_rows = load_existing_rows(matrix_path)
    existing_dois = {row.get("doi", "").strip() for row in existing_rows if row.get("doi", "").strip()}
    new_rows = collect_new_rows(evidence_dir, existing_dois, len(existing_rows) + 1)
    combined_rows = existing_rows + new_rows
    write_rows(matrix_path, combined_rows)
    print(f"Seeded {len(new_rows)} new downloaded articles into: {matrix_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
