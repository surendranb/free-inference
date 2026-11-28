"""Catalog Verifier: Reason over full 3-route observations using gemini-3.5-flash-lite."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
import json
import threading
import time
from typing import Any, Dict, List, Optional

from core.intake import (
    acquire_observation,
    fetch_web_route_antigravity,
    is_router_model,
    normalize_model_key,
    resolve_route,
)
from core.model import call_with_self_correction, get_api_key
from core.telemetry import classify_http_status, tracer

ALLOWED_FREE_TYPES = {
    "Rate-limited free",
    "Rate-limited free (Free Trial)",
    "Rate-limited free (Experiment)",
    "Promo free",
    "Promo free (limited time)",
    "Trial credits",
    "Free Developer Tier",
    "Permanent $0",
    "Trial / Free tokens",
}

VERIFIER_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "status": {
            "type": "STRING",
            "enum": ["active", "changed", "deprecated", "inconclusive"],
        },
        "is_free_active": {"type": "BOOLEAN"},
        "payment_method_required": {"type": "BOOLEAN"},
        "free_type": {"type": "STRING"},
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
                    "tpd": {"type": "STRING"},
                },
                "required": ["name", "cost", "context"],
            },
        },
        "notes": {"type": "STRING"},
        "summary": {"type": "STRING"},
    },
    "required": ["status", "is_free_active", "models", "summary"],
}


def _expected_priced_feed_keys(obs: Optional[Dict[str, Any]]) -> set[str]:
    if not obs or obs.get("route") != "feed":
        return set()
    payload = obs.get("payload") or {}
    if not payload.get("priced"):
        return set()
    return {
        normalize_model_key(m.get("id") or m.get("name", ""))
        for m in payload.get("free_models", [])
        if isinstance(m, dict) and (m.get("id") or m.get("name"))
    }


def validate_verification_output(data: dict, obs: Optional[Dict[str, Any]] = None) -> Optional[str]:
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
    ft = data.get("free_type")
    if ft and ft not in ALLOWED_FREE_TYPES:
        return f"free_type '{ft}' must be one of {sorted(ALLOWED_FREE_TYPES)}"

    expected = _expected_priced_feed_keys(obs)
    if expected and status in ("active", "changed") and data.get("is_free_active"):
        got = {
            normalize_model_key(m.get("name", ""))
            for m in data.get("models", [])
            if isinstance(m, dict) and m.get("name")
        }
        missing = sorted(expected - got)
        if missing:
            return (
                f"Priced feed returned {len(expected)} canonical free models, but your output missed "
                f"{len(missing)} of them ({missing[:5]}). Include EVERY non-duplicate item from payload.free_models."
            )
    return None


def _build_reason_prompt(provider: Dict[str, Any], obs: Dict[str, Any]) -> str:
    route = obs["route"]
    pname = provider.get("name", "Unknown")
    existing = provider.get("models", [])

    route_rules = {
        "feed": (
            "ROUTE 1 (FEED): Check `payload.priced`. "
            "If `payload.priced` is true (OpenRouter, Kilo, Requesty, Nous), EVERY entry in `payload.free_models` ALREADY passed `$0`/free pricing check: "
            "you MUST include EVERY distinct model using its exact canonical `id` (deduplicate `:free` vs bare ID twins if twice; "
            "preserve existing `rpm`/`tpm`/`rpd`/`tpd` where feed omits limits). "
            "If `payload.priced` is false (unpriced gateway like OVHcloud), `payload.available_models` lists available endpoints without pricing: "
            "verify free-tier scope against `docs_text` & existing catalog carefully and avoid blindly dumping paid-only TTS/ASR/Embedding endpoints as $0."
        ),
        "api": (
            "ROUTE 2 (API): Cross-check every live model in `payload` against `docs_text` (e.g. pricing & rate-limit tables). "
            "Include ONLY models confirmed eligible for $0/free developer access (e.g. Google `Free of charge` in Free Tier table — strictly EXCLUDE models documented as `'not available on the Free tier'` like Argon/Carbon/Neon; ADD newly confirmed Free Tier models like `gemini-4-hydrogen`; REMOVE retired models absent from `payload` UNLESS docs explain temporary allowance). "
            "For account-allowance APIs (e.g. Synap where `/v1/models` marks `is_free: false` while `/api/account/free-tier` grants a $0 daily token allowance), preserve the active free model and exact allowance cost/limits."
        ),
        "web": (
            "ROUTE 3 (WEBSITE via Antigravity Cloud Agent): Analyze `docs_text` gathered live from Google Chrome. "
            "Check whether $0 developer/free access is active, note any card requirement or trial credit changes, and "
            "compare models and rate limits against baseline. Do NOT omit valid cataloged models just because `docs_text` "
            "only sampled a subset; return the full confirmed list or `models: []` when `status == 'active'` with unchanged models."
        ),
    }[route]

    return (
        f"You are the catalog verification reasoning engine for FreeInference.dev.\n"
        f"{route_rules}\n\n"
        f"PROVIDER: {pname}\n"
        f"Current Catalog Entry:\n"
        f"- free_type: {provider.get('free_type')}\n"
        f"- payment_method_required / notes: {provider.get('notes', '')}\n"
        f"- existing_models ({len(existing)}): {json.dumps(existing, ensure_ascii=False)}\n\n"
        f"LATEST ACQUIRED TRUTH ({route.upper()}):\n"
        f"source_urls: {obs.get('source_urls', [])}\n"
        f"payload:\n{json.dumps(obs.get('payload', {}), ensure_ascii=False)}\n\n"
        f"docs_text:\n{obs.get('docs_text', '')}\n\n"
        "Instructions:\n"
        "1. Set `status`: 'active' (confirmed active, no meaningful change), 'changed' (models/quotas/credits/card policy updated), "
        "'deprecated' (explicitly discontinued/paywalled with zero free access), or 'inconclusive' (insufficient/blocked evidence).\n"
        "2. Populate `models` with canonical `name`, `cost` (e.g. '$0', '$0 ($5 trial credits)', '$0 (100,000 tokens/day account allowance)'), "
        "`context`, and `rpm`/`tpm`/`rpd`/`tpd`. Preserve existing model quota strings whenever upstream leaves them unpublished.\n"
        "3. Do NOT output meta-routers (`openrouter/free`, `kilo-auto/*`) or duplicate display names alongside slug IDs.\n"
        "4. Write a concise 1-2 sentence `summary` explaining what was verified or what changed."
    )


def _dedup_and_merge_models(
    proposed_models: List[Dict[str, Any]],
    existing_models: List[Dict[str, Any]],
    today: str,
) -> List[Dict[str, Any]]:
    """Normalize IDs, strip routers, deduplicate twins, and inherit preserved quotas."""
    old_by_exact = {str(m.get("name", "")).lower().strip(): m for m in existing_models}
    old_by_norm = {normalize_model_key(m.get("name", "")): m for m in existing_models if m.get("name")}

    seen_norm: Dict[str, Dict[str, Any]] = {}
    ordered_keys: List[str] = []

    for m in proposed_models:
        if not isinstance(m, dict):
            continue
        raw_name = str(m.get("name") or "").strip()
        if not raw_name or is_router_model({"id": raw_name, "name": raw_name}):
            continue

        norm = normalize_model_key(raw_name)
        if not norm:
            continue

        # Prefer canonical slug IDs (with "/" or ":free") if twin display title collides
        if norm in seen_norm:
            prev_name = seen_norm[norm]["name"]
            if ("/" in raw_name or ":free" in raw_name) and "/" not in prev_name:
                seen_norm[norm]["name"] = raw_name
            continue

        old = old_by_exact.get(raw_name.lower()) or old_by_norm.get(norm) or {}
        cost = str(m.get("cost") or "").strip() or old.get("cost") or "$0"
        if cost == "$0" and old.get("cost", "").startswith("$0 (") and "allowance" in old.get("cost", ""):
            cost = old["cost"]

        merged = {
            "name": raw_name,
            "cost": cost,
            "context": _pick_metric(m.get("context"), old.get("context"), "Not published"),
            "rpm": _pick_metric(m.get("rpm"), old.get("rpm"), "Not published"),
            "tpm": _pick_metric(m.get("tpm"), old.get("tpm"), "Not published"),
            "rpd": _pick_metric(m.get("rpd"), old.get("rpd"), "Not published"),
            "tpd": _pick_metric(m.get("tpd"), old.get("tpd"), "Not published"),
            "verified": today,
        }
        seen_norm[norm] = merged
        ordered_keys.append(norm)

    return [seen_norm[k] for k in ordered_keys]


def _pick_metric(new_val: Any, old_val: Any, fallback: str) -> str:
    s_new = str(new_val or "").strip()
    s_old = str(old_val or "").strip()
    placeholder = {"", "not published", "unknown", "none", "n/a"}
    if s_new and s_new.lower() not in placeholder:
        return s_new
    if s_old and s_old.lower() not in placeholder:
        return s_old
    return s_new or s_old or fallback


def apply_write_gate(
    provider: Dict[str, Any],
    obs: Dict[str, Any],
    verdict: Dict[str, Any],
    today: str,
    apply_updates: bool,
) -> Dict[str, Any]:
    """Enforce strict integrity gates before mutating a provider in data/providers.json."""
    route = obs["route"]
    status = verdict.get("status", "inconclusive")
    is_free = bool(verdict.get("is_free_active"))
    old_models = list(provider.get("models", []))
    proposed = verdict.get("models") or []

    outcome = {
        "write_applied": False,
        "review_required": False,
        "review_reason": "",
        "models_before": len(old_models),
        "models_after": len(old_models),
    }

    if not obs.get("ok") or status == "inconclusive":
        return outcome

    # Single-run deprecation / non-free flag never wipes catalog state silently
    if status == "deprecated" or not is_free:
        outcome["review_required"] = True
        outcome["review_reason"] = "Deprecation or suspended free tier flagged; preserved catalog pending corroboration."
        return outcome

    merged_models = _dedup_and_merge_models(proposed, old_models, today)

    # Guard priced feeds against partial LLM omissions (e.g. Kilo 15 -> 1 truncation)
    expected_feed = _expected_priced_feed_keys(obs)
    if expected_feed:
        got_feed = {normalize_model_key(m["name"]) for m in merged_models}
        missing_feed = expected_feed - got_feed
        if missing_feed:
            outcome["review_required"] = True
            outcome["review_reason"] = (
                f"Priced feed completeness check failed: missing {len(missing_feed)}/{len(expected_feed)} live feed models; blocked."
            )
            return outcome

    # Anomaly guard: block suspicious >50% model shrink on web route unless corroborated
    if route == "web" and len(old_models) >= 2 and merged_models and len(merged_models) < len(old_models) * 0.5:
        outcome["review_required"] = True
        outcome["review_reason"] = (
            f"Web verdict proposed shrinking models from {len(old_models)} to {len(merged_models)}; blocked by Write Gate."
        )
        return outcome

    # Prevent active verification from accidentally emptying a provider's model table
    final_models = merged_models if merged_models else [
        {**m, "verified": today} for m in old_models
    ]
    if not final_models:
        outcome["review_required"] = True
        outcome["review_reason"] = "Verdict yielded 0 models while claiming free tier active; blocked."
        return outcome

    outcome["models_after"] = len(final_models)
    if not apply_updates:
        return outcome

    provider["models"] = final_models
    provider["verified"] = today
    provider["verified_method"] = "live-probe" if route in ("feed", "api") else "docs"
    if verdict.get("free_type") in ALLOWED_FREE_TYPES:
        provider["free_type"] = verdict["free_type"]
    if verdict.get("notes") and str(verdict["notes"]).strip():
        provider["notes"] = str(verdict["notes"]).strip()
    outcome["write_applied"] = True
    return outcome


def verify_provider(
    provider: Dict[str, Any],
    key: Optional[str] = None,
    apply_updates: bool = False,
    today: Optional[str] = None,
    trace_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Acquire full route observation, reason with gemini-3.5-flash-lite, apply Write Gate, emit span."""
    today = today or date.today().isoformat()
    pname = provider.get("name", "Unknown")
    route = resolve_route(provider)
    t0 = time.time()

    obs = acquire_observation(provider, gemini_key=key)
    acq_mode = (obs.get("agent_meta") or {}).get("acquisition_mode") or obs.get("route", route)

    def _reason(cur_obs: Dict[str, Any]) -> Dict[str, Any]:
        prompt = _build_reason_prompt(provider, cur_obs)
        return call_with_self_correction(
            prompt,
            VERIFIER_SCHEMA,
            lambda d: validate_verification_output(d, obs=cur_obs),
            key=key,
        )

    if not obs.get("ok"):
        verdict = {
            "status": "inconclusive",
            "is_free_active": None,
            "models": [],
            "summary": f"{route} acquisition failed ({obs.get('error_code')}): {obs.get('docs_text', '')[:160]}",
        }
    else:
        verdict = _reason(obs)
        # Escalate seamlessly from llms.txt/.md -> Chrome only when machine docs are inconclusive
        if acq_mode == "llms_md" and verdict.get("status") == "inconclusive" and key:
            chrome_obs = fetch_web_route_antigravity(provider, gemini_key=key)
            acq_mode = "llms_then_chrome"
            obs = chrome_obs
            if chrome_obs.get("ok"):
                verdict = _reason(chrome_obs)
            else:
                verdict = {
                    "status": "inconclusive",
                    "is_free_active": None,
                    "models": [],
                    "summary": f"llms.txt inconclusive; Chrome failed ({chrome_obs.get('error_code')}): {chrome_obs.get('docs_text', '')[:120]}",
                }

    gate = apply_write_gate(provider, obs, verdict, today, apply_updates=apply_updates)
    t1 = time.time()

    status = verdict.get("status", "inconclusive")
    if gate["review_required"] and status != "deprecated":
        status = "inconclusive"

    agent_meta = {**(obs.get("agent_meta") or {}), "acquisition_mode": acq_mode}
    if trace_id:
        tracer.log_span(
            trace_id=trace_id,
            name=f"verify.{pname}",
            start_time_s=t0,
            end_time_s=t1,
            attributes={
                "provider": pname,
                "route": route,
                "acquisition_mode": acq_mode,
                "status_class": classify_http_status(obs.get("http_status"), obs.get("error_code")),
                "verdict": status,
                "write_applied": gate["write_applied"],
                "review_required": gate["review_required"],
                "models_before": gate["models_before"],
                "models_after": gate["models_after"],
                "agent.interaction_id": agent_meta.get("interaction_id"),
                "agent.steps": agent_meta.get("steps"),
                "agent.total_tokens": agent_meta.get("total_tokens"),
            },
            status_ok=bool(obs.get("ok") and status != "inconclusive"),
            status_message="" if obs.get("ok") else str(obs.get("error_code") or "error"),
        )

    return {
        "provider": pname,
        "route": route,
        "channel": route,
        "acquisition_mode": acq_mode,
        "status": status,
        "is_free_active": verdict.get("is_free_active"),
        "payment_method_required": verdict.get("payment_method_required"),
        "summary": gate["review_reason"] or verdict.get("summary", ""),
        "error_code": obs.get("error_code"),
        "write_applied": gate["write_applied"],
        "review_required": gate["review_required"],
        "models_before": gate["models_before"],
        "models_after": gate["models_after"],
        "agent_meta": agent_meta,
        "audited_date": today,
        "duration_s": round(t1 - t0, 2),
    }


