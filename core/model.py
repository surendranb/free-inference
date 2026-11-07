"""Gemini model client with structured JSON outputs and self-correcting retry loop."""

import json
import os
import subprocess
import urllib.error
import urllib.request

MODEL_NAME = "gemini-3.5-flash-lite"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def get_api_key() -> str:
    """Retrieve Gemini API key from environment or macOS keychain."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip()
    try:
        res = subprocess.run(
            ["security", "find-generic-password", "-w", "-s", "gemini-api-key"],
            capture_output=True, text=True, check=True
        )
        return res.stdout.strip()
    except Exception:
        return ""


def call_gemini_json(prompt: str, schema: dict, key: str = None, model: str = MODEL_NAME) -> dict:
    """Invoke Gemini with hardware-enforced JSON schema output."""
    api_key = key or get_api_key()
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY")

    url = f"{API_BASE}/{model}:generateContent?key={api_key}"
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
    with urllib.request.urlopen(req, timeout=20) as r:
        res = json.load(r)

    candidates = res.get("candidates", [])
    if not candidates:
        raise RuntimeError(f"No candidates returned: {res}")

    text = candidates[0]["content"]["parts"][0]["text"]
    return json.loads(text)


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
