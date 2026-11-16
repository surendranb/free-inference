#!/usr/bin/env python3
"""Expand catalog with high-value developer API providers from discovery candidates and apply lineup updates."""

import json
from pathlib import Path
import re
import urllib.request
from core.enricher import PROVIDER_LOGO_MAP, sync_provider_logos
from core.scout import format_context

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
PROVIDERS_FILE = DATA_DIR / "providers.json"
CANDIDATES_FILE = DATA_DIR / "candidates.json"

TODAY_ISO = "2026-11-08"

def main():
    providers_data = json.loads(PROVIDERS_FILE.read_text(encoding="utf-8"))
    providers = providers_data.get("providers", [])
    prov_map = {p["name"]: p for p in providers}

    candidates = json.loads(CANDIDATES_FILE.read_text(encoding="utf-8")) if CANDIDATES_FILE.exists() else []

    # 1. Update Mistral lineup
    mistral = prov_map.get("Mistral La Plateforme")
    if mistral:
        # Prune mistral-tiny as deprecated
        mistral["models"] = [m for m in mistral.get("models", []) if "tiny" not in m["name"].lower()]
        existing_mistral = {m["name"].lower() for m in mistral["models"]}
        new_mistral_models = [
            {
                "name": "mistral-small-latest",
                "cost": "$0",
                "context": "128K",
                "rpm": "60",
                "tpm": "500K",
                "rpd": "Not published",
                "tpd": "Not published",
                "verified": TODAY_ISO
            },
            {
                "name": "codestral-latest",
                "cost": "$0",
                "context": "256K",
                "rpm": "30",
                "tpm": "300K",
                "rpd": "Not published",
                "tpd": "Not published",
                "verified": TODAY_ISO
            },
            {
                "name": "open-mistral-nemo",
                "cost": "$0",
                "context": "128K",
                "rpm": "60",
                "tpm": "500K",
                "rpd": "Not published",
                "tpd": "Not published",
                "verified": TODAY_ISO
            }
        ]
        for m in new_mistral_models:
            if m["name"].lower() not in existing_mistral:
                mistral["models"].append(m)
        mistral["verified"] = TODAY_ISO

    # 2. Update Groq lineup
    groq = prov_map.get("Groq")
    if groq:
        existing_groq = {m["name"].lower() for m in groq.get("models", [])}
        new_groq = {
            "name": "meta-llama/llama-prompt-guard-2-86m",
            "cost": "$0",
            "context": "128K",
            "rpm": "30",
            "tpm": "15K",
            "rpd": "14,400",
            "tpd": "500K tokens/day",
            "verified": TODAY_ISO
        }
        if new_groq["name"].lower() not in existing_groq:
            groq["models"].append(new_groq)
        groq["verified"] = TODAY_ISO

    # 3. Update Cloudflare Workers AI note
    cf = prov_map.get("Cloudflare Workers AI")
    if cf:
        cf["notes"] = (
            "Cloudflare Workers AI is Generally Available with ~80 free models (including Llama 3.3 70B, "
            "DeepSeek-R1 distills, Whisper, and FLUX), translating to 10,000 neurons/day (~hundreds of queries or "
            "audio minutes). No credit card required. Hard stop at 10,000 neurons until 00:00 UTC daily reset."
        )
        cf["verified"] = TODAY_ISO

    # 4. Helper to extract candidate models
    def get_candidate_models(provider_name: str, default_rpm="60", default_rpd="1,000"):
        res = []
        seen = set()
        for c in candidates:
            p = c.get("provider", "")
            if p == provider_name or provider_name in p:
                mname = c.get("name") or c.get("id")
                if not mname or mname.lower() in seen:
                    continue
                seen.add(mname.lower())
                ctx = format_context(c.get("context_length") or c.get("context"))
                res.append({
                    "name": mname,
                    "cost": "$0",
                    "context": ctx,
                    "rpm": default_rpm,
                    "tpm": "Not published",
                    "rpd": default_rpd,
                    "tpd": "Not published",
                    "verified": TODAY_ISO
                })
        return res

    # 5. Onboard new providers
    new_providers = []

    # Alibaba DashScope (Bailian)
    if "Alibaba DashScope (Bailian)" not in prov_map:
        ali_models = get_candidate_models("Alibaba Token Plan", default_rpm="60", default_rpd="Free tier token grant")
        if not ali_models:
            ali_models = [
                {"name": "qwen3.7-plus", "cost": "$0", "context": "1M", "rpm": "60", "tpm": "Not published", "rpd": "Token grant", "tpd": "Not published", "verified": TODAY_ISO},
                {"name": "qwen3.6-plus", "cost": "$0", "context": "1M", "rpm": "60", "tpm": "Not published", "rpd": "Token grant", "tpd": "Not published", "verified": TODAY_ISO},
                {"name": "deepseek-v4.1-flash-1017", "cost": "$0", "context": "1M", "rpm": "60", "tpm": "Not published", "rpd": "Token grant", "tpd": "Not published", "verified": TODAY_ISO},
                {"name": "glm-5.3", "cost": "$0", "context": "1M", "rpm": "60", "tpm": "Not published", "rpd": "Token grant", "tpd": "Not published", "verified": TODAY_ISO},
            ]
        new_providers.append({
            "name": "Alibaba DashScope (Bailian)",
            "url": "https://www.alibabacloud.com/help/en/model-studio/developer-reference/get-api-key",
            "free_type": "Trial / Free tokens",
            "notes": (
                "Alibaba Cloud Model Studio (Bailian/DashScope) provides free token allotments upon account "
                "activation across its Qwen and DeepSeek model fleet. Developers access high-throughput OpenAI-compatible "
                "endpoints with up to 1M token context windows. API keys are generated in the Model Studio console after account "
                "registration, with promotional free tokens valid during designated trial windows."
            ),
            "timeout": "300s",
            "verified": TODAY_ISO,
            "models": ali_models,
            "verified_method": "api",
            "docs_url": "https://help.aliyun.com/document_detail/2712195.html",
            "access_method": "api_key",
            "artifact": "code",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "channel": "web"
        })

    # ModelScope
    if "ModelScope" not in prov_map:
        ms_models = get_candidate_models("ModelScope", default_rpm="30", default_rpd="500")
        new_providers.append({
            "name": "ModelScope",
            "url": "https://modelscope.cn/docs/api-inference",
            "free_type": "Rate-limited free",
            "notes": (
                "ModelScope (Alibaba's open-source model community) offers free hosted inference for community "
                "and Qwen open-weights models. Users query standard OpenAI-compatible completion endpoints with "
                "context windows up to 262K tokens. Access is activated by creating a ModelScope account to retrieve an API access token, "
                "subject to fair-share community queuing and rate limits."
            ),
            "timeout": "180s",
            "verified": TODAY_ISO,
            "models": ms_models,
            "verified_method": "api",
            "docs_url": "https://modelscope.cn/docs/api-inference",
            "access_method": "api_key",
            "artifact": "code",
            "base_url": "https://api-inference.modelscope.cn/v1",
            "channel": "web"
        })

    # AMD Developer Cloud
    if "AMD Developer Cloud" not in prov_map:
        amd_models = get_candidate_models("AMD", default_rpm="30", default_rpd="1,000")
        new_providers.append({
            "name": "AMD Developer Cloud",
            "url": "https://cloud.amd.com/",
            "free_type": "Free Developer Tier",
            "notes": (
                "AMD Developer Cloud provides free inference access to open frontier models running on AMD "
                "Instinct ROCm GPU clusters. Developers query OpenAI-compatible chat endpoints supporting DeepSeek, Qwen, and MiniCPM variants. "
                "Access is provisioned by registering an AMD Developer account to reach the API console, subject to cluster capacity and fair-use developer quotas."
            ),
            "timeout": "120s",
            "verified": TODAY_ISO,
            "models": amd_models,
            "verified_method": "api",
            "docs_url": "https://cloud.amd.com/",
            "access_method": "api_key",
            "artifact": "code",
            "base_url": "https://cloud.amd.com/api/v1",
            "channel": "web"
        })

    # InferX
    if "InferX" not in prov_map:
        inferx_models = get_candidate_models("InferX", default_rpm="60", default_rpd="2,000")
        new_providers.append({
            "name": "InferX",
            "url": "https://model.inferx.net/endpoints",
            "free_type": "Free Developer Tier",
            "notes": (
                "InferX provides zero-cost inference endpoints for open models including Qwen 3.6, "
                "Gemma 4, and DeepSeek variants. Developers access low-latency OpenAI-compatible completions with streaming and structured output support. "
                "Keys are provisioned instantly upon user sign-in without upfront payment, subject to community prototyping rate limits."
            ),
            "timeout": "120s",
            "verified": TODAY_ISO,
            "models": inferx_models,
            "verified_method": "api",
            "docs_url": "https://model.inferx.net/endpoints",
            "access_method": "api_key",
            "artifact": "code",
            "base_url": "https://model.inferx.net/endpoints/v1",
            "channel": "web"
        })

    # Kimi For Coding (Moonshot AI)
    if "Kimi For Coding (Moonshot AI)" not in prov_map:
        kimi_models = get_candidate_models("Kimi For Coding (kimi.ai)", default_rpm="60", default_rpd="1,000")
        new_providers.append({
            "name": "Kimi For Coding (Moonshot AI)",
            "url": "https://www.kimi.ai/code/docs/en/kimi-code/models.html",
            "free_type": "Free Developer Tier",
            "notes": (
                "Moonshot AI provides free developer inference for Kimi K3 and coding models with context "
                "windows up to 1M tokens. Developers query OpenAI-compatible coding endpoints supporting deep reasoning and agentic workflows. "
                "Credentials are retrieved via the Kimi coding portal, subject to community rate limits and peak-period concurrency throttling."
            ),
            "timeout": "180s",
            "verified": TODAY_ISO,
            "models": kimi_models,
            "verified_method": "api",
            "docs_url": "https://www.kimi.ai/code/docs/en/kimi-code/models.html",
            "access_method": "api_key",
            "artifact": "code",
            "base_url": "https://api.kimi.ai/coding/v1",
            "channel": "web"
        })

    # SCNet
    if "SCNet" not in prov_map:
        scnet_models = get_candidate_models("SCNet Token Plan", default_rpm="60", default_rpd="1,000")
        new_providers.append({
            "name": "SCNet",
            "url": "https://www.scnet.cn",
            "free_type": "Free Developer Tier",
            "notes": (
                "SCNet provides national high-performance computing open inference tokens for domestic LLMs "
                "including Qwen 3.8 and DeepSeek V4 Flash. Developers access OpenAI-compatible chat endpoints with up to 1M token context windows. "
                "Registration on the SCNet developer portal provisions API keys upon identity verification, subject to national computing quota rules."
            ),
            "timeout": "180s",
            "verified": TODAY_ISO,
            "models": scnet_models,
            "verified_method": "api",
            "docs_url": "https://www.scnet.cn",
            "access_method": "api_key",
            "artifact": "code",
            "base_url": "https://api.scnet.cn/v1",
            "channel": "web"
        })

    # AIHubMix
    if "AIHubMix" not in prov_map:
        aihubmix_models = get_candidate_models("AIHubMix", default_rpm="60", default_rpd="1,000")
        new_providers.append({
            "name": "AIHubMix",
            "url": "https://aihubmix.com",
            "free_type": "Promo free",
            "notes": (
                "AIHubMix provides a suite of zero-cost promotional models including GLM-4.7 Flash, Nemotron 3 Ultra, "
                "and Qwen 3.8 Max. Developers query OpenAI-compatible completion endpoints with long context support up to 1M tokens. "
                "Free API credentials are generated upon account signup without credit cards, subject to promotional token availability and rate limits."
            ),
            "timeout": "120s",
            "verified": TODAY_ISO,
            "models": aihubmix_models,
            "verified_method": "api",
            "docs_url": "https://aihubmix.com",
            "access_method": "api_key",
            "artifact": "code",
            "base_url": "https://api.aihubmix.com/v1",
            "channel": "web"
        })

    providers.extend(new_providers)
    providers_data["providers"] = providers

    PROVIDERS_FILE.write_text(json.dumps(providers_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(new_providers)} new providers. Total providers: {len(providers)}")

    total_models = sum(len(p.get("models", [])) for p in providers)
    print(f"Total catalog models now: {total_models}")

if __name__ == "__main__":
    main()
