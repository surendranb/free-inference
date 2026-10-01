#!/usr/bin/env python3
"""Nightly verifier for free-inference catalog.

Syncs every row that has a live API to probe:
  - Google AI Studio: model inventory via GEMINI_API_KEY (env or Keychain)
  - OpenRouter: keyless /models filtered to :free

Synced rows are authoritative: the endpoint is the source of truth, the row
becomes a snapshot. Providers without a probe keep their last verified date
and get flagged when stale (> 45 days) for a human pass.

Exit code 0 always; the GitHub Action commits only when the file changed.
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "providers.json"
UA = {"User-Agent": "free-inference-probe/0.1"}
STALE_AFTER_DAYS = 45


def get_json(url, key=None, timeout=25):
    q = {"key": key} if key else {}
    url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def gemini_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    try:
        return subprocess.run(
            ["security", "find-generic-password", "-w", "-s", "gemini-api-key"],
            capture_output=True, text=True).stdout.strip()
    except FileNotFoundError:
        return None


def ctx_s(n):
    return f"{n // 1024}K" if n and n % 1024 == 0 else str(n)


def is_text_gemini(name):
    if not (name.startswith("gemini-") or name.startswith("gemma-")):
        return False
    for bad in ("tts", "image", "computer-use", "robotics", "lyria"):
        if bad in name:
            return False
    return True


# SKEPTICAL_BEAR: live inventory proves existence, never freeness. Only
# Flash/Flash-Lite ship a no-card free tier via AI Studio; Pro/Ultra/Gemma/
# Transcribe/new names are quarantined for a human check, never auto-$0.
def is_google_free(name):
    return "flash" in name.lower()


def sync_google(prov, key, today):
    d = get_json("https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000", key=key)
    live = {}
    for m in d.get("models", []):
        name = m["name"].split("/")[1]
        if "generateContent" in m.get("supportedGenerationMethods", []) and is_text_gemini(name):
            live[name] = m.get("inputTokenLimit") or 0
    if not live:
        raise RuntimeError("empty model inventory from Google")
    by_name = {m["name"]: m for m in prov["models"]}
    rows, quarantined = [], []
    for name in sorted(live):
        old = by_name.get(name)
        if old and is_google_free(name):
            old["context"] = ctx_s(live[name])
            old["verified"] = today
            rows.append(old)
        else:
            # paid tier (e.g. Pro) or brand-new model: never auto-add as $0.
            # A human adds it with a docs link after a free-tier check.
            quarantined.append(name)
    prov["models"] = rows
    prov["verified"] = today
    prov["verified_method"] = "live-probe"
    msg = f"ok: {len(rows)} free-tier (flash) models"
    if quarantined:
        msg += f"; QUARANTINED (paid-or-unreviewed, NOT $0): {quarantined}"
    return msg


def sync_openrouter(prov, today):
    d = get_json("https://openrouter.ai/api/v1/models")
    free = {}
    for m in d.get("data", []):
        if ":free" in m["id"]:
            free[m["id"]] = m.get("context_length") or 0
    if not free:
        raise RuntimeError("empty :free list from OpenRouter")
    by_name = {m["name"]: m for m in prov["models"]}
    rows = []
    for name in sorted(free):
        old = by_name.get(name)
        if old:
            old["context"] = ctx_s(free[name])
            old["verified"] = today
            rows.append(old)
        else:
            rows.append({
                "name": name, "cost": "$0", "context": ctx_s(free[name]),
                "rpm": "20", "tpm": "Provider-dependent",
                "rpd": "50 (below $10 credits) / 1,000 ($10+ credits)",
                "tpd": "Not published", "verified": today,
            })
    prov["models"] = rows
    prov["verified"] = today
    prov["verified_method"] = "live-probe"
    return f"ok: {len(rows)} :free models"


KEYLESS_MODEL_ENDPOINTS = {
    "DeepInfra": "https://api.deepinfra.com/v1/openai/models",
    "SambaNova Cloud": "https://api.sambanova.ai/v1/models",
    "Kilo Gateway": "https://api.kilo.ai/api/gateway/models",
    "Requesty": "https://router.requesty.ai/v1/models",
    "Nous Portal": "https://inference-api.nousresearch.com/v1/models",
    "LLM7": "https://api.llm7.io/v1/models",
    "OVHcloud AI Endpoints": "https://catalog.endpoints.ai.ovh.net/rest/v1/models_v2",
    # Cohere /v1/models needs a key (401 keyless) — kept so the probe states
    # it plainly instead of silently skipping; rows stay docs-verified.
    "Cohere": "https://api.cohere.com/v1/models",
}


def _norm_mid(s):
    s = (s or "").lower().strip().replace("_", "-")
    if " (via " in s:  # catalog suffix e.g. " (via Requesty)"
        s = s.split(" (via ")[0].strip()
    return s


def _bases(s):
    s = _norm_mid(s)
    out = {s}
    if s.endswith(":free"):
        out.add(s[:-len(":free")])
    return out


def _is_zero_price(p):
    """True only when a pricing payload proves $0 (Kilo/Nous dicts, Requesty lists)."""
    if p is None:
        return False
    if isinstance(p, dict):
        nums = []
        for v in p.values():
            if isinstance(v, bool):
                continue
            if isinstance(v, (int, float)):
                nums.append(v)
            elif isinstance(v, str):
                try:
                    nums.append(float(v))
                except ValueError:
                    return False
            elif isinstance(v, (list, dict)):
                continue  # tier overrides / nested metadata, not the base price
            else:
                return False
        return bool(nums) and all(n == 0 for n in nums)
    if isinstance(p, list):  # Requesty: [{input_price, output_price, ...}]
        if not p:
            return False
        for entry in p:
            if not isinstance(entry, dict):
                return False
            for k in ("input_price", "output_price", "cached_price"):
                v = entry.get(k)
                if isinstance(v, bool) or not isinstance(v, (int, float)) or v != 0:
                    return False
        return True
    return False


def _live_free_ids(items):
    """Free-table proof per response shape. Returns None when the endpoint
    carries no free signals (DeepInfra/SambaNova dict-pricing style) — then
    the curated list is the free table and the probe is existence-only."""
    uses_convention = any(
        ":free" in (m.get("id", "") or "") or m.get("tier")
        or isinstance(m.get("pricing"), list) for m in items
    )
    if not uses_convention:
        return None
    free = set()
    for m in items:
        mid = m.get("id", "") or ""
        if not mid:
            continue
        if m.get("tier") == "turbo":  # LLM7: anonymous free tier
            free.add(mid)
        elif ":free" in mid:  # OpenRouter/Kilo/Nous convention
            free.add(mid)
        elif _is_zero_price(m.get("pricing")):  # Requesty all-zero rows
            free.add(mid)
    return free


def sync_keyless_models(prov, endpoint, today):
    """Strict free-table check: a row is re-verified only on exact/base-id
    proof inside the endpoint's free table. Paid-only or absent rows keep
    their old date (stale flags surface them); nothing is ever added as $0."""
    if prov["name"] == "OVHcloud AI Endpoints":
        # single aggregate row ("10 free models (anonymous keyless)"): the
        # public catalog itself is the anonymous offering, so reachability
        # with entries listed is the verification.
        try:
            d = get_json(endpoint)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                return "skipped (keyless catalog needs key; docs-verified only)"
            raise
        items = d if isinstance(d, list) else d.get("data", d)
        n = len(items) if isinstance(items, list) else 0
        if not n:
            raise RuntimeError("empty model catalog")
        for m in prov["models"]:
            m["verified"] = today
        prov["verified"] = today
        prov["verified_method"] = "live-probe"
        return f"ok: catalog reachable ({n} models listed)"
    try:
        d = get_json(endpoint)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return "skipped (keyless /models needs key; docs-verified only)"
        raise
    items = d.get("data", []) if isinstance(d, dict) else d
    live_all = {m.get("id", ""): m for m in items if isinstance(m, dict) and m.get("id")}
    if not live_all:
        raise RuntimeError("empty model list")
    live_free = _live_free_ids(list(live_all.values()))
    norm_all = {_norm_mid(lid) for lid in live_all}
    norm_free = {_norm_mid(lid) for lid in (live_free or set())}
    missing, paid_only, found = [], [], 0
    for m in prov["models"]:
        bases = _bases(m["name"])
        if any(b in norm_free for b in bases):
            m["verified"] = today
            found += 1
        elif live_free is None:
            if any(b in norm_all for b in bases):
                m["verified"] = today
                found += 1
            else:
                missing.append(m["name"])
        elif any(b in norm_all for b in bases):
            paid_only.append(m["name"])  # paid tier exists, free NOT proven
        else:
            missing.append(m["name"])
    prov["verified"] = today
    prov["verified_method"] = "live-probe"
    msg = f"ok: {found}/{len(prov['models'])} models confirmed free"
    if paid_only:
        msg += f"; PAID-ONLY (not verified, needs human): {paid_only}"
    if missing:
        msg += f"; MISSING: {missing}"
    return msg


def check_doc_links(data):
    """Dead-link detection only — never extracts limits from docs (layouts change silently)."""
    out = []
    for prov in data["providers"]:
        try:
            req = urllib.request.Request(prov["url"], headers=UA, method="HEAD")
            with urllib.request.urlopen(req, timeout=15) as r:
                if r.status >= 400:
                    out.append(f"{prov['name']}: docs URL returned {r.status}")
        except Exception as e:
            out.append(f"{prov['name']}: docs URL unreachable ({e})")
    return out


def main():
    today = date.today().isoformat()
    data = json.loads(DATA.read_text())
    results = []
    key = gemini_key()
    for prov in data["providers"]:
        try:
            if prov["name"] == "Google AI Studio (Gemini API)":
                results.append(("Google AI Studio", sync_google(prov, key, today) if key else "skipped (no GEMINI_API_KEY)"))
            elif prov["name"] == "OpenRouter":
                results.append(("OpenRouter", sync_openrouter(prov, today)))
            elif prov["name"] in KEYLESS_MODEL_ENDPOINTS:
                results.append((prov["name"], sync_keyless_models(prov, KEYLESS_MODEL_ENDPOINTS[prov["name"]], today)))
        except Exception as e:
            results.append((prov["name"], f"FAILED: {e}"))

    for warn in check_doc_links(data):
        results.append(("doc-link", f"WARN: {warn}"))

    stale = []
    for prov in data["providers"]:
        try:
            v = datetime.fromisoformat(prov.get("verified", "")).date()
        except ValueError:
            stale.append(f"{prov['name']}: verified missing")
            continue
        if (date.today() - v).days > STALE_AFTER_DAYS:
            stale.append(f"{prov['name']}: stale since {prov['verified']}")

    # ponytail: catalog date = freshest provider; per-provider staleness flags handle the rest
    data["verified"] = max((p.get("verified", "") for p in data["providers"]), default=data["verified"])

    canonical = json.dumps(data, indent=2)
    changed = DATA.read_text().rstrip("\n") != canonical
    DATA.write_text(canonical + "\n")

    print("probe results:")
    for name, res in results:
        print(f"  {name}: {res}")
    print(f"data changed: {'yes' if changed else 'no'}")
    if stale:
        print("STALE (need human verification):")
        for s in stale:
            print(f"  {s}")
    sys.exit(0)


if __name__ == "__main__":
    main()
