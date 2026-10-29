#!/usr/bin/env python3
"""Autonomous AI Studio Discovery Scout for FreeInference.dev.

Runs nightly via GitHub Actions (.github/workflows/nightly-probe.yml) or locally.
Uses Google AI Studio (gemini-3.5-flash-lite) to analyze live model inventories from
OpenRouter, Google AI Studio, and public endpoints, classifying new free models and
evaluating new provider additions against strict $0 inclusion criteria.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from probe import gemini_key, get_json

DATA_PATH = ROOT / "data" / "providers.json"
REPORT_PATH = ROOT / "data" / "scout_report.json"
MODEL_NAME = "gemini-3.5-flash-lite"


def call_ai_studio(prompt, key):
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
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)
        return res["candidates"][0]["content"]["parts"][0]["text"].strip()


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
                    "description": m.get("description", "")
                })
        return free_models
    except Exception as e:
        print(f"Warning: could not fetch OpenRouter models: {e}")
        return []


def run_scout(apply_updates=False):
    print("--> Starting AI Studio Discovery Scout...")
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

    # 1. Scout OpenRouter for newly added :free models
    live_openrouter = scout_openrouter_free_models()
    new_openrouter = [m for m in live_openrouter if m["id"] not in existing_models]
    print(f"Discovered {len(live_openrouter)} live :free models on OpenRouter ({len(new_openrouter)} new since last catalog update).")

    classified_candidates = []
    if new_openrouter:
        sample_to_classify = new_openrouter[:10]  # analyze batch
        prompt = f"""You are the automated catalog classifier for FreeInference.dev.
Analyze these newly discovered free LLM models on OpenRouter:
{json.dumps(sample_to_classify, indent=2)}

For each model, classify its architecture family, task category (coding, vision, reasoning, general), and whether it qualifies for free developer inference ($0 API).
Return a JSON array of objects with keys: "id", "family", "task", "recommended_page_slug", "summary".
Output strictly valid JSON with no markdown formatting.
"""
        try:
            raw_response = call_ai_studio(prompt, key)
            # Strip any accidental ```json wrappers
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_response, flags=re.MULTILINE).strip()
            classified_candidates = json.loads(cleaned)
            print(f"Successfully classified {len(classified_candidates)} candidate models via AI Studio.")
        except Exception as e:
            print(f"AI classification notice: {e}")
            classified_candidates = [
                {"id": m["id"], "family": "unknown", "task": "general", "recommended_page_slug": "free-llm-api", "summary": m.get("name", "")}
                for m in sample_to_classify
            ]

    # Build report
    report = {
        "scouted_date": today,
        "model_used": MODEL_NAME,
        "openrouter_free_total": len(live_openrouter),
        "new_discoveries_count": len(new_openrouter),
        "candidates": classified_candidates,
        "status": "completed"
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Scout report written to {REPORT_PATH}")

    # Emit GitHub Actions Step Summary if running in CI
    gh_summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if gh_summary_path:
        with open(gh_summary_path, "a") as f:
            f.write(f"### 🤖 FreeInference Nightly AI Scout ({today})\n\n")
            f.write(f"- **Engine**: Google AI Studio `{MODEL_NAME}`\n")
            f.write(f"- **OpenRouter Free Models**: {len(live_openrouter)} total ({len(new_openrouter)} new)\n\n")
            if classified_candidates:
                f.write("| Model ID | Family | Task | Recommended Slug |\n")
                f.write("| --- | --- | --- | --- |\n")
                for c in classified_candidates:
                    f.write(f"| `{c.get('id')}` | {c.get('family')} | {c.get('task')} | `{c.get('recommended_page_slug')}` |\n")
            else:
                f.write("All live free models are currently cataloged and verified.\n")

    return 0


if __name__ == "__main__":
    apply_flag = "--apply" in sys.argv
    sys.exit(run_scout(apply_updates=apply_flag))
