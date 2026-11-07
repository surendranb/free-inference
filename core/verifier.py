"""Task 1: Catalog Verifier (Update What We Know)."""

from datetime import date
import json
from pathlib import Path
from typing import Dict, List, Optional

from core.intake import fetch_api, fetch_feed, fetch_web
from core.model import call_with_self_correction, get_api_key

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
                    "context": {"type": "STRING"}
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
    """Verify an individual catalog provider against live data."""
    pname = provider.get("name", "Unknown")
    channel = (provider.get("channel") or "web").lower()
    if channel not in ("api", "feed", "web"):
        channel = "web"

    # Determine target URL
    primary_url = provider.get("url", "")
    docs_url = provider.get("docs_url", "")
    base_url = provider.get("base_url", "")

    if channel == "api":
        target_url = base_url or primary_url
        if "/models" not in target_url and not target_url.endswith("/v1"):
            target_url = target_url.rstrip("/") + "/models"
        elif target_url.endswith("/v1"):
            target_url = target_url + "/models"
        raw_data = fetch_api(target_url, key=key)
    elif channel == "feed":
        target_url = provider.get("feed_url") or primary_url
        raw_data = fetch_feed(target_url)
    else:
        target_url = docs_url or primary_url
        raw_data = fetch_web(target_url, key=key)

    existing_models = [m.get("name") for m in provider.get("models", [])]
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
{raw_data[:3000]}

Task: Determine what changed between our catalog and the latest live data:
1. Is the $0 developer free tier confirmed active?
2. Are all existing cataloged models still offered, or were any removed or added?
3. If the page is blocked, inconclusive, or requires an authenticated login, mark status as "inconclusive".
4. If the free tier is explicitly discontinued, mark status as "deprecated".
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
    key: Optional[str] = None
) -> List[dict]:
    """Task 1: Verify all catalog providers."""
    today = date.today().isoformat()
    api_key = key or get_api_key()
    results = []
    audited = 0

    providers = list(catalog_data.get("providers", []))
    for p in providers:
        if limit is not None and audited >= limit:
            break

        pname = p.get("name", "Unknown")
        # Skip if already verified today via live-probe unless force_all
        if not force_all and p.get("verified") == today and p.get("verified_method") == "live-probe":
            continue

        print(f"--> Verifying {pname} ({p.get('channel', 'web')})...")
        res = verify_provider(p, key=api_key)
        audited += 1

        status = res.get("status", "inconclusive")
        is_free = res.get("is_free_active", False)
        summary = res.get("summary", "")

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
            p["verified_method"] = "live-probe" if p.get("channel") == "api" else "docs"
            for m in p.get("models", []):
                m.setdefault("cost", "$0")
                m.setdefault("context", "Not published")
                m.setdefault("rpm", "Not published")
                m.setdefault("tpm", "Not published")
                m.setdefault("rpd", "Not published")
                m.setdefault("tpd", "Not published")
                m["verified"] = today
            print(f"  ✓ Active: updated verification to {today}")
        elif status == "deprecated":
            print(f"  ⚠ Deprecation flagged: {summary}")
            print(f"  --> Preserving catalog entry. Human review required.")
        else:
            print(f"  Notice: Inconclusive/retained: {summary[:80]}")

    return results
