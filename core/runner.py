"""FreeInference CLI Runner: Unified 3-route entry point for verification, discovery, and rebuild."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid

from core.model import MODEL_CASCADE, get_api_key
from core.scout import expand_base_catalog_from_sources, scout_frontier
from core.slack import notify_job_completed, notify_job_failed, notify_job_started
from core.telemetry import tracer
from core.verifier import audit_catalog_quality, verify_catalog

ROOT = Path(__file__).resolve().parent.parent
PROVIDERS_PATH = ROOT / "data" / "providers.json"
SUMMARY_PATH = ROOT / "data" / "run_summary.json"


def load_catalog() -> dict:
    if not PROVIDERS_PATH.exists():
        raise FileNotFoundError(f"{PROVIDERS_PATH} not found")
    with open(PROVIDERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_atomic(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def build_and_verify_site() -> None:
    """Rebuild static site outputs and verify all programmatic /free-*/ routes."""
    print("\n--- Phase 3: Rebuilding Website & Verifying Programmatic Matrix ---")
    subprocess.run([sys.executable, str(ROOT / "build.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "verify_matrix.py")], cwd=ROOT, check=True)


def _summarize_routes(results: list[dict]) -> dict:
    routes: dict[str, dict[str, int]] = {}
    for r in results:
        rt = r.get("route") or r.get("channel") or "web"
        bucket = routes.setdefault(rt, {"audited": 0, "active": 0, "changed": 0, "deprecated": 0, "inconclusive": 0})
        bucket["audited"] += 1
        st = r.get("status", "inconclusive")
        bucket[st] = bucket.get(st, 0) + 1
    return routes


def main():
    parser = argparse.ArgumentParser(description="FreeInference 3-Route Autonomous Engine")
    parser.add_argument("--verify", action="store_true", help="Run catalog verification across Route 1/2/3")
    parser.add_argument("--scout", action="store_true", help="Run frontier discovery across OpenRouter & Models.dev")
    parser.add_argument("--all", action="store_true", help="Run both frontier discovery and catalog verification")
    parser.add_argument("--route", choices=["feed", "api", "web"], default=None, help="Restrict verification to one route")
    parser.add_argument("--provider", type=str, default=None, help="Verify only providers matching substring")
    parser.add_argument("--apply", action="store_true", help="Persist catalog updates, run_summary.json, and rebuild site")
    parser.add_argument("--skip-rebuild", action="store_true", help="Skip running build.py + verify_matrix.py after --apply")
    parser.add_argument("--no-slack", action="store_true", help="Suppress Slack alerts (dry runs already skip Slack)")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of catalog providers to verify")
    parser.add_argument("--force-all", action="store_true", help="Force verification even if already verified today")
    parser.add_argument("--workers", type=int, default=6, help="Worker pool size (machine docs run parallel; Chrome capped by semaphore)")
    args = parser.parse_args()

    if not (args.verify or args.scout or args.all or args.route or args.provider):
        parser.print_help()
        sys.exit(1)

    run_verify = bool(args.verify or args.all or args.route or args.provider)
    run_scout = bool(args.scout or args.all)

    key = get_api_key()
    if not key:
        print("Error: Missing GEMINI_API_KEY or GOOGLE_API_KEY", file=sys.stderr)
        if args.apply and not args.no_slack:
            notify_job_failed("Missing GEMINI_API_KEY or GOOGLE_API_KEY", stage="Initialization")
        sys.exit(1)

    t0 = time.time()
    run_id = uuid.uuid4().hex[:12]
    entry_point = "nightly_ci" if os.getenv("GITHUB_ACTIONS") == "true" else (
        "manual_route" if (args.route or args.provider) else "cli"
    )
    trace_id = tracer.start_trace("freeinference.run", run_id=run_id, entry_point=entry_point)

    catalog = load_catalog()
    initial_prov_count = len(catalog.get("providers", []))
    flags = " ".join(sys.argv[1:])
    print(f"=== FreeInference 3-Route Engine (run_id={run_id}, entry={entry_point}, catalog={initial_prov_count} providers) ===")

    send_slack = bool(args.apply and not args.no_slack and not args.provider and not args.route)
    if send_slack:
        notify_job_started(initial_prov_count, flags, MODEL_CASCADE)

    results = []
    discovered = []
    contradictions = []

    try:
        if run_scout:
            print("\n--- Phase 1: Frontier Scan & Canonical Expansion (OpenRouter + Models.dev) ---")
            t_s0 = time.time()
            added_to_base = expand_base_catalog_from_sources(catalog, apply_updates=args.apply)
            print(f"Base Catalog Expansion: {len(added_to_base)} new $0 models attached cleanly.")
            for item in added_to_base:
                contradictions.append(f"New Free Model Added: `{item['model']}` to *{item['provider']}* ({item['context']})")

            discovered = scout_frontier(catalog, apply_updates=args.apply, key=key)
            tracer.log_span(
                trace_id,
                "scout.frontier",
                t_s0,
                time.time(),
                attributes={
                    "route": "feed",
                    "status_class": "2xx",
                    "verdict": "active",
                    "added_to_base": len(added_to_base),
                    "candidates_queued": len(discovered),
                },
                status_ok=True,
            )

        if run_verify:
            print("\n--- Phase 2: Three-Route Catalog Verification (Feed / API / Web + gemini-3.5-flash-lite) ---")
            results = verify_catalog(
                catalog,
                apply_updates=args.apply,
                limit=args.limit,
                force_all=args.force_all,
                key=key,
                route_filter=args.route,
                provider_filter=args.provider,
                max_workers=args.workers,
                trace_id=trace_id,
            )
            active_count = sum(1 for r in results if r["status"] == "active")
            changed_count = sum(1 for r in results if r["status"] == "changed")
            deprecated_count = sum(1 for r in results if r["status"] == "deprecated")
            inconclusive_count = sum(1 for r in results if r["status"] == "inconclusive")
            print(f"\nVerification Summary ({len(results)} audited):")
            print(f"  Active: {active_count} · Changed: {changed_count} · Deprecated: {deprecated_count} · Inconclusive: {inconclusive_count}")

            for r in results:
                if r["status"] in ("changed", "deprecated") or r.get("review_required"):
                    contradictions.append(f"*{r['provider']}* [{r['route']}/{r['status'].upper()}]: {r['summary']}")

        if args.apply:
            issues = audit_catalog_quality(catalog)
            if issues:
                raise RuntimeError(f"Post-run catalog quality audit failed: {issues[:5]}")

            today = date.today().isoformat()
            catalog["verified"] = today
            save_json_atomic(PROVIDERS_PATH, catalog)
            print(f"\n✓ Saved verified catalog to {PROVIDERS_PATH} (0 quality audit issues)")

            duration_now = round(time.time() - t0, 2)
            summary_payload = {
                "run_id": run_id,
                "entry_point": entry_point,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "model_primary": MODEL_CASCADE[0],
                "web_agent": "antigravity-preview-09-2026",
                "duration_s": duration_now,
                "providers_total": len(catalog.get("providers", [])),
                "models_total": sum(len(p.get("models", [])) for p in catalog.get("providers", [])),
                "audited_count": len(results),
                "routes": _summarize_routes(results),
                "candidates_queued": len(discovered),
                "results": results,
            }
            save_json_atomic(SUMMARY_PATH, summary_payload)
            print(f"✓ Saved run telemetry summary to {SUMMARY_PATH}")

            if not args.skip_rebuild:
                build_and_verify_site()

        flush_res = tracer.flush()
        print(f"Arize Cloud Telemetry: {flush_res}")

        duration = time.time() - t0
        print(f"\n=== Completed in {duration:.1f}s ===")

        if send_slack:
            notify_job_completed(
                duration_s=duration,
                verified_count=len(results),
                active_count=sum(1 for r in results if r["status"] == "active"),
                changed_count=sum(1 for r in results if r["status"] == "changed"),
                deprecated_count=sum(1 for r in results if r["status"] == "deprecated"),
                inconclusive_count=sum(1 for r in results if r["status"] == "inconclusive"),
                discovered_count=len(discovered),
                contradictions=contradictions,
            )

    except Exception as e:
        tracer.flush()
        if send_slack or (args.apply and not args.no_slack):
            notify_job_failed(str(e), stage="Execution")
        raise


if __name__ == "__main__":
    main()
