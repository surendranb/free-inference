#!/usr/bin/env python3
"""Autonomous AI Studio Discovery Scout & Catalog Auditor for FreeInference.dev.

Runs nightly via GitHub Actions (.github/workflows/nightly-probe.yml) or locally.
1. Audits existing providers for staleness (>30 days), cost syntax errors, and missing base URLs.
2. Polls live model inventories across multiple aggregators (OpenRouter, Kilo, Nous, Requesty).
3. Uses Google AI Studio (gemini-3.5-flash-lite) to classify newly discovered free models.
4. Autonomously audits official documentation for stale/bundled providers, confirming active status
   and refreshing verified timestamps.
"""
import json
import os
import random
import re
import sys
import time
import urllib.request
import urllib.error
from urllib.parse import urlparse
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from probe import gemini_key, get_json, _live_free_ids, UA

DATA_PATH = ROOT / "data" / "providers.json"
REPORT_PATH = ROOT / "data" / "scout_report.json"
MODEL_NAME = "gemini-3.5-flash-lite"
ANTIGRAVITY_AGENT = "antigravity-preview-09-2026"
INTERACTIONS_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
GITHUB_REPO = "surendranb/free-inference"


def extract_first_json(text):
    """Robustly extract the first valid JSON object or array from model output."""
    if not text:
        raise ValueError("Empty response text")
    
    # 1. Check for markdown json code fence
    fence_matches = re.findall(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    for m in fence_matches:
        try:
            return json.loads(m.strip())
        except Exception:
            pass

    # 2. Balanced bracket scan for JSON object
    start_idx = text.find('{')
    while start_idx != -1:
        depth = 0
        in_string = False
        escape = False
        for i in range(start_idx, len(text)):
            c = text[i]
            if escape:
                escape = False
                continue
            if c == '\\':
                escape = True
                continue
            if c == '"':
                in_string = not in_string
                continue
            if not in_string:
                if c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        candidate = text[start_idx:i+1]
                        try:
                            val = json.loads(candidate)
                            if isinstance(val, dict):
                                return val
                        except Exception:
                            break
        start_idx = text.find('{', start_idx + 1)

    # 3. Fallback: stripped load
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    return json.loads(cleaned)


def get_github_token():
    """Retrieve GitHub token from environment or local gh CLI."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        try:
            import subprocess
            token = subprocess.check_output(["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL).strip()
        except Exception:
            token = None
    return token


def find_existing_issue(title_prefix, state="open", repo=GITHUB_REPO):
    """Check if an issue matching title_prefix already exists in repo."""
    token = get_github_token()
    if not token:
        return None
    url = f"https://api.github.com/repos/{repo}/issues?state={state}&per_page=100"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "FreeInference-Scout/1.0"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            issues = json.load(r)
            norm_prefix = title_prefix.lower().strip()
            for issue in issues:
                if issue.get("pull_request"):
                    continue  # skip PRs
                issue_title = issue.get("title", "").lower()
                if norm_prefix in issue_title:
                    return issue
    except Exception as e:
        print(f"Notice: Querying existing GitHub issues skipped: {e}")
    return None


def create_github_issue(title, body, labels, repo=GITHUB_REPO):
    """Create a GitHub Issue via REST API with gh CLI fallback."""
    token = get_github_token()
    if not token:
        print(f"Notice: No GitHub token available to create issue: '{title}'")
        return None

    url = f"https://api.github.com/repos/{repo}/issues"
    payload = {
        "title": title,
        "body": body,
        "labels": labels
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
            "User-Agent": "FreeInference-Scout/1.0"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            res = json.load(r)
            issue_url = res.get("html_url")
            print(f"  ✓ Created GitHub Issue #{res.get('number')}: {issue_url}")
            return res
    except Exception as e:
        print(f"Notice: GitHub REST API failed ({e}), attempting gh CLI fallback...")
        try:
            import subprocess
            cmd = ["gh", "issue", "create", "--repo", repo, "--title", title, "--body", body]
            for lbl in labels:
                cmd.extend(["--label", lbl])
            out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
            print(f"  ✓ Created GitHub Issue via gh CLI: {out}")
            return {"html_url": out}
        except Exception as gh_err:
            print(f"Notice: Failed to create GitHub issue via gh CLI: {gh_err}")
    return None


def close_github_issue(issue_number, comment):
    """Close a GitHub issue with an explanation comment."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY", "surendranb/free-inference")
    try:
        if token:
            comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
            req = urllib.request.Request(
                comment_url,
                data=json.dumps({"body": comment}).encode("utf-8"),
                headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=15):
                pass
            issue_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
            req = urllib.request.Request(
                issue_url,
                data=json.dumps({"state": "closed", "state_reason": "completed"}).encode("utf-8"),
                headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "Content-Type": "application/json"},
                method="PATCH"
            )
            with urllib.request.urlopen(req, timeout=15):
                print(f"  ✓ Closed GitHub Issue #{issue_number}")
                return
    except Exception as e:
        print(f"Notice: Failed to close issue #{issue_number} via API ({e}), attempting gh CLI fallback...")
    try:
        import subprocess
        subprocess.run(["gh", "issue", "comment", str(issue_number), "--repo", repo, "--body", comment], check=True, stderr=subprocess.DEVNULL)
        subprocess.run(["gh", "issue", "close", str(issue_number), "--repo", repo, "--reason", "completed"], check=True, stderr=subprocess.DEVNULL)
        print(f"  ✓ Closed GitHub Issue #{issue_number} via gh CLI")
    except Exception as gh_err:
        print(f"Notice: Failed to close issue #{issue_number} via gh CLI: {gh_err}")


def report_deprecation_issue(pname, doc_url, audit_entry):
    """File a GitHub deprecation issue if one is not already open."""
    search_prefix = f"[Deprecation] {pname}"
    existing = find_existing_issue(search_prefix, state="open")
    if existing:
        print(f"  Notice: Deprecation issue already open #{existing.get('number')}: {existing.get('html_url')}")
        return existing

    title = f"[Deprecation] {pname}: Free tier discontinued"
    body = f"""### ⚠ Provider Deprecation Alert: {pname}

The Antigravity ground truth agent audited official documentation for **{pname}** and verified that its free tier has been discontinued or degraded to paid-only.

- **Provider**: {pname}
- **Docs / Pricing URL**: {doc_url}
- **Verified Date**: {audit_entry.get('audited_date')}
- **Agent Interaction**: `{audit_entry.get('interaction_id')}` ({audit_entry.get('agent_steps')} steps)
- **Status**: `{audit_entry.get('status')}`

#### Audit Findings
> {audit_entry.get('summary')}

#### Recommended Action
Retire `{pname}` from `data/providers.json` and rebuild the site matrix via `python3 build.py`.
"""
    return create_github_issue(title, body, ["catalog:deprecation"])


