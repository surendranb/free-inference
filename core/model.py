"""Gemini model client with text & schema-enforced JSON outputs and resilient failover."""

import json
import os
import random
import subprocess
import time
from typing import Any, Dict, List, Optional
import urllib.error
import urllib.request

MODEL_CASCADE = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.1-flash-lite-preview",
]
MODEL_NAME = MODEL_CASCADE[0]
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
TRANSIENT_HTTP_CODES = (404, 429, 500, 502, 503, 504)


def get_api_key() -> str:
    """Retrieve Gemini API key from environment or macOS keychain."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key.strip()
    for cmd in (
        ["security", "find-generic-password", "-w", "-s", "gemini-api-key"],
        ["security", "find-generic-password", "-s", "agent-core", "-a", "GOOGLE_API_KEY", "-w"],
    ):
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass
    return ""


def _extract_text(response: Dict[str, Any]) -> str:
    """Extract non-thought text content from the first Gemini candidate."""
    for cand in response.get("candidates", []):
        parts = cand.get("content", {}).get("parts", [])
        chunks = [p["text"] for p in parts if isinstance(p, dict) and p.get("text") and not p.get("thought")]
        if chunks:
            return "\n".join(chunks).strip()
        raw_chunks = [p["text"] for p in parts if isinstance(p, dict) and p.get("text")]
        if raw_chunks:
            return "\n".join(raw_chunks).strip()
    return ""


def _generate_content(
    prompt: str,
    generation_config: Dict[str, Any],
    key: Optional[str] = None,
    model: Optional[str] = None,
    timeout: int = 60,
    attempts_per_model: int = 2,
) -> tuple[str, str]:
    """Call Gemini generateContent across MODEL_CASCADE with jittered retries."""
    api_key = key or get_api_key()
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY or GOOGLE_API_KEY")

    models_to_try: List[str] = [model] if model else MODEL_CASCADE
    last_err: Optional[Exception] = None

    for m in models_to_try:
        url = f"{API_BASE}/{m}:generateContent?key={api_key}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": generation_config,
        }).encode("utf-8")

        for attempt in range(attempts_per_model):
            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    res = json.load(r)
                text = _extract_text(res)
                if text:
                    return text, m
                last_err = RuntimeError(f"{m} returned empty candidate content")
            except urllib.error.HTTPError as e:
                last_err = e
                if e.code not in TRANSIENT_HTTP_CODES:
                    raise
                # Fail fast on 404 without retrying the same missing model
                if e.code == 404:
                    break
            except Exception as e:
                last_err = e

            if attempt < attempts_per_model - 1:
                time.sleep((2 ** attempt) + random.uniform(0.2, 0.8))

        print(f"  [model-cascade] {m} exhausted/unavailable ({last_err}), failing over...")

    raise RuntimeError(f"All models in cascade ({models_to_try}) failed. Last error: {last_err}")


def call_gemini_text(
    prompt: str,
    key: Optional[str] = None,
    model: Optional[str] = None,
    timeout: int = 45,
    temperature: float = 0.2,
    max_output_tokens: int = 2048,
) -> str:
    """Invoke Gemini for freeform/markdown text output with failover cascade."""
    text, _ = _generate_content(
        prompt,
        {"temperature": temperature, "maxOutputTokens": max_output_tokens},
        key=key,
        model=model,
        timeout=timeout,
    )
    return text


def call_gemini_json(
    prompt: str,
    schema: dict,
    key: Optional[str] = None,
    model: Optional[str] = None,
    timeout: int = 60,
) -> dict:
    """Invoke Gemini with schema-enforced JSON output and cascade failover."""
    text, _ = _generate_content(
        prompt,
        {
            "responseMimeType": "application/json",
            "responseSchema": schema,
            "temperature": 0.1,
        },
        key=key,
        model=model,
        timeout=timeout,
    )
    return json.loads(text)


def call_with_self_correction(
    base_prompt: str,
    schema: dict,
    validator_fn,
    key: Optional[str] = None,
    max_tries: int = 3,
    timeout: int = 60,
) -> dict:
    """Execute model call with iterative self-correction if output fails semantic validation."""
    current_prompt = base_prompt
    last_err = ""
    for attempt in range(max_tries):
        try:
            output = call_gemini_json(current_prompt, schema, key=key, timeout=timeout)
            err = validator_fn(output)
            if not err:
                return output
            last_err = err
        except Exception as e:
            last_err = f"API or JSON decoding error: {e}"

        current_prompt = (
            f"{base_prompt}\n\n"
            f"--- REPAIR INSTRUCTION (Attempt {attempt + 2}/{max_tries}) ---\n"
            f"Your previous output was rejected due to this validation error:\n"
            f"\"{last_err}\"\n"
            f"Please carefully correct the issue and output strictly conforming JSON."
        )

    return {
        "status": "inconclusive",
        "is_free_active": None,
        "models": [],
        "summary": f"Self-correction failed after {max_tries} iterations: {last_err}",
    }
