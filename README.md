# Free Inference

Every provider that gives developers free API access to LLM inference — usable from a harness, agent, or CLI. Web-chat-only free tiers (ChatGPT, Claude.ai, Gemini app, deepseek.com, Grok, Copilot) are excluded on purpose.

**Last verified: 2026-08-12** · 13 providers · 70 free models tracked ·
Maintained in [data/providers.json](data/providers.json) — edit that one file, run `python3 build.py`,
and this README plus [index.html](index.html), [llms.txt](llms.txt) and [data/schema.json](data/schema.json)
regenerate in sync. Live website: [freeinference.dev](https://freeinference.dev).
Agent entrypoint: [llms.txt](llms.txt) · machine data: [data/providers.json](data/providers.json)
(validate against [data/schema.json](data/schema.json)).

## The table

| Provider | Free tier | Free models | RPM | TPM | RPD | Day tokens | Context | Timeout | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenCode Zen | Promo free (limited time) | Big Pickle, DeepSeek V4 Flash, MiMo-V2.5, Laguna S 2.1, Ling-3.0-tiny, LongCat-2.0, North Mini Code, Nemotron 3 Ultra | — | — | — | — | — | Not published | Free models are limited-time promos; some may use data for training. No credit card. OpenAI-compatible base URL opencode.ai/zen/v1. List free models: opencode models \| grep -i free |
| OpenRouter | Rate-limited free | cohere/north-mini-code:free, google/gemma-4-26b-a4b-it:free, google/gemma-4-31b-it:free, inclusionai/ling-3.0-tiny:free, liquid/lfm-2.5-2.6b:free, nvidia/nemotron-3-nano-30b-a3b:free, nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free, nvidia/nemotron-3-super-120b-a12b:free, nvidia/nemotron-3-ultra-550b-a55b:free, nvidia/nemotron-3.5-content-safety:free, nvidia/nemotron-3.5-lightning:free, nvidia/nemotron-nano-12b-v2-vl:free, nvidia/nemotron-nano-9b-v2:free, openai/gpt-oss-20b:free, poolside/laguna-s-2.1:free, poolside/laguna-xs-2.1:free | — | — | — | — | — | Not published | Gateway, not a model owner. Shared best-effort capacity, no SLA. BYOK program: 1M free routing requests/month with your own provider keys. |
| Google AI Studio (Gemini API) | Rate-limited free | gemini-2.5-flash, gemini-2.5-flash-lite, gemini-2.5-pro, gemini-3-flash-preview, gemini-3.1-flash-lite, gemini-3.1-flash-lite-preview, gemini-3.1-pro-preview, gemini-3.1-pro-preview-customtools, gemini-3.5-flash, gemini-3.5-flash-lite, gemini-3.6-flash, gemini-flash-latest, gemini-flash-lite-latest, gemini-omni-flash-preview, gemini-pro-latest, gemma-4-26b-a4b-it, gemma-4-31b-it | — | — | — | — | — | Not published | Free forever, no card, most generous major-provider tier. Live-verified against the v1beta API with an API key (2026-08-12) — model list and context windows are real; per-account quota varies by account age (see AI Studio rate-limit dashboard). Free-tier data may be used for training. |
| Groq | Rate-limited free | Llama 3.1 / 3.3, Llama 4 Scout, Qwen 3, Kimi K2, GPT-OSS 120B, Gemma 2 9B | — | — | — | — | — | Not published | LPU hardware, fastest time-to-first-token. Limits per API key per model; some models get half allowance. No credit card. Limits visible in x-ratelimit-* response headers. |
| Cerebras | Rate-limited free (Free Trial) | gpt-oss-120b, zai-glm-4.7, gemma-4-31b | — | — | — | — | — | Not published | Wafer-scale hardware, 2,000+ tok/s. Free tier caps context at 8K (temporary). Per-model limits on a rotating shortlist. No credit card. |
| Cloudflare Workers AI | Rate-limited free | ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings) | — | — | — | — | — | Not published | Neurons are normalized GPU-compute units, shared pool across all models. Resets 00:00 UTC. Hard stop when pool exhausted, errors not overage. No credit card. |
| Hugging Face | Rate-limited free | Llama 3.2 8B (Serverless), Qwen 2.5 7B (Serverless), Mistral 7B (Serverless), Inference Providers gateway (15+ partners) | — | — | — | — | — | Not published | Two products: Serverless API (free, rate-limited) and Inference Providers gateway. Cold starts 10-30s on unpopular models. Limits not published as fixed numbers. |
| Mistral La Plateforme | Rate-limited free (Experiment) | Mistral Large, Codestral, All API models (Experiment tier) | — | — | — | — | — | Not published | Phone (SMS) verification required, no card. Exact limits no longer published - see Admin Console Limits per workspace. Evaluation tier, not production. |
| SambaNova Cloud | Rate-limited free | DeepSeek-V3.1, MiniMax-M2.7, Gemma 4 31B preview | — | — | — | — | — | Not published | OpenAI-compatible base URL api.sambanova.ai/v1. Preview models can be pulled at any time. No credit card, no phone verification. |
| NVIDIA NIM (build.nvidia.com) | Trial credits | GLM-5, Kimi-2.5, NIM-packaged open models | — | — | — | — | — | Not published | Credit-based, not a rate-limited-free tier. Larger grants need corporate email, tie to ~90-day evaluation windows. |
| Z.AI (Zhipu) | Rate-limited free | GLM-5.1, GLM-4.5-Flash, GLM-4.7-Flash, GLM-4.6V-Flash (vision) | — | — | — | — | — | Not published | Free-tier limits revised twice in the past year - verify. Peak-hour throttling. Flash models are free regardless of tier. OpenAI-compatible. |
| Together AI | Trial credits | 200+ open models (Llama, Qwen, DeepSeek) | — | — | — | — | — | Not published | One-time credit, not forever-free. Card required once credits run out. Startup programs can grant far more. |
| DeepInfra | Trial credits | 40+ open models (Llama, Qwen, DeepSeek, Mistral) | — | — | — | — | — | Not published | 200 concurrent requests per model - high ceiling. Credit-based, no daily cap while credits last. OpenAI-compatible. |

