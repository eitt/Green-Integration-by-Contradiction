from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DEFAULT_RENDER_SCRIPT = Path(
    os.environ.get(
        "DOC_SKILL_RENDER_SCRIPT",
        r"C:\Users\LEONA\.codex\skills\doc\scripts\render_docx.py",
    )
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a DOCX file to page images using the local doc skill helper."
    )
    parser.add_argument(
        "--docx",
        default="output/doc/chapter_submission_template.docx",
        help="DOCX file to render.",
    )
    parser.add_argument(
        "--output-dir",
        default="tmp/docs/chapter_submission_template",
        help="Directory for page images.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    docx_path = (ROOT_DIR / args.docx).resolve()
    output_dir = (ROOT_DIR / args.output_dir).resolve()

    if not docx_path.exists():
        print(f"Missing DOCX file: {docx_path}", file=sys.stderr)
        return 1

    if not DEFAULT_RENDER_SCRIPT.exists():
        print(
            "The doc skill render helper was not found. Set DOC_SKILL_RENDER_SCRIPT or install the skill.",
            file=sys.stderr,
        )
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(DEFAULT_RENDER_SCRIPT),
        str(docx_path),
        "--output_dir",
        str(output_dir),
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print(
            "Rendering failed. This usually means LibreOffice or Poppler is missing.",
            file=sys.stderr,
        )
        print(str(exc), file=sys.stderr)
        return exc.returncode or 1

    print(f"Preview images generated in: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