def audit_catalog_quality(catalog_data: dict) -> List[str]:
    """Validate structural invariants & uniqueness required by build.py."""
    issues: List[str] = []
    req_p = {"name", "url", "free_type", "verified", "verified_method", "models"}
    req_m = {"name", "cost", "context", "rpm", "tpm", "rpd", "tpd", "verified"}
    for p in catalog_data.get("providers", []):
        pname = p.get("name", "<unknown>")
        missing_p = req_p - set(p)
        if missing_p:
            issues.append(f"{pname}: missing provider keys {sorted(missing_p)}")
        if p.get("verified_method") not in ("live-probe", "api", "docs"):
            issues.append(f"{pname}: invalid verified_method {p.get('verified_method')!r}")
        models = p.get("models") or []
        if not models:
            issues.append(f"{pname}: 0 cataloged models")
        seen = set()
        for m in models:
            missing_m = req_m - set(m)
            if missing_m:
                issues.append(f"{pname}/{m.get('name', '?')}: missing model keys {sorted(missing_m)}")
            key = str(m.get("name", "")).lower().strip()
            if key in seen:
                issues.append(f"{pname}: duplicate model entry '{m.get('name')}'")
            seen.add(key)
    return issues


def verify_catalog(
    catalog_data: dict,
    apply_updates: bool = False,
    limit: Optional[int] = None,
    force_all: bool = False,
    key: Optional[str] = None,
    route_filter: Optional[str] = None,
    provider_filter: Optional[str] = None,
    max_workers: int = 6,
    trace_id: Optional[str] = None,
) -> List[dict]:
    """Verify catalog providers dispatched across Route 1 (feed), Route 2 (api), Route 3 (web)."""
    today = date.today().isoformat()
    api_key = key or get_api_key()
    tid = trace_id or tracer.start_trace("freeinference.verify_catalog")

    targets: List[Dict[str, Any]] = []
    for p in catalog_data.get("providers", []):
        pname = p.get("name", "Unknown")
        route = resolve_route(p)
        if route_filter and route != route_filter:
            continue
        if provider_filter and provider_filter.lower() not in pname.lower():
            continue
        if not force_all and not provider_filter and p.get("verified") == today and p.get("verified_method") == "live-probe":
            continue
        if apply_updates and resolve_route(p) != p.get("channel") and route in ("feed", "api", "web"):
            p["channel"] = route
        targets.append(p)
        if limit is not None and len(targets) >= limit:
            break

    fast_targets = [p for p in targets if resolve_route(p) in ("feed", "api")]
    web_targets = [p for p in targets if resolve_route(p) == "web"]

    results_by_name: Dict[str, dict] = {}
    total = len(targets)
    completed = 0
    print_lock = threading.Lock()

    def _run_one(prov: Dict[str, Any], stagger_s: float = 0.0) -> dict:
        if stagger_s > 0:
            time.sleep(stagger_s)
        res = verify_provider(prov, key=api_key, apply_updates=apply_updates, today=today, trace_id=tid)
        nonlocal completed
        with print_lock:
            completed += 1
            m_info = f"{res['models_before']}->{res['models_after']}"
            mode = res.get("acquisition_mode", res["route"])
            print(f"[{completed}/{total}] {res['provider']} ({res['route']}/{mode}) -> {res['status']} ({m_info}, {res['duration_s']}s): {res['summary'][:85]}")
        return res

    # Route 1 & 2 run fast first
    for p in fast_targets:
        r = _run_one(p)
        results_by_name[p["name"]] = r

    # Route 3 (llms.txt/.md parallel fast-path, Chrome gated cleanly by _CHROME_SEMAPHORE(2))
    if web_targets:
        workers = min(max_workers, len(web_targets))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futs = {
                pool.submit(_run_one, p, 0.0): p
                for p in web_targets
            }
            for fut in as_completed(futs):
                p = futs[fut]
                try:
                    results_by_name[p["name"]] = fut.result()
                except Exception as e:
                    results_by_name[p["name"]] = {
                        "provider": p["name"],
                        "route": "web",
                        "channel": "web",
                        "status": "inconclusive",
                        "is_free_active": None,
                        "summary": f"Unhandled worker exception: {e}",
                        "audited_date": today,
                        "duration_s": 0.0,
                        "write_applied": False,
                        "review_required": False,
                        "models_before": len(p.get("models", [])),
                        "models_after": len(p.get("models", [])),
                    }

    if trace_id is None:
        flush_res = tracer.flush()
        if flush_res.get("status") == "ok":
            print(f"  Telemetry: exported {flush_res.get('spans_exported')} spans to Arize Cloud")

    return [results_by_name[p["name"]] for p in targets if p["name"] in results_by_name]
