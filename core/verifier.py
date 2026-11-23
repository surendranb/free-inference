"""Task 1: Catalog Verifier (Update What We Know)."""

from datetime import date
import json
from pathlib import Path
import time
from typing import Dict, List, Optional

from core.intake import fetch_api, fetch_feed, fetch_web, verify_source_with_antigravity
from core.model import call_with_self_correction, get_api_key
from probe import DETERMINISTIC_SYNCS

VERIFIER_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "status": {
            "type": "STRING",
            "enum": ["active", "changed", "deprecated", "inconclusive"]
        },
        "is_free_active": {"type": "BOOLEAN"},
        "models": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "cost": {"type": "STRING"},
                    "context": {"type": "STRING"},
                    "rpm": {"type": "STRING"},
                    "tpm": {"type": "STRING"},
                    "rpd": {"type": "STRING"},
                    "tpd": {"type": "STRING"}
                },
                "required": ["name", "cost"]
            }
        },
        "summary": {"type": "STRING"}
    },
    "required": ["status", "is_free_active", "models", "summary"]
}


def validate_verification_output(data: dict) -> Optional[str]:
    """Semantic validator for self-correction loop."""
    if not isinstance(data, dict):
        return "Output must be a JSON object"
    status = data.get("status")
    if status not in ("active", "changed", "deprecated", "inconclusive"):
        return f"Invalid status: {status}"
    if not isinstance(data.get("is_free_active"), bool):
        return "is_free_active must be a boolean"
    if not isinstance(data.get("summary"), str) or not data["summary"].strip():
        return "summary must be a non-empty string"
    if not isinstance(data.get("models"), list):
        return "models must be a list"
    return None


def verify_provider(provider: dict, key: str = None) -> dict:
    """Verify an individual catalog provider against live ground truth (one source at a time)."""
    pname = provider.get("name", "Unknown")
    channel = (provider.get("channel") or "web").lower()
    if channel not in ("api", "feed", "web"):
        channel = "web"

    # Determine target URL
    primary_url = provider.get("url", "")
    docs_url = provider.get("docs_url", "")
    base_url = provider.get("base_url", "")
    existing_models = [m.get("name") for m in provider.get("models", [])]

    # For web/docs sources: invoke Antigravity Managed Agent driving Google Chrome in cloud sandbox
    if channel == "web":
        agent_key = key or get_api_key()
        if agent_key:
            res = verify_source_with_antigravity(provider, key=agent_key)
            if res and res.get("status") in ("active", "changed", "deprecated"):
                return res
            if res and res.get("status") == "inconclusive" and res.get("summary"):
                # Antigravity agent encountered a challenge/block or timeout
                return res

    if channel == "api":
        target_url = base_url or primary_url
        if "/models" not in target_url and not target_url.endswith("/v1"):
            target_url = target_url.rstrip("/") + "/models"
        elif target_url.endswith("/v1"):
            target_url = target_url + "/models"
        raw_data = fetch_api(target_url, key=key)
        if "HTTP Error 401" in raw_data or "HTTP Error 403" in raw_data:
            return {
                "status": "inconclusive",
                "is_free_active": True,
                "models": [{"name": m, "cost": "$0"} for m in existing_models],
                "summary": f"Target API endpoint {target_url} requires authenticated API key credentials. Preserved existing catalog entry without modification."
            }
    elif channel == "feed":
        target_url = provider.get("feed_url") or primary_url
        raw_data = fetch_feed(target_url)
    else:
        target_url = docs_url or primary_url
        raw_data = fetch_web(target_url, key=key)

    prompt = f"""You are the catalog verification auditor for FreeInference.dev.
Compare our EXISTING catalog data against the LATEST LIVE DATA retrieved from the provider.

Provider: {pname}
Native Modality: {channel.upper()}
Target URL: {target_url}

EXISTING CATALOG DATA:
- Free Tier Type: {provider.get('free_type')}
- Cataloged Free Models: {existing_models}
- Documented Notes: {provider.get('notes', '')}

LATEST LIVE DATA:
{raw_data[:3500]}

Task: Rigorously audit for any CONTRADICTIONS, CHANGES, or CONFIRMATIONS:
1. Is the $0 developer free tier confirmed active, or is there a contradiction (e.g. requires card/subscription, trial credit expired, service discontinued)?
2. Model comparison:
   - Were any cataloged models deprecated, renamed, or dropped?
   - Were new free models added?
   - Any contradictory rate limits, context caps, or restrictions mentioned?
3. Status rules:
   - "active": Free tier active and models verified without negative contradictions.
   - "changed": Confirmed change or discrepancy (new models added, models retired, quota adjustments).
   - "deprecated": Free tier explicitly discontinued or fully paywalled.
   - "inconclusive": Page blocked by Cloudflare/WAF challenge, requires login, or live data insufficient.
4. Summary: Provide an explicit 1-2 sentence audit verdict stating clearly whether contradictions were found or catalog was confirmed.
"""
    return call_with_self_correction(
        prompt,
        VERIFIER_SCHEMA,
        validate_verification_output,
        key=key
    )


