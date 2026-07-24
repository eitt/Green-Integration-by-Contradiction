from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SKILL_DIR = Path(
    os.environ.get(
        "SCI_PAPERS_SKILL_DIR",
        r"C:\Users\LEONA\.codex\skills\sci-papers-downloder",
    )
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the local sci-papers-downloder skill over the configured literature clusters."
    )
    parser.add_argument(
        "--config",
        default="config/literature_queries.json",
        help="JSON file with Scopus query plans.",
    )
    parser.add_argument(
        "--cluster",
        action="append",
        help="Run only the given cluster id. Repeat for multiple clusters.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the commands without executing them.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_command(entry: dict[str, Any], outdir: Path, summary_path: Path, script_path: Path) -> list[str]:
    cmd = [sys.executable, str(script_path)]
    mode = entry.get("mode", "query")
    value = entry["value"]

    if mode == "query":
        cmd.extend(["--query", value])
    elif mode == "keywords":
        cmd.extend(["--keywords", value])
    elif mode == "title":
        cmd.extend(["--title", value])
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    cmd.extend(["--quantity-mode", entry.get("quantity_mode", "batch")])

    target = entry.get("target")
    if target:
        cmd.extend(["--target", str(target)])

    if entry.get("latest"):
        cmd.append("--latest")

    from_year = entry.get("from_year")
    if from_year:
        cmd.extend(["--from-year", str(from_year)])

    years_back = entry.get("years_back")
    if years_back:
        cmd.extend(["--years-back", str(years_back)])

    max_search_results = entry.get("max_search_results")
    if max_search_results:
        cmd.extend(["--max-search-results", str(max_search_results)])

    max_attempts = entry.get("max_attempts")
    if max_attempts:
        cmd.extend(["--max-attempts", str(max_attempts)])

    max_success = entry.get("max_success")
    if max_success:
        cmd.extend(["--max-success", str(max_success)])

    sort = entry.get("sort")
    if sort:
        cmd.append(f"--sort={sort}")

    page_size = entry.get("page_size")
    if page_size:
        cmd.extend(["--page-size", str(page_size)])

    cmd.extend(
        [
            "--outdir",
            str(outdir),
            "--json",
            "--out",
            str(summary_path),
        ]
    )
    return cmd


def main() -> int:
    args = parse_args()
    config_path = (ROOT_DIR / args.config).resolve()
    if not config_path.exists():
        print(f"Missing config file: {config_path}", file=sys.stderr)
        return 1

    skill_script = DEFAULT_SKILL_DIR / "scripts" / "topic_batch_download.py"
    if not skill_script.exists():
        print(
            "The sci-papers-downloder skill script was not found. "
            "Set SCI_PAPERS_SKILL_DIR or install the skill locally.",
            file=sys.stderr,
        )
        return 1

    api_key = os.environ.get("ELSEVIER_API_KEY")
    email = os.environ.get("UNPAYWALL_EMAIL")
    if not args.dry_run and (not api_key or not email):
        print(
            "Missing ELSEVIER_API_KEY or UNPAYWALL_EMAIL. "
            "Set both variables before running downloads.",
            file=sys.stderr,
        )
        return 2

    config = load_json(config_path)
    queries = config.get("queries", [])
    selected = set(args.cluster or [])

    exit_code = 0
    for entry in queries:
        cluster_id = entry["id"]
        if selected and cluster_id not in selected:
            continue

        cluster_outdir = (ROOT_DIR / "papers" / cluster_id).resolve()
        cluster_outdir.mkdir(parents=True, exist_ok=True)
        summary_path = (ROOT_DIR / "evidence" / f"{cluster_id}_download_summary.json").resolve()
        cmd = build_command(entry, cluster_outdir, summary_path, skill_script)

        print(f"[{cluster_id}]")
        print(subprocess.list2cmdline(cmd))
        print("Reminder: Q1 verification still has to be audited manually in the evidence matrix.")

        if args.dry_run:
            continue

        result = subprocess.run(cmd)
        if result.returncode != 0:
            exit_code = result.returncode
            print(f"Cluster failed: {cluster_id}", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
