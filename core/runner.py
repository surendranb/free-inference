"""FreeInference CLI Runner: Single unified entry point for verification and discovery."""

import argparse
from datetime import date
import json
from pathlib import Path
import sys
import time

from core.model import get_api_key
from core.scout import scout_frontier
from core.verifier import verify_catalog

PROVIDERS_PATH = Path("data/providers.json")


def load_catalog() -> dict:
    if not PROVIDERS_PATH.exists():
        raise FileNotFoundError(f"{PROVIDERS_PATH} not found")
    with open(PROVIDERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_catalog(data: dict):
    with open(PROVIDERS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(description="FreeInference Autonomous Engine")
    parser.add_argument("--verify", action="store_true", help="Task 1: Update What We Know (Catalog Verification)")
    parser.add_argument("--scout", action="store_true", help="Task 2: Look For New (Frontier Discovery)")
    parser.add_argument("--all", action="store_true", help="Run both Task 1 and Task 2")
    parser.add_argument("--apply", action="store_true", help="Persist updates to data/providers.json")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of catalog providers to verify")
    parser.add_argument("--force-all", action="store_true", help="Force verification even if verified today")
    args = parser.parse_args()

    if not (args.verify or args.scout or args.all):
        parser.print_help()
        sys.exit(1)

    key = get_api_key()
    if not key:
        print("Error: Missing GEMINI_API_KEY", file=sys.stderr)
        sys.exit(1)

    t0 = time.time()
    catalog = load_catalog()
    initial_prov_count = len(catalog.get("providers", []))
    print(f"=== FreeInference Engine 2.0 (Catalog: {initial_prov_count} providers) ===")

    # Task 1: Verify Catalog
    if args.verify or args.all:
        print("\n--- Task 1: Updating What We Know (Catalog Verification) ---")
        results = verify_catalog(
            catalog,
            apply_updates=args.apply,
            limit=args.limit,
            force_all=args.force_all,
            key=key
        )
        active_count = sum(1 for r in results if r["status"] == "active")
        changed_count = sum(1 for r in results if r["status"] == "changed")
        deprecated_count = sum(1 for r in results if r["status"] == "deprecated")
        inconclusive_count = sum(1 for r in results if r["status"] == "inconclusive")
        print(f"\nVerification Results ({len(results)} audited):")
        print(f"  Active: {active_count} · Changed: {changed_count} · Deprecated: {deprecated_count} · Inconclusive: {inconclusive_count}")

    # Task 2: Scout Frontier
    if args.scout or args.all:
        print("\n--- Task 2: Looking For New (Frontier Discovery) ---")
        discovered = scout_frontier(catalog, apply_updates=args.apply, key=key)
        print(f"Discovery Results: {len(discovered)} candidate models queued.")

    # Save Catalog if applied
    if args.apply:
        today = date.today().isoformat()
        catalog["verified"] = today
        save_catalog(catalog)
        print(f"\n✓ Saved updated catalog to {PROVIDERS_PATH}")

    duration = time.time() - t0
    print(f"\n=== Completed in {duration:.1f}s ===")


if __name__ == "__main__":
    main()