def report_candidate_issue(cand_entry):
    """File a GitHub candidate issue if this provider hasn't been evaluated yet."""
    cname = cand_entry["name"]
    search_prefix = f"[New Provider Candidate] {cname}"
    existing = find_existing_issue(search_prefix, state="all")
    if existing:
        print(f"  Notice: Candidate issue already exists #{existing.get('number')}: {existing.get('html_url')}")
        return existing

    title = f"[New Provider Candidate] {cname}: Free tier verified"
    models_str = "\n".join(f"- `{m}`" for m in cand_entry.get("candidate_models", [])) or "- Model catalog discovery pending"
    
    staged_models = []
    for m in cand_entry.get("candidate_models", [])[:3]:
        staged_models.append({
            "name": m,
            "cost": "$0",
            "context": "Model-dependent",
            "rpm": "Published on portal",
            "verified": cand_entry.get("audited_date")
        })
    if not staged_models:
        staged_models.append({
            "name": f"{cname} Free Model",
            "cost": "$0",
            "context": "Model-dependent",
            "rpm": "Published on portal",
            "verified": cand_entry.get("audited_date")
        })

    staged_json = {
        "name": cname,
        "url": cand_entry["url"],
        "free_type": cand_entry.get("free_type", "Permanent $0"),
        "notes": cand_entry.get("summary", ""),
        "timeout": "Not published",
        "verified": cand_entry.get("audited_date"),
        "models": staged_models,
        "verified_method": "antigravity-agent",
        "docs_url": cand_entry["url"],
        "access_method": "api_key",
        "base_url": cand_entry.get("base_url") or "https://api..."
    }

    body = f"""### 🚀 New Provider Candidate Discovered: {cname}

The Antigravity ground truth agent discovered and verified a new free inference provider.

- **Provider**: {cname}
- **Website / Docs**: {cand_entry['url']}
- **Discovered Via**: {cand_entry['source']}
- **Free Tier Type**: {cand_entry.get('free_type')}
- **Verified Date**: {cand_entry.get('audited_date')}
- **Agent Interaction**: `{cand_entry.get('interaction_id')}` ({cand_entry.get('agent_steps')} steps)

#### Verified Allowance
> {cand_entry.get('summary')}

#### Candidate Models
{models_str}

#### Ready-to-Merge JSON Staging
```json
{json.dumps(staged_json, indent=2)}
```
"""
    return create_github_issue(title, body, ["catalog:candidate"])


