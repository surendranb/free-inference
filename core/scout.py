"""Task 2: Frontier Scout (Look For New Providers)."""

from datetime import date
import json
from pathlib import Path
from typing import Dict, List, Optional
import urllib.request

from core.intake import UA, fetch_web
from core.model import call_with_self_correction, get_api_key

CANDIDATE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "is_valid_free_tier": {"type": "BOOLEAN"},
        "provider_name": {"type": "STRING"},
        "free_tier_type": {
            "type": "STRING",
            "enum": ["Rate-limited free", "Trial credits", "Promo free", "None"]
        },
        "summary": {"type": "STRING"}
    },
    "required": ["is_valid_free_tier", "provider_name", "free_tier_type", "summary"]
}


def validate_candidate_output(data: dict) -> Optional[str]:
    """Validate candidate evaluation output."""
    if not isinstance(data, dict):
        return "Must be JSON object"
    if not isinstance(data.get("is_valid_free_tier"), bool):
        return "is_valid_free_tier must be boolean"
    if not data.get("provider_name"):
        return "provider_name required"
    if not data.get("summary"):
        return "summary required"
    return None


def scout_openrouter_free_models(catalog_data: dict) -> List[dict]:
    """Scan OpenRouter API for uncataloged free models."""
    existing_providers = {p["name"].lower() for p in catalog_data.get("providers", [])}
    existing_models = set()
    for p in catalog_data.get("providers", []):
        for m in p.get("models", []):
            existing_models.add(m.get("name", "").lower())

    url = "https://openrouter.ai/api/v1/models"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
    except Exception as e:
        print(f"Notice: OpenRouter scout fetch failed: {e}")
        return []

    candidates = []
    for m in data.get("data", []):
        mid = m.get("id", "")
        pricing = m.get("pricing", {})
        prompt_cost = float(pricing.get("prompt", 0) or 0)
        comp_cost = float(pricing.get("completion", 0) or 0)
        if ":free" in mid or (prompt_cost == 0 and comp_cost == 0):
            mname = m.get("name", mid)
            if mname.lower() not in existing_models:
                candidates.append({
                    "id": mid,
                    "name": mname,
                    "context_length": m.get("context_length"),
                    "source": "OpenRouter API"
                })
    return candidates


def evaluate_candidate(name: str, url: str, key: str = None) -> dict:
    """Evaluate whether a discovered candidate offers a genuine developer free tier."""
    page_text = fetch_web(url, key=key)
    prompt = f"""You are the frontier scout for FreeInference.dev.
Evaluate this newly discovered candidate provider:

Provider: {name}
Website: {url}
Raw Content:
{page_text[:3000]}

Determine:
1. Does this provider offer a genuine $0 developer API tier (or free trial credits without mandatory credit card)?
2. If yes, classify the free tier type (Rate-limited free, Trial credits, Promo free).
3. If it is paid-only, enterprise-only, or lacks an API, mark is_valid_free_tier as false.
"""
    return call_with_self_correction(
        prompt,
        CANDIDATE_SCHEMA,
        validate_candidate_output,
        key=key
    )


def scout_frontier(catalog_data: dict, apply_updates: bool = False, key: str = None) -> List[dict]:
    """Task 2: Discover new free models and providers."""
    api_key = key or get_api_key()
    discovered_models = scout_openrouter_free_models(catalog_data)
    print(f"--> Frontier Scout: found {len(discovered_models)} uncataloged free models on OpenRouter.")

    verified_candidates = []
    if apply_updates and discovered_models:
        candidates_file = Path("data/candidates.json")
        candidates_file.parent.mkdir(parents=True, exist_ok=True)
        candidates_file.write_text(json.dumps(discovered_models, indent=2) + "\n")
        print(f"  ✓ Saved {len(discovered_models)} candidate models to {candidates_file}")

    return discovered_models
