#!/usr/bin/env python3
"""Autonomous Weekly Newsletter Generator for FreeInference.dev.

Runs every Monday via GitHub Actions or local CLI.
Uses core.model (gemini-3.5-flash-lite cascade + resilient retries) and falls back
to deterministic markdown if the LLM API is unavailable.
"""

from datetime import date
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.model import call_gemini_text, get_api_key  # noqa: E402

DATA_PATH = ROOT / "data" / "providers.json"
CHANGELOG_PATH = ROOT / "dist" / "data" / "changelog.json"
SUMMARY_PATH = ROOT / "data" / "run_summary.json"
NEWSLETTERS_DIR = ROOT / "data" / "newsletters"


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
            headers={"Authorization": f"Bearer {token}"},
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
            capture_output=True, text=True,
        )
        return res.stdout.strip() or None
    except Exception:
        return None


def _deterministic_template(today: str, total_provs: int, total_models: int, changelog_data: dict) -> str:
    return f"""# The Free Inference Dispatch — {today}

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
res = client.chat.completions.create(model="GLM-5.3", messages=[{{"role": "user", "content": "Hello"}}])
print(res.choices[0].message.content)
```
"""


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

    recent_issues = []
    if SUMMARY_PATH.exists():
        try:
            summary = json.loads(SUMMARY_PATH.read_text())
            recent_issues = [
                f"{r['provider']} ({r['route']}/{r['status']}): {r['summary']}"
                for r in summary.get("results", [])
                if r.get("status") in ("changed", "deprecated") or r.get("review_required")
            ][:10]
        except Exception:
            pass

    key = get_api_key()
    content = ""
    if key:
        prompt = f"""You are the autonomous editor for FreeInference.dev's weekly developer newsletter: 'The Free Inference Dispatch'.
Write the edition for {today}.

Current Catalog Stats:
- Total Providers: {total_provs}
- Total Models: {total_models}
- Recent verified changes: {json.dumps(changelog_data.get('recent', [])[:8])}
- Active review/change highlights: {json.dumps(recent_issues)}

Format requirements:
- Title: # The Free Inference Dispatch — {today}
- Sections:
  1. This Week in $0 Inference (factual bullet summary of verified updates, quotas, additions).
  2. Provider Spotlight (deep dive on 1 top provider with exact base_url and free-tier limits).
  3. Weekly Recipe (5-line terminal cURL or Python drop-in recipe).
  4. Tooling Links (links to /v1/models, /skill.md, /feed.xml).

Tone guidelines:
- Strictly technical, honest, zero hype, no emojis, verified facts only.
"""
        try:
            content = call_gemini_text(prompt, key=key, timeout=60).strip()
        except Exception as e:
            print(f"Notice: Gemini newsletter synthesis failed ({e}); using deterministic template.")

    if not content:
        content = _deterministic_template(today, total_provs, total_models, changelog_data)

    out_file.write_text(content + "\n")
    print(f"✓ Saved dispatch to {out_file}")

    subprocess.run([sys.executable, str(ROOT / "build.py")], check=True)

    subscribers = get_kv_subscribers()
    print(f"--> Active subscribers in Cloudflare KV: {len(subscribers)}")

    bd_key = get_buttondown_key()
    if bd_key:
        print("--> Sending draft to Buttondown API...")
        try:
            bd_payload = {
                "subject": f"The Free Inference Dispatch — {today}",
                "body": content,
                "status": "draft",
            }
            req = urllib.request.Request(
                "https://api.buttondown.email/v1/emails",
                data=json.dumps(bd_payload).encode("utf-8"),
                headers={
                    "Authorization": f"Token {bd_key}",
                    "Content-Type": "application/json",
                },
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
