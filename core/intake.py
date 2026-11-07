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


def fetch_web_browser_agent(url: str, key: str, timeout: int = 60) -> str:
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
        time.sleep(5)
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

    return "Browser agent timed out after 60s"


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
