"""Gemini model client with structured JSON outputs and self-correcting retry loop."""

import json
import os
import random
import re
import subprocess
import time
import urllib.error
import urllib.request

MODEL_CASCADE = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemma-4-26b-a4b-it",
    "gemma-4-31b-it",
]
MODEL_NAME = MODEL_CASCADE[0]
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def get_api_key() -> str:
    """Retrieve Gemini API key from environment or macOS keychain."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key.strip()
    try:
        res = subprocess.run(
            ["security", "find-generic-password", "-w", "-s", "gemini-api-key"],
            capture_output=True, text=True, check=True
        )
        return res.stdout.strip()
    except Exception:
        pass
    try:
        res = subprocess.run(
            ["security", "find-generic-password", "-s", "agent-core", "-a", "GOOGLE_API_KEY", "-w"],
            capture_output=True, text=True, check=True
        )
        return res.stdout.strip()
    except Exception:
        return ""


def call_gemini_json(prompt: str, schema: dict, key: str = None, model: str = None) -> dict:
    """Invoke Gemini with hardware-enforced JSON schema output and cascade failover."""
    api_key = key or get_api_key()
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY or GOOGLE_API_KEY")

    models_to_try = [model] if model else MODEL_CASCADE
    last_err = None

    for m in models_to_try:
        url = f"{API_BASE}/{m}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": schema
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        # In-place exponential backoff with jitter on transient 503/429 before cascading
        max_model_retries = 2
        for attempt in range(max_model_retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=25) as r:
                    res = json.load(r)

                candidates = res.get("candidates", [])
                if not candidates:
                    break

                text = candidates[0]["content"]["parts"][0]["text"].strip()
                if text.startswith("```"):
                    text = re.sub(r"^```(?:json)?\s*", "", text)
                    text = re.sub(r"\s*```$", "", text)
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    m_json = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
                    if m_json:
                        return json.loads(m_json.group(1))
                    raise
            except urllib.error.HTTPError as e:
                last_err = e
                if e.code in (429, 500, 502, 503) and attempt < max_model_retries:
                    backoff = (2 ** attempt * 1.5) + random.uniform(0.5, 1.5)
                    print(f"  [model-retry] {m} returned HTTP {e.code}, retrying in {backoff:.1f}s (attempt {attempt + 1}/{max_model_retries})...")
                    time.sleep(backoff)
                    continue
                if e.code in (429, 500, 502, 503):
                    print(f"  [model-cascade] {m} returned HTTP {e.code} after retries, failing over to next model in cascade...")
                    break
                raise
            except Exception as e:
                last_err = e
                if attempt < max_model_retries:
                    time.sleep(1)
                    continue
                print(f"  [model-cascade] {m} failed with {e}, failing over to next model...")
                break

    raise RuntimeError(f"All models in cascade ({models_to_try}) failed. Last error: {last_err}")


def call_with_self_correction(
    base_prompt: str,
    schema: dict,
    validator_fn,
    key: str = None,
    max_tries: int = 3
) -> dict:
    """Execute model call with iterative self-correction if output fails semantic validation."""
    current_prompt = base_prompt
    last_err = ""
    for attempt in range(max_tries):
        try:
            output = call_gemini_json(current_prompt, schema, key=key)
            err = validator_fn(output)
            if not err:
                return output
            last_err = err
        except Exception as e:
            last_err = f"API or JSON decoding error: {e}"

        # Feed the error back to the model for self-correction
        current_prompt = (
            f"{base_prompt}\n\n"
            f"--- REPAIR INSTRUCTION (Attempt {attempt + 2}/{max_tries}) ---\n"
            f"Your previous output was rejected due to this validation error:\n"
            f"\"{last_err}\"\n"
            f"Please carefully correct the issue and output strictly conforming JSON."
        )

    # Safe fallback if model fails after max iterations
    return {
        "status": "inconclusive",
        "is_free_active": None,
        "models": [],
        "summary": f"Self-correction failed after {max_tries} iterations: {last_err}"
    }
