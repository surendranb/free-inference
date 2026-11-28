"""Unified acquisition layer for the 3 routes: Open Feeds, APIs + Machine Docs (llms.txt/.md), and Antigravity Chrome."""

from __future__ import annotations

import html as _html
import json
import re
import threading
import time
from typing import Any, Dict, List, Optional
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from core.model import call_gemini_json

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    )
}
MD_HEADERS = {
    **UA,
    "Accept": "text/markdown, text/plain;q=0.9, application/json;q=0.8",
}

INTERACTIONS_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
ANTIGRAVITY_AGENT = "antigravity-preview-09-2026"
MAX_TOTAL_TOKENS = 80000
MAX_DOCS_CHARS = 120000
_CHROME_SEMAPHORE = threading.Semaphore(2)

FEED_ENDPOINTS: Dict[str, str] = {
    "OpenRouter": "https://openrouter.ai/api/v1/models",
    "Kilo Gateway": "https://api.kilo.ai/api/gateway/models",
    "Requesty": "https://router.requesty.ai/v1/models",
    "Nous Portal": "https://inference-api.nousresearch.com/v1/models",
    "OVHcloud AI Endpoints": "https://catalog.endpoints.ai.ovh.net/rest/v1/models_v2",
    "AIHubMix": "https://aihubmix.com/call/free_quota_config",
}

API_ENDPOINTS: Dict[str, str] = {
    "Google AI Studio (Gemini API)": "https://generativelanguage.googleapis.com/v1beta/models",
    "SambaNova Cloud": "https://api.sambanova.ai/v1/models",
    "DeepInfra": "https://api.deepinfra.com/v1/openai/models",
    "Synap by Linkrra": "https://synap402.com/v1/models",
    "NVIDIA NIM (build.nvidia.com)": "https://integrate.api.nvidia.com/v1/models",
    "ModelScope": "https://api-inference.modelscope.cn/v1/models",
}

API_DOCS_URLS: Dict[str, List[str]] = {
    "Google AI Studio (Gemini API)": [
        "https://ai.google.dev/gemini-api/docs/rate-limits",
        "https://ai.google.dev/gemini-api/docs/pricing",
    ],
    "SambaNova Cloud": [
        "https://docs.sambanova.ai/docs/en/models/rate-limits",
        "https://docs.sambanova.ai/docs/en/models/sambacloud-models",
    ],
    "NVIDIA NIM (build.nvidia.com)": [
        "https://build.nvidia.com/llms.txt",
        "https://build.nvidia.com/models.md",
    ],
    "ModelScope": [
        "https://modelscope.cn/docs/llms.txt",
    ],
}

# Explicit docs subdomain / nested path hints where /llms.txt is hosted separately from provider url
LLMS_INDEX_HINTS: Dict[str, List[str]] = {
    "OpenCode Zen": ["https://opencode.ai/v2/llms.txt", "https://opencode.ai/llms.txt"],
    "Cloudflare Workers AI": ["https://developers.cloudflare.com/workers-ai/llms.txt", "https://developers.cloudflare.com/llms.txt"],
    "Cohere": ["https://docs.cohere.com/v2/llms.txt", "https://docs.cohere.com/docs/llms.txt"],
    "AssemblyAI": ["https://www.assemblyai.com/docs/llms.txt", "https://www.assemblyai.com/llms.txt"],
    "Z.AI (Zhipu)": ["https://docs.z.ai/llms.txt"],
    "SiliconFlow": ["https://docs.siliconflow.com/llms.txt"],
    "Liquid AI": ["https://docs.liquid.ai/llms.txt"],
    "ModelScope": ["https://modelscope.cn/docs/llms.txt"],
    "NVIDIA NIM (build.nvidia.com)": ["https://build.nvidia.com/llms.txt"],
    "AIHubMix": ["https://aihubmix.com/llms.txt"],
}

# Exact machine-markdown URLs always fetched first for providers whose free/billing policy lives off-path
REQUIRED_MD_URLS: Dict[str, List[str]] = {
    "Mistral La Plateforme": [
        "https://docs.mistral.ai/llms/admin/billing-usage/usage-limits/llms.txt",
        "https://docs.mistral.ai/llms/admin/billing-usage/subscriptions/llms.txt",
    ],
    "AIHubMix": [
        "https://aihubmix.com/agents.md",
    ],
}

