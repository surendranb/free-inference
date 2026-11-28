"""Frontier Scout: Discover uncataloged $0 models/providers across OpenRouter & Models.dev."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import urllib.request

from core.intake import (
    UA,
    fetch_docs_static,
    fetch_web_route_antigravity,
    format_context,
    is_feed_model_free,
    is_router_model,
    normalize_model_key,
)
from core.model import call_with_self_correction, get_api_key

CANDIDATE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "is_valid_free_tier": {"type": "BOOLEAN"},
        "provider_name": {"type": "STRING"},
        "free_tier_type": {
            "type": "STRING",
            "enum": ["Rate-limited free", "Trial credits", "Promo free", "None"],
        },
        "summary": {"type": "STRING"},
    },
    "required": ["is_valid_free_tier", "provider_name", "free_tier_type", "summary"],
}


def _known_model_keys(models: List[Dict[str, Any]]) -> set[str]:
    keys = set()
    for m in models:
        raw = str(m.get("name") or "").strip()
        if raw:
            keys.add(raw.lower())
            keys.add(normalize_model_key(raw))
    return keys


def expand_base_catalog_from_sources(catalog_data: dict, apply_updates: bool = False) -> List[dict]:
    """Attach verified uncataloged $0 models from Models.dev & OpenRouter using canonical IDs."""
    from core.enricher import PROVIDER_LOGO_MAP

    our_provs = {p["name"]: p for p in catalog_data.get("providers", [])}
    expand_excludes = {"Antigravity CLI (Google)", "Google Colab", "v0 (Vercel)"}
    mdev_to_our = {
        v: k for k, v in PROVIDER_LOGO_MAP.items() if k not in expand_excludes
    }
    mdev_to_our["google"] = "Google AI Studio (Gemini API)"
    for pid in ("sambanova", "cohere", "kilo", "requesty", "nvidia", "zai", "groq", "mistral", "deepseek"):
        if pid not in mdev_to_our:
            for our_name in our_provs:
                if pid in our_name.lower():
                    mdev_to_our[pid] = our_name

    added_models: List[dict] = []
    today_iso = date.today().isoformat()

    # 1. Models.dev fanout
    try:
        req = urllib.request.Request("https://models.dev/api.json", headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            mdev = json.load(r)
    except Exception as e:
        print(f"Notice: Models.dev fetch failed: {e}")
        mdev = {}

    if isinstance(mdev, dict):
        for pid, pdata in mdev.items():
            our_pname = mdev_to_our.get(pid)
            if not our_pname or our_pname not in our_provs:
                continue
            our_p = our_provs[our_pname]
            existing = _known_model_keys(our_p.get("models", []))
            template = our_p["models"][0] if our_p.get("models") else {}

            for mid, mdata in (pdata.get("models") or {}).items():
                cost = mdata.get("cost", {})
                if cost.get("input") == 0 and cost.get("output") == 0 and mdata.get("status") != "deprecated":
                    canon_name = mid
                    display_name = mdata.get("name", mid)
                    if is_router_model({"id": canon_name, "name": display_name}):
                        continue
                    k_id = normalize_model_key(canon_name)
                    k_disp = normalize_model_key(display_name)
                    if canon_name.lower() in existing or k_id in existing or k_disp in existing:
                        continue
                    new_m = {
                        "name": canon_name if "/" in canon_name or ":" in canon_name else display_name,
                        "cost": "$0",
                        "context": format_context((mdata.get("limit") or {}).get("context")),
                        "rpm": template.get("rpm", "Published on portal"),
                        "tpm": template.get("tpm", "Not published"),
                        "rpd": template.get("rpd", "Not published"),
                        "tpd": template.get("tpd", "Not published"),
                        "verified": today_iso,
                    }
                    if apply_updates:
                        our_p.setdefault("models", []).append(new_m)
                    existing.update({new_m["name"].lower(), k_id, k_disp})
                    added_models.append({
                        "provider": our_pname,
                        "model": new_m["name"],
                        "context": new_m["context"],
                        "source": "Models.dev API",
                    })

    # 2. OpenRouter canonical ID expansion (never appends routers or display-name duplicates)
    or_p = our_provs.get("OpenRouter")
    if or_p:
        existing_or = _known_model_keys(or_p.get("models", []))
        try:
            req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                or_data = json.load(r).get("data", [])
            for m in or_data:
                if not isinstance(m, dict) or is_router_model(m) or not is_feed_model_free(m):
                    continue
                mid = str(m.get("id") or "").strip()
                if not mid:
                    continue
                mname = str(m.get("name") or mid)
                k_id = normalize_model_key(mid)
                k_name = normalize_model_key(mname)
                if mid.lower() in existing_or or k_id in existing_or or k_name in existing_or:
                    continue
                new_m = {
                    "name": mid,
                    "cost": "$0",
                    "context": format_context(m.get("context_length")),
                    "rpm": "20",
                    "tpm": "Provider-dependent",
                    "rpd": "50 (below $10 credits) / 1,000 ($10+ credits)",
                    "tpd": "Not published",
                    "verified": today_iso,
                }
                if apply_updates:
                    or_p.setdefault("models", []).append(new_m)
                existing_or.update({mid.lower(), k_id, k_name})
                added_models.append({
                    "provider": "OpenRouter",
                    "model": mid,
                    "context": new_m["context"],
                    "source": "OpenRouter API",
                })
        except Exception as e:
            print(f"Notice: OpenRouter base expansion failed: {e}")

    return added_models


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
    """Scan OpenRouter API for uncataloged free models (canonical IDs, routers excluded)."""
    existing_keys = set()
    for p in catalog_data.get("providers", []):
        existing_keys.update(_known_model_keys(p.get("models", [])))

    try:
        req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.load(r)
    except Exception as e:
        print(f"Notice: OpenRouter scout fetch failed: {e}")
        return []

    candidates = []
    for m in data.get("data", []):
        if not isinstance(m, dict) or is_router_model(m) or not is_feed_model_free(m):
            continue
        mid = str(m.get("id") or "").strip()
        mname = str(m.get("name") or mid)
        k_id = normalize_model_key(mid)
        k_name = normalize_model_key(mname)
        if mid.lower() not in existing_keys and k_id not in existing_keys and k_name not in existing_keys:
            candidates.append({
                "id": mid,
                "name": mid,
                "display_name": mname,
                "provider": "OpenRouter",
                "provider_id": "openrouter",
                "context_length": m.get("context_length"),
                "output_limit": None,
                "reasoning": False,
                "tool_call": True,
                "source": "OpenRouter API",
            })
    return candidates


def scout_models_dev_free_models(catalog_data: dict) -> List[dict]:
    """Scan Models.dev API for uncataloged zero-cost models across ecosystem providers."""
    existing_keys = set()
    cataloged_provs = {p["name"].lower() for p in catalog_data.get("providers", [])}
    for p in catalog_data.get("providers", []):
        existing_keys.update(_known_model_keys(p.get("models", [])))

    try:
        req = urllib.request.Request("https://models.dev/api.json", headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.load(r)
    except Exception as e:
        print(f"Notice: Models.dev scout fetch failed: {e}")
        return []

    candidates = []
    if not isinstance(data, dict):
        return candidates

    for pid, pdata in data.items():
        pname = pdata.get("name", pid)
        if pname.lower() in cataloged_provs:
            continue
        doc_url = pdata.get("doc") or ""
        api_url = pdata.get("api") or ""
        for mid, mdata in (pdata.get("models") or {}).items():
            if not isinstance(mdata, dict) or is_router_model({"id": mid, "name": mdata.get("name", "")}):
                continue
            cost = mdata.get("cost", {})
            if cost.get("input") == 0 and cost.get("output") == 0 and mdata.get("status") != "deprecated":
                mname = mdata.get("name", mid)
                k_id = normalize_model_key(mid)
                k_name = normalize_model_key(mname)
                if k_id not in existing_keys and k_name not in existing_keys:
                    candidates.append({
                        "id": mid,
                        "name": mname,
                        "provider": pname,
                        "provider_id": pid,
                        "context_length": (mdata.get("limit") or {}).get("context"),
                        "output_limit": (mdata.get("limit") or {}).get("output"),
                        "reasoning": bool(mdata.get("reasoning", False)),
                        "tool_call": bool(mdata.get("tool_call", False)),
                        "structured_output": bool(mdata.get("structured_output", False)),
                        "open_weights": bool(mdata.get("open_weights", False)),
                        "modalities": mdata.get("modalities", {}),
                        "doc": doc_url,
                        "api": api_url,
                        "source": "Models.dev API",
                    })
    return candidates


def evaluate_candidate(name: str, url: str, key: Optional[str] = None) -> dict:
    """Evaluate whether a discovered candidate offers a genuine $0 developer tier."""
    ok, _, text = fetch_docs_static(url)
    if not ok and key:
        obs = fetch_web_route_antigravity({"name": name, "url": url}, gemini_key=key, timeout=120)
        text = obs.get("docs_text") or text
    prompt = (
        f"Evaluate this candidate LLM inference provider for FreeInference.dev:\n"
        f"Provider: {name}\nWebsite: {url}\nDocs/Pricing Content:\n{text}\n\n"
        "Determine:\n"
        "1. Does this provider offer a genuine $0 developer API tier or free credits without mandatory paid subscription?\n"
        "2. Classify `free_tier_type`: 'Rate-limited free', 'Trial credits', 'Promo free', or 'None'.\n"
        "3. Mark `is_valid_free_tier` false if paid-only or missing a developer API."
    )
    return call_with_self_correction(prompt, CANDIDATE_SCHEMA, validate_candidate_output, key=key)


def scout_frontier(catalog_data: dict, apply_updates: bool = False, key: Optional[str] = None) -> List[dict]:
    """Discover new uncataloged free models/providers across OpenRouter & Models.dev."""
    api_key = key or get_api_key()
    openrouter_candidates = scout_openrouter_free_models(catalog_data)
    print(f"--> Frontier Scout: found {len(openrouter_candidates)} uncataloged free models on OpenRouter.")

    models_dev_candidates = scout_models_dev_free_models(catalog_data)
    print(f"--> Frontier Scout: found {len(models_dev_candidates)} uncataloged zero-cost models across Models.dev.")

    seen_keys = set()
    combined = []
    for c in openrouter_candidates + models_dev_candidates:
        ckey = (c.get("provider", "").lower(), normalize_model_key(c.get("id") or c.get("name", "")))
        if ckey not in seen_keys:
            seen_keys.add(ckey)
            combined.append(c)

    print(f"--> Frontier Scout Total: {len(combined)} unique candidate free models queued.")

    if apply_updates and combined:
        # Evaluate up to 3 uncataloged third-party providers that advertise doc URLs
        evaluated_provs: Dict[str, dict] = {}
        for c in combined:
            pname = c.get("provider", "")
            doc = c.get("doc") or ""
            if not doc or pname.lower() in evaluated_provs or pname == "OpenRouter":
                continue
            if len(evaluated_provs) >= 3:
                break
            evaluated_provs[pname.lower()] = evaluate_candidate(pname, doc, key=api_key)
        for c in combined:
            ev = evaluated_provs.get(c.get("provider", "").lower())
            if ev:
                c["evaluation"] = ev

        candidates_file = Path("data/candidates.json")
        candidates_file.parent.mkdir(parents=True, exist_ok=True)
        candidates_file.write_text(json.dumps(combined, indent=2) + "\n")
        print(f"  ✓ Saved {len(combined)} candidate models to {candidates_file}")

    return combined
