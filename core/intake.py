"""Data intake modalities: Feed, API, Website (static first, cloud browser agent fallback)."""

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    )
}

INTERACTIONS_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
ANTIGRAVITY_AGENT = "antigravity-preview-09-2026"


def fetch_feed(url: str, max_items: int = 5) -> str:
    """Modality 1: Feed (RSS / Atom / JSON). Returns top updates as plain text."""
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"Feed fetch failed: {e}"

    # Try XML parsing (RSS / Atom)
    try:
        root = ET.fromstring(raw)
        items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
        lines = []
        for it in items[:max_items]:
            title = it.findtext("title") or it.findtext("{http://www.w3.org/2005/Atom}title") or ""
            desc = it.findtext("description") or it.findtext("{http://www.w3.org/2005/Atom}summary") or ""
            clean_desc = re.sub(r"<[^>]+>", " ", desc).strip()[:200]
            lines.append(f"- {title.strip()}: {clean_desc}")
        if lines:
            return "\n".join(lines)
    except ET.ParseError:
        pass

    # Try JSON feed
    try:
        data = json.loads(raw)
        items = data.get("items") or data.get("feed") or []
        lines = [f"- {it.get('title')}: {it.get('summary', '')[:200]}" for it in items[:max_items]]
        if lines:
            return "\n".join(lines)
    except Exception:
        pass

    return raw[:2000]


def fetch_api(url: str, key: str = None) -> str:
    """Modality 2: API (REST / JSON / /models). Returns compact JSON of free models."""
    try:
        headers = {**UA}
        if key:
            headers["Authorization"] = f"Bearer {key}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.load(r)
    except Exception as e:
        return f"API fetch failed: {e}"

    models = data.get("data") or data.get("models") or data
    if isinstance(models, list):
        compact = []
        for m in models:
            if not isinstance(m, dict):
                continue
            pricing = m.get("pricing")
            if pricing and isinstance(pricing, dict):
                p_prompt = float(pricing.get("prompt", 0) or 0)
                p_comp = float(pricing.get("completion", 0) or 0)
                if p_prompt > 0 or p_comp > 0:
                    continue
            mid = m.get("id") or m.get("name")
            ctx = m.get("context_length") or m.get("inputTokenLimit")
            compact.append({"id": mid, "context": ctx})
        return json.dumps(compact[:50], indent=2)

    return json.dumps(data, indent=2)[:3500]


def extract_json_payload(text: str) -> dict:
    """Extract first valid JSON object from agent output (handling markdown code fences and whitespace)."""
    if not text or not text.strip():
        return {}
    # 1. Try markdown code fences: ```json { ... } ```
    m = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
    # 2. Try raw outer curly braces
    m = re.search(r"(\{[\s\S]*\})", text)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
    # 3. Direct parse
    try:
        return json.loads(text.strip())
    except Exception:
        return {}


