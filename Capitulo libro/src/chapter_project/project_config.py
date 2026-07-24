from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_config(config_path: Path | str | None = None) -> dict[str, Any]:
    root = repo_root()
    path = Path(config_path) if config_path else root / "config" / "chapter_project.json"
    if not path.is_absolute():
        path = root / path
    return json.loads(path.read_text(encoding="utf-8-sig"))