ROUTER_ID_RE = re.compile(
    r"^(?:openrouter/free|openrouter/auto|kilo-auto/.+|free\s+models\s+router|auto\s+(?:efficient|free|router).*)$",
    re.I,
)
CHALLENGE_MARKERS = (
    "security checkpoint",
    "cf-browser-verification",
    "turnstile",
    "checking your browser",
    "cloudflare ray id",
    "challenge-platform",
    "just a moment",
    "access denied",
    "please verify you are human",
)
LIMIT_HINT_RE = re.compile(r"\b(?:rate\s+limit|rpm|tpm|rpd|tpd|concurrent|requests?\s+per|\$0)\b", re.I)
MD_LINK_RE = re.compile(r"\[([^\]]{1,80})\]\((https?://[^\s\)\"']+|/[^\s\)\"']+)\)")
LLMS_NAV_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "urls": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
        }
    },
    "required": ["urls"],
}


def normalize_model_key(name: str) -> str:
    """Canonical alphanumeric comparison key to deduplicate ID vs display-name twins."""
    s = str(name or "").lower().strip()
    if "/" in s:
        s = s.rsplit("/", 1)[-1]
    if ":" in s:
        head, tail = s.split(":", 1)
        if tail.strip() == "free":
            s = head
        elif " " in tail:
            s = tail
    s = s.replace("+", "plus")
    s = re.sub(r"\(free\)", "", s, flags=re.I)
    return re.sub(r"[^a-z0-9]", "", s)