def call_antigravity_agent(prompt, key, timeout=60, retries=3):
    """Invoke Antigravity Managed Agent in Google's cloud sandbox with Chrome & web access.
    
    Includes exponential backoff with jitter on HTTP 429 (rate limit) and 503 (transient overload).
    Capped at 15,000 total tokens to prevent runaway TPM/quota exhaustion.
    """
    url = f"{INTERACTIONS_URL}?key={key}"
    body = {
        "agent": ANTIGRAVITY_AGENT,
        "input": prompt,
        "environment": "remote",
        "background": True,
        "store": True,
        "agent_config": {
            "type": "antigravity",
            "max_total_tokens": 15000
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    init_res = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                init_res = json.load(r)
                break
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            if e.code in (429, 503) and attempt < retries:
                backoff = (2 ** attempt * 12) + random.uniform(2, 6)
                print(f"  Notice: AI Studio Interactions API returned {e.code} ({e.reason}): {err_body[:300]}. Backing off for {backoff:.1f}s (retry {attempt + 1}/{retries})...")
                time.sleep(backoff)
                continue
            raise RuntimeError(f"AI Studio Interactions API HTTP {e.code}: {err_body}") from e
    
    if not init_res:
        raise RuntimeError("Failed to initialize Antigravity Agent interaction")

    iid = init_res.get("id")
    if not iid:
        raise RuntimeError("No interaction ID returned by Antigravity Agent API")
    
    poll_url = f"{INTERACTIONS_URL}/{iid}?key={key}"
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(5)
        try:
            with urllib.request.urlopen(poll_url, timeout=30) as r:
                poll_res = json.load(r)
        except urllib.error.HTTPError as pe:
            if pe.code in (429, 503):
                # Transient rate-limit during poll, wait and retry next tick
                time.sleep(5)
                continue
            raise

        status = poll_res.get("status")
        if status in ("completed", "failed", "incomplete"):
            steps = poll_res.get("steps", [])
            output_text = ""
            for s in reversed(steps):
                for c in s.get("content", []):
                    if "text" in c and c["text"].strip():
                        output_text = c["text"].strip()
                        break
                if output_text:
                    break

            # If no conversational text was generated (e.g. status == incomplete),
            # harvest thought summaries across steps
            if not output_text:
                summaries = []
                for s in steps:
                    for sm in s.get("summary", []):
                        if isinstance(sm, dict) and sm.get("text"):
                            summaries.append(sm["text"])
                if summaries:
                    output_text = "\n\n".join(summaries)

            return {
                "status": status,
                "output_text": output_text,
                "steps_count": len(steps),
                "interaction_id": iid,
                "usage": poll_res.get("usage", {})
            }
    raise TimeoutError(f"Antigravity agent interaction {iid} timed out after {timeout}s")


def call_ai_studio(prompt, key, retries=1):
    """Call Google AI Studio gemini-3.5-flash-lite with retry."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={key}"
    req_body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(req_body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                res = json.load(r)
                return res["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
                continue
            raise RuntimeError(f"AI Studio call failed after retries: {e}")


def clean_html(html_str):
    """Strip scripts, styles, tags, and normalize whitespace."""
    s = re.sub(r'<(script|style|svg|noscript|head)[^>]*>.*?</\1>', ' ', html_str, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def extract_pricing_context(text, max_len=3000):
    """Extract relevant pricing and free-tier sentences to fit LLM prompt."""
    keywords = ["free", "pricing", "plan", "token", "credit", "rate limit", "allowance", "model", "tier", "quota"]
    sentences = re.split(r'(?<=[.!?])\s+', text)
    matched = [s for s in sentences if any(kw in s.lower() for kw in keywords)]
    snippet = " ".join(matched)
    if len(snippet) < 300:
        snippet = text[:max_len]
    return snippet[:max_len]


def scout_openrouter_free_models():
    """Fetch all :free models from OpenRouter."""
    try:
        d = get_json("https://openrouter.ai/api/v1/models")
        free_models = []
        for m in d.get("data", []):
            mid = m.get("id", "")
            if ":free" in mid:
                free_models.append({
                    "id": mid,
                    "name": m.get("name", mid),
                    "context_length": m.get("context_length", 0),
                    "source": "OpenRouter"
                })
        return free_models
    except Exception as e:
        print(f"Warning: could not fetch OpenRouter models: {e}")
        return []


def poll_openrouter_rss(existing_models):
    """Directly poll OpenRouter RSS feed for new model additions with (free) tag."""
    url = "https://openrouter.ai/api/v1/models?use_rss=true"
    req = urllib.request.Request(url, headers={"User-Agent": "FreeInference-Scout/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            xml_data = r.read()
    except Exception as e:
        print(f"Notice: OpenRouter RSS fetch skipped: {e}")
        return []

    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"Notice: OpenRouter RSS parse failed: {e}")
        return []

    channel = root.find("channel")
    if channel is None:
        return []

    catalog_ids = {m.lower().split("/")[-1].replace(":free", "") for m in existing_models}
    rss_discoveries = []
    for item in channel.findall("item"):
        title = item.find("title").text if item.find("title") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""
        pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
        desc = item.find("description").text if item.find("description") is not None else ""

        if "(free)" in title.lower() or ":free" in title.lower():
            id_match = re.search(r"\(([^()]+/[^()]+)\)", title)
            model_id = id_match.group(1).strip() if id_match else link.replace("https://openrouter.ai/", "").strip()
            base_id = model_id.split("/")[-1].replace(":free", "").lower()
            is_new = base_id not in catalog_ids and model_id.lower() not in {m.lower() for m in existing_models}
            rss_discoveries.append({
                "model_id": model_id,
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "description": desc[:200],
                "is_new_to_catalog": is_new
            })

    return rss_discoveries


def scout_endpoint_models(name, url):
    """Fetch all $0 / free models from a zero-price gateway endpoint."""
    try:
        d = get_json(url)
        items = d.get("data", d) if isinstance(d, dict) else d
        if not isinstance(items, list):
            return []
        free_ids = _live_free_ids(items)
        out = []
        for m in items:
            if isinstance(m, dict) and m.get("id") in free_ids:
                out.append({
                    "id": m.get("id"),
                    "name": m.get("name", m.get("id")),
                    "context_length": m.get("context_length", 0),
                    "source": name
                })
        return out
    except Exception as e:
        print(f"Warning: could not fetch {name} models: {e}")
        return []


def audit_catalog(catalog_data):
    """Perform ground truth audit on providers and models."""
    issues = []
    stale_providers = []
    today = date.today()

    for p in catalog_data.get("providers", []):
        pname = p.get("name", "Unknown")
        # Staleness check (>30 days)
        v_str = p.get("verified", "")
        try:
            v_date = datetime.fromisoformat(v_str).date()
            days_old = (today - v_date).days
            if days_old > 30:
                stale_providers.append({
                    "provider": pname,
                    "days_stale": days_old,
                    "verified": v_str,
                    "docs_url": p.get("docs_url") or p.get("url")
                })
        except ValueError:
            issues.append(f"{pname}: missing or invalid verified date '{v_str}'")

        # Base URL check on API providers
        if p.get("access_method") == "api_key" and not p.get("base_url"):
            issues.append(f"{pname}: API provider missing base_url")

        # Cost syntax check
        for m in p.get("models", []):
            cost = m.get("cost", "")
            if cost and not (cost.startswith("$") or "free" in cost.lower() or "0" in cost):
                issues.append(f"{pname} / {m.get('name')}: suspicious cost '{cost}'")

    return {
        "stale_count": len(stale_providers),
        "stale_providers": stale_providers,
        "syntax_issues": issues
    }


def verify_catalog_providers(catalog_data, key, apply_updates=False, max_audits=None, priority_providers=None, force_all=False):
    """Engine 1: Multi-Modal Verification Runner (api, feed, web/html).
    
    1. Identifies provider native modality (api, feed, web).
    2. Runner fetches latest ground-truth payload directly:
       - API: fetches live /models JSON
       - Feed: fetches RSS/Atom announcements
       - Web: uses Antigravity Agent in cloud sandbox to capture live pricing DOM
    3. Prompts agent with clean diff: "Here is existing catalog data, here is latest data. Determine what changed."
    4. Human-approved retirement invariant: automated runs NEVER delete or auto-retire providers.
       Deprecations flag GitHub issues for human review and approval.
    """
    today = date.today().isoformat()
    audit_results = []
    audited_count = 0
    consecutive_rate_limits = 0
    priority_set = set(priority_providers or [])

    provs = list(catalog_data.get("providers", []))
    # Prioritize probe failures first
    provs.sort(key=lambda p: 0 if p.get("name") in priority_set else 1)

    for p in provs:
        if max_audits is not None and audited_count >= max_audits:
            break

        pname = p.get("name")
        is_priority = pname in priority_set
        channel = (p.get("channel") or "web").lower()
        if channel not in ("api", "feed", "web"):
            channel = "web"

        # If already verified today via live-probe (and not a priority failure), ground truth is already established
        if not is_priority and not force_all:
            if p.get("verified") == today and p.get("verified_method") == "live-probe":
                continue

        # Prioritize canonical /pricing URL over deep documentation subpages
        primary_url = p.get("url", "")
        docs_url = p.get("docs_url", "")
        if "pricing" in primary_url.lower():
            doc_url = primary_url
        elif "pricing" in docs_url.lower():
            doc_url = docs_url
        else:
            doc_url = docs_url or primary_url

        prefix_tag = f"[{channel.upper()}]"
        print(f"--> {prefix_tag} Verifying {pname} via {channel} modality ({doc_url or primary_url})...")

        raw_out = ""
        agent_steps = 1
        interaction_id = None
        eval_data = {}

        try:
            # =========================================================
            # MODALITY 1: API (Runner fetches JSON endpoint, agent diffs)
            # =========================================================
            if channel == "api":
                endpoint_url = p.get("base_url") or p.get("url", "")
                if "/models" not in endpoint_url and not endpoint_url.endswith("/v1"):
                    models_url = endpoint_url.rstrip("/") + "/models"
                elif endpoint_url.endswith("/v1"):
                    models_url = endpoint_url + "/models"
                else:
                    models_url = endpoint_url

                latest_payload = ""
                try:
                    api_json = get_json(models_url)
                    latest_payload = json.dumps(api_json, indent=2)[:3500]
                except Exception as api_err:
                    latest_payload = f"API fetch failed for {models_url}: {api_err}"

                prompt = f"""You are the catalog verification auditor for FreeInference.dev.
Compare the EXISTING catalog data against the LATEST API data retrieved from the provider endpoint:

Provider: {pname}
Native Modality: API
Endpoint URL: {models_url}

EXISTING CATALOG DATA:
- Free Tier Type: {p.get('free_type')}
- Cataloged Free Models: {[m.get('name') for m in p.get('models', [])]}
- Documented Notes: {p.get('notes', '')}

LATEST LIVE API DATA:
{latest_payload}

Task: Compare existing catalog data against latest API data and determine what changed:
1. Is the free tier still confirmed active on this API?
2. Are all existing catalog models still offered, or were any discontinued?
3. Were any new free models added?
4. Output strictly valid JSON:
{{
  "status": "active" (if confirmed active) | "changed" (if models changed) | "retired" (only if explicitly discontinued/no free models) | "inconclusive",
  "is_free_active": true | false,
  "summary": "1 concise sentence explaining what changed compared to existing catalog data"
}}
"""
                raw_out = call_ai_studio(prompt, key)
                interaction_id = "api-runner-diff"

            # =========================================================
            # MODALITY 2: FEED (Runner fetches RSS/Atom, agent diffs)
            # =========================================================
            elif channel == "feed":
                feed_url = p.get("feed_url") or p.get("url")
                latest_payload = ""
                try:
                    req = urllib.request.Request(feed_url, headers=UA)
                    with urllib.request.urlopen(req, timeout=15) as r:
                        raw_feed = r.read().decode("utf-8", errors="ignore")
                    latest_payload = clean_html(raw_feed)[:3500]
                except Exception as feed_err:
                    latest_payload = f"Feed fetch failed for {feed_url}: {feed_err}"

                prompt = f"""You are the catalog verification auditor for FreeInference.dev.
Compare the EXISTING catalog data against the LATEST FEED announcements:

Provider: {pname}
Native Modality: Feed / Changelog
Feed URL: {feed_url}

EXISTING CATALOG DATA:
- Free Tier Type: {p.get('free_type')}
- Cataloged Free Models: {[m.get('name') for m in p.get('models', [])]}
- Documented Notes: {p.get('notes', '')}

LATEST FEED ANNOUNCEMENTS:
{latest_payload}

Task: Determine what changed based on these latest announcements:
1. Are there new free model releases or quota updates?
2. Are any cataloged free models announced as deprecated or discontinued?
3. Output strictly valid JSON:
{{
  "status": "active" (if free tier confirmed) | "changed" (if updates announced) | "retired" (if deprecation announced) | "inconclusive",
  "is_free_active": true | false,
  "summary": "1 concise sentence explaining what changed based on the feed"
}}
"""
                raw_out = call_ai_studio(prompt, key)
                interaction_id = "feed-runner-diff"

            # =========================================================
            # MODALITY 3: WEB / HTML (Antigravity cloud browser sandbox)
            # =========================================================
            else:
                prompt = f"""You are the Antigravity verification auditor for FreeInference.dev.
Task: Open {doc_url} and compare what you see on the live page against our existing catalog data.

Provider: {pname}
Native Modality: Web / HTML
Canonical URL: {doc_url}

EXISTING CATALOG DATA:
- Free Tier Type: {p.get('free_type')}
- Cataloged Free Models: {[m.get('name') for m in p.get('models', [])]}
- Documented Notes: {p.get('notes', '')}

Verification Instructions:
1. Navigate directly to {doc_url} using Google Chrome.
2. Compare the live pricing and model offerings against our existing catalog data above.
3. Determine what changed:
   - Is the free tier still actively offered?
   - Are any cataloged free models discontinued or moved to paid-only?
   - Are there any new free models or quota changes?
4. Keep your check concise: navigate, inspect the pricing tier, and output your answer immediately (aim for 1-3 browser actions). Do not wander into external pages.
5. If the page is blocked by a security checkpoint, captcha, Cloudflare challenge, or redirects to an internal login page, mark status as "inconclusive". Do NOT mark "retired" unless the page explicitly states the free tier is discontinued or paid-only.

Output strictly valid JSON:
{{
  "status": "active" (if free tier confirmed) | "changed" (if models/quotas changed) | "retired" (only if explicitly discontinued/paid-only) | "inconclusive" (if blocked),
  "is_free_active": true | false | null,
  "summary": "1 concise sentence confirming the verified free allowance or explaining why verification was inconclusive."
}}
"""
                agent_res = call_antigravity_agent(prompt, key, timeout=60)
                consecutive_rate_limits = 0
                raw_out = agent_res.get("output_text", "")
                agent_steps = agent_res.get("steps_count", 0)
                interaction_id = agent_res.get("interaction_id")

            # Extract JSON from agent output
            try:
                eval_data = extract_first_json(raw_out)
            except Exception as parse_err:
                print(f"  Notice: JSON unwrap error for {pname} ({parse_err}), synthesizing from observations...")
                try:
                    synth_prompt = f"""Based on these observations from verifying {pname} ({doc_url or primary_url}):
{raw_out[:2000]}

Is the $0 developer free tier confirmed active? What changed? Output strictly valid JSON with keys:
- "status": "active", "changed", "inconclusive", or "retired"
- "is_free_active": boolean or null
- "summary": concise 1-sentence verification result
"""
                    synth_raw = call_ai_studio(synth_prompt, key)
                    eval_data = extract_first_json(synth_raw)
                except Exception as synth_err:
                    print(f"  Notice: Synthesis failed for {pname}: {synth_err}")
                    eval_data = {
                        "status": "inconclusive",
                        "is_free_active": None,
                        "summary": f"Parse error: {parse_err}"
                    }

            audit_entry = {
                "provider": pname,
                "docs_url": doc_url or primary_url,
                "channel": channel,
                "status": eval_data.get("status", "active"),
                "is_free_active": eval_data.get("is_free_active", True),
                "summary": eval_data.get("summary", ""),
                "audited_date": today,
                "agent_steps": agent_steps,
                "interaction_id": interaction_id
            }
            audit_results.append(audit_entry)
            audited_count += 1

            if eval_data.get("is_free_active") and apply_updates:
                p["verified"] = today
                p["verified_method"] = "live-probe" if channel == "api" else "docs"
                if eval_data.get("free_type") in ("Rate-limited free", "Trial credits", "Promo free (limited time)"):
                    p["free_type"] = eval_data["free_type"]
                for m in p.get("models", []):
                    m.setdefault("cost", "$0")
                    m.setdefault("context", "Not published")
                    m.setdefault("rpm", "Not published")
                    m.setdefault("tpm", "Not published")
                    m.setdefault("rpd", "Not published")
                    m.setdefault("tpd", "Not published")
                    m["verified"] = today
                print(f"  ✓ Verified active ({agent_steps} steps): refreshed {pname} verification date to {today}.")

            # -------------------------------------------------------------
            # HUMAN-APPROVED RETIREMENT ONLY: NEVER AUTO-RETIRE IN CI
            # -------------------------------------------------------------
            elif eval_data.get("is_free_active") is False or eval_data.get("status") == "retired":
                summary_text = (eval_data.get("summary") or "").lower()
                is_inconclusive = eval_data.get("status") == "inconclusive" or any(w in summary_text for w in [
                    "checkpoint", "security check", "captcha", "cloudflare", "blocked",
                    "inconclusive", "unconfirmed", "unverified", "redirects to login", "login page"
                ])
                if is_inconclusive or channel == "api":
                    print(f"  Notice: {pname} audit inconclusive or protected ({summary_text[:80]}); preserving existing catalog status.")
                    audit_entry["status"] = "inconclusive"
                else:
                    print(f"  ⚠ DEPRECATION DETECTED for {pname}: {eval_data.get('summary')}")
                    print(f"  --> Flagging GitHub deprecation issue for human approval. Automated runs NEVER auto-retire.")
                    report_deprecation_issue(pname, doc_url or primary_url, audit_entry)

        except Exception as e:
            is_429 = "429" in str(e) or (isinstance(e, urllib.error.HTTPError) and getattr(e, "code", None) == 429)
            if is_429:
                consecutive_rate_limits += 1
                status_val = "rate_limited"
                summary_val = f"AI Studio rate limit (429): {e}"
                print(f"  Notice: Agent audit rate-limited for {pname}: {e}")
            else:
                consecutive_rate_limits = 0
                status_val = "unreachable"
                summary_val = str(e)
                print(f"  Notice: Agent audit skipped for {pname}: {e}")

            audit_results.append({
                "provider": pname,
                "docs_url": doc_url or primary_url,
                "channel": channel,
                "status": status_val,
                "is_free_active": None,
                "summary": summary_val,
                "audited_date": today
            })

            if consecutive_rate_limits >= 3:
                print("  ⚠ WARNING: Google AI Studio Interactions API quota exhausted across retries. Halting remaining audits to avoid spamming the endpoint.")
                break
        finally:
            if channel == "web":
                # Pacing delay between sequential cloud sandbox browser audits
                time.sleep(8)
            else:
                time.sleep(1)

    return audit_results


# Backwards compatibility alias
verify_web_providers_docs = verify_catalog_providers
audit_stale_provider_docs = verify_catalog_providers


def scout_candidates_search_first(catalog_data, key):
    """Engine 2: Search-First Discovery Scout.
    
    1. Queries live web signals via Google Search for newly announced/updated developer free tiers.
    2. Traces newly surfaced upstream creator labs from aggregator :free models.
    3. Resolves provider identity, modality (api, feed, web), and access method.
    """
    existing_names = {re.sub(r'[^a-z0-9]', '', p.get("name", "").lower()) for p in catalog_data.get("providers", [])}
    existing_domains = set()
    for p in catalog_data.get("providers", []):
        for ukey in ("url", "docs_url", "base_url"):
            u = p.get(ukey)
            if u:
                netloc = urlparse(u).netloc.lower()
                if netloc.startswith("www."):
                    netloc = netloc[4:]
                existing_domains.add(netloc)

    candidates = {}

    # 1. Search Grounding via Google Search (Live Frontier)
    if key:
        print("--> [Discovery Scout] Querying Google Search for live free inference announcements...")
        search_prompt = """You are the Discovery Scout for FreeInference.dev.
Search the live web for active or recently launched AI model providers offering genuine developer free tiers, free trial credits without upfront credit card purchase, or free inference APIs (text, coding, vision, speech-to-text, text-to-speech) in 2026.
Focus on developer inference you can build with (API keys, OpenAI-compatible endpoints, CLI tools, libraries). Chat-only web UIs are strictly excluded.

Find up to 3 genuine, uncataloged candidate providers that have an active free tier.
For each candidate, determine:
- "name": Provider name
- "url": Official developer / documentation / pricing URL
- "channel": Native verification modality: "api" (public endpoint / OpenAPI specs), "web" (documentation / pricing table), or "feed" (changelog / releases)
- "access_method": "api_key", "login", or "bundled"
- "free_type": "Rate-limited free", "Trial credits", or "Promo free (limited time)"
- "free_signal": Specific evidence of the free grant (e.g. dollar amount, free models, rate limits)

Output strictly a JSON array of objects with these keys, with no conversational text or markdown code fences.
"""
        cascade_models = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemma-4-26b-a4b-it", "gemma-4-31b-it"]
        for target_model in cascade_models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent?key={key}"
                body = {
                    "contents": [{"parts": [{"text": search_prompt}]}],
                    "tools": [{"googleSearch": {}}]
                }
                req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    res = json.load(r)
                    raw_text = res["candidates"][0]["content"]["parts"][0]["text"]
                    search_candidates = extract_first_json(raw_text)
                    if isinstance(search_candidates, list):
                        for sc in search_candidates:
                            cname = sc.get("name", "").strip()
                            curl = sc.get("url", "").strip()
                            norm_name = re.sub(r'[^a-z0-9]', '', cname.lower())
                            if norm_name and norm_name not in existing_names and curl:
                                cdomain = urlparse(curl).netloc.lower().replace("www.", "")
                                if cdomain and cdomain not in existing_domains:
                                    candidates[norm_name] = {
                                        "name": cname,
                                        "url": curl,
                                        "channel": sc.get("channel", "web"),
                                        "access_method": sc.get("access_method", "api_key"),
                                        "free_type": sc.get("free_type", "Rate-limited free"),
                                        "source": "Google Search Live Frontier",
                                        "free_signal": sc.get("free_signal", "")
                                    }
                                    print(f"  ✓ Search surfaced candidate: {cname} ({curl}) [modality: {sc.get('channel', 'web')}]")
                        break
            except Exception as e:
                continue

    # 2. Upstream Model Creator Labs from Aggregators
    # Traces active free models like typesafe/*, liquid/*, stepfun/*, thinkingmachines/*, etc.
    creator_map = {
        "liquid": ("Liquid AI", "https://console.liquid.ai", "web"),
        "stepfun": ("StepFun", "https://platform.stepfun.com", "web"),
        "thinkingmachines": ("Thinking Machines Lab", "https://thinkingmachines.ai", "web"),
        "recursive": ("Recursive AI", "https://recursive.ai", "web"),
        "dots-studio": ("Dots Studio", "https://dots.ai", "web"),
        "poolside": ("Poolside AI", "https://poolside.ai", "web"),
    }
    for p in catalog_data.get("providers", []):
        if p.get("name") in ("OpenRouter", "OpenCode Zen", "Kilo Gateway", "Requesty", "Nous Portal"):
            for m in p.get("models", []):
                m_name = m.get("name", "")
                if "/" in m_name:
                    creator_slug = m_name.split("/")[0].strip().lower()
                    if creator_slug in creator_map:
                        cname, curl, cmodality = creator_map[creator_slug]
                        norm_name = re.sub(r'[^a-z0-9]', '', cname.lower())
                        if norm_name not in existing_names and norm_name not in candidates:
                            candidates[norm_name] = {
                                "name": cname,
                                "url": curl,
                                "channel": cmodality,
                                "access_method": "api_key",
                                "free_type": "Rate-limited free",
                                "source": f"Upstream Creator for {m_name}",
                                "free_signal": f"Aggregator model {m_name} actively offered"
                            }

    return list(candidates.values())


# Backwards compatibility alias
poll_candidate_providers = scout_candidates_search_first


def audit_provider_candidates(candidates, key, max_audits=None, catalog_data=None, apply_updates=False):
    """Engine 2: Use Antigravity Managed Agent in cloud sandbox to audit new provider candidates."""
    if not key or not candidates:
        return {"verified": [], "all_audited": []}

    # Check previously audited candidate history to avoid re-auditing paid-only providers
    audited_history = {}
    if REPORT_PATH.exists():
        try:
            prev_report = json.loads(REPORT_PATH.read_text())
            for ca in prev_report.get("candidate_audits", []):
                c_name = ca.get("name")
                if c_name:
                    audited_history[c_name.lower()] = ca.get("audited_date")
        except Exception:
            pass

    verified_candidates = []
    audit_records = []
    audited_count = 0

    for cand in candidates:
        if max_audits is not None and audited_count >= max_audits:
            break

        cname = cand["name"]
        curl = cand["url"]
        
        # Skip if audited within last 60 days
        prev_date = audited_history.get(cname.lower())
        if prev_date:
            try:
                days_since = (date.today() - datetime.fromisoformat(prev_date).date()).days
                if days_since < 60:
                    continue
            except Exception:
                pass

        # Also skip if an issue already exists in GitHub (open or closed)
        if find_existing_issue(f"[New Provider Candidate] {cname}", state="all"):
            continue

        print(f"--> [Discovery Scout] Auditing candidate provider {cname} ({curl})...")
        audited_count += 1
        prompt = f"""You are the Antigravity ground truth auditor for FreeInference.dev.
Investigate newly discovered AI inference provider candidate: {cname} at {curl}.

Task:
1. Navigate directly to {curl} using Google Chrome.
2. Confirm if {cname} offers a genuine $0 developer inference free tier or free trial credits without requiring upfront paid credit card purchase.
3. Keep your check concise (aim for 1-3 browser actions). Do not wander into external sites.

Output strictly valid JSON:
{{
  "status": "active" (if free tier exists) | "paid_only" | "no_api",
  "is_free_active": true | false,
  "free_type": "Permanent $0" | "Trial credits" | "Rate limited" | "None",
  "notes": "string strictly following 4-point fact format: [The Grant] + [The Output] + [The Process] + [The Condition]",
  "summary": "concise 1-sentence summary of the verified free allowance, limits, and reset cadence.",
  "candidate_models": ["model1", "model2"],
  "base_url": "API base URL if discovered, or null"
}}
"""
        try:
            agent_res = call_antigravity_agent(prompt, key, timeout=60)
            raw_out = agent_res.get("output_text", "")
            try:
                eval_data = extract_first_json(raw_out)
            except Exception:
                # If agent was cut off or emitted thoughts, synthesize structured JSON from its real observations
                synth_prompt = f"""Based on these Antigravity agent observations from auditing {cname} ({curl}):
{raw_out[:2000]}

Does this provider offer a genuine $0 developer inference free tier or free trial credits without upfront card payment?
Output strictly valid JSON with keys:
- "status": "active" (free tier exists), "paid_only" (strictly prepaid/credit card purchase required), or "no_api"
- "is_free_active": boolean (true if developer can use models for $0)
- "free_type": "Permanent $0", "Trial credits", "Rate limited", or "None"
- "notes": string strictly following 4-point fact format: [The Grant] + [The Output] + [The Process] + [The Condition]
- "summary": concise 1-sentence summary of the verified free allowance, limits, and reset cadence.
- "candidate_models": list of free model names/IDs (strings)
- "base_url": API base URL if discovered, or null
"""
                synth_raw = call_ai_studio(synth_prompt, key)
                eval_data = extract_first_json(synth_raw)

            audit_entry = {
                "name": cname,
                "url": curl,
                "source": cand["source"],
                "status": eval_data.get("status", "unknown"),
                "is_free_active": eval_data.get("is_free_active", False),
                "free_type": eval_data.get("free_type", "None"),
                "notes": eval_data.get("notes") or eval_data.get("summary", ""),
                "summary": eval_data.get("summary", ""),
                "candidate_models": eval_data.get("candidate_models", []),
                "base_url": eval_data.get("base_url"),
                "audited_date": date.today().isoformat(),
                "agent_steps": agent_res.get("steps_count", 0),
                "interaction_id": agent_res.get("interaction_id")
            }
            audit_records.append(audit_entry)

            if eval_data.get("is_free_active"):
                print(f"  ✓ Verified FREE provider candidate: {cname}! ({agent_res.get('steps_count')} agent steps)")
                verified_candidates.append(audit_entry)
                report_candidate_issue(audit_entry)
                if apply_updates and catalog_data is not None:
                    # Auto-graduate verified candidate into catalog
                    candidate_models = []
                    raw_c_models = eval_data.get("candidate_models") or [f"{cname} Free Model"]
                    for cm in raw_c_models:
                        m_name = cm if isinstance(cm, str) else cm.get("name", f"{cname} Free Model")
                        candidate_models.append({
                            "name": m_name,
                            "cost": "$0 (trial)" if "trial" in audit_entry.get("free_type", "").lower() else "$0",
                            "context": "Model-dependent",
                            "rpm": "Published on portal",
                            "tpm": "Not published",
                            "rpd": "Not published",
                            "tpd": "Not published",
                            "verified": date.today().isoformat()
                        })
                    new_provider_entry = {
                        "name": cname,
                        "url": curl,
                        "free_type": audit_entry.get("free_type", "Trial credits"),
                        "notes": audit_entry.get("notes") or audit_entry.get("summary", ""),
                        "timeout": "Not published",
                        "verified": date.today().isoformat(),
                        "channel": cand.get("channel", "web"),
                        "verified_method": "docs",
                        "access_method": cand.get("access_method", "api_key"),
                        "artifact": "code",
                        "base_url": audit_entry.get("base_url") or "",
                        "models": candidate_models
                    }
                    catalog_data.setdefault("providers", []).append(new_provider_entry)
                    print(f"  ✓ Auto-graduated new provider candidate {cname} into catalog.")
                    existing_cand_issue = find_existing_issue(f"[New Provider Candidate] {cname}", state="open")
                    if existing_cand_issue:
                        close_github_issue(existing_cand_issue["number"], f"Resolved: {cname} auto-graduated into catalog with verified 4-point fact notes.")
            else:
                print(f"  ✗ Provider candidate {cname} is paid-only / not free: {eval_data.get('summary')}")

        except Exception as e:
            is_429 = "429" in str(e) or (isinstance(e, urllib.error.HTTPError) and getattr(e, "code", None) == 429)
            status_val = "rate_limited" if is_429 else "unreachable"
            print(f"  Notice: Candidate audit skipped for {cname}: {e}")
            audit_records.append({
                "name": cname,
                "url": curl,
                "source": cand["source"],
                "status": status_val,
                "is_free_active": False,
                "summary": str(e),
                "audited_date": date.today().isoformat()
            })
            if is_429:
                print("  ⚠ Candidate audit hit rate limit. Halting candidate audits.")
                break
        finally:
            time.sleep(5)

    return {
        "verified": verified_candidates,
        "all_audited": audit_records
    }


def run_scout(apply_updates=False, audit_limit=None, force_all=False):
    print("--> Starting AI Studio Discovery Scout & Catalog Auditor...")
    today = date.today().isoformat()
    key = gemini_key()
    
    if not key:
        print("Skipped: No GEMINI_API_KEY available.")
        return 0

    catalog_data = json.loads(DATA_PATH.read_text())
    existing_models = {
        m["name"]: p["name"]
        for p in catalog_data["providers"]
        for m in p["models"]
    }

    # 0. Check for probe failures from Loop 1 (probe.py)
    probe_failures_path = ROOT / "data" / "probe_failures.json"
    failing_providers = []
    if probe_failures_path.exists():
        try:
            pf_data = json.loads(probe_failures_path.read_text())
            failing_providers = [f["provider"] for f in pf_data.get("failures", []) if "provider" in f]
            if failing_providers:
                print(f"--> [Loop 1->2] Prioritizing {len(failing_providers)} providers flagged by probe.py: {failing_providers}")
        except Exception as pf_err:
            print(f"Notice: Failed to read probe_failures.json: {pf_err}")

    # 1. Run Catalog Ground Truth Audit
    audit_summary = audit_catalog(catalog_data)
    print(f"Catalog status: {len(catalog_data['providers'])} providers, {len(existing_models)} models.")
    print(f"Stale providers (>30d): {audit_summary['stale_count']}")

    # 2. Multi-Source Discovery Scout across 4 gateways
    live_models = []
    live_models.extend(scout_openrouter_free_models())
    live_models.extend(scout_endpoint_models("Kilo Gateway", "https://api.kilo.ai/api/gateway/models"))
    live_models.extend(scout_endpoint_models("Nous Portal", "https://inference-api.nousresearch.com/v1/models"))
    live_models.extend(scout_endpoint_models("Requesty", "https://router.requesty.ai/v1/models"))

    new_discoveries = [m for m in live_models if m["id"] not in existing_models]
    print(f"Discovered {len(live_models)} live free models across 4 gateways ({len(new_discoveries)} new).")

    # 2b. Direct OpenRouter RSS Feed Stream for Real-Time Additions
    rss_free_models = poll_openrouter_rss(existing_models)
    new_rss_models = [m for m in rss_free_models if m.get("is_new_to_catalog")]
    print(f"OpenRouter RSS Stream: {len(rss_free_models)} free models found in feed ({len(new_rss_models)} new to catalog).")

    classified_candidates = []
    if new_discoveries:
        sample_to_classify = new_discoveries[:10]  # analyze top candidates
        prompt = f"""You are the automated catalog classifier for FreeInference.dev.
Analyze these newly discovered free LLM models from public gateways:
{json.dumps(sample_to_classify, indent=2)}

For each model, classify its architecture family, task category (coding, vision, reasoning, general), and whether it qualifies for free developer inference ($0 API).
Return a JSON array of objects with keys: "id", "family", "task", "recommended_page_slug", "summary".
Output strictly valid JSON with no markdown formatting.
"""
        try:
            raw_response = call_ai_studio(prompt, key)
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_response, flags=re.MULTILINE).strip()
            classified_candidates = json.loads(cleaned)
            print(f"Successfully classified {len(classified_candidates)} candidate models via AI Studio.")
        except Exception as e:
            print(f"AI classification notice: {e}")
            classified_candidates = [
                {"id": m["id"], "family": "unknown", "task": "general", "recommended_page_slug": "free-llm-api", "summary": m.get("name", "")}
                for m in sample_to_classify
            ]

    # 3. Autonomous Ground Truth Verifier for Web & Docs Providers
    doc_audits = verify_web_providers_docs(catalog_data, key, apply_updates=apply_updates, max_audits=audit_limit, priority_providers=failing_providers, force_all=force_all)
    print(f"Completed {len(doc_audits)} autonomous doc-audits.")

    # 4. Search-First Discovery & Modality Queueing
    candidate_providers = scout_candidates_search_first(catalog_data, key)
    print(f"Discovered {len(candidate_providers)} candidate providers via Search Frontier & Aggregators.")

    cand_limit = 1 if audit_limit is None else audit_limit
    candidate_audit_results = audit_provider_candidates(
        candidate_providers, key, max_audits=cand_limit,
        catalog_data=catalog_data, apply_updates=apply_updates
    )
    verified_candidates = candidate_audit_results.get("verified", [])
    candidate_records = candidate_audit_results.get("all_audited", [])

    completed_doc_audits = [d for d in doc_audits if d.get("status") in ("active", "changed", "retired", "inconclusive")]
    rate_limited_doc_audits = [d for d in doc_audits if d.get("status") == "rate_limited"]
    unreachable_doc_audits = [d for d in doc_audits if d.get("status") == "unreachable"]

    if apply_updates and (completed_doc_audits or verified_candidates):
        catalog_data["verified"] = max((p.get("verified", "") for p in catalog_data["providers"]), default=today)
        DATA_PATH.write_text(json.dumps(catalog_data, indent=2) + "\n")
        print(f"Updated {DATA_PATH} with fresh verification and catalog changes.")

    # Build report
    report = {
        "scouted_date": today,
        "model_used": f"{MODEL_NAME} + {ANTIGRAVITY_AGENT}",
        "providers_audited": len(completed_doc_audits),
        "doc_audits_rate_limited": len(rate_limited_doc_audits),
        "doc_audits_unreachable": len(unreachable_doc_audits),
        "models_cataloged": len(existing_models),
        "audit_summary": audit_summary,
        "doc_audits": doc_audits,
        "candidate_providers_count": len(candidate_providers),
        "candidate_audits": candidate_records,
        "verified_new_providers": verified_candidates,
        "live_gateway_free_total": len(live_models),
        "new_discoveries_count": len(new_discoveries),
        "openrouter_rss_stream_count": len(rss_free_models),
        "openrouter_rss_new_count": len(new_rss_models),
        "openrouter_rss_stream": rss_free_models,
        "candidates": classified_candidates,
        "status": "completed"
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Scout report written to {REPORT_PATH}")

    # Emit GitHub Actions Step Summary if running in CI
    gh_summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if gh_summary_path:
        with open(gh_summary_path, "a") as f:
            f.write(f"### 🤖 FreeInference Nightly AI Scout & Audit ({today})\n\n")
            f.write(f"- **Engines**: Discovery via `{MODEL_NAME}` · Live Sandbox Audits via `{ANTIGRAVITY_AGENT}`\n")
            f.write(f"- **Catalog Size**: {len(catalog_data['providers'])} providers · {len(existing_models)} models\n")
            f.write(f"- **Doc Audits Conducted**: {len(completed_doc_audits)} completed · {len(rate_limited_doc_audits)} rate-limited · {len(unreachable_doc_audits)} unreachable\n")
            f.write(f"- **New Providers Discovered**: {len(candidate_providers)} across HF & OpenRouter ({len(verified_candidates)} verified free)\n")
            f.write(f"- **Live Gateway Models**: {len(live_models)} across 4 endpoints\n\n")
            if verified_candidates:
                f.write("#### 🚀 Verified New Provider Candidates\n\n")
                f.write("| Provider | Source | Free Tier Type | Summary |\n")
                f.write("| --- | --- | --- | --- |\n")
                for vp in verified_candidates:
                    f.write(f"| [{vp['name']}]({vp['url']}) | {vp['source']} | {vp['free_type']} | {vp['summary']} |\n")
                f.write("\n")
            if doc_audits:
                f.write("#### Autonomous Doc Audits\n\n")
                f.write("| Provider | Status | Summary |\n")
                f.write("| --- | --- | --- |\n")
                for d in doc_audits:
                    status_icon = "✓" if d.get("is_free_active") else "⚠"
                    f.write(f"| {d['provider']} | {status_icon} {d['status']} | {d['summary']} |\n")
                f.write("\n")
            deprecations = [d for d in doc_audits if d.get("is_free_active") is False]
            if deprecations:
                f.write("#### ⚠ Deprecations Flagged to GitHub Issues\n\n")
                for dep in deprecations:
                    f.write(f"- **{dep['provider']}**: {dep['summary']}\n")
                f.write("\n")
            if classified_candidates:
                f.write("#### Newly Discovered Candidate Models\n\n")
                f.write("| Model ID | Family | Task | Recommended Slug |\n")
                f.write("| --- | --- | --- | --- |\n")
                for c in classified_candidates:
                    f.write(f"| `{c.get('id')}` | {c.get('family')} | {c.get('task')} | `{c.get('recommended_page_slug')}` |\n")

    return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Autonomous Discovery Scout & Catalog Verifier for FreeInference.dev")
    parser.add_argument("--apply", action="store_true", help="Apply updates to data/providers.json")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of audits (for testing; default is unconstrained)")
    parser.add_argument("--force-all", action="store_true", help="Force audit of all web providers even if verified today")
    args = parser.parse_args()
    sys.exit(run_scout(apply_updates=args.apply, audit_limit=args.limit, force_all=args.force_all))
