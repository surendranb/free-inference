# Free Inference

Every provider that gives developers free API access to LLM inference — usable from a harness, agent, or CLI. Web-chat-only free tiers (ChatGPT, Claude.ai, Gemini app, deepseek.com, Grok, Copilot) are excluded on purpose.

> **2026-09-03** · 13 providers · 81 free models
> Interactive site: https://freeinference.dev · Agent summary: https://freeinference.dev/llms.txt · Machine data: https://freeinference.dev/data/providers.json (validate against https://freeinference.dev/data/schema.json)

## Providers

| Provider | Free tier | Notable models | Notes |
| --- | --- | --- | --- |
| [OpenCode Zen](https://opencode.ai/docs/zen) | Promo free (limited time) | Big Pickle, MiMo-V2.5 Free, Ling 3.0 Flash Fin Free, Nemotron 3 Ultra Free, Nemotron 3.5 Lightning Free, Muse Spark 1.2 Contributor Free | Free models are limited-time promos; some may use data for training. No credit card. OpenAI-compatible base URL opencode.ai/zen/v1. List free models: opencode models | grep -i free |
| [OpenRouter](https://openrouter.ai/models?max_price=0) | Rate-limited free | cohere/north-mini-code:free, dots-studio/dots-3-note-preview:free, google/gemma-4-26b-a4b-it:free, google/gemma-4-31b-it:free, inclusionai/ling-3.0-flash-fin:free, liquid/lfm-2.5-2.6b:free, +12 more | Updated via GitHub Connect test (2026-08-12) |
| [Google AI Studio (Gemini API)](https://ai.google.dev/gemini-api/docs/rate-limits) | Rate-limited free | gemini-2.5-flash, gemini-2.5-flash-lite, gemini-2.5-pro, gemini-3-flash-preview, gemini-3.1-flash-lite, gemini-3.1-flash-lite-preview, +16 more | Free forever, no card, most generous major-provider tier. Live-verified against the v1beta API with an API key (2026-08-12) — model list and context windows are real; per-account quota varies by account age (see AI Studio rate-limit dashboard). Free-tier data may be used for training. |
| [Groq](https://console.groq.com/docs/rate-limits) | Rate-limited free | openai/gpt-oss-120b, openai/gpt-oss-20b, qwen/qwen3.6-27b, qwen/qwen3.8-27b, meta-llama/llama-prompt-guard-2-22m, groq/compound | LPU hardware, fastest time-to-first-token. Limits per API key per model; some models get half allowance. No credit card. Limits visible in x-ratelimit-* response headers. |
| [Cerebras](https://inference-docs.cerebras.ai/support/rate-limits) | Rate-limited free (Free Trial) | gpt-oss-120b, gemma-4-31b | Wafer-scale hardware, 2,000+ tok/s. Free tier caps context at 8K (temporary). Per-model limits on a rotating shortlist. No credit card. |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/limits) | Rate-limited free | ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings) | Neurons are normalized GPU-compute units, shared pool across all models. Resets 00:00 UTC. Hard stop when pool exhausted, errors not overage. No credit card. |
| [Hugging Face](https://huggingface.co/docs/inference-providers) | Rate-limited free | Llama 3.2 8B (Serverless), Qwen 2.5 7B (Serverless), Mistral 7B (Serverless), Inference Providers gateway (15+ partners) | Two products: Serverless API (free, rate-limited) and Inference Providers gateway. Cold starts 10-30s on unpopular models. Limits not published as fixed numbers. |
| [Mistral La Plateforme](https://docs.mistral.ai) | Rate-limited free (Experiment) | Mistral Large, Codestral, All API models (Experiment tier) | Phone (SMS) verification required, no card. Exact limits no longer published - see Admin Console Limits per workspace. Evaluation tier, not production. |
| [SambaNova Cloud](https://cloud.sambanova.ai/apis) | Rate-limited free | DeepSeek-V3.1, DeepSeek-V3.2, Meta-Llama-3.3-70B-Instruct, MiniMax-M2.7, MiniMax-M3, gemma-4-31B-it, +1 more | OpenAI-compatible base URL api.sambanova.ai/v1. Preview models can be pulled at any time. No credit card, no phone verification. |
| [NVIDIA NIM (build.nvidia.com)](https://build.nvidia.com) | Trial credits | GLM-5, Kimi-2.5, NIM-packaged open models | Credit-based, not a rate-limited-free tier. Larger grants need corporate email, tie to ~90-day evaluation windows. |
| [Z.AI (Zhipu)](https://z.ai) | Rate-limited free | GLM-5.1, GLM-4.5-Flash, GLM-4.7-Flash, GLM-4.6V-Flash (vision) | Free-tier limits revised twice in the past year - verify. Peak-hour throttling. Flash models are free regardless of tier. OpenAI-compatible. |
| [Together AI](https://www.together.ai/pricing) | Trial credits | 200+ open models (Llama, Qwen, DeepSeek) | One-time credit, not forever-free. Card required once credits run out. Startup programs can grant far more. |
| [DeepInfra](https://docs.deepinfra.com/account/rate-limits) | Trial credits | deepseek-ai/DeepSeek-V3.1, Qwen/Qwen3-32B, Qwen/Qwen2.5-72B-Instruct, zai-org/GLM-4.7 | 200 concurrent requests per model - high ceiling. Credit-based, no daily cap while credits last. Notable models below; 185+ total in catalog-wide trial credits. |

## Models (per provider)

### OpenCode Zen

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Big Pickle | zsh (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-30 |
| MiMo-V2.5 Free | zsh (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-30 |
| Ling 3.0 Flash Fin Free | zsh (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-30 |
| Nemotron 3 Ultra Free | zsh (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-30 |
| Nemotron 3.5 Lightning Free | zsh (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-30 |
| Muse Spark 1.2 Contributor Free | zsh (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-08-30 |

### OpenRouter

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cohere/north-mini-code:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| dots-studio/dots-3-note-preview:free | $0 | 500K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| google/gemma-4-26b-a4b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| google/gemma-4-31b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| inclusionai/ling-3.0-flash-fin:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| liquid/lfm-2.5-2.6b:free | $0 | 64K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| minimax/minimax-m2.7:free | $0 | 192K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| minimax/minimax-m3:free | $0 | 1024K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| nvidia/nemotron-3-super-120b-a12b:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| nvidia/nemotron-3-ultra-550b-a55b:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| nvidia/nemotron-3.5-content-safety:free | $0 | 125K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| nvidia/nemotron-3.5-lightning:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| poolside/laguna-s-2.1:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| poolside/laguna-xs-2.1:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| thinkingmachines/inkling-small:free | $0 | 1024K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| thinkingmachines/inkling:free | $0 | 1024K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |
| z-ai/glm-5.2:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-09-03 |

### Google AI Studio (Gemini API)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gemini-2.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-2.5-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-2.5-pro | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-3-flash-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-3.1-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-3.1-flash-lite-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-3.1-pro-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-3.1-pro-preview-customtools | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-3.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-3.5-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-3.5-transcribe | $0 | 96K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-3.6-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-3.7-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-3.8-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-flash-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-flash-latest-high-res-exp | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-flash-lite-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-omni-1.1-flash | $0 | 128K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-omni-flash-preview | $0 | 128K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemini-pro-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemma-4-26b-a4b-it | $0 | 256K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |
| gemma-4-31b-it | $0 | 256K | Varies by account | Varies by account | Varies by account | Not published | 2026-09-03 |

### Groq

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| openai/gpt-oss-120b | zsh | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-08-30 |
| openai/gpt-oss-20b | zsh | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-08-30 |
| qwen/qwen3.6-27b | zsh | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-08-30 |
| qwen/qwen3.8-27b | zsh | 128K | 30 | 8K | 1,000 | 2M tokens/day | 2026-08-30 |
| meta-llama/llama-prompt-guard-2-22m | zsh | 128K | 30 | 15K | 14,400 | 500K tokens/day | 2026-08-30 |
| groq/compound | zsh | 128K | 30 | 70K | 250 | Not published | 2026-08-30 |

### Cerebras

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gpt-oss-120b | zsh | 8K cap on free tier | 5 | 30K | Not published | 1M tokens/day (per model) | 2026-08-30 |
| gemma-4-31b | zsh | 8K cap on free tier | 5 | 30K | Not published | 1M tokens/day (per model) | 2026-08-30 |

### Cloudflare Workers AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings) | $0 | 8K-128K+ (model-dependent) | 300 text gen (720-1,500 other tasks) | Model-dependent | Not published | 10,000 neurons/day | 2026-08-30 |

### Hugging Face

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Llama 3.2 8B (Serverless) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-08-30 |
| Qwen 2.5 7B (Serverless) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-08-30 |
| Mistral 7B (Serverless) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-08-30 |
| Inference Providers gateway (15+ partners) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-08-30 |

### Mistral La Plateforme

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mistral Large | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-08-30 |
| Codestral | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-08-30 |
| All API models (Experiment tier) | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-08-30 |

### SambaNova Cloud

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DeepSeek-V3.1 | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-09-03 |
| DeepSeek-V3.2 | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-09-03 |
| Meta-Llama-3.3-70B-Instruct | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-09-03 |
| MiniMax-M2.7 | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-09-03 |
| MiniMax-M3 | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-09-03 |
| gemma-4-31B-it | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-09-03 |
| gpt-oss-120b | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-09-03 |

### NVIDIA NIM (build.nvidia.com)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-5 | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-08-30 |
| Kimi-2.5 | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-08-30 |
| NIM-packaged open models | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-08-30 |

### Z.AI (Zhipu)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-5.1 | $0 | Up to 203K | 3 (burst) | Not published | 1,000 (1K RPD tier) | Not published | 2026-08-30 |
| GLM-4.5-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-08-30 |
| GLM-4.7-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-08-30 |
| GLM-4.6V-Flash (vision) | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-08-30 |

### Together AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 200+ open models (Llama, Qwen, DeepSeek) | $0 (trial credits) | Model-dependent | ~60 (Build tier) | ~100K (Build tier) | Not published | $25 one-time credit | 2026-08-30 |

### DeepInfra

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-ai/DeepSeek-V3.1 | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-09-03 |
| Qwen/Qwen3-32B | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-09-03 |
| Qwen/Qwen2.5-72B-Instruct | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-09-03 |
| zai-org/GLM-4.7 | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-09-03 |
## Definitions

| Term | Meaning |
| --- | --- |
| RPM | Requests per minute — API calls in any 60-second window. |
| TPM | Tokens per minute — input + output tokens across all calls in a minute. |
| RPD | Requests per day — hard daily cap, resets on the provider's clock. |
| Day tokens | Daily or periodic token/compute quota (some providers meter a token pool per day, month, or one-time credits instead). |
| Timeout | Max request duration before the provider kills the connection. |
| Context | Maximum context window available on the free tier. |

## What counts as free

- **API-accessible** — an endpoint callable from a harness, agent, or CLI (key or keyless). Web-chat-only free tiers (ChatGPT, Claude.ai, Gemini app, deepseek.com, Grok, Copilot) are excluded on purpose.
- **Strictly $0** — no credit card for the free tier; expiring trial credits are flagged as such.
- Shapes: rate-limited free (forever, throttled), promo free (limited time), free gateways (OpenRouter, OpenCode Zen), trial credits (one-time).

## Caveats

Limits change without notice and vary per model, account age, region, peak hours. Treat this as a map, not a contract — verify before you architect on it.

## Maintain this catalog

Edit [`data/providers.json`](data/providers.json) (single source of truth), run `python3 build.py` to regenerate this README plus the site, open a PR with a primary-source link and verification date. Unverifiable rows are rejected. See [CONTRIBUTING.md](CONTRIBUTING.md).