def verify_catalog(
    catalog_data: dict,
    apply_updates: bool = False,
    limit: Optional[int] = None,
    force_all: bool = False,
    key: Optional[str] = None,
    target_provider: Optional[str] = None
) -> List[dict]:
    """Task 1: Verify catalog providers (one source at a time or full catalog)."""
    today = date.today().isoformat()
    api_key = key or get_api_key()
    results = []
    audited = 0

    providers = list(catalog_data.get("providers", []))
    if target_provider:
        needle = target_provider.strip().lower()
        matched = [p for p in providers if needle in p.get("name", "").lower() or needle in p.get("slug", "").lower()]
        if not matched:
            print(f"Warning: No provider found matching '{target_provider}'")
            return []
        providers = matched
        print(f"--> Filtering verification to single source: {providers[0].get('name')}")

    for p in providers:
        if limit is not None and audited >= limit:
            break

        pname = p.get("name", "Unknown")
        # Machine-checkable free tiers: the deterministic sync owns the row,
        # no LLM audit (verified_method stays a proven, not a claimed, value).
        if apply_updates and pname in DETERMINISTIC_SYNCS:
            msg = DETERMINISTIC_SYNCS[pname](p, today)
            print(f"--> Verified {pname} (deterministic): {msg}")
            results.append({
                "provider": pname, "channel": p.get("channel", "web"),
                "status": "active", "is_free_active": True,
                "summary": msg, "audited_date": today,
            })
            audited += 1
            continue

        # Skip if already verified today via live-probe unless force_all or single provider target
        if not force_all and not target_provider and p.get("verified") == today and p.get("verified_method") in ("live-probe", "antigravity-agent"):
            continue

        print(f"--> Verifying {pname} ({p.get('channel', 'web')})...")
        res = verify_provider(p, key=api_key)
        audited += 1
        time.sleep(1.0)

        status = res.get("status", "inconclusive")
        is_free = res.get("is_free_active", False)
        summary = res.get("summary", "")
        verified_models = res.get("models", [])

        entry = {
            "provider": pname,
            "channel": p.get("channel", "web"),
            "status": status,
            "is_free_active": is_free,
            "summary": summary,
            "audited_date": today
        }
        results.append(entry)

        if is_free and status in ("active", "changed") and apply_updates:
            p["verified"] = today
            p["verified_method"] = "live-probe" if p.get("channel") == "api" else "antigravity-agent"
            if status == "changed" and verified_models:
                # Update catalog with verified models
                for m in verified_models:
                    m.setdefault("cost", "$0")
                    m.setdefault("context", "Not published")
                    m.setdefault("rpm", "Not published")
                    m.setdefault("tpm", "Not published")
                    m.setdefault("rpd", "Not published")
                    m.setdefault("tpd", "Not published")
                    m["verified"] = today
                p["models"] = verified_models
                print(f"  ✓ Changed: updated {len(verified_models)} models for {pname}")
            else:
                for m in p.get("models", []):
                    m.setdefault("cost", "$0")
                    m.setdefault("context", "Not published")
                    m.setdefault("rpm", "Not published")
                    m.setdefault("tpm", "Not published")
                    m.setdefault("rpd", "Not published")
                    m.setdefault("tpd", "Not published")
                    m["verified"] = today
                print(f"  ✓ Active: updated verification to {today}")
        elif status == "deprecated" and apply_updates:
            p["free_type"] = "Deprecated"
            p["verified"] = today
            p["notes"] = f"[DEPRECATED {today}] {summary}"
            print(f"  ⚠ Deprecation recorded for {pname}: {summary}")
        else:
            print(f"  Notice: Inconclusive/retained: {summary[:80]}")

    return results