## Models (per-provider detail)

| Provider | Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenCode Zen | Big Pickle | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-12 |
| OpenCode Zen | DeepSeek V4 Flash | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-12 |
| OpenCode Zen | MiMo-V2.5 | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-12 |
| OpenCode Zen | Laguna S 2.1 | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-12 |
| OpenCode Zen | Ling-3.0-tiny | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-12 |
| OpenCode Zen | LongCat-2.0 | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-12 |
| OpenCode Zen | North Mini Code | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-12 |
| OpenCode Zen | Nemotron 3 Ultra | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-12 |
| OpenRouter | cohere/north-mini-code:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | google/gemma-4-26b-a4b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | google/gemma-4-31b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | inclusionai/ling-3.0-tiny:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | liquid/lfm-2.5-2.6b:free | $0 | 125K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | nvidia/nemotron-3-nano-30b-a3b:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | nvidia/nemotron-3-super-120b-a12b:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | nvidia/nemotron-3-ultra-550b-a55b:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | nvidia/nemotron-3.5-content-safety:free | $0 | 125K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | nvidia/nemotron-3.5-lightning:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | nvidia/nemotron-nano-12b-v2-vl:free | $0 | 125K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | nvidia/nemotron-nano-9b-v2:free | $0 | 125K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | openai/gpt-oss-20b:free | $0 | 128K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | poolside/laguna-s-2.1:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| OpenRouter | poolside/laguna-xs-2.1:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-2.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-2.5-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-2.5-pro | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-3-flash-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-3.1-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-3.1-flash-lite-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-3.1-pro-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-3.1-pro-preview-customtools | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-3.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-3.5-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-3.6-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-flash-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-flash-lite-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-omni-flash-preview | $0 | 128K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemini-pro-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemma-4-26b-a4b-it | $0 | 256K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Google AI Studio (Gemini API) | gemma-4-31b-it | $0 | 256K | Varies by account | Varies by account | Varies by account | Not published | 2026-08-12 |
| Groq | Llama 3.1 / 3.3 | $0 | 128K | 30 (15 for some) | 6K | 14,400 (org-wide) | Not published | 2026-08-12 |
| Groq | Llama 4 Scout | $0 | 128K | 30 (15 for some) | 6K | 14,400 (org-wide) | Not published | 2026-08-12 |
| Groq | Qwen 3 | $0 | 128K | 30 (15 for some) | 6K | 14,400 (org-wide) | Not published | 2026-08-12 |
| Groq | Kimi K2 | $0 | 128K | 30 (15 for some) | 6K | 14,400 (org-wide) | Not published | 2026-08-12 |
| Groq | GPT-OSS 120B | $0 | 128K | 30 (15 for some) | 6K | 14,400 (org-wide) | Not published | 2026-08-12 |
| Groq | Gemma 2 9B | $0 | 128K | 30 (15 for some) | 15K | 14,400 (org-wide) | Not published | 2026-08-12 |
| Cerebras | gpt-oss-120b | $0 | 8K cap on free tier | 5 | 30K | Not published | 1M tokens/day (per model) | 2026-08-12 |
| Cerebras | zai-glm-4.7 | $0 | 8K cap on free tier | 5 | 30K | Not published | 1M tokens/day (per model) | 2026-08-12 |
| Cerebras | gemma-4-31b | $0 | 8K cap on free tier | 5 | 30K | Not published | 1M tokens/day (per model) | 2026-08-12 |
| Cloudflare Workers AI | ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings) | $0 | 8K-128K+ (model-dependent) | 300 text gen (720-1,500 other tasks) | Model-dependent | Not published | 10,000 neurons/day | 2026-08-12 |
| Hugging Face | Llama 3.2 8B (Serverless) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-08-12 |
| Hugging Face | Qwen 2.5 7B (Serverless) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-08-12 |
| Hugging Face | Mistral 7B (Serverless) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-08-12 |
| Hugging Face | Inference Providers gateway (15+ partners) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-08-12 |
| Mistral La Plateforme | Mistral Large | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-08-12 |
| Mistral La Plateforme | Codestral | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-08-12 |
| Mistral La Plateforme | All API models (Experiment tier) | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-08-12 |
| SambaNova Cloud | DeepSeek-V3.1 | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-08-12 |
| SambaNova Cloud | MiniMax-M2.7 | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-08-12 |
| SambaNova Cloud | Gemma 4 31B preview | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-08-12 |
| NVIDIA NIM (build.nvidia.com) | GLM-5 | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-08-12 |
| NVIDIA NIM (build.nvidia.com) | Kimi-2.5 | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-08-12 |
| NVIDIA NIM (build.nvidia.com) | NIM-packaged open models | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-08-12 |
| Z.AI (Zhipu) | GLM-5.1 | $0 | Up to 203K | 3 (burst) | Not published | 1,000 (1K RPD tier) | Not published | 2026-08-12 |
| Z.AI (Zhipu) | GLM-4.5-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-08-12 |
| Z.AI (Zhipu) | GLM-4.7-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-08-12 |
| Z.AI (Zhipu) | GLM-4.6V-Flash (vision) | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-08-12 |
| Together AI | 200+ open models (Llama, Qwen, DeepSeek) | $0 (trial credits) | Model-dependent | ~60 (Build tier) | ~100K (Build tier) | Not published | $25 one-time credit | 2026-08-12 |
| DeepInfra | 40+ open models (Llama, Qwen, DeepSeek, Mistral) | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-08-12 |