def verify_source_with_antigravity(provider: dict, key: str, timeout: int = 150) -> dict:
    """Run Antigravity Managed Agent in Google Cloud sandbox with real Chrome to audit one source at a time.
    
    Given a single provider source entry, the agent drives Chrome to inspect live pricing tables,
    rate limits, and model availability, returning a structured audit verdict with verified models.
    """
    if not key:
        return {
            "status": "inconclusive",
            "is_free_active": None,
            "models": [],
            "summary": "Antigravity agent unavailable: missing GEMINI_API_KEY / GOOGLE_API_KEY"
        }

    pname = provider.get("name", "Unknown")
    target_url = provider.get("docs_url") or provider.get("url", "")
    existing_models = [
        {
            "name": m.get("name"),
            "context": m.get("context", "Not published"),
            "rpm": m.get("rpm", "Not published"),
            "tpm": m.get("tpm", "Not published"),
            "rpd": m.get("rpd", "Not published"),
            "tpd": m.get("tpd", "Not published")
        }
        for m in provider.get("models", [])
    ]

    prompt = f"""You are the Antigravity Autonomous Catalog Verification Agent for FreeInference.dev.
Your mission: Audit and verify the live ground truth for a single free AI inference provider against real-world documentation.

PROVIDER TO VERIFY:
- Provider Name: {pname}
- Target URL: {target_url}
- Access Method: {provider.get('access_method')}
- Current Free Tier Type: {provider.get('free_type')}
- Current Cataloged Models: {json.dumps(existing_models, indent=2)}
- Current Documented Notes: {provider.get('notes', '')}

INSTRUCTIONS (using Google Chrome in your hosted sandbox):
1. Navigate to {target_url} in Google Chrome.
2. If the page contains tabs, navigation links, or sub-sections for "Pricing", "Rate Limits", "Free Tier", or "Models", click and inspect them.
3. Determine whether an active $0 developer free tier is confirmed:
   - Does it require a credit card upfront? (If yes, classify as 'trial credits' or paid).
   - Are there permanent rate-limited free allowances (e.g. RPM, RPD, TPM)?
   - Is the free tier explicitly discontinued or paywalled?
4. Extract the exact list of available $0 free models:
   - Specific model identifiers (e.g. "llama-3.3-70b-versatile", "gemini-2.5-flash")
   - Context window (e.g. "128K", "1M")
   - Rate limits: RPM (requests/min), TPM (tokens/min), RPD (requests/day), TPD (tokens/day)
5. Compare against the currently cataloged models:
   - Confirm which existing models remain active.
   - Detect newly added free models.
   - Flag any removed or discontinued models.
6. Status verdict rules:
   - "active": Free tier confirmed active with existing cataloged models verified.
   - "changed": Confirmed changes in model lineup (new models added, older models dropped) or updated rate limits.
   - "deprecated": Free tier explicitly discontinued, shut down, or fully paywalled.
   - "inconclusive": Page blocked by anti-bot checkpoint (Cloudflare Turnstile, CAPTCHA) or requires internal authentication.

OUTPUT FORMAT:
Output ONLY a single valid JSON object matching this schema:
{{
  "status": "active" | "changed" | "deprecated" | "inconclusive",
  "is_free_active": true | false | null,
  "summary": "1-2 concise sentences summarizing the verification verdict.",
  "models": [
    {{
      "name": "model-identifier",
      "cost": "$0",
      "context": "context-length",
      "rpm": "RPM or 'Not published'",
      "tpm": "TPM or 'Not published'",
      "rpd": "RPD or 'Not published'",
      "tpd": "TPD or 'Not published'"
    }}
  ]
}}
"""
    api_url = f"{INTERACTIONS_URL}?key={key}"
    body = {
        "agent": ANTIGRAVITY_AGENT,
        "input": prompt,
        "environment": "remote",
        "background": True,
        "store": True,
        "agent_config": {"type": "antigravity", "max_total_tokens": 15000}
    }
    req = urllib.request.Request(
        api_url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            init_res = json.load(r)
    except Exception as e:
        return {
            "status": "inconclusive",
            "is_free_active": None,
            "models": [],
            "summary": f"Antigravity agent failed to initialize: {e}"
        }

    iid = init_res.get("id")
    if not iid:
        return {
            "status": "inconclusive",
            "is_free_active": None,
            "models": [],
            "summary": "Antigravity agent initialization returned no interaction ID"
        }
    print(f"  [antigravity] Started interaction {iid} for {pname} (timeout={timeout}s)")

    poll_url = f"{INTERACTIONS_URL}/{iid}?key={key}"
    t0 = time.time()
    last_reported_step = -1
    while time.time() - t0 < timeout:
        poll_interval = 3 if (time.time() - t0) < 30 else 6
        time.sleep(poll_interval)
        try:
            with urllib.request.urlopen(poll_url, timeout=30) as r:
                poll_res = json.load(r)
        except Exception as pe:
            print(f"  [antigravity] poll error: {pe}")
            continue

        st = poll_res.get("status")
        steps = poll_res.get("steps", [])
        if len(steps) != last_reported_step:
            print(f"  [antigravity] status={st}, steps={len(steps)}, elapsed={time.time()-t0:.1f}s")
            last_reported_step = len(steps)

        if st in ("completed", "failed", "incomplete"):
            output_text = ""
            for s in reversed(steps):
                for c in s.get("content", []):
                    if "text" in c and c["text"].strip():
                        output_text = c["text"].strip()
                        break
                if output_text:
                    break

            if not output_text:
                summaries = []
                for s in steps:
                    for sm in s.get("summary", []):
                        if isinstance(sm, dict) and sm.get("text"):
                            summaries.append(sm["text"])
                output_text = "\n\n".join(summaries)

            payload = extract_json_payload(output_text)
            if payload and payload.get("status") in ("active", "changed", "deprecated", "inconclusive"):
                return payload

            # Fallback if agent provided conversational observations rather than raw JSON
            if output_text:
                from core.model import call_gemini_json
                from core.verifier import VERIFIER_SCHEMA
                synth_prompt = (
                    f"Based on these live Chrome browser audit observations for {pname} ({target_url}):\n\n"
                    f"{output_text[:3500]}\n\n"
                    f"Synthesize the structured audit verdict matching the schema."
                )
                try:
                    synth_res = call_gemini_json(synth_prompt, VERIFIER_SCHEMA, key=key)
                    if synth_res and synth_res.get("status"):
                        return synth_res
                except Exception as synth_err:
                    print(f"  Notice: Synthesis from agent observations failed: {synth_err}")

            return {
                "status": "inconclusive",
                "is_free_active": None,
                "models": [],
                "summary": f"Antigravity agent finished with status {poll_res.get('status')} but generated unparseable output."
            }

    # If timed out but steps were recorded, harvest observations rather than discarding
    steps = poll_res.get("steps", []) if 'poll_res' in locals() else []
    if steps:
        summaries = []
        for s in steps:
            for sm in s.get("summary", []):
                if isinstance(sm, dict) and sm.get("text"):
                    summaries.append(sm["text"])
            for c in s.get("content", []):
                if isinstance(c, dict) and "text" in c and c["text"].strip():
                    summaries.append(c["text"].strip())
        if summaries:
            partial_text = "\n\n".join(summaries)
            payload = extract_json_payload(partial_text)
            if payload and payload.get("status") in ("active", "changed", "deprecated", "inconclusive"):
                return payload
            from core.model import call_gemini_json
            from core.verifier import VERIFIER_SCHEMA
            synth_prompt = (
                f"Antigravity Chrome browser agent timed out after {timeout}s while auditing {pname} ({target_url}), "
                f"but recorded these intermediate observations:\n\n{partial_text[:3500]}\n\n"
                f"Based on what was observed, synthesize the best audit verdict matching the schema."
            )
            try:
                synth_res = call_gemini_json(synth_prompt, VERIFIER_SCHEMA, key=key)
                if synth_res and synth_res.get("status"):
                    return synth_res
            except Exception as synth_err:
                print(f"  [antigravity] Partial timeout synthesis failed: {synth_err}")

    return {
        "status": "inconclusive",
        "is_free_active": None,
        "models": [],
        "summary": f"Antigravity agent timed out after {timeout}s on {target_url}"
    }


def fetch_web_browser_agent(url: str, key: str, timeout: int = 150) -> str:
    """Escalation Fallback: Cloud Antigravity Agent driving real Google Chrome."""
    if not key:
        return "Browser agent unavailable: missing GEMINI_API_KEY"

    prompt = (
        f"Navigate to {url} using Google Chrome. Inspect the pricing table, "
        "developer free tier allowance, rate limits, and models. "
        "Summarize the findings in 3-5 concise bullet points."
    )
    api_url = f"{INTERACTIONS_URL}?key={key}"
    body = {
        "agent": ANTIGRAVITY_AGENT,
        "input": prompt,
        "environment": "remote",
        "background": True,
        "store": True,
        "agent_config": {"type": "antigravity", "max_total_tokens": 15000}
    }
    req = urllib.request.Request(
        api_url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            init_res = json.load(r)
    except Exception as e:
        return f"Browser agent failed to initialize: {e}"

    iid = init_res.get("id")
    if not iid:
        return "Browser agent failed: no interaction ID"

    poll_url = f"{INTERACTIONS_URL}/{iid}?key={key}"
    t0 = time.time()
    while time.time() - t0 < timeout:
        poll_interval = 3 if (time.time() - t0) < 30 else 6
        time.sleep(poll_interval)
        try:
            with urllib.request.urlopen(poll_url, timeout=30) as r:
                poll_res = json.load(r)
        except Exception:
            continue

        if poll_res.get("status") in ("completed", "failed", "incomplete"):
            steps = poll_res.get("steps", [])
            for s in reversed(steps):
                for c in s.get("content", []):
                    if "text" in c and c["text"].strip():
                        return c["text"].strip()
            return f"Browser agent completed with status {poll_res.get('status')}"

    return f"Browser agent timed out after {timeout}s"


def fetch_web(url: str, key: str = None, fallback_to_browser: bool = True) -> str:
    """Modality 3: Website. Static HTML strip first (100ms); browser agent only if blocked/SPA."""
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8", errors="ignore")

        # Strip scripts, styles, svgs, nav, footer
        text = re.sub(r"<(script|style|svg|nav|footer|header)[^>]*>[\s\S]*?</\1>", " ", html, flags=re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        clean_text = " ".join(text.split())

        # Check if text is sufficient and not a bot challenge / empty shell
        is_challenge = any(w in clean_text.lower() for w in [
            "security checkpoint", "cf-browser-verification", "turnstile", "checking your browser",
            "cloudflare ray id", "challenge-platform", "just a moment",
            "access denied", "please verify you are human"
        ])
        if len(clean_text) >= 150 and not is_challenge:
            return clean_text[:4000]

    except Exception:
        pass

    # Static fetch was blocked or yielded empty SPA shell — escalate to cloud browser agent
    if fallback_to_browser and key:
        return fetch_web_browser_agent(url, key)

    return "Web fetch failed or page requires JavaScript execution."
