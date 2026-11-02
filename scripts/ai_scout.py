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


def call_antigravity_agent(prompt, key, timeout=120):
    """Invoke Antigravity Managed Agent in Google's cloud sandbox with Chrome & web access."""
    url = f"{INTERACTIONS_URL}?key={key}"
    body = {
        "agent": ANTIGRAVITY_AGENT,
        "input": prompt,
        "environment": "remote",
        "background": True,
        "store": True,
        "agent_config": {
            "type": "antigravity",
            "max_total_tokens": 50000
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        init_res = json.load(r)
    
    iid = init_res.get("id")
    if not iid:
        raise RuntimeError("No interaction ID returned by Antigravity Agent API")
    
    poll_url = f"{INTERACTIONS_URL}/{iid}?key={key}"
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(5)
        with urllib.request.urlopen(poll_url, timeout=30) as r:
            poll_res = json.load(r)
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


def audit_stale_provider_docs(catalog_data, key, apply_updates=False, max_audits=10):
    """Autonomously audit stale providers using Google AI Studio Antigravity Managed Agent in cloud sandbox."""
    today = date.today().isoformat()
    audit_results = []
    audited_count = 0

    for p in catalog_data.get("providers", []):
        if audited_count >= max_audits:
            break

        v_str = p.get("verified", "")
        try:
            v_date = datetime.fromisoformat(v_str).date()
            days_old = (date.today() - v_date).days
            if days_old <= 30:
                continue
        except ValueError:
            continue

        pname = p.get("name")
        doc_url = p.get("docs_url") or p.get("url")
        if not doc_url:
            continue

        print(f"--> [Antigravity Agent] Auditing live ground truth for {pname} ({doc_url})...")
        try:
            prompt = f"""You are the Antigravity ground truth auditor for FreeInference.dev.
Audit the official free tier for provider: {pname}.
Official Documentation / Pricing URL: {doc_url}

Current catalog data:
- Free tier type: {p.get('free_type')}
- Access method: {p.get('access_method')}
- Cataloged models: {[m.get('name') for m in p.get('models', [])]}

Task:
1. Navigate to {doc_url} using your tools (Google Chrome / url_context / curl / bash).
2. Inspect the live rendered page, pricing tables, quotas, token limits, and free allowances.
3. If the page redirected or pricing moved to a subpage, find the current pricing/free tier.
4. Output your conclusion strictly as a JSON object with keys:
- "status": "active" (free tier exists), "retired" (discontinued/paid-only), or "changed"
- "is_free_active": boolean
- "summary": concise 1-sentence summary of the verified free allowance, limits, and reset cadence.

Output valid JSON only with no conversational text.
"""
            agent_res = call_antigravity_agent(prompt, key, timeout=150)
            raw_out = agent_res.get("output_text", "")
            
            # Extract JSON block robustly
            try:
                eval_data = extract_first_json(raw_out)
            except Exception as parse_err:
                print(f"  Notice: JSON unwrap error for {pname} ({parse_err}): {raw_out[:180]}")
                eval_data = {
                    "status": "unreachable",
                    "is_free_active": None,
                    "summary": f"Parse error: {parse_err}"
                }

            audit_entry = {
                "provider": pname,
                "docs_url": doc_url,
                "status": eval_data.get("status", "active"),
                "is_free_active": eval_data.get("is_free_active", True),
                "summary": eval_data.get("summary", ""),
                "audited_date": today,
                "agent_steps": agent_res.get("steps_count", 0),
                "interaction_id": agent_res.get("interaction_id")
            }
            audit_results.append(audit_entry)
            audited_count += 1

            if eval_data.get("is_free_active") and apply_updates:
                p["verified"] = today
                for m in p.get("models", []):
                    m["verified"] = today
                print(f"  ✓ Verified active ({agent_res.get('steps_count', 0)} agent steps): refreshed {pname} verification date to {today}.")
            elif eval_data.get("is_free_active") is False or eval_data.get("status") == "retired":
                print(f"  ⚠ WARNING: Agent flagged {pname} as NOT active/free: {eval_data.get('summary')}")
                report_deprecation_issue(pname, doc_url, audit_entry)

        except Exception as e:
            print(f"  Notice: Antigravity agent audit skipped for {pname}: {e}")
            audit_results.append({
                "provider": pname,
                "docs_url": doc_url,
                "status": "unreachable",
                "is_free_active": None,
                "summary": str(e),
                "audited_date": today
            })

    return audit_results


def poll_candidate_providers(catalog_data):
    """Discover uncataloged external providers across Hugging Face & OpenRouter registries."""
    existing_names = set()
    existing_domains = set()

    def norm(s):
        return re.sub(r'[^a-z0-9]', '', s.lower())

    for p in catalog_data.get("providers", []):
        existing_names.add(norm(p.get("name", "")))
        for ukey in ("url", "docs_url", "base_url"):
            u = p.get(ukey)
            if u:
                netloc = urlparse(u).netloc.lower()
                if netloc.startswith("www."):
                    netloc = netloc[4:]
                existing_domains.add(netloc)

    # Exclude known non-qualifying or retired providers from auto-re-auditing
    ignore_names = {"togetherai", "openai", "anthropic"}
    candidates = {}

    # 1. Hugging Face Inference Providers
    try:
        hf_url = "https://huggingface.co/docs/inference-providers/en/index"
        req = urllib.request.Request(hf_url, headers={"User-Agent": "FreeInference-Scout/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8")
        hf_slugs = set(re.findall(r'href="/docs/inference-providers/en/providers/([^"]+)"', html))
        
        hf_names = {
            "baseten": ("Baseten", "https://www.baseten.co/pricing"),
            "fal-ai": ("fal.ai", "https://fal.ai/pricing"),
            "featherless-ai": ("Featherless", "https://featherless.ai/pricing"),
            "fireworks-ai": ("Fireworks AI", "https://fireworks.ai/pricing"),
            "novita": ("Novita AI", "https://novita.ai/pricing"),
            "nscale": ("nScale", "https://nscale.com"),
            "publicai": ("PublicAI", "https://publicai.com"),
            "replicate": ("Replicate", "https://replicate.com/pricing"),
            "scaleway": ("Scaleway", "https://www.scaleway.com/en/pricing/"),
            "wavespeed": ("WaveSpeed", "https://wavespeed.ai")
        }
        for slug in hf_slugs:
            if slug in hf_names:
                cname, curl = hf_names[slug]
                if norm(cname) not in existing_names and norm(cname) not in ignore_names:
                    candidates[norm(cname)] = {
                        "name": cname,
                        "url": curl,
                        "source": "Hugging Face Inference Providers",
                        "slug": slug
                    }
    except Exception as e:
        print(f"Notice: HF inference providers fetch skipped: {e}")

    # 2. OpenRouter Providers API
    try:
        or_url = "https://openrouter.ai/api/v1/providers"
        req = urllib.request.Request(or_url, headers={"User-Agent": "FreeInference-Scout/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            or_data = json.load(r)
        for p in or_data.get("data", []):
            cname = p.get("name")
            if not cname:
                continue
            if norm(cname) in existing_names or norm(cname) in ignore_names:
                continue
            website = p.get("privacy_policy_url") or p.get("terms_of_service_url") or ""
            domain = ""
            if website:
                d = urlparse(website).netloc.lower()
                if d.startswith("www."):
                    d = d[4:]
                domain = d
            if domain and domain in existing_domains:
                continue
            target_url = f"https://{domain}" if domain else ""
            if target_url and norm(cname) not in candidates:
                candidates[norm(cname)] = {
                    "name": cname,
                    "url": target_url,
                    "source": "OpenRouter Providers Registry",
                    "slug": p.get("slug")
                }
    except Exception as e:
        print(f"Notice: OpenRouter providers fetch skipped: {e}")

    return list(candidates.values())


def audit_provider_candidates(candidates, key, max_audits=2):
    """Use Antigravity Managed Agent in cloud sandbox to audit new provider candidates."""
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
        if audited_count >= max_audits:
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
Investigate newly discovered AI inference provider candidate: {cname}.
Official Website / Docs URL: {curl}

Task:
1. Navigate to {curl} using your tools (Google Chrome / url_context / curl / bash).
2. Find developer pricing, free tier, trial credits, rate limits, or API keys.
3. Check if {cname} offers a genuine $0 developer free tier, recurring free allowance, or free trial credits without requiring an upfront paid credit card purchase.
4. Output your conclusion strictly as a JSON object with keys:
- "status": "active" (free tier exists), "paid_only" (strictly prepaid/credit card purchase required), or "no_api"
- "is_free_active": boolean (true if developer can use models for $0)
- "free_type": "Permanent $0", "Trial credits", "Rate limited", or "None"
- "summary": concise 1-sentence summary of the verified free allowance, limits, and reset cadence.
- "candidate_models": list of free model names/IDs (strings)
- "base_url": API base URL if discovered, or null

Output valid JSON only with no conversational text.
"""
        try:
            agent_res = call_antigravity_agent(prompt, key, timeout=150)
            raw_out = agent_res.get("output_text", "")
            try:
                eval_data = extract_first_json(raw_out)
            except Exception:
                # If agent was cut off or emitted thoughts, synthesize structured JSON from its real observations
                synth_prompt = f"""Based on these Antigravity agent observations from auditing {cname} ({curl}):
{raw_out[:3000]}

Does this provider offer a genuine $0 developer inference free tier or free trial credits without upfront card payment?
Output strictly valid JSON with keys:
- "status": "active" (free tier exists), "paid_only" (strictly prepaid/credit card purchase required), or "no_api"
- "is_free_active": boolean (true if developer can use models for $0)
- "free_type": "Permanent $0", "Trial credits", "Rate limited", or "None"
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
            else:
                print(f"  ✗ Provider candidate {cname} is paid-only / not free: {eval_data.get('summary')}")

        except Exception as e:
            print(f"  Notice: Candidate audit skipped for {cname}: {e}")
            audit_records.append({
                "name": cname,
                "url": curl,
                "source": cand["source"],
                "status": "unreachable",
                "is_free_active": False,
                "summary": str(e),
                "audited_date": date.today().isoformat()
            })

    return {
        "verified": verified_candidates,
        "all_audited": audit_records
    }


def run_scout(apply_updates=False):
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

    # 3. Autonomous Doc-Auditor for Stale Providers
    doc_audits = audit_stale_provider_docs(catalog_data, key, apply_updates=apply_updates, max_audits=18)
    print(f"Completed {len(doc_audits)} autonomous doc-audits.")

    if apply_updates and doc_audits:
        DATA_PATH.write_text(json.dumps(catalog_data, indent=2) + "\n")
        print(f"Updated {DATA_PATH} with fresh verification timestamps.")

    # 4. Autonomous Discovery & Audit of New Service Providers
    candidate_providers = poll_candidate_providers(catalog_data)
    print(f"Discovered {len(candidate_providers)} uncataloged external providers across Hugging Face & OpenRouter.")

    candidate_audit_results = audit_provider_candidates(candidate_providers, key, max_audits=2)
    verified_candidates = candidate_audit_results.get("verified", [])
    candidate_records = candidate_audit_results.get("all_audited", [])

    # Build report
    report = {
        "scouted_date": today,
        "model_used": f"{MODEL_NAME} + {ANTIGRAVITY_AGENT}",
        "providers_audited": len(catalog_data["providers"]),
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
            f.write(f"- **Doc Audits Conducted**: {len(doc_audits)}\n")
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
    apply_flag = "--apply" in sys.argv
    sys.exit(run_scout(apply_updates=apply_flag))
