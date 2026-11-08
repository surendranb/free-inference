"""Enricher module: Syncs vector logos and capability metadata from Models.dev."""

import json
from pathlib import Path
import re
import urllib.request
from typing import Dict, Optional

from core.intake import UA

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
LOGOS_DIR = DATA_DIR / "logos"

# Explicit mapping of FreeInference catalog provider names to Models.dev slugs
PROVIDER_LOGO_MAP = {
    "OpenCode Zen": "opencode",
    "OpenRouter": "openrouter",
    "Google AI Studio (Gemini API)": "google",
    "Groq": "groq",
    "Cerebras": "cerebras",
    "Cloudflare Workers AI": "cloudflare",
    "Mistral La Plateforme": "mistral",
    "SambaNova Cloud": "sambanova",
    "NVIDIA NIM (build.nvidia.com)": "nvidia",
    "Z.AI (Zhipu)": "zai",
    "DeepInfra": "deepinfra",
    "GitHub Copilot (Free)": "github-copilot",
    "Kiro (AWS)": "amazon-bedrock",
    "Trae (ByteDance)": "bytedance",
    "Bolt.new": "stackblitz",
    "Lovable": "lovable",
    "v0 (Vercel)": "vercel",
    "Hugging Face Spaces": "huggingface",
    "Cursor (Hobby)": "cursor",
    "Windsurf": "codeium",
    "Devin (Free)": "cognition",
    "Qoder": "qoder",
    "Antigravity CLI (Google)": "google",
    "Google Colab": "google",
    "Figma (Starter)": "figma",
    "Canva (Free)": "canva",
    "Framer (Free)": "framer",
    "Replit (Starter)": "replit",
    "Kilo Gateway": "kilo",
    "Nous Portal": "nous",
    "Cohere": "cohere",
    "Requesty": "requesty",
    "OVHcloud AI Endpoints": "ovhcloud",
    "SiliconFlow": "siliconflow",
    "DeepSeek Platform": "deepseek",
    "Braintrust": "braintrust",
    "Deepgram": "deepgram",
    "AssemblyAI": "assemblyai",
    "Dots Studio": "dots-studio",
    "Liquid AI": "liquid",
    "Speka": "speka",
    "Kaggle Notebooks": "kaggle",
    "Alibaba DashScope (Bailian)": "alibaba",
    "ModelScope": "modelscope",
    "AMD Developer Cloud": "amd",
    "InferX": "inferx",
    "Kimi For Coding (Moonshot AI)": "kimi",
    "SCNet": "scnet",
    "AIHubMix": "aihubmix",
}


def slugify(name: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")


def fetch_models_dev_api() -> dict:
    """Fetch complete Models.dev catalog."""
    url = "https://models.dev/api.json"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def sync_provider_logos() -> int:
    """Download vector SVG logos from models.dev into data/logos/."""
    LOGOS_DIR.mkdir(parents=True, exist_ok=True)
    catalog = json.loads((DATA_DIR / "providers.json").read_text())
    synced = 0

    for p in catalog.get("providers", []):
        pname = p["name"]
        pslug = slugify(pname)
        mdev_id = PROVIDER_LOGO_MAP.get(pname)
        if not mdev_id:
            continue

        logo_path = LOGOS_DIR / f"{pslug}.svg"
        if logo_path.exists() and logo_path.stat().st_size > 50:
            synced += 1
            continue

        url = f"https://models.dev/logos/{mdev_id}.svg"
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.getcode() == 200:
                    svg_data = r.read().decode("utf-8", errors="ignore")
                    if "<svg" in svg_data:
                        logo_path.write_text(svg_data)
                        synced += 1
                        print(f"  ✓ Synced logo: {pname} -> data/logos/{pslug}.svg")
        except Exception as e:
            # Fallback or silent skip
            pass

    return synced


if __name__ == "__main__":
    print("--> Syncing provider vector logos from Models.dev...")
    count = sync_provider_logos()
    print(f"✓ Total logos available: {count}")
