#!/usr/bin/env python3
"""Autonomous Weekly Newsletter Generator for FreeInference.dev.

Runs every Monday at 09:00 IST (03:30 UTC) via cron or GitHub Actions.
1. Synthesizes catalog diffs, probe results, and scout observations from the past 7 days.
2. Prompts Google AI Studio (gemini-3.5-flash-lite) to draft "The Free Inference Dispatch".
3. Saves to data/newsletters/{today}.md and rebuilds dist/newsletter/index.html.
4. If BUTTONDOWN_API_KEY is configured, sends or drafts the newsletter via Buttondown API.
"""
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from probe import gemini_key

DATA_PATH = ROOT / "data" / "providers.json"
CHANGELOG_PATH = ROOT / "dist" / "data" / "changelog.json"
FAILURES_PATH = ROOT / "data" / "probe_failures.json"
NEWSLETTERS_DIR = ROOT / "data" / "newsletters"
MODEL_NAME = "gemini-3.5-flash-lite"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"


def get_kv_subscribers():
    """Retrieve verified subscriber emails from Cloudflare KV."""
    account_id = "b8a2db803c867cf7208358fd8bcb191a"
    ns_id = "6daab6e498a74ac9b022fa84605ffb9d"
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not token:
        try:
            import tomllib
            cfg = Path.home() / ".wrangler" / "config" / "default.toml"
            if cfg.exists():
                with open(cfg, "rb") as f:
                    token = tomllib.load(f).get("oauth_token")
        except Exception:
            pass
    if not token:
        return []
    try:
        req = urllib.request.Request(
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{ns_id}/keys?prefix=sub:",
            headers={"Authorization": f"Bearer {token}"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return [k["name"].removeprefix("sub:") for k in data.get("result", []) if "name" in k]
    except Exception as e:
        print(f"Notice: Could not list KV subscribers: {e}")
        return []


def get_buttondown_key():
    key = os.environ.get("BUTTONDOWN_API_KEY")
    if key:
        return key
    try:
        res = subprocess.run(
            ["security", "find-generic-password", "-w", "-s", "buttondown-api-key"],
            capture_output=True, text=True
        )
        return res.stdout.strip() or None
    except Exception:
        return None


def call_ai_studio(prompt, api_key):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2048}
    }
    req = urllib.request.Request(
        f"{API_URL}?key={api_key}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        res_data = json.load(resp)
        return res_data["candidates"][0]["content"]["parts"][0]["text"]


def generate_newsletter():
    today = date.today().isoformat()
    NEWSLETTERS_DIR.mkdir(parents=True, exist_ok=True)
    out_file = NEWSLETTERS_DIR / f"{today}.md"

    print(f"--> Generating Free Inference Dispatch for {today}...")

    catalog = json.loads(DATA_PATH.read_text())
    total_provs = len(catalog["providers"])
    total_models = sum(len(p["models"]) for p in catalog["providers"])

    changelog_data = {}
    if CHANGELOG_PATH.exists():
        try:
            changelog_data = json.loads(CHANGELOG_PATH.read_text())
        except Exception:
            pass

    probe_failures = []
    if FAILURES_PATH.exists():
        try:
            probe_failures = json.loads(FAILURES_PATH.read_text()).get("failures", [])
        except Exception:
            pass

    key = gemini_key()
    if not key:
        print("Notice: No GEMINI_API_KEY available. Using deterministic template.")
        content = f"""# The Free Inference Dispatch — {today}

Autonomous weekly digest of verified $0 LLM APIs, rate limits, and endpoint changes across {total_provs} providers and {total_models} models.

---

## 1. Catalog Status ({today})
- **Total Providers**: {total_provs}
- **Total Verified Free Models**: {total_models}
- **OpenAI /v1/models API**: `https://freeinference.dev/v1/models`
- **Agent Skill**: `https://freeinference.dev/skill.md`
- **RSS Feed**: `https://freeinference.dev/feed.xml`

## 2. Recent Updates
{json.dumps(changelog_data.get('recent', [])[:5], indent=2)}

## 3. Weekly Recipe: Universal OpenAI Drop-in
```python
from openai import OpenAI
client = OpenAI(base_url="https://api.sambanova.ai/v1", api_key="your-key")
res = client.chat.completions.create(model="DeepSeek-V3.2", messages=[{{"role": "user", "content": "Hello"}}])
print(res.choices[0].message.content)
```
"""
    else:
        prompt = f"""You are the autonomous editor for FreeInference.dev's weekly developer newsletter: 'The Free Inference Dispatch'.
Write the edition for {today}.

Current Catalog Stats:
- Total Providers: {total_provs}
- Total Models: {total_models}
- Recent verified changes: {json.dumps(changelog_data.get('recent', [])[:8])}
- Active probe issues/deprecations: {json.dumps(probe_failures)}

Format requirements:
- Title: # The Free Inference Dispatch — {today}
- Sections:
  1. This Week in $0 Inference (factual, bulleted summary of recent changes, quota limits, model additions).
  2. Provider Spotlight (deep dive on 1 top provider e.g. SambaNova, Groq, or Google AI Studio with exact base_url and limits).
  3. Weekly Recipe (5-line terminal cURL or Python drop-in recipe).
  4. Tooling Links (links to /v1/models, /skill.md, /feed.xml).

Tone guidelines:
- Strictly technical, honest, zero marketing hype.
- No emojis except in section accents.
- All claims must be factual based on the catalog.
"""
        content = call_ai_studio(prompt, key).strip()

    out_file.write_text(content + "\n")
    print(f"✓ Saved dispatch to {out_file}")

    # Rebuild site so newsletter archive updates
    subprocess.run([sys.executable, str(ROOT / "build.py")], check=True)

    subscribers = get_kv_subscribers()
    print(f"--> Active subscribers in Cloudflare KV: {len(subscribers)}")

    # Optional Buttondown dispatch
    bd_key = get_buttondown_key()
    if bd_key:
        print("--> Sending draft to Buttondown API...")
        try:
            bd_payload = {
                "subject": f"The Free Inference Dispatch — {today}",
                "body": content,
                "status": "draft"  # safety first: save as draft for one-click approval
            }
            req = urllib.request.Request(
                "https://api.buttondown.email/v1/emails",
                data=json.dumps(bd_payload).encode("utf-8"),
                headers={
                    "Authorization": f"Token {bd_key}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                res = json.load(r)
                print(f"✓ Buttondown draft created: {res.get('id')}")
        except Exception as bd_err:
            print(f"Notice: Buttondown dispatch skipped: {bd_err}")
    else:
        print("Notice: No BUTTONDOWN_API_KEY set. Dispatch saved to web archive.")

    return 0


if __name__ == "__main__":
    sys.exit(generate_newsletter())
