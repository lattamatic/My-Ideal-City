#!/usr/bin/env python3
"""
Rebuilds checkpoint.txt from an existing ville_ideale_idf.csv.
Run this once if you already have partial data, before running the scraper.

RUN:
    python rebuild_checkpoint.py
"""

import csv
from pathlib import Path

CSV_FILE        = "ville_ideale_idf.csv"
CHECKPOINT_FILE = "checkpoint.txt"
CRITERIA = [
    "Environnement", "Transports", "Sécurité", "Santé",
    "Sports et loisirs", "Culture", "Enseignement", "Commerces", "Qualité de vie",
]

def has_data(row: dict) -> bool:
    """Row is considered complete if at least one score is filled."""
    return any(row.get(c, "").strip() for c in CRITERIA)

def main():
    p = Path(CSV_FILE)
    if not p.exists():
        print(f"{CSV_FILE} not found.")
        return

    with open(p, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    complete   = [r for r in rows if r.get("Slug") and has_data(r)]
    incomplete = [r for r in rows if r.get("Slug") and not has_data(r)]

    print(f"Total rows in CSV : {len(rows)}")
    print(f"Complete (has scores)  : {len(complete)}  → will be added to checkpoint")
    print(f"Incomplete (no scores) : {len(incomplete)} → will be retried by scraper")

    # Load existing checkpoint to avoid duplicates
    cp_path = Path(CHECKPOINT_FILE)
    existing = set(cp_path.read_text().splitlines()) if cp_path.exists() else set()

    new_slugs = [r["Slug"] for r in complete if r["Slug"] not in existing]

    with open(CHECKPOINT_FILE, "a") as f:
        for slug in new_slugs:
            f.write(slug + "\n")

    print(f"\nAdded {len(new_slugs)} slugs to {CHECKPOINT_FILE}")
    print(f"Scraper will retry {len(incomplete)} incomplete cities on next run.")

if __name__ == "__main__":
    main()
