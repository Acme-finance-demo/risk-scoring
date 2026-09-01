"""The scoring rules themselves."""

from __future__ import annotations

from dataclasses import dataclass

from .config import Rules


@dataclass(frozen=True)
class Decision:
    score: int
    outcome: str
    reasons: tuple[str, ...]


def score(
    transaction: dict,
    rules: Rules,
    watchlist: set[str] | None = None,
) -> Decision:
    watchlist = watchlist or set()
    reasons: list[str] = []
    total = 0

    if int(transaction.get("amount", 0)) > int(rules.limits.get("amount", 0)):
        total += rules.weight("amount_over_limit")
        reasons.append("amount_over_limit")

    if transaction.get("new_beneficiary"):
        total += rules.weight("new_beneficiary")
        reasons.append("new_beneficiary")

    country = str(transaction.get("country", "")).upper()
    if country and country in watchlist:
        total += rules.weight("country_watchlist")
        reasons.append("country_watchlist")

    if int(transaction.get("recent_count", 0)) > int(rules.limits.get("velocity_per_hour", 0)):
        total += rules.weight("velocity")
        reasons.append("velocity")

    if total >= int(rules.thresholds.get("block", 10**9)):
        outcome = "block"
    elif total >= int(rules.thresholds.get("review", 10**9)):
        outcome = "review"
    else:
        outcome = "approve"

    return Decision(score=total, outcome=outcome, reasons=tuple(reasons))
