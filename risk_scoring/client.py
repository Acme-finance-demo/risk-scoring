"""Sanctions list lookup.

Kept behind a small function so the scoring rules stay testable without the network.
"""

from __future__ import annotations

import requests

TIMEOUT_SECONDS = 5


def fetch_watchlist(url: str) -> set[str]:
    """Country codes on the current watchlist. An empty set when the list is unreachable."""
    if not url:
        return set()
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException:
        # A missing list must not fail a payment; the country rule simply does not fire.
        return set()
    payload = response.json()
    return {str(code).upper() for code in payload.get("countries", [])}
