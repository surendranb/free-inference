# Free Inference

Free LLM inference you can build with: an API key, a CLI login, or inference bundled inside a coding tool or builder. The test is whether you can ship an artifact you keep — code, an app, a site, a design, an agent, a skill. Chat-only free tiers are excluded on purpose.

> **2026-10-30** · 38 providers · 132 free models
> Interactive site: https://freeinference.dev · Agent summary: https://freeinference.dev/llms.txt · Machine data: https://freeinference.dev/data/providers.json (validate against https://freeinference.dev/data/schema.json)

## Providers

| Provider | Access | Free tier | Notable models | Notes |
| --- | --- | --- | --- | --- |
| [OpenCode Zen](https://opencode.ai/v2/docs/console/models/) | api_key | Promo free (limited time) | Big Pickle, GLM-5.3-Flash Free, DeepSeek V4.1 Flash Free, MiMo-V2.6-Flash Free, Beam Free, Flint 40B Free, +4 more | Free models are limited-time promos; some may use data for training. No credit card. OpenAI-compatible base URL: https://opencode.ai/inference/openai/v1 (Jev 1.13 uses systemone endpoint). Free-tier chat models require the OpenCode client. Live CLI: opencode models | grep -i free |
| [OpenRouter](https://openrouter.ai/models?max_price=0) | api_key | Rate-limited free | cohere/north-mini-code:free, dots-studio/dots-3-note-preview:free, google/gemma-4-26b-a4b-it:free, google/gemma-4-31b-it:free, liquid/lfm-2.5-2.6b:free, nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free, +11 more | OpenAI-compatible gateway (https://openrouter.ai/api/v1). 50 RPD on $0 accounts, 1,000 RPD with $10+ credits. No credit card required. Permanent $0 models have :free suffix. |
| [Google AI Studio (Gemini API)](https://ai.google.dev/gemini-api/docs/rate-limits) | api_key | Rate-limited free | gemini-2.5-flash, gemini-2.5-flash-lite, gemini-3-flash-preview, gemini-3.1-flash-lite, gemini-3.1-flash-lite-preview, gemini-3.5-flash, +10 more | Free forever, no card, most generous major-provider tier. Live-verified against the v1beta API with an API key (2026-08-12) — model list and context windows are real; per-account quota varies by account age (see AI Studio rate-limit dashboard). Free-tier data may be used for training. |
| [Groq](https://console.groq.com/docs/rate-limits) | api_key | Rate-limited free | llama-3.3-70b-versatile, llama-3.1-8b-instant, meta-llama/llama-4-scout-17b-16e-instruct, openai/gpt-oss-120b, openai/gpt-oss-20b, qwen/qwen3.6-27b, +3 more | LPU hardware, fastest time-to-first-token. Limits pooled at organization level per model. No credit card required. Limits visible in x-ratelimit-* response headers. |
| [Cerebras](https://inference-docs.cerebras.ai/support/rate-limits) | api_key | Trial credits | gpt-oss-120b, qwen-3.8-27b | Wafer-scale hardware, 2,000+ tok/s. No permanent free tier — $5 trial credits, 30-day expiry, card required. Per-model limits on a rotating shortlist. |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/limits) | api_key | Rate-limited free | ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings), @cf/meta/llama-3.3-70b-instruct-fp8-fast, @cf/deepseek-ai/deepseek-r1-distill-qwen-32b, @cf/qwen/qwen2.5-72b-instruct, @cf/meta/llama-3.1-8b-instruct | Neurons are normalized GPU-compute units, shared pool across all models. Resets 00:00 UTC. Hard stop when pool exhausted, errors not overage. No credit card. |
| [Hugging Face](https://huggingface.co/docs/inference-providers) | api_key | Rate-limited free | Llama 3.2 8B (Serverless), Qwen 2.5 7B (Serverless), Mistral 7B (Serverless), Inference Providers gateway (15+ partners) | Two products: Serverless API (free, rate-limited) and Inference Providers gateway. Cold starts 10-30s on unpopular models. Limits not published as fixed numbers. |
| [Mistral La Plateforme](https://docs.mistral.ai) | api_key | Rate-limited free (Experiment) | Mistral Large, Codestral, All API models (Experiment tier) | Phone (SMS) verification required, no card. Exact limits no longer published - see Admin Console Limits per workspace. Evaluation tier, not production. |
| [SambaNova Cloud](https://cloud.sambanova.ai/apis) | api_key | Rate-limited free | DeepSeek-V3.1, DeepSeek-V3.2, Meta-Llama-3.3-70B-Instruct, gemma-4-31B-it, gpt-oss-120b | OpenAI-compatible base URL api.sambanova.ai/v1. Preview models can be pulled at any time. No credit card, no phone verification. |
| [NVIDIA NIM (build.nvidia.com)](https://build.nvidia.com) | api_key | Trial credits | GLM-5, Kimi-2.5, NIM-packaged open models | Credit-based, not a rate-limited-free tier. Larger grants need corporate email, tie to ~90-day evaluation windows. |
| [Z.AI (Zhipu)](https://z.ai) | api_key | Rate-limited free | GLM-5.1, GLM-4.5-Flash, GLM-4.7-Flash, GLM-4.6V-Flash (vision) | Free-tier limits revised twice in the past year - verify. Peak-hour throttling. Flash models are free regardless of tier. OpenAI-compatible. |
| [Together AI](https://www.together.ai/pricing) | api_key | Trial credits | 200+ open models (Llama, Qwen, DeepSeek) | No trial — paid entry, $5 minimum credit purchase, card required. Prepaid balance, no expiry. Startup programs can grant more. |
| [DeepInfra](https://docs.deepinfra.com/account/rate-limits) | api_key | Trial credits | deepseek-ai/DeepSeek-V3.1, Qwen/Qwen3-32B, Qwen/Qwen2.5-72B-Instruct, zai-org/GLM-4.7 | 200 concurrent requests per model - high ceiling. Credit-based, no daily cap while credits last. Notable models below; 185+ total in catalog-wide trial credits. |
| [GitHub Copilot (Free)](https://github.com/features/copilot) | login | Rate-limited free | Auto-selected (GPT-5 mini, Claude Haiku/Sonnet, Gemini Flash line) | Free plan: 2,000 completions/mo plus an unpublished allowance of GitHub AI Credits; models auto-selected. Login with GitHub OAuth, no card. |
| [Kiro (AWS)](https://kiro.dev/pricing) | login | Rate-limited free | Qwen3 Coder Next, DeepSeek 3.2, MiniMax M2.1, Claude Sonnet 4.5 | Free plan: 50 credits/mo, resets monthly, unused credits do not roll over. Login via social or AWS Builder ID; no card for the free tier. |
| [Trae (ByteDance)](https://www.trae.ai/pricing) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Free plan: 5,000 autocompletions/mo plus limited standard-queue usage and SOLO mode. Frontier models bundled in the vendor UI; no card. |
| [Bolt.new](https://support.bolt.new/account-and-subscription/tokens) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Free plan: 1M tokens/mo with a 300K/day cap, resets monthly. Frontier models bundled; no card. |
| [Lovable](https://docs.lovable.dev/introduction/credits-and-usage) | bundled | Rate-limited free | Frontier models (bundled, Fable 5.1) | Free plan: 5 build credits/day (max 30/mo) plus 20 cloud and 4 AI credits/mo. Frontier models bundled (Fable 5.1); no card. |
| [v0 (Vercel)](https://v0.app/docs/pricing) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Free plan: $5/mo credits plus 7 messages/day. Frontier models bundled; no card. |
| [Kaggle Notebooks](https://www.kaggle.com/docs/efficient-gpu-usage) | login | Rate-limited free | Open-weight models you load (GPU runtime) | Free ~30 GPU-h/week (resets weekly), P100 or 2xT4, 12h sessions. Open-weight models you load yourself; phone verification may apply. |
| [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces-overview) | login | Rate-limited free | Any Hugging Face model you load (ZeroGPU) | Static Spaces free for everyone; free personal accounts host up to 2 ZeroGPU Gradio Spaces. Any HF model you load; no card. Persistent or upgraded Spaces require a Pro subscription. |
| [Cursor (Hobby)](https://cursor.com/pricing) | bundled | Rate-limited free | Composer 2 (own), Auto (auto-selected, limited frontier) | Hobby plan: limited Agent requests and Tab completions; quota unpublished by the vendor. Own + limited frontier models bundled; no card. |
| [Devin (Free)](https://devin.ai/pricing) | bundled | Rate-limited free | SWE-1.7 / SWE-2 (own), Open models (auto-selected) | Free plan: light quota, unpublished. SWE-1.7/SWE-2 plus open models bundled; no card. |
| [Windsurf](https://docs.windsurf.com/windsurf/accounts/usage) | bundled | Rate-limited free | Frontier models (via Auto) | Free plan: light quota plus unlimited Tab/inline edits; numeric limits unpublished. Frontier models via Auto; no card. |
| [Qoder](https://docs.qoder.com/account/pricing) | bundled | Rate-limited free | Frontier models + BYO key | Free plan: limited completions/NES and basic models, plus BYOK; quota unpublished. No card. |
| [Antigravity CLI (Google)](https://antigravity.google/pricing) | login | Rate-limited free | Gemini 3.8/3.7/3.6 Flash, Gemini 3.1 Pro, Claude Sonnet/Opus 4.6, gpt-oss-120b | Individual plan: unlimited Tab and command requests with unpublished basic weekly rate limits. Google login; no card. |
| [Google Colab](https://research.google.com/colaboratory/faq.html) | login | Rate-limited free | Gemini (AI features) + GPU for your code | Free GPU/TPU with 12h max sessions; Colab does not publish these limits. Google login; no card. |
| [Figma (Starter)](https://www.figma.com/pricing/) | bundled | Rate-limited free | Figma AI, Make, agent | Starter plan: 150 AI credits/day, up to 500/mo. Figma AI, Make, and agent bundled; no card. |
| [Canva (Free)](https://www.canva.com/en/pricing/) | bundled | Rate-limited free | Canva AI, Magic Media | Free plan: up to 20 Standard AI uses or 20 Premium per month (resets monthly); Magic Media text-to-image is 50 lifetime. No card. |
| [Framer (Free)](https://www.framer.com/pricing) | bundled | Trial credits | Framer Agents | Free plan: 500 AI credits to try (one-off), free Framer domain, non-commercial. No card. |
| [Replit (Starter)](https://docs.replit.com/help/pricing-and-plans) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Starter: daily Agent allowance plus limited monthly cloud credits and 1 published app; numbers unpublished. Frontier models bundled; no card. |
| [Kilo Gateway](https://kilo.ai/gateway) | api_key | Rate-limited free | cohere/north-mini-code:free, poolside/laguna-s-2.1:free, poolside/laguna-xs-2.1:free, liquid/lfm-2.5-2.6b:free, dots-studio/dots-3-note-preview:free, nvidia/nemotron-3.5-lightning:free, +1 more | Universal gateway, $0 forever for default free models. Anonymous keyless at 200 req/hour per IP; :free-tagged models. OpenAI-compatible. No credit card. |
| [Nous Portal](https://portal.nousresearch.com/api-docs) | api_key | Rate-limited free | poolside/laguna-s-2.1:free, poolside/laguna-xs-2.1:free, stepfun/step-3.7-flash:free, upstage/solar-mini4:free, reflection/beam-1.0-501b-a23b:free, ornith/ornith-1.5-122b:free | Nous Research Hermes models, $0 monthly plan. Free 50 RPM / 500k TPM. OpenAI-compatible. No card on free plan. |
| [Cohere](https://docs.cohere.com/docs/rate-limits) | api_key | Rate-limited free | Command A, Command R+, Command R7B | Evaluation key, 1,000 calls/month. Chat 20 req/min per model. Embed 2k inputs/min. No card for trial key. Non-production limits. |
| [Requesty](https://www.requesty.ai/pricing) | api_key | Rate-limited free | nvidia/nemotron-3-super-120b-a12b, google/gemma-4-31b-it, poolside/laguna-xs.2 | Gateway, $0 free models at 200 req/day. Routing, caching, EU residency. No credit card required. |
| [OVHcloud AI Endpoints](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/) | api_key | Rate-limited free | 10 free models (anonymous keyless) | EU-sovereign. Anonymous keyless 2 req/min per IP per model. Authed 400 req/min. No usage cap apart from rate. No card for anonymous. |
| [SiliconFlow](https://siliconflow.cn) | api_key | Rate-limited free | deepseek-ai/DeepSeek-R1-Distill-Qwen-7B, deepseek-ai/DeepSeek-V3, Qwen/Qwen2.5-7B-Instruct, THUDM/glm-4-9b-chat | Large-scale inference gateway offering permanently free open-source model tiers plus 14M free signup tokens. OpenAI-compatible API. No credit card required. |
| [DeepSeek Platform](https://api-docs.deepseek.com) | api_key | Trial credits | deepseek-chat, deepseek-reasoner | 5M free tokens granted on new account creation (valid 30 days). OpenAI-compatible API format with cache-miss/cache-hit pricing. |

## Models (per provider)

### OpenCode Zen

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Big Pickle | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-10-30 |
| GLM-5.3-Flash Free | $0 (promo) | 128K - 1M | Not published | Not published | Not published | Not published | 2026-10-30 |
| DeepSeek V4.1 Flash Free | $0 (promo) | 128K - 1M | Not published | Not published | Not published | Not published | 2026-10-30 |
| MiMo-V2.6-Flash Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-10-30 |
| Beam Free | $0 (promo) | 128K - 1M | Not published | Not published | Not published | Not published | 2026-10-30 |
| Flint 40B Free | $0 (promo) | 128K - 1M | Not published | Not published | Not published | Not published | 2026-10-30 |
| Nemotron 3 Ultra Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-10-30 |
| Nemotron 3.5 Lightning Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-10-30 |
| Nemotron 3.5 Super VL Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-10-30 |
| Jev 1.13 Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-10-30 |

### OpenRouter

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cohere/north-mini-code:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| dots-studio/dots-3-note-preview:free | $0 | 500K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| google/gemma-4-26b-a4b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| google/gemma-4-31b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| liquid/lfm-2.5-2.6b:free | $0 | 64K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| nvidia/nemotron-3-ultra-550b-a55b:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| nvidia/nemotron-3.5-content-safety:free | $0 | 125K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| nvidia/nemotron-3.5-lightning:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| nvidia/nemotron-3.5-super-vl:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| poolside/laguna-s-2.1:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| poolside/laguna-xs-2.1:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| recursive/flint-v1.0:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| thinkingmachines/inkling-small:free | $0 | 1024K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| thinkingmachines/inkling:free | $0 | 1024K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| xingchen-agi/xing4.0-29b-a4b:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |
| meta/muse-spark-1.3-contributor:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-10-30 |

### Google AI Studio (Gemini API)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gemini-2.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-2.5-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-3-flash-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-3.1-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-3.1-flash-lite-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-3.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-3.5-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-3.6-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-3.7-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-3.8-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-flash-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-flash-lite-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-omni-1.1-flash | $0 | 128K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemini-omni-flash-preview | $0 | 128K | Varies by account | Varies by account | Varies by account | Not published | 2026-10-30 |
| gemma-4-26b-a4b-it | $0 | 256K | 15 | 1M | 1,500 | Not published | 2026-10-30 |
| gemma-4-31b-it | $0 | 256K | 15 | 1M | 1,500 | Not published | 2026-10-30 |

### Groq

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| llama-3.3-70b-versatile | $0 | 128K | 30 | 12K | 1,000 | 100K tokens/day | 2026-10-30 |
| llama-3.1-8b-instant | $0 | 128K | 30 | 6K | 14,400 | 500K tokens/day | 2026-10-30 |
| meta-llama/llama-4-scout-17b-16e-instruct | $0 | 128K | 30 | 30K | 1,000 | 500K tokens/day | 2026-10-30 |
| openai/gpt-oss-120b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-10-30 |
| openai/gpt-oss-20b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-10-30 |
| qwen/qwen3.6-27b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-10-30 |
| qwen/qwen3.8-27b | $0 | 128K | 30 | 8K | 1,000 | 2M tokens/day | 2026-10-30 |
| meta-llama/llama-prompt-guard-2-22m | $0 | 128K | 30 | 15K | 14,400 | 500K tokens/day | 2026-10-30 |
| compound-beta | $0 | 128K | 30 | 70K | 250 | Not published | 2026-10-30 |

### Cerebras

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gpt-oss-120b | $5 trial credits (30-day, card required) | 8K cap on free tier | 5 | 30K | Not published | 1M tokens/day (per model) | 2026-10-01 |
| qwen-3.8-27b | $5 trial credits (30-day, card required) | 8K cap on free tier | 5 | 30K | Not published | 1M tokens/day (per model) | 2026-10-01 |

### Cloudflare Workers AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings) | $0 | 8K-128K+ (model-dependent) | 300 text gen (720-1,500 other tasks) | Model-dependent | Not published | 10,000 neurons/day | 2026-08-30 |
| @cf/meta/llama-3.3-70b-instruct-fp8-fast | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-10-29 |
| @cf/deepseek-ai/deepseek-r1-distill-qwen-32b | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-10-29 |
| @cf/qwen/qwen2.5-72b-instruct | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-10-29 |
| @cf/meta/llama-3.1-8b-instruct | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-10-29 |

### Hugging Face

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Llama 3.2 8B (Serverless) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-10-29 |
| Qwen 2.5 7B (Serverless) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-10-29 |
| Mistral 7B (Serverless) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-10-29 |
| Inference Providers gateway (15+ partners) | $0 | Model-dependent | ~300 req/hour (Serverless) | Model max context | Not published | Small monthly credit pool (PRO: 2M credits/mo) | 2026-10-29 |

### Mistral La Plateforme

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mistral Large | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-10-29 |
| Codestral | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-10-29 |
| All API models (Experiment tier) | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-10-29 |

### SambaNova Cloud

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DeepSeek-V3.1 | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-10-30 |
| DeepSeek-V3.2 | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-10-30 |
| Meta-Llama-3.3-70B-Instruct | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-10-30 |
| gemma-4-31B-it | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-10-30 |
| gpt-oss-120b | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-10-30 |

### NVIDIA NIM (build.nvidia.com)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-5 | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-10-29 |
| Kimi-2.5 | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-10-29 |
| NIM-packaged open models | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-10-29 |

### Z.AI (Zhipu)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-5.1 | $0 | Up to 203K | 3 (burst) | Not published | 1,000 (1K RPD tier) | Not published | 2026-10-29 |
| GLM-4.5-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-10-29 |
| GLM-4.7-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-10-29 |
| GLM-4.6V-Flash (vision) | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-10-29 |

### Together AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 200+ open models (Llama, Qwen, DeepSeek) | $5 minimum (no trial) | Model-dependent | ~60 (Build tier) | ~100K (Build tier) | Not published | $5 minimum purchase, prepaid, no expiry | 2026-10-01 |

### DeepInfra

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-ai/DeepSeek-V3.1 | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-10-30 |
| Qwen/Qwen3-32B | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-10-30 |
| Qwen/Qwen2.5-72B-Instruct | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-10-30 |
| zai-org/GLM-4.7 | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-10-30 |

### GitHub Copilot (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Auto-selected (GPT-5 mini, Claude Haiku/Sonnet, Gemini Flash line) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Kiro (AWS)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3 Coder Next | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |
| DeepSeek 3.2 | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |
| MiniMax M2.1 | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |
| Claude Sonnet 4.5 | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Trae (ByteDance)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Bolt.new

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Lovable

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, Fable 5.1) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### v0 (Vercel)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Kaggle Notebooks

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Open-weight models you load (GPU runtime) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Hugging Face Spaces

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Any Hugging Face model you load (ZeroGPU) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Cursor (Hobby)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Composer 2 (own) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |
| Auto (auto-selected, limited frontier) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Devin (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWE-1.7 / SWE-2 (own) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |
| Open models (auto-selected) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Windsurf

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (via Auto) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Qoder

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models + BYO key | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Antigravity CLI (Google)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini 3.8/3.7/3.6 Flash, Gemini 3.1 Pro, Claude Sonnet/Opus 4.6, gpt-oss-120b | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Google Colab

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini (AI features) + GPU for your code | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Figma (Starter)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Figma AI, Make, agent | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Canva (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Canva AI, Magic Media | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-30 |

### Framer (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Framer Agents | $0 (trial credits) | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Replit (Starter)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-10-29 |

### Kilo Gateway

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cohere/north-mini-code:free | $0 | 250K | 20 | Provider-dependent | 200/day | Not published | 2026-10-30 |
| poolside/laguna-s-2.1:free | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-10-30 |
| poolside/laguna-xs-2.1:free | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-10-30 |
| liquid/lfm-2.5-2.6b:free | $0 | 64K | 20 | Provider-dependent | 200/day | Not published | 2026-10-30 |
| dots-studio/dots-3-note-preview:free | $0 | 500K | 20 | Provider-dependent | 200/day | Not published | 2026-10-30 |
| nvidia/nemotron-3.5-lightning:free | $0 | 1000000 | 20 | Provider-dependent | 200/day | Not published | 2026-10-30 |
| nvidia/nemotron-3.5-super-vl:free | $0 | 1000000 | 20 | Provider-dependent | 200/day | Not published | 2026-10-30 |

### Nous Portal

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| poolside/laguna-s-2.1:free | $0 | 256K | 50 | 500K | Not published | Not published | 2026-10-30 |
| poolside/laguna-xs-2.1:free | $0 | 256K | 50 | 500K | Not published | Not published | 2026-10-30 |
| stepfun/step-3.7-flash:free | $0 | 128K | 50 | 500K | Not published | Not published | 2026-10-30 |
| upstage/solar-mini4:free | $0 | 64K | 50 | 500K | Not published | Not published | 2026-10-30 |
| reflection/beam-1.0-501b-a23b:free | $0 | 128K | 50 | 500K | Not published | Not published | 2026-10-30 |
| ornith/ornith-1.5-122b:free | $0 | 128K | 50 | 500K | Not published | Not published | 2026-10-30 |

### Cohere

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Command A | $0 | 256K | 20 | Not published | Not published | Not published | 2026-10-01 |
| Command R+ | $0 | 128K | 20 | Not published | Not published | Not published | 2026-10-01 |
| Command R7B | $0 | 128K | 20 | Not published | Not published | Not published | 2026-10-01 |

### Requesty

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nvidia/nemotron-3-super-120b-a12b | $0 | 128K | Not published | Not published | 200/day shared | Not published | 2026-10-30 |
| google/gemma-4-31b-it | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-10-30 |
| poolside/laguna-xs.2 | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-10-30 |

### OVHcloud AI Endpoints

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 free models (anonymous keyless) | $0 | Model-dependent | 2/min per IP | Not published | Not published | Not published | 2026-10-30 |

### SiliconFlow

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-ai/DeepSeek-R1-Distill-Qwen-7B | $0 | 32K | 1000 | 40K | 100 | Not published | 2026-10-29 |
| deepseek-ai/DeepSeek-V3 | $0 | 64K | 30 RPH | 40K | 100 | Not published | 2026-10-29 |
| Qwen/Qwen2.5-7B-Instruct | $0 | 32K | 1000 | 40K | Not published | Not published | 2026-10-29 |
| THUDM/glm-4-9b-chat | $0 | 32K | 1000 | 40K | Not published | Not published | 2026-10-29 |

### DeepSeek Platform

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-chat | $0 (5M signup tokens) | 64K | 60 | Not published | Not published | 5M tokens grant | 2026-10-29 |
| deepseek-reasoner | $0 (5M signup tokens) | 64K | 60 | Not published | Not published | 5M tokens grant | 2026-10-29 |
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