## Definitions

| Term | Meaning |
| --- | --- |
| RPM | Requests per minute — API calls in any 60-second window. |
| TPM | Tokens per minute — input + output tokens across all calls in a minute. |
| RPD | Requests per day — hard daily cap, resets on the provider's clock. |
| Day tokens | Daily or periodic token/compute quota (some providers meter a token pool per day, month, or one-time credits instead). |
| Timeout | Max request duration before the provider kills the connection. |
| Context | Maximum context window available on the free tier. |

## What counts as free here

- **API-accessible** — an endpoint you can call from a harness, agent, or CLI with a key (or no key). Web-chat-only free tiers (ChatGPT, Claude.ai, Gemini app, deepseek.com, Grok, Copilot) are excluded on purpose.
- **Strictly $0** — no credit card required for the free tier. Trial credits that expire are included but flagged as such.
- Four shapes: **rate-limited free** (forever free, throttled), **promo free** (free for a limited time), **free gateways** (OpenRouter, OpenCode Zen), **trial credits** (one-time, expires).

## Caveats

Limits change without notice and vary per model, account age, region, and peak hours. Every row links to official docs from the provider name. Treat this table as a map, not a contract — verify before you architect on it.

## Retired

| Provider | Note |
| --- | --- |
| GitHub Models | Fully retired 2026-07-30 (playground, catalog, API, BYOK). |

## Watchlist — candidate providers not yet verified

| Provider | Why it's on the list |
| --- | --- |
| Pollinations | No-key free text/image API, but limits are unpublished and unverified. |
| SiliconFlow | China-hosted free model endpoints with daily token caps, numbers not verified. |
| Moonshot / Kimi | Free-tier API access is rumoured, not confirmed. |
| Azure AI Foundry | Free monthly quota for select models, numbers not verified. |

## Contributing — providers, add yourself

One file to edit: `data/providers.json`. Add your row with a link to your official limits page, then:

```bash
python3 build.py   # regenerates README.md + index.html + llms.txt + data/schema.json in sync
```

Open a PR. Every change must name a *primary source* (official docs or dashboard) and the date it was verified — an unverifiable row gets rejected. Corrections are welcome the same way.

## Sources

Each provider name in the table links to its official docs. Aggregate numbers were cross-checked against provider docs and third-party trackers as of 2026-08-12.
