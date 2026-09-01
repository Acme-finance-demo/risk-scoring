"""Rule loading.

The rules file is operator-supplied, not user-supplied, but it is still parsed with
`yaml.safe_load` rather than `yaml.load`: safe_load will not construct arbitrary Python
objects, so a mistake in the file cannot turn into code execution.
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass

import yaml

DEFAULT_RULES = pathlib.Path(__file__).resolve().parent.parent / "rules.yaml"


@dataclass(frozen=True)
class Rules:
    weights: dict[str, int]
    limits: dict[str, int]
    thresholds: dict[str, int]
    watchlist_url: str

    def weight(self, name: str) -> int:
        return int(self.weights.get(name, 0))


def load_rules(path: pathlib.Path | None = None) -> Rules:
    raw = (path or DEFAULT_RULES).read_text(encoding="utf-8")
    parsed = yaml.safe_load(raw) or {}
    missing = [key for key in ("weights", "limits", "thresholds") if key not in parsed]
    if missing:
        raise ValueError(f"rules file is missing: {', '.join(missing)}")
    return Rules(
        weights=parsed["weights"],
        limits=parsed["limits"],
        thresholds=parsed["thresholds"],
        watchlist_url=parsed.get("watchlist_url", ""),
    )
