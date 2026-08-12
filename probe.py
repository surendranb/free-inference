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
    rows = []
    for name in sorted(live):
        old = by_name.get(name)
        if old:
            old["context"] = ctx_s(live[name])
            old["verified"] = today
            rows.append(old)
        else:
            rows.append({
                "name": name, "cost": "$0", "context": ctx_s(live[name]),
                "rpm": "Varies by account", "tpm": "Varies by account",
                "rpd": "Varies by account", "tpd": "Not published", "verified": today,
            })
    prov["models"] = rows
    prov["verified"] = today
    return f"ok: {len(rows)} text-gen models"


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
    return f"ok: {len(rows)} :free models"


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
        except Exception as e:
            results.append((prov["name"], f"FAILED: {e}"))

    stale = []
    for prov in data["providers"]:
        try:
            v = datetime.fromisoformat(prov.get("verified", "")).date()
        except ValueError:
            stale.append(f"{prov['name']}: verified missing")
            continue
        if (date.today() - v).days > STALE_AFTER_DAYS:
            stale.append(f"{prov['name']}: stale since {prov['verified']}")

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
