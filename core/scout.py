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
    existing_models = set()
    for p in catalog_data.get("providers", []):
        for m in p.get("models", []):
            existing_models.add(m.get("name", "").lower().replace(":free", "").strip())
            existing_models.add(m.get("name", "").lower().strip())

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
            norm_name = mname.lower().replace(":free", "").strip()
            norm_id = mid.lower().replace(":free", "").strip()
            if norm_name not in existing_models and norm_id not in existing_models:
                candidates.append({
                    "id": mid,
                    "name": mname,
                    "provider": "OpenRouter",
                    "provider_id": "openrouter",
                    "context_length": m.get("context_length"),
                    "output_limit": None,
                    "reasoning": False,
                    "tool_call": True,
                    "source": "OpenRouter API"
                })
    return candidates


def scout_models_dev_free_models(catalog_data: dict) -> List[dict]:
    """Scan Models.dev API (235 providers) for uncataloged zero-cost models."""
    existing_models = set()
    for p in catalog_data.get("providers", []):
        for m in p.get("models", []):
            existing_models.add(m.get("name", "").lower().replace(":free", "").strip())
            existing_models.add(m.get("name", "").lower().strip())

    url = "https://models.dev/api.json"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.load(r)
    except Exception as e:
        print(f"Notice: Models.dev scout fetch failed: {e}")
        return []

    candidates = []
    for pid, pdata in data.items():
        pname = pdata.get("name", pid)
        doc_url = pdata.get("doc") or ""
        api_url = pdata.get("api") or ""
        models = pdata.get("models", {})
        for mid, mdata in models.items():
            cost = mdata.get("cost", {})
            inp_cost = cost.get("input", None)
            out_cost = cost.get("output", None)
            status = mdata.get("status", "active")
            if inp_cost == 0 and out_cost == 0 and status != "deprecated":
                mname = mdata.get("name", mid)
                norm_m = mname.lower().replace(":free", "").strip()
                norm_id = mid.lower().replace(":free", "").strip()
                if norm_m not in existing_models and norm_id not in existing_models:
                    candidates.append({
                        "id": mid,
                        "name": mname,
                        "provider": pname,
                        "provider_id": pid,
                        "context_length": mdata.get("limit", {}).get("context"),
                        "output_limit": mdata.get("limit", {}).get("output"),
                        "reasoning": bool(mdata.get("reasoning", False)),
                        "tool_call": bool(mdata.get("tool_call", False)),
                        "structured_output": bool(mdata.get("structured_output", False)),
                        "open_weights": bool(mdata.get("open_weights", False)),
                        "modalities": mdata.get("modalities", {}),
                        "doc": doc_url,
                        "api": api_url,
                        "source": "Models.dev API"
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
    """Task 2: Discover new free models and providers across OpenRouter and Models.dev."""
    api_key = key or get_api_key()

    openrouter_candidates = scout_openrouter_free_models(catalog_data)
    print(f"--> Frontier Scout: found {len(openrouter_candidates)} uncataloged free models on OpenRouter.")

    models_dev_candidates = scout_models_dev_free_models(catalog_data)
    print(f"--> Frontier Scout: found {len(models_dev_candidates)} uncataloged zero-cost models across Models.dev.")

    # Combine and deduplicate
    seen_keys = set()
    combined = []
    for c in openrouter_candidates + models_dev_candidates:
        key = (c.get("provider", "").lower(), c.get("name", "").lower().replace(":free", "").strip())
        if key not in seen_keys:
            seen_keys.add(key)
            combined.append(c)

    print(f"--> Frontier Scout Total: {len(combined)} unique candidate free models queued.")

    if apply_updates and combined:
        candidates_file = Path("data/candidates.json")
        candidates_file.parent.mkdir(parents=True, exist_ok=True)
        candidates_file.write_text(json.dumps(combined, indent=2) + "\n")
        print(f"  ✓ Saved {len(combined)} candidate models to {candidates_file}")

    return combined