def make_observation(
    route: str,
    provider: str,
    ok: bool,
    http_status: Optional[int] = None,
    error_code: Optional[str] = None,
    payload: Any = None,
    docs_text: str = "",
    agent_meta: Optional[Dict[str, Any]] = None,
    source_urls: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Create the standardized RouteObservation dict shared across intake -> verifier."""
    return {
        "route": route,
        "provider": provider,
        "ok": ok,
        "http_status": http_status,
        "error_code": error_code,
        "payload": payload if payload is not None else {},
        "docs_text": docs_text,
        "agent_meta": agent_meta or {},
        "source_urls": source_urls or [],
    }


def resolve_route(provider: Dict[str, Any]) -> str:
    """Classify provider cleanly into Route 1 (feed), Route 2 (api), or Route 3 (web)."""
    pname = provider.get("name", "")
    if pname in FEED_ENDPOINTS or provider.get("feed_url") or (provider.get("channel") or "").lower() == "feed":
        return "feed"
    if pname in API_ENDPOINTS or (provider.get("channel") or "").lower() == "api":
        return "api"
    return "web"


def is_router_model(model_obj: Dict[str, Any]) -> bool:
    """Detect synthetic meta-routers (openrouter/free, kilo-auto/*) that wrap other models."""
    mid = str(model_obj.get("id") or model_obj.get("name") or "")
    return bool(model_obj.get("autoRouting") or ROUTER_ID_RE.match(mid.strip()))


def _to_float(val: Any) -> Optional[float]:
    if val is None or val == "":
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def is_feed_model_free(m: Dict[str, Any]) -> bool:
    """Determine if a feed model entry advertises $0 pricing across heterogeneous feed schemas."""
    mid = str(m.get("id") or m.get("model_id") or m.get("name") or "")
    if ":free" in mid.lower() or m.get("isFree") is True:
        return True

    pricing = m.get("pricing")
    if isinstance(pricing, dict):
        p_in = _to_float(pricing.get("prompt") if "prompt" in pricing else pricing.get("input"))
        p_out = _to_float(pricing.get("completion") if "completion" in pricing else pricing.get("output"))
        if p_in == 0.0 and p_out == 0.0:
            return True

    in_p = _to_float(m.get("input_price"))
    out_p = _to_float(m.get("output_price"))
    if in_p == 0.0 and out_p == 0.0:
        return True

    return False


def _http_get_text(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 20) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers=headers or UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status = getattr(r, "status", None) or r.getcode() or 200
            ct = r.headers.get("Content-Type", "") if hasattr(r, "headers") else ""
            return int(status), ct, r.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="ignore")[:500]
        except Exception:
            pass
        return int(e.code), "", body


def format_context(ctx: Any) -> str:
    """Format numeric context length into human-readable representation."""
    if not ctx:
        return "Model-dependent"
    if isinstance(ctx, (int, float)):
        if ctx >= 1048576:
            return f"{int(ctx // 1048576)}M" if ctx % 1048576 == 0 else f"{round(ctx / 1048576, 1)}M"
        if ctx >= 1000000:
            return f"{round(ctx / 1000000, 1)}M"
        if ctx >= 1024:
            return f"{int(ctx // 1024)}K" if ctx % 1024 == 0 else f"{round(ctx / 1024, 1)}K"
        if ctx >= 1000:
            return f"{int(ctx // 1000)}K"
        return str(ctx)
    return str(ctx)


def _strip_html(html: str) -> str:
    text = re.sub(r"<(script|style|svg|nav|footer|header)[^>]*>[\s\S]*?</\1>", " ", html, flags=re.I)
    text = re.sub(r"<[^>]+>|\{%[^%]+%\}", " ", text)
    return " ".join(_html.unescape(text).split())


def _is_challenge(text: str) -> bool:
    low = text.lower()
    return any(marker in low for marker in CHALLENGE_MARKERS)


def _looks_like_html(text: str) -> bool:
    head = text.lstrip()[:350].lower()
    return (
        head.startswith(("<!doctype", "<html", "<?xml"))
        or "<head>" in head
        or "<script" in head
        or _is_challenge(head)
    )


def fetch_markdown_only(url: str, timeout: int = 12) -> tuple[bool, int, str]:
    """Fetch machine-readable Markdown / plain text only; strictly reject HTML shells."""
    if not url:
        return False, 0, ""
    try:
        status, ct, raw = _http_get_text(url, headers=MD_HEADERS, timeout=timeout)
        if status >= 400 or not raw.strip():
            return False, status, ""
        if "text/html" in ct.lower() or _looks_like_html(raw):
            return False, status, ""
        return True, status, raw.strip()[:MAX_DOCS_CHARS]
    except Exception:
        return False, 0, ""


def fetch_docs_static(url: str, timeout: int = 15) -> tuple[bool, int, str]:
    """Try markdown mirror first, then fallback to stripped HTML for Feed/API pricing references."""
    if not url:
        return False, 0, ""
    parsed = urllib.parse.urlparse(url)
    if parsed.path and parsed.path != "/" and not url.endswith((".md", ".txt")):
        ok_md, st_md, raw_md = fetch_markdown_only(url.rstrip("/") + ".md", timeout=10)
        if ok_md and len(raw_md) > 80:
            return True, st_md, raw_md
    ok_direct, st_dir, raw_dir = fetch_markdown_only(url, timeout=10)
    if ok_direct and len(raw_dir) > 80:
        return True, st_dir, raw_dir
    try:
        status, _, raw = _http_get_text(url, headers=UA, timeout=timeout)
        if status >= 400:
            return False, status, f"HTTP {status}"
        clean = _strip_html(raw)
        if not clean or _is_challenge(clean):
            return False, status, "Blocked by WAF/challenge"
        return True, status, clean[:MAX_DOCS_CHARS]
    except Exception as e:
        return False, 0, f"Static fetch error: {e}"


def _select_llms_links(
    provider_name: str,
    llms_text: str,
    base_origin: str,
    gemini_key: Optional[str] = None,
) -> List[str]:
    """Select top 1-3 pricing/free-tier/rate-limit/model links from an llms.txt index."""
    candidates: List[tuple[str, str]] = []
    seen = set()
    for label, href in MD_LINK_RE.findall(llms_text):
        full = urllib.parse.urljoin(base_origin + "/", href) if href.startswith("/") else href
        if full not in seen and full.startswith("http"):
            seen.add(full)
            candidates.append((label.strip(), full))

    if not candidates:
        return []

    hint_re = re.compile(r"(pric|free|rate[-_ ]?limit|quota|credit|plan|tier|model|usage|billing)", re.I)
    shortlisted = [c for c in candidates if hint_re.search(c[0]) or hint_re.search(c[1])]
    pool = (shortlisted if shortlisted else candidates)[:60]

    if gemini_key and len(pool) > 3:
        listing = "\n".join(f"- [{lbl}] {u}" for lbl, u in pool)
        prompt = (
            f"Provider: {provider_name}\n"
            "From these links in `llms.txt`, pick the top 1 to 3 URLs most likely to state "
            "free tier eligibility, pricing, credits, rate limits (RPM/TPM/RPD/TPD), and available models:\n"
            f"{listing}"
        )
        try:
            picked = call_gemini_json(prompt, LLMS_NAV_SCHEMA, key=gemini_key, timeout=20).get("urls", [])
            valid_set = {u for _, u in candidates}
            chosen = [u for u in picked if u in valid_set][:3]
            if chosen:
                return chosen
        except Exception:
            pass

    return [u for _, u in pool[:3]]


def fetch_machine_docs(provider: Dict[str, Any], gemini_key: Optional[str] = None) -> Dict[str, Any]:
    """Agent-native Markdown intake (url.md, Accept: text/markdown, llms.txt + linked .md docs)."""
    pname = provider.get("name", "Unknown")
    target_url = provider.get("docs_url") or provider.get("url", "")
    parsed = urllib.parse.urlparse(target_url)
    origin = f"{parsed.scheme}://{parsed.netloc}" if parsed.netloc else ""
    parts = [seg for seg in parsed.path.split("/") if seg]

    chunks: List[str] = []
    fetched_urls: List[str] = []

    def _add_md(u: str, cap: int = 65000) -> bool:
        if not u or u in fetched_urls:
            return False
        ok, _, txt = fetch_markdown_only(u)
        if not ok or len(txt) < 60:
            return False
        fetched_urls.append(u)
        chunks.append(f"[SOURCE: {u}]\n{txt[:cap]}")
        return True

    # 1. Fetch pinned policy/billing markdown docs + direct .md / Accept: text/markdown on docs url
    for req_u in REQUIRED_MD_URLS.get(pname, []):
        _add_md(req_u, cap=40000)

    if target_url:
        if parsed.path and parsed.path != "/" and not target_url.endswith((".md", ".html")):
            _add_md(target_url.rstrip("/") + ".md")
        _add_md(target_url)

    # 2. Discover & fetch llms.txt index (domain + explicit docs subdomain hints)
    index_candidates: List[str] = list(LLMS_INDEX_HINTS.get(pname, []))
    if origin:
        if parts:
            index_candidates.append(f"{origin}/{parts[0]}/llms.txt")
        index_candidates.append(f"{origin}/llms.txt")
        if not chunks:
            index_candidates.append(f"{origin}/llms-full.txt")

    seen_idx = set()
    index_candidates = [u for u in index_candidates if not (u in seen_idx or seen_idx.add(u))]

    for idx_url in index_candidates:
        if idx_url in fetched_urls:
            continue
        ok, _, idx_txt = fetch_markdown_only(idx_url)
        if not ok or len(idx_txt) < 60:
            continue
        fetched_urls.append(idx_url)
        if idx_url.endswith("llms-full.txt"):
            chunks.append(f"[SOURCE: {idx_url}]\n{idx_txt[:55000]}")
            break

        # Parse & follow top 1-3 pricing/rate-limit/model links inside llms.txt
        idx_origin = f"{urllib.parse.urlparse(idx_url).scheme}://{urllib.parse.urlparse(idx_url).netloc}"
        chosen_links = _select_llms_links(pname, idx_txt, idx_origin, gemini_key=gemini_key)
        followed_any = False
        for link in chosen_links:
            if not link.endswith((".md", ".txt", ".json")):
                if _add_md(link.rstrip("/") + ".md", cap=35000):
                    followed_any = True
                    continue
            if _add_md(link, cap=35000):
                followed_any = True
        if not followed_any or not chunks:
            chunks.append(f"[SOURCE: {idx_url}]\n{idx_txt[:40000]}")
        break

    if not chunks:
        return make_observation(
            route="web",
            provider=pname,
            ok=False,
            error_code="NO_MACHINE_DOCS",
            agent_meta={"acquisition_mode": "none"},
            source_urls=[target_url] if target_url else [],
        )

    combined = "\n\n".join(chunks)[:MAX_DOCS_CHARS]
    return make_observation(
        route="web",
        provider=pname,
        ok=True,
        http_status=200,
        payload={"docs_kind": "machine_markdown", "urls_read": len(fetched_urls)},
        docs_text=combined,
        agent_meta={"acquisition_mode": "llms_md", "urls_read": len(fetched_urls)},
        source_urls=fetched_urls,
    )


def fetch_feed(url: str, max_items: int = 50) -> str:
    """Parse RSS/Atom/JSON feed text cleanly."""
    try:
        status, _, raw = _http_get_text(url, headers=UA, timeout=15)
        if status >= 400:
            return f"Feed fetch failed: HTTP {status}"
    except Exception as e:
        return f"Feed fetch failed: {e}"

    try:
        root = ET.fromstring(raw)
        items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
        lines = []
        for it in items[:max_items]:
            title = it.findtext("title") or it.findtext("{http://www.w3.org/2005/Atom}title") or ""
            desc = it.findtext("description") or it.findtext("{http://www.w3.org/2005/Atom}summary") or ""
            clean_desc = re.sub(r"<[^>]+>", " ", desc).strip()[:240]
            lines.append(f"- {title.strip()}: {clean_desc}")
        if lines:
            return "\n".join(lines)
    except ET.ParseError:
        pass

    return raw[:MAX_DOCS_CHARS]


def _compact_feed_item(m: Dict[str, Any]) -> Dict[str, Any]:
    mid = m.get("id") or m.get("model_id") or m.get("name")
    item: Dict[str, Any] = {"id": mid}
    if m.get("name") and m["name"] != mid:
        item["display_name"] = m["name"]
    ctx = m.get("context_length") or m.get("inputTokenLimit") or (m.get("limit") or {}).get("context")
    if ctx:
        item["context"] = format_context(ctx)
    if "available" in m:
        item["available"] = m["available"]
    if m.get("category"):
        item["category"] = m["category"]
    return item


def _has_explicit_pricing(items: List[Any]) -> bool:
    for m in items:
        if isinstance(m, dict) and (
            "pricing" in m or "isFree" in m or "input_price" in m or "output_price" in m or ":free" in str(m.get("id", "")).lower()
        ):
            return True
    return False


def fetch_feed_route(provider: Dict[str, Any]) -> Dict[str, Any]:
    """Route 1 (Feed): Acquire complete structured model feed + pricing/rate-limit docs text."""
    pname = provider.get("name", "Unknown")
    base_url = provider.get("base_url", "")
    docs_url = provider.get("docs_url") or provider.get("url", "")
    feed_url = provider.get("feed_url") or FEED_ENDPOINTS.get(pname) or (
        base_url.rstrip("/") + ("/models" if base_url.rstrip("/").endswith("/v1") else "")
    )
    source_urls = [u for u in (feed_url, docs_url) if u]

    try:
        status, _, raw = _http_get_text(feed_url, headers=UA, timeout=25)
    except Exception as e:
        code = "TIMEOUT" if "timed out" in str(e).lower() else "FETCH_ERROR"
        return make_observation("feed", pname, False, error_code=code, docs_text=str(e), agent_meta={"acquisition_mode": "feed"}, source_urls=source_urls)

    if status >= 400:
        return make_observation("feed", pname, False, http_status=status, error_code=f"HTTP_{status}", docs_text=raw, agent_meta={"acquisition_mode": "feed"}, source_urls=source_urls)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        text_feed = fetch_feed(feed_url)
        return make_observation("feed", pname, True, http_status=status, payload={"feed_text": text_feed}, agent_meta={"acquisition_mode": "feed"}, source_urls=source_urls)

    # AIHubMix /call/free_quota_config live free-tier JSON
    if isinstance(data, dict) and isinstance((data.get("data") or {}), dict) and "weight_map" in data["data"]:
        cfg = data["data"]
        wmap = cfg.get("weight_map") or {}
        free_models = [
            {
                "id": mid,
                "request_weight": weight,
                "minute_limit": cfg.get("minute_limit"),
                "daily_request_limit": cfg.get("daily_request_limit"),
                "daily_token_limit": cfg.get("daily_token_limit"),
                "trial_unpaid_request_limit": cfg.get("trial_unpaid_request_limit"),
            }
            for mid, weight in wmap.items()
        ]
        docs_obs = fetch_machine_docs(provider)
        payload = {
            "feed_url": feed_url,
            "priced": True,
            "total_models": len(free_models),
            "free_models_count": len(free_models),
            "router_excluded": [],
            "quota_config": {k: v for k, v in cfg.items() if k != "weight_map"},
            "free_models": free_models,
        }
        return make_observation(
            route="feed",
            provider=pname,
            ok=True,
            http_status=status,
            payload=payload,
            docs_text=docs_obs.get("docs_text", ""),
            agent_meta={"acquisition_mode": "feed"},
            source_urls=source_urls,
        )

    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get("data") or data.get("models") or []
    else:
        items = []

    priced = _has_explicit_pricing(items)
    free_models: List[Dict[str, Any]] = []
    available_models: List[Dict[str, Any]] = []
    router_excluded: List[str] = []
    for m in items:
        if not isinstance(m, dict):
            continue
        if is_router_model(m):
            router_excluded.append(str(m.get("id") or m.get("name")))
            continue
        if priced:
            if is_feed_model_free(m):
                free_models.append(_compact_feed_item(m))
        elif m.get("available", True):
            available_models.append(_compact_feed_item(m))

    docs_ok, _, docs_text = fetch_docs_static(docs_url)
    payload = {
        "feed_url": feed_url,
        "priced": priced,
        "total_models": len(items),
        "free_models_count": len(free_models),
        "router_excluded": router_excluded,
        "free_models": free_models,
    }
    if available_models:
        payload["available_models_count"] = len(available_models)
        payload["available_models"] = available_models

    return make_observation(
        route="feed",
        provider=pname,
        ok=True,
        http_status=status,
        payload=payload,
        docs_text=docs_text if docs_ok else "",
        agent_meta={"acquisition_mode": "feed"},
        source_urls=source_urls,
    )


def fetch_api_route(provider: Dict[str, Any], gemini_key: Optional[str] = None) -> Dict[str, Any]:
    """Route 2 (API): Query provider API without foreign key leaks + corroborate with live docs."""
    pname = provider.get("name", "Unknown")
    base_url = provider.get("base_url", "")
    docs_url = provider.get("docs_url") or provider.get("url", "")
    api_url = API_ENDPOINTS.get(pname) or (
        base_url.rstrip("/") + ("/models" if base_url and "/models" not in base_url else "")
    )
    source_urls = [u for u in (api_url, docs_url) if u]

    is_google = "generativelanguage.googleapis.com" in api_url
    if is_google and not gemini_key:
        return make_observation("api", pname, False, error_code="MISSING_API_KEY", docs_text="Missing GEMINI_API_KEY", agent_meta={"acquisition_mode": "api"}, source_urls=source_urls)

    request_url = f"{api_url}?pageSize=1000&key={gemini_key}" if is_google else api_url
    try:
        # Never inject Gemini's API key as Authorization Bearer onto third-party hosts
        status, _, raw = _http_get_text(request_url, headers=UA, timeout=25)
    except Exception as e:
        code = "TIMEOUT" if "timed out" in str(e).lower() else "FETCH_ERROR"
        return make_observation("api", pname, False, error_code=code, docs_text=str(e), agent_meta={"acquisition_mode": "api"}, source_urls=source_urls)

    if status >= 400:
        return make_observation("api", pname, False, http_status=status, error_code=f"HTTP_{status}", docs_text=raw, agent_meta={"acquisition_mode": "api"}, source_urls=source_urls)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return make_observation("api", pname, False, http_status=status, error_code="INVALID_JSON", docs_text=str(e), agent_meta={"acquisition_mode": "api"}, source_urls=source_urls)

    payload: Dict[str, Any] = {"api_url": api_url}
    if pname == "Synap by Linkrra":
        ft_status, _, ft_raw = _http_get_text("https://synap402.com/api/account/free-tier", headers=UA, timeout=15)
        payload["free_tier"] = json.loads(ft_raw) if ft_status == 200 else {"error": f"HTTP {ft_status}"}
        payload["models"] = [
            {"id": m.get("id"), "is_free": m.get("is_free"), "routing": m.get("routing")}
            for m in (data.get("data") or [])
            if isinstance(m, dict)
        ]
    elif is_google:
        raw_models = data.get("models", [])
        gen_models = []
        for m in raw_models:
            if not isinstance(m, dict):
                continue
            methods = m.get("supportedGenerationMethods", [])
            if not any(gm in methods for gm in ("generateContent", "bidiGenerateContent")):
                continue
            gen_models.append({
                "id": str(m.get("name", "")).removeprefix("models/"),
                "displayName": m.get("displayName"),
                "inputTokenLimit": m.get("inputTokenLimit"),
                "outputTokenLimit": m.get("outputTokenLimit"),
                "methods": methods,
            })
        payload["total_models"] = len(raw_models)
        payload["generation_models"] = gen_models
    else:
        raw_models = data if isinstance(data, list) else (data.get("data") or data.get("models") or [])
        compact = []
        for m in raw_models:
            if not isinstance(m, dict):
                continue
            entry: Dict[str, Any] = {"id": m.get("id") or m.get("name")}
            if m.get("context_length"):
                entry["context_length"] = m["context_length"]
            if "pricing" in m:
                entry["pricing"] = m["pricing"]
            elif isinstance(m.get("metadata"), dict) and "pricing" in m["metadata"]:
                entry["pricing"] = m["metadata"]["pricing"]
            compact.append(entry)
        payload["total_models"] = len(raw_models)
        payload["models"] = compact

    # Gather docs via API_DOCS_URLS or machine llms.txt/.md before checking browser escalation
    doc_targets = API_DOCS_URLS.get(pname) or ([docs_url] if docs_url else [])
    for durl in doc_targets:
        if durl not in source_urls:
            source_urls.append(durl)

    doc_chunks: List[str] = []
    for durl in doc_targets:
        if durl.endswith(".txt") or durl.endswith(".md"):
            ok_md, _, md_txt = fetch_markdown_only(durl)
            if ok_md and md_txt:
                doc_chunks.append(f"[SOURCE: {durl}]\n{md_txt}")
        else:
            d_ok, _, d_txt = fetch_docs_static(durl)
            if d_ok and d_txt:
                doc_chunks.append(f"[SOURCE: {durl}]\n{d_txt}")

    docs_text = "\n\n".join(doc_chunks)[:MAX_DOCS_CHARS]
    if (not docs_text or (len(docs_text) < 250 and not LIMIT_HINT_RE.search(docs_text))) and pname in LLMS_INDEX_HINTS:
        md_obs = fetch_machine_docs(provider, gemini_key=gemini_key)
        if md_obs["ok"] and md_obs["docs_text"]:
            docs_text = md_obs["docs_text"]

    agent_meta: Dict[str, Any] = {"acquisition_mode": "api"}
    needs_browser_docs = (
        not docs_text
        or (len(docs_text) < 250 and not LIMIT_HINT_RE.search(docs_text))
    )
    if docs_url and needs_browser_docs and gemini_key:
        web_obs = fetch_web_route_antigravity(provider, gemini_key=gemini_key, timeout=120)
        if web_obs["ok"] and web_obs["docs_text"]:
            docs_text = web_obs["docs_text"]
            agent_meta = {**web_obs["agent_meta"], "acquisition_mode": "api_then_chrome"}

    return make_observation(
        route="api",
        provider=pname,
        ok=True,
        http_status=status,
        payload=payload,
        docs_text=docs_text,
        agent_meta=agent_meta,
        source_urls=source_urls,
    )


def fetch_web_route_antigravity(
    provider: Dict[str, Any],
    gemini_key: Optional[str],
    timeout: int = 260,
) -> Dict[str, Any]:
    """Route 3 (Website): Run Cloud Antigravity Agent (real Chrome) with bounded concurrency."""
    with _CHROME_SEMAPHORE:
        return _run_antigravity_chrome(provider, gemini_key=gemini_key, timeout=timeout)


def _run_antigravity_chrome(
    provider: Dict[str, Any],
    gemini_key: Optional[str],
    timeout: int = 260,
) -> Dict[str, Any]:
    pname = provider.get("name", "Unknown")
    target_url = provider.get("docs_url") or provider.get("url", "")
    if not gemini_key:
        return make_observation("web", pname, False, error_code="MISSING_API_KEY", docs_text="Missing GEMINI_API_KEY", agent_meta={"acquisition_mode": "antigravity_chrome"}, source_urls=[target_url])
    if not target_url:
        return make_observation("web", pname, False, error_code="MISSING_URL", docs_text="Provider has no url/docs_url", agent_meta={"acquisition_mode": "antigravity_chrome"})

    existing_models = [m.get("name") for m in provider.get("models", []) if m.get("name")]
    prompt = (
        f"Verify the free developer / API tier for '{pname}' by opening this URL in Google Chrome:\n"
        f"{target_url}\n\n"
        f"Cataloged baseline ({len(existing_models)} models): {', '.join(existing_models[:20])}\n"
        f"Recorded Free Type: {provider.get('free_type', 'Unknown')}\n\n"
        "Inspect Pricing, Rate Limits, Developer Tier, and Models tabs if present (visit at most 2-3 key pages so you finish concisely). Be factual:\n"
        "1. Is a $0 developer API tier or free starter/trial tier currently active without mandatory paid subscription?\n"
        "2. Is a credit card or payment method required to use free tier/credits?\n"
        "3. Exact trial dollar credit/token cap (e.g. $5 credit, 1M tokens) or expiry, if applicable.\n"
        "4. Active free model IDs and published RPM / TPM / RPD / TPD limits or context lengths.\n"
        "5. Any explicit announcement of deprecation, suspension, or paywalling (quote exact words if found)."
    )

    api_url = f"{INTERACTIONS_URL}?key={gemini_key}"
    body = {
        "agent": ANTIGRAVITY_AGENT,
        "input": prompt,
        "environment": "remote",
        "background": True,
        "store": True,
        "agent_config": {"type": "antigravity", "max_total_tokens": MAX_TOTAL_TOKENS},
    }
    encoded = json.dumps(body).encode("utf-8")
    t0 = time.time()
    init_res = None
    last_http_err: Optional[urllib.error.HTTPError] = None
    for attempt in range(4):
        req = urllib.request.Request(api_url, data=encoded, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                init_res = json.load(r)
            break
        except urllib.error.HTTPError as e:
            last_http_err = e
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(15 * (2 ** attempt))
                continue
            return make_observation("web", pname, False, http_status=e.code, error_code=f"HTTP_{e.code}", docs_text=str(e), agent_meta={"acquisition_mode": "antigravity_chrome"}, source_urls=[target_url])
        except Exception as e:
            code = "TIMEOUT" if "timed out" in str(e).lower() else "AGENT_INIT_ERROR"
            return make_observation("web", pname, False, error_code=code, docs_text=str(e), agent_meta={"acquisition_mode": "antigravity_chrome"}, source_urls=[target_url])

    if init_res is None:
        code = f"HTTP_{last_http_err.code}" if last_http_err else "AGENT_INIT_ERROR"
        return make_observation("web", pname, False, http_status=getattr(last_http_err, "code", None), error_code=code, docs_text=str(last_http_err), agent_meta={"acquisition_mode": "antigravity_chrome"}, source_urls=[target_url])

    iid = init_res.get("id")
    if not iid:
        return make_observation("web", pname, False, error_code="MISSING_INTERACTION_ID", docs_text="No interaction id returned", agent_meta={"acquisition_mode": "antigravity_chrome"}, source_urls=[target_url])

    poll_req = urllib.request.Request(
        f"{INTERACTIONS_URL}/{iid}?key={gemini_key}",
        headers={"Content-Type": "application/json"},
    )
    while time.time() - t0 < timeout:
        time.sleep(5)
        try:
            with urllib.request.urlopen(poll_req, timeout=30) as r:
                poll_res = json.load(r)
        except Exception:
            continue

        status = poll_res.get("status")
        if status not in ("completed", "failed", "incomplete", "cancelled"):
            continue

        steps = poll_res.get("steps", [])
        total_tokens = (poll_res.get("usage") or {}).get("total_tokens", 0)
        elapsed = round(time.time() - t0, 2)
        agent_meta = {
            "acquisition_mode": "antigravity_chrome",
            "interaction_id": iid,
            "status": status,
            "steps": len(steps),
            "total_tokens": total_tokens,
            "duration_s": elapsed,
        }
        texts = [
            c["text"].strip()
            for s in reversed(steps)
            for c in s.get("content", [])
            if isinstance(c, dict) and c.get("text", "").strip()
        ]
        summary_text = texts[0] if texts else ""

        if status == "completed" and summary_text:
            return make_observation(
                route="web",
                provider=pname,
                ok=True,
                http_status=200,
                docs_text=summary_text[:MAX_DOCS_CHARS],
                agent_meta=agent_meta,
                source_urls=[target_url],
            )

        err_code = "AGENT_INCOMPLETE" if status == "incomplete" else "AGENT_FAILED"
        return make_observation(
            route="web",
            provider=pname,
            ok=False,
            http_status=200,
            error_code=err_code,
            docs_text=summary_text[:MAX_DOCS_CHARS],
            agent_meta=agent_meta,
            source_urls=[target_url],
        )

    return make_observation(
        route="web",
        provider=pname,
        ok=False,
        error_code="AGENT_TIMEOUT",
        agent_meta={"acquisition_mode": "antigravity_chrome", "interaction_id": iid, "status": "timeout", "duration_s": round(time.time() - t0, 2)},
        source_urls=[target_url],
    )


def acquire_observation(provider: Dict[str, Any], gemini_key: Optional[str] = None) -> Dict[str, Any]:
    """Dispatch provider cleanly: Feed -> API -> Machine Markdown (llms.txt/.md) -> Antigravity Chrome."""
    route = resolve_route(provider)
    if route == "feed":
        return fetch_feed_route(provider)
    if route == "api":
        return fetch_api_route(provider, gemini_key=gemini_key)
    md_obs = fetch_machine_docs(provider, gemini_key=gemini_key)
    if md_obs.get("ok"):
        return md_obs
    return fetch_web_route_antigravity(provider, gemini_key=gemini_key)


def fetch_web(url: str, key: Optional[str] = None, fallback_to_browser: bool = True) -> str:
    """Fetch machine markdown docs first, escalating to Antigravity Cloud Agent if unavailable."""
    ok, _, text = fetch_markdown_only(url.rstrip("/") + ".md" if not url.endswith(".md") else url)
    if ok and len(text) >= 150:
        return text
    if fallback_to_browser and key:
        obs = fetch_web_route_antigravity({"name": url, "url": url}, gemini_key=key)
        return obs.get("docs_text") or obs.get("error_code") or "Web fetch unavailable"
    return text or "Machine docs unavailable; browser verification required."
