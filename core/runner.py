"""FreeInference CLI Runner: Single unified entry point for verification and discovery."""

import argparse
from datetime import date
import json
from pathlib import Path
import sys
import time

from core.model import MODEL_CASCADE, get_api_key
from core.scout import scout_frontier
from core.slack import notify_job_completed, notify_job_failed, notify_job_started
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
        print("Error: Missing GEMINI_API_KEY or GOOGLE_API_KEY", file=sys.stderr)
        notify_job_failed("Missing GEMINI_API_KEY or GOOGLE_API_KEY", stage="Initialization")
        sys.exit(1)

    t0 = time.time()
    catalog = load_catalog()
    initial_prov_count = len(catalog.get("providers", []))
    flags = " ".join(sys.argv[1:])
    print(f"=== FreeInference Engine 2.0 (Catalog: {initial_prov_count} providers) ===")

    # Send Slack alert: Job started
    notify_job_started(initial_prov_count, flags, MODEL_CASCADE)

    results = []
    discovered = []
    contradictions = []

    try:
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

            for r in results:
                if r["status"] in ("changed", "deprecated"):
                    contradictions.append(f"*{r['provider']}* [{r['status'].upper()}]: {r['summary']}")

        # Task 2: Scout Frontier
        if args.scout or args.all:
            print("\n--- Task 2: Looking For New (Frontier Discovery) ---")
            discovered = scout_frontier(catalog, apply_updates=args.apply, key=key)
            print(f"Discovery Results: {len(discovered)} candidate models queued.")
            for d in discovered:
                contradictions.append(f"✨ *New Frontier Candidate*: `{d.get('name')}` ({d.get('url')})")

        # Save Catalog if applied
        if args.apply:
            today = date.today().isoformat()
            catalog["verified"] = today
            save_catalog(catalog)
            print(f"\n✓ Saved updated catalog to {PROVIDERS_PATH}")

        duration = time.time() - t0
        print(f"\n=== Completed in {duration:.1f}s ===")

        # Send Slack alert: Job completed
        notify_job_completed(
            duration_s=duration,
            verified_count=len(results),
            active_count=sum(1 for r in results if r["status"] == "active"),
            changed_count=sum(1 for r in results if r["status"] == "changed"),
            deprecated_count=sum(1 for r in results if r["status"] == "deprecated"),
            inconclusive_count=sum(1 for r in results if r["status"] == "inconclusive"),
            discovered_count=len(discovered),
            contradictions=contradictions
        )

    except Exception as e:
        notify_job_failed(str(e), stage="Execution")
        raise


if __name__ == "__main__":
    main()
