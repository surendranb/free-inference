# Free Inference

Free AI & LLM inference you can build with: an API key, a CLI login, or inference bundled inside a coding tool or builder. Speech-to-text, voice synthesis, code, vision, and reasoning. The test is whether you can ship an artifact you keep — code, an app, an audio file, a site, a design, an agent, a skill. Chat-only free tiers are excluded on purpose.

> **2026-11-28** · 50 providers · 406 models
> Interactive site: https://freeinference.dev · Agent summary: https://freeinference.dev/llms.txt · Machine data: https://freeinference.dev/data/providers.json (validate against https://freeinference.dev/data/schema.json)

### Quick Navigation & Machine Access

- 🤖 **Agent Skill (`SKILL.md`)**: [https://freeinference.dev/skill.md](https://freeinference.dev/skill.md) (install: `curl -fsSL https://freeinference.dev/skill.md -o ~/.agents/skills/free-inference/SKILL.md`)
- 📋 **OpenAI Catalog Endpoint**: `GET https://freeinference.dev/v1/models`
- 📡 **Changelog RSS/Atom Feed**: [https://freeinference.dev/feed.xml](https://freeinference.dev/feed.xml)
- 📬 **Weekly Dispatch (Newsletter)**: [https://freeinference.dev/newsletter/](https://freeinference.dev/newsletter/)
- 💳 **No Credit Card or Subscription**: [https://freeinference.dev/free-llm-api-no-credit-card/](https://freeinference.dev/free-llm-api-no-credit-card/)
- ⚡ **OpenAI-Compatible Drop-in Endpoints**: [https://freeinference.dev/free-openai-compatible-api/](https://freeinference.dev/free-openai-compatible-api/)
- 🛠 **Free Coding & Cursor / Cline Keys**: [https://freeinference.dev/free-coding-api/](https://freeinference.dev/free-coding-api/) · [https://freeinference.dev/free-cursor-api/](https://freeinference.dev/free-cursor-api/)
- 🧠 **Top Model Guides**: [DeepSeek V3.2](https://freeinference.dev/free-deepseek-api/) · [Llama 3.3 70B](https://freeinference.dev/free-llama-api/) · [Qwen 3.8](https://freeinference.dev/free-qwen-api/) · [Gemini 3.5 Flash-Lite](https://freeinference.dev/free-gemini-api/) · [GLM-5 / 4.7](https://freeinference.dev/free-glm-api/)

## Providers

| Provider | Access | Free tier | Notable models | Notes |
| --- | --- | --- | --- | --- |
| [Synap by Linkrra](https://synap402.com/ai/account.html) | api_key | Rate-limited free | qwen3-coder-30b | Synap provides a no-card free tier for qwen3-coder-30b through an OpenAI-compatible API. Google or email sign-in grants 100,000 tokens and 50 requests per day, with a 10 requests/minute per-key limit. |
| [OpenCode Zen](https://opencode.ai/v2/docs/console/models/) | api_key | Promo free (limited time) | Big Pickle, Iceman Free, Inkling 2 Small Free, Crouton Alpha Free, GLM-5.3-Flash Free, DeepSeek V4.1 Flash Free, +12 more | OpenCode Zen provides a zero-cost promotional tier covering experimental open models across text and vision modalities. Developers authenticate via API key to query high-throughput endpoints directly without upfront billing. Access is bounded by limited-time promotional windows, a zero-data-retention policy, and fair-use concurrency caps. |
| [OpenRouter](https://openrouter.ai/models?max_price=0) | api_key | Rate-limited free | baidu/ernie-5.5-flash-preview:free, liquid/lfm-3-1.7b:free, particle-ai/particle-1:free, recursive/flint-v1.0:free, nvidia/nemotron-3.5-super-vl:free, nvidia/nemotron-3.5-lightning:free, +6 more | OpenRouter offers permanently free models with flexible context windows, translating to 50 requests/day (1,000 requests/day with + purchased credits). No credit card required. |
| [Google AI Studio (Gemini API)](https://ai.google.dev/gemini-api/docs/rate-limits) | api_key | Rate-limited free | gemini-3.5-flash-lite, gemini-3.1-flash-lite, gemma-4-26b-a4b-it, gemma-4-31b-it, gemini-4-hydrogen, gemini-3.5-flash, +11 more | Google AI Studio offers free model access with up to 1M context. Paid models like Gemini 4 Argon, Carbon, and Neon are excluded from the free tier. No credit card required. |
| [Groq](https://console.groq.com/docs/rate-limits) | api_key | Rate-limited free | llama-3.3-70b-versatile, llama-3.1-8b-instant, openai/gpt-oss-120b, openai/gpt-oss-20b, openai/gpt-oss-safeguard-20b, qwen/qwen3.8-27b, +7 more | Groq offers 13 free models (9 LLMs, 2 Whisper STT, 2 Orpheus TTS), translating to up to 14,400 text requests/day and 2,000 audio transcriptions/day (~8 hours/day). No credit card required. Limits are pooled at organization level. |
| [Cerebras](https://inference-docs.cerebras.ai/support/rate-limits) | api_key | Trial credits | gpt-oss-120b, qwen-3.8-27b | Cerebras offers $5 trial credit across 2 models (gpt-oss-120b, qwen-3.8-27b). Credit card required. Trial credits expire in 30 days. |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/limits) | api_key | Rate-limited free | ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings), @cf/meta/llama-3.3-70b-instruct-fp8-fast, @cf/deepseek-ai/deepseek-r1-distill-qwen-32b, @cf/qwen/qwen2.5-72b-instruct, @cf/meta/llama-3.1-8b-instruct, @cf/openai/whisper | Cloudflare Workers AI is Generally Available with ~80 free models. No credit card required. |
| [Mistral La Plateforme](https://docs.mistral.ai) | api_key | Rate-limited free | mistral-small-latest, codestral-latest, open-mistral-nemo | Mistral provides a rate-limited free tier on La Plateforme for developers evaluating frontier and open models. Access is available via direct API key upon account registration with no credit card required upfront. Usage is bounded by default platform rate limits and standard evaluation terms of service. |
| [SambaNova Cloud](https://cloud.sambanova.ai/apis) | api_key | Trial credits | gemma-4-31B-it, gpt-oss-120b | SambaNova Cloud provides a free developer tier when no payment method is linked, offering access to preview models like gemma-4-31B-it and gpt-oss-120b. |
| [NVIDIA NIM (build.nvidia.com)](https://build.nvidia.com) | api_key | Trial credits | bigcode/starcoder2-15b, fastino/gliner2-pii, google/gemma-3-12b-it, google/gemma-3-4b-it, minimaxai/minimax-m3.1-flash, mistralai/mistral-large-4-1t-a52b, +40 more | NVIDIA NIM offers 1,000 free trial credits across catalog models with no credit card required. |
| [Z.AI (Zhipu)](https://z.ai) | api_key | Rate-limited free | GLM-4.7-Flash, GLM-4.5-Flash, GLM-4.6V-Flash | Z.AI offers free API access to GLM-4.7-Flash, GLM-4.5-Flash, and GLM-4.6V-Flash. No credit card required. |
| [DeepInfra](https://docs.deepinfra.com/account/rate-limits) | api_key | Trial credits | deepseek-ai/DeepSeek-V3.1, Qwen/Qwen3-32B, Qwen/Qwen2.5-72B-Instruct, zai-org/GLM-4.7 | DeepInfra offers $5 signup trial credit across available models with no credit card required. |
| [GitHub Copilot (Free)](https://github.com/features/copilot) | login | Rate-limited free | Auto-selected (GPT-5 mini, Claude Haiku/Sonnet, Gemini Flash line) | GitHub provides Copilot Free with limited features for individual developers, including inline suggestions limited to 2000 completions per month and Copilot Chat on GitHub.com and mobile. |
| [Kiro (AWS)](https://kiro.dev/pricing) | login | Rate-limited free | Claude Sonnet 4.5, Claude Sonnet 4.0, Auto, DeepSeek 3.2, MiniMax M2.5, GLM-5, +2 more | Free tier users are limited to specific models (Auto, Claude Sonnet 4.5/4.0, DeepSeek 3.2, MiniMax M2.5/M2.1, GLM-5, Qwen3 Coder Next). |
| [Trae (ByteDance)](https://www.trae.ai/pricing) | bundled | Trial credits | Frontier models (bundled, auto-selected) | Trae offers a $0 free plan with limited auto-mode usage, 5,000 monthly autocompletions, and 2 concurrent cloud tasks. Free users receive a one-time allowance that does not reset monthly, and no credit card is required. |
| [Bolt.new](https://support.bolt.new/account-and-subscription/tokens) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Bolt offers 1,000,000 tokens per month with a 300,000 daily token cap, translating to bundled frontier model inference for full-stack web and code generation via the Standard agent alongside hosting for up to 333k requests. No credit card required to sign up. Daily tokens reset every 24 hours without rollover, monthly quotas reset on the 1st of each calendar month, and free plan tokens do not roll over. |
| [Lovable](https://docs.lovable.dev/introduction/credits-and-usage) | bundled | Rate-limited free | Fable 5.1 (Frontier model) | Lovable provides a rate-limited free plan for developers building full-stack web applications with daily build credits, daily chat allowances, and monthly Cloud/AI grants without upfront subscription cost. |
| [v0 (Vercel)](https://v0.app/docs/pricing) | bundled | Rate-limited free | Frontier models (bundled, auto-selected), Beam 1.0, Glyph Cluster, Nemotron 3.5 Lightning Free, Ampersand v0.1, Flint | v0 offers a free plan granting 7 messages per day with bundled frontier models, plus a one-time $5 credit bonus for new accounts. No credit card required to sign up. |
| [Kaggle Notebooks](https://www.kaggle.com/docs/efficient-gpu-usage) | login | Rate-limited free | Open-weight models you load (GPU runtime) | Phone verification is required to unlock accelerators and internet access; no credit card required. |
| [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces-overview) | login | Rate-limited free | Any Hugging Face model you load (ZeroGPU), GLM-4.7-Flash | Hugging Face Spaces provides free hosting for up to 2 Gradio Spaces with ZeroGPU compute access for personal accounts in good standing. |
| [Cursor (Hobby)](https://cursor.com/pricing) | bundled | Rate-limited free | Cursor Free Models (Agent/Chat) | Cursor provides a complimentary Free tier for developers, subject to monthly request allowances and rate limits. Third-party models are unavailable on Free and Plus tiers. |
| [Windsurf](https://docs.windsurf.com/windsurf/accounts/usage) | bundled | Rate-limited free | SWE-2 Flash Medium, SWE-2, SWE-2.1 | Windsurf provides a free tier operating on a quota-based system with daily and weekly usage allowances, complemented by specific promotional free periods for models such as SWE-2 Flash, SWE-2, and SWE-2.1. |
| [Devin (Free)](https://devin.ai/pricing) | bundled | Rate-limited free | SWE-2 (Free), Limited models (auto-selected) | Devin offers a Free plan with a light quota to code with agents, free use of SWE-2, unlimited inline edits, and unlimited Tab completions. Account login required, no credit card required. |
| [Qoder](https://docs.qoder.com/account/pricing) | bundled | Rate-limited free | Basic models + BYO key | Account login required, no credit card required. Unlimited usage requires bringing your own API keys. 14-day Pro trial available for new users. |
| [Antigravity CLI (Google)](https://antigravity.google/pricing) | login | Rate-limited free | Gemini 4 Hydrogen, Gemini 3.8 Flash | Free access remains available via Google account authentication without a payment instrument, though model availability has been restricted to specific Gemini versions. |
| [Google Colab](https://research.google.com/colaboratory/faq.html) | login | Rate-limited free | Gemini (AI features) + GPU for your code, Lyria 3 Clip Preview, Lyria 3 Pro Preview, Gemma 4 31B IT, Gemma 4 26B A4B IT | Google Colab offers free access to hosted Jupyter notebook compute resources including shared GPUs/TPUs and integrated Gemini AI coding features, translating to interactive execution sessions of up to 12 hours with standard system memory. Google account login required (age 18+ for AI features), no credit card required. Resources and rate limits fluctuate dynamically, idle runtimes disconnect, and non-interactive background execution is disallowed. |
| [Figma (Starter)](https://www.figma.com/pricing/) | bundled | Rate-limited free | Figma Make, The Figma agent, GPT Image 2.5 Sunburst, Nano Banana 2 Lite, Nano Banana 2, Nano Banana 2.1, +2 more | Figma Starter offers free AI generation credits capped at 150/day and 500/month with no credit card required. |
| [Canva (Free)](https://www.canva.com/en/pricing/) | bundled | Rate-limited free | Canva AI, Magic Media | Canva provides free users with a recurring monthly allowance across standard and premium AI tools directly in the design canvas. Free usage excludes Ultra AI tools and paid enterprise API service accounts. |
| [Framer (Free)](https://www.framer.com/pricing) | bundled | Trial credits | Framer Agents | The 500 AI credits are now provided on a monthly basis for workspaces without active subscriptions. No credit card is required to sign up. |
| [Replit (Starter)](https://docs.replit.com/help/pricing-and-plans) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Starter plan is deprecated for new signups, but existing Starter users retain limited Free Mode allowances and cloud credits. New builders are directed to a 3-day free trial of Core. |
| [Kilo Gateway](https://kilo.ai/gateway) | api_key | Rate-limited free | baidu/ernie-5.5-flash-preview:free, liquid/lfm-3-1.7b:free, particle-ai/particle-1:free, recursive/flint-v1.0:free, nvidia/nemotron-3.5-super-vl:free, nvidia/nemotron-3.5-lightning:free, +8 more | Kilo Gateway offers free models with standard rate limits. No credit card required. |
| [Nous Portal](https://portal.nousresearch.com/api-docs) | api_key | Rate-limited free | upstage/solar-mini4:free, tencent/hy4-flash:free, stepfun/step-3.7-flash:free | Nous Portal offers 3 free models with 50 requests/minute and 500,000 tokens/minute. Free account registration required, no credit card required. |
| [Cohere](https://docs.cohere.com/docs/rate-limits) | api_key | Rate-limited free | Command A+, Command A Reasoning, Command A Translate, Command A Vision, Command A, Command R+, +4 more | Cohere provides free trial API keys for developers building with Command models. Users register an account to instantly retrieve trial credentials without entering a payment method. Usage is bounded by trial rate limits of 20 requests per minute and 1,000 API calls per month. |
| [Requesty](https://www.requesty.ai/pricing) | api_key | Rate-limited free | nvidia/nemotron-3.5-lightning-30b-a3b, nvidia/muse-glimmer-30b, nvidia/nemotron-3-ultra-550b-a55b, nvidia/nemotron-3-nano-omni-30b-a3b-reasoning, google/gemma-4-31b-it | Requesty offers free models with 200 requests/day per account. Email registration required, no credit card required. |
| [OVHcloud AI Endpoints](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/) | api_key | Rate-limited free | 10 free models (anonymous keyless), Qwen3Guard-Gen-0.6B, Qwen3Guard-Gen-8B, Olala-v1.0-translate | OVHcloud offers free playground testing and open-source models with keyless access, rate-limited to 2 requests per minute per IP. |
| [SiliconFlow](https://siliconflow.cn) | api_key | Trial credits | Speech models (unspecified) | SiliconFlow provides $200 in free trial credits upon developer account registration. Credits can be applied across speech, text, and multimodal open-source models through an OpenAI-compatible API. |
| [DeepSeek Platform](https://api-docs.deepseek.com) | api_key | Trial credits | deepseek-chat, deepseek-reasoner | DeepSeek offers an initial free grant balance upon developer account registration. Users access production deepseek-chat and deepseek-reasoner endpoints via OpenAI-compatible APIs without immediate paid top-ups. The platform automatically exhausts the granted balance first before requiring paid credits or subscription upgrades. |
| [Braintrust](https://www.braintrust.dev/pricing) | api_key | Trial credits | deepseek-v4.1-flash, deepseek-v4-flash-0731, glm-5.3-flash, glm-5.2, kimi-k3, jev, +7 more | Braintrust offers $10/month recurring model credit on Starter across built-in models. Work email required, no credit card required. Model credit resets monthly with no rollover. |
| [Deepgram](https://deepgram.com/pricing) | api_key | Trial credits | nova-3, nova-2, flux, aura | Deepgram provides free trial credits upon registration, unlocking public speech-to-text and text-to-speech models with no credit card required upfront. |
| [AssemblyAI](https://www.assemblyai.com/pricing) | api_key | Trial credits | AssemblyAI-TTS-1, AssemblyAI-STT-3.7, Universal-2, AssemblyAI-STT-3.7-Realtime-Agent, AssemblyAI-STT-3.7-Realtime, Universal-3.6 Pro Realtime, +1 more | New accounts receive $50 in free credits for Pre-recorded STT, Real-time STT, and Speech Understanding. No credit card is required to start. |
| [Dots Studio](https://dots.ai) | api_key | Trial credits | dots3-note-prev | The API is currently free of charge during a trial period without requiring a payment method or credit card. |
| [Liquid AI](https://console.liquid.ai) | api_key | Trial credits | lfm3-1.7b, lfm3-vl-2b, lfm3-audio-2b, lfm3-omni-2b, lfm2.5-24b-a2b, d1.2-ultra, +1 more | Liquid AI provides promotional developer API credits upon registration in the Liquid developer console without upfront card requirements. |
| [Speka](https://speka.me) | api_key | Permanent $0 | deepseek-ai/deepseek-v4-flash, deepseek-ai/deepseek-v4-pro, nvidia/nemotron-3-super-120b-a12b, nvidia/nemotron-3-nano-30b-a3b, nvidia/llama-3.3-nemotron-super-49b-v1.5, nvidia/nvidia-nemotron-nano-9b-v2, +21 more | Speka provides a $1 lifetime usage credit upon signup with a rate limit of 2 RPM without requiring a credit card. |
| [Alibaba DashScope (Bailian)](https://www.alibabacloud.com/help/en/model-studio/developer-reference/get-api-key) | api_key | Trial / Free tokens | Qwen3.7 Plus, DeepSeek V4.1 Flash 1017, GLM-5.3, Qwen3.6 Plus, Wan2.7 Image, HappyHorse 1.1 Reference-to-Video, +15 more | Alibaba Cloud Model Studio (Bailian/DashScope) provides free token allotments upon account activation across its Qwen and DeepSeek model fleet. Developers access high-throughput OpenAI-compatible endpoints with up to 1M token context windows. |
| [ModelScope](https://modelscope.cn/docs/api-inference) | api_key | Rate-limited free | deepseek-ai/DeepSeek-V4-Flash-0731, deepseek-ai/DeepSeek-V4-Pro, deepseek-ai/DeepSeek-V4-Pro-0813, deepseek-ai/DeepSeek-V4.1-Flash, deepseek-ai/DeepSeek-V4.1-Flash-1017, early-access/EA-29B-A4B, +38 more | ModelScope (Alibaba's open-source model community) offers free hosted inference for community and Qwen open-weights models. Users query standard OpenAI-compatible completion endpoints with context windows up to 262K tokens. Access is activated by creating a ModelScope account to retrieve an API access token, subject to fair-share community queuing and rate limits. |
| [AMD Developer Cloud](https://cloud.amd.com/) | api_key | Free Developer Tier | MiniCPM5-2B, Qwen3.8 Flash Next, DeepSeek V4 Flash 0731, MiniCPM-V 4.7 1B, MiniCPM-V 4.7 35B-A3B, Qwen3.8 27B, +4 more | AMD Developer Cloud provides free inference access to open frontier models running on AMD Instinct ROCm GPU clusters. Developers query OpenAI-compatible chat endpoints supporting DeepSeek, Qwen, and MiniCPM variants. Access is provisioned by registering an AMD Developer account to reach the API console, subject to cluster capacity and fair-use developer quotas. |
| [InferX](https://model.inferx.net/endpoints) | api_key | Free Developer Tier | Qwen3.6 35B A3B FP8, deepseek-v4-flash, Ornith-1.0-35B-FP8, Qwen3.6 27B FP8, mimo-v25, Qwen3 Coder Next FP8, +6 more | InferX provides zero-cost inference endpoints for open models including Qwen 3.6, Gemma 4, and DeepSeek variants. Developers access low-latency OpenAI-compatible completions with streaming and structured output support. Keys are provisioned instantly upon user sign-in without upfront payment, subject to community prototyping rate limits. |
| [Kimi For Coding (Moonshot AI)](https://www.kimi.ai/code/docs/en/kimi-code/models.html) | api_key | Free Developer Tier | Kimi K3.1 Pro Highspeed, Kimi K3-256K, Kimi K3.1 Pro, Kimi K3, kimi-for-coding, Kimi For Coding HighSpeed | Moonshot AI provides free developer inference for Kimi K3 and coding models with context windows up to 1M tokens. Developers query OpenAI-compatible coding endpoints supporting deep reasoning and agentic workflows. Credentials are retrieved via the Kimi coding portal, subject to community rate limits and peak-period concurrency throttling. |
| [SCNet](https://www.scnet.cn) | api_key | Free Developer Tier | Kimi K2.7 Code, Qwen3.8 Flash, MiniMax-M2.5, DeepSeek V4 Flash, DeepSeek V4 Pro 0813, GLM-5.3, +6 more | SCNet provides national high-performance computing open inference tokens for domestic LLMs including Qwen 3.8 and DeepSeek V4 Flash. Developers access OpenAI-compatible chat endpoints with up to 1M token context windows. Registration on the SCNet developer portal provisions API keys upon identity verification, subject to national computing quota rules. |
| [AIHubMix](https://aihubmix.com) | api_key | Promo free | coding-glm-5-turbo-free, coding-glm-5.3-flash-free, coding-glm-5.3-free, coding-glm-5.4-free, gemini-3-flash-preview-free, gemini-3.1-flash-image-preview-free, +23 more | AIHubMix provides a suite of zero-cost promotional models including GLM-4.7 Flash, Nemotron 3 Ultra, and Qwen 3.8 Max. Developers query OpenAI-compatible completion endpoints with long context support up to 1M tokens. Free API credentials are generated upon account signup without credit cards, subject to promotional token availability and rate limits. |

## Models (per provider)

### Synap by Linkrra

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen3-coder-30b | $0 (100,000 tokens/day account allowance) | 98.3K | 10 | Not published | 50 | 100,000 | 2026-11-28 |

### OpenCode Zen

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Big Pickle | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Iceman Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Inkling 2 Small Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Crouton Alpha Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| GLM-5.3-Flash Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| DeepSeek V4.1 Flash Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Beam Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Flint 40B Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| MiMo-V2.6-Flash Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Nemotron 3 Ultra Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Nemotron 3.5 Lightning Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Nemotron 3.5 Super VL Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Jev 1.13 Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| MiniMax M3.1 Flash Free | $0 | 1.0M | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| LongCat 2.5 Free | $0 | 1.0M | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Hy4 flash Free | $0 | 1M | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Tidepool Alpha Free | $0 | 1M | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |
| Seaglass Alpha Free | $0 | 1M | Unknown | Unknown | Unknown | Unknown | 2026-11-28 |

### OpenRouter

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baidu/ernie-5.5-flash-preview:free | $0 | 1.0M | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |
| liquid/lfm-3-1.7b:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |
| particle-ai/particle-1:free | $0 | 1M | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |
| recursive/flint-v1.0:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |
| nvidia/nemotron-3.5-super-vl:free | $0 | 1.0M | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |
| nvidia/nemotron-3.5-lightning:free | $0 | 1.0M | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |
| nvidia/nemotron-3-ultra-550b-a55b:free | $0 | 1.0M | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |
| google/gemma-4-26b-a4b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |
| google/gemma-4-31b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |
| google/lyria-3-pro-preview | $0 | 1M | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |
| google/lyria-3-clip-preview | $0 | 1M | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-28 |

### Google AI Studio (Gemini API)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gemini-3.5-flash-lite | $0 | 1024K | 15 | 250K | 500 | Not published | 2026-11-28 |
| gemini-3.1-flash-lite | $0 | 1024K | 15 | 250K | 500 | Not published | 2026-11-28 |
| gemma-4-26b-a4b-it | $0 | 256K | 30 | 16K | 14.4K | Not published | 2026-11-28 |
| gemma-4-31b-it | $0 | 256K | 30 | 16K | 14.4K | Not published | 2026-11-28 |
| gemini-4-hydrogen | $0 | 1024K | Varies by account | Varies by account | Not published | Not published | 2026-11-28 |
| gemini-3.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |
| gemini-3-flash-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |
| gemini-3.1-flash-lite-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |
| gemini-3.6-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |
| gemini-3.7-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |
| gemini-3.8-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |
| gemini-flash-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |
| gemini-flash-lite-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |
| gemini-2.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |
| gemini-2.5-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |
| gemini-omni-1.1-flash | $0 | 128K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |
| gemini-omni-flash-preview | $0 | 128K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-28 |

### Groq

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| llama-3.3-70b-versatile | $0 | 131K | 30 | 12K | 1,000 | 100K tokens/day | 2026-11-28 |
| llama-3.1-8b-instant | $0 | 131K | 30 | 6K | 14,400 | 500K tokens/day | 2026-11-28 |
| openai/gpt-oss-120b | $0 | 131K | 30 | 8K | 1,000 | 200K tokens/day | 2026-11-28 |
| openai/gpt-oss-20b | $0 | 131K | 30 | 8K | 1,000 | 200K tokens/day | 2026-11-28 |
| openai/gpt-oss-safeguard-20b | $0 | 131K | 3 | 2K | 1,000 | 200K tokens/day | 2026-11-28 |
| qwen/qwen3.8-27b | $0 | 131K | 30 | 8K | 1,000 | 2M tokens/day | 2026-11-28 |
| meta-llama/llama-prompt-guard-2-22m | $0 | 512 | 30 | 15K | 14,400 | 500K tokens/day | 2026-11-28 |
| meta-llama/llama-prompt-guard-2-86m | $0 | 512 | 30 | 15K | 14,400 | 500K tokens/day | 2026-11-28 |
| whisper-large-v3-turbo | $0 | 100MB audio | 20 | 7.2K ASH | 2,000 | 28.8K ASD | 2026-11-28 |
| whisper-large-v3 | $0 | 100MB audio | 20 | 7.2K ASH | 2,000 | 28.8K ASD | 2026-11-28 |
| canopylabs/orpheus-v1-english | $0 | 4K | 10 | 1.2K | 100 | 3.6K ASD | 2026-11-28 |
| canopylabs/orpheus-arabic-saudi | $0 | 4K | 10 | 1.2K | 100 | 3.6K ASD | 2026-11-28 |
| ALLaM-2-7b | $0 | 4K | 30 | 12K | 1,000 | 100K tokens/day | 2026-11-28 |

### Cerebras

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gpt-oss-120b | $5 trial credits (30-day, card required) | 65k free / 131k paid | 5 | 30K (Uncached), 90K (Total), 1M TPH, 1M TPD via Free Trial limits table; context cap updated to 65k on free tier per documentation updates over prior 8k assumption | Not published | 1M tokens/day (per model) | 2026-11-28 |
| qwen-3.8-27b | $5 trial credits (30-day, card required) | 64k free / 128k paid | 300 | 150K (Uncached), 750K (Total) via Free Trial limits table; context cap updated to 64k on free tier | Not published | 1M tokens/day (per model) | 2026-11-28 |

### Cloudflare Workers AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings) | $0 | 8K-128K+ (model-dependent) | 300 text gen (720-1,500 other tasks) | Model-dependent | Not published | 10,000 neurons/day | 2026-11-28 |
| @cf/meta/llama-3.3-70b-instruct-fp8-fast | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-28 |
| @cf/deepseek-ai/deepseek-r1-distill-qwen-32b | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-28 |
| @cf/qwen/qwen2.5-72b-instruct | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-28 |
| @cf/meta/llama-3.1-8b-instruct | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-28 |
| @cf/openai/whisper | $0 | 25MB audio | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-28 |

### Mistral La Plateforme

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mistral-small-latest | $0 | 128K | 60 | 500K | Not published | Not published | 2026-11-26 |
| codestral-latest | $0 | 256K | 30 | 300K | Not published | Not published | 2026-11-26 |
| open-mistral-nemo | $0 | 128K | 60 | 500K | Not published | Not published | 2026-11-26 |

### SambaNova Cloud

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gemma-4-31B-it | $0 (free tier) | 131072 | 20 | unknown | Not published | Not published | 2026-11-28 |
| gpt-oss-120b | $0 (free tier) | 131072 | 20 | unknown | Not published | Not published | 2026-11-28 |

### NVIDIA NIM (build.nvidia.com)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bigcode/starcoder2-15b | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| fastino/gliner2-pii | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| google/gemma-3-12b-it | $0 (trial credits) | 128K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| google/gemma-3-4b-it | $0 (trial credits) | 128K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| minimaxai/minimax-m3.1-flash | $0 (trial credits) | 256K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-28 |
| mistralai/mistral-large-4-1t-a52b | $0 (trial credits) | 1.0M | ~40 | Not published | Not published | Not published | 2026-11-28 |
| moonshotai/kimi-k3.1-pro | $0 (trial credits) | 1.0M | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/ai-synthetic-video-detector | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/cosmos-reason2-8b | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/embed-qa-4 | $0 (trial credits) | 8K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/ising-calibration-1.5-31b | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/llama-3.1-nemoguard-8b-topic-control | $0 (trial credits) | 125K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/llama-3.1-nemotron-safety-guard-8b-v3 | $0 (trial credits) | 125K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-28 |
| nvidia/llama-3.2-nemoretriever-1b-vlm-embed-v1 | $0 (trial credits) | 8K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/llama-3.2-nv-embedqa-1b-v1 | $0 (trial credits) | 8K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning | $0 (trial credits) | 250K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-3-ultra-550b-a55b | $0 (trial credits) | 1.0M | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-28 |
| nvidia/nemotron-3.5-bolt-e4b | $0 (trial credits) | 125K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-3.5-content-safety | $0 (trial credits) | 125K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-28 |
| nvidia/nemotron-3.5-embed-1b | $0 (trial credits) | 8K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-3.5-embed-8b | $0 (trial credits) | 8K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-3.5-lightning-30b-a3b | $0 (trial credits) | 256K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-28 |
| nvidia/nemotron-3.5-super-vl-120b-a12b | $0 (trial credits) | 1M | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-28 |
| nvidia/nv-embedqa-mistral-7b-v2 | $0 (trial credits) | 32K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nvclip | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/riva-translate-4b-instruct-v2 | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| poolside/laguna-xs-2.1 | $0 (trial credits) | 256K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-28 |
| snowflake/arctic-embed-l | $0 (trial credits) | 512 | ~40 | Not published | Not published | Not published | 2026-11-28 |
| stepfun-ai/step-5-preview | $0 (trial credits) | 1M | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-28 |
| z-ai/glm-5.3-flash | $0 (trial credits) | 1.0M | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-28 |
| google/google-paligemma | $0 | 125K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/cosmos-transfer2_5-2b | $0 | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/magpie-tts-zeroshot | $0 | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/sparsedrive | $0 | 125K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/bevformer | $0 | 125K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/synthetic-video-detector | $0 | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/studiovoice | $0 | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/active-speaker-detection | $0 | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/streampetr | $0 | 125K | ~40 | Not published | Not published | Not published | 2026-11-28 |
| openai/whisper-large-v3 | $0 | 448 | ~40 | Not published | Not published | Not published | 2026-11-28 |
| qwen/qwen-image | $0 | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| qwen/qwen-image-edit | $0 | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| black-forest-labs/flux_1-kontext-dev | $0 | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| black-forest-labs/flux_1-schnell | $0 | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| black-forest-labs/flux_2-klein-4b | $0 | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |
| black-forest-labs/flux.1-dev | $0 | Model-dependent | ~40 | Not published | Not published | Not published | 2026-11-28 |

### Z.AI (Zhipu)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.7-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-11-28 |
| GLM-4.5-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-11-28 |
| GLM-4.6V-Flash | $0 | 125K | 3 (burst) | Not published | 1,000 (1K RPD tier) | Not published | 2026-11-28 |

### DeepInfra

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-ai/DeepSeek-V3.1 | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-28 |
| Qwen/Qwen3-32B | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-28 |
| Qwen/Qwen2.5-72B-Instruct | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-28 |
| zai-org/GLM-4.7 | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-28 |

### GitHub Copilot (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Auto-selected (GPT-5 mini, Claude Haiku/Sonnet, Gemini Flash line) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |

### Kiro (AWS)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Sonnet 4.5 | $0 | 200K | Not published | Not published | Not published | Not published | 2026-11-28 |
| Claude Sonnet 4.0 | $0 | 200K | Not published | Not published | Not published | Not published | 2026-11-28 |
| Auto | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |
| DeepSeek 3.2 | $0 | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| MiniMax M2.5 | $0 | 200K | Not published | Not published | Not published | Not published | 2026-11-28 |
| GLM-5 | $0 | 200K | Not published | Not published | Not published | Not published | 2026-11-28 |
| MiniMax M2.1 | $0 | 200K | Not published | Not published | Not published | Not published | 2026-11-28 |
| Qwen3 Coder Next | $0 | 256K | Not published | Not published | Not published | Not published | 2026-11-28 |

### Trae (ByteDance)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 (limited allowance) | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |

### Bolt.new

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Dynamic project context | Unspecified | Unspecified | Unspecified | 300,000 tokens/day (1,000,000 tokens/month) | 2026-11-28 |

### Lovable

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fable 5.1 (Frontier model) | $0 | Not specified | Not specified | Not specified000 tokens/day account allowance or standard limits via bundled access | Not specified | 5 daily build credits (capped at 30/month on Free plan) | 2026-11-28 |

### v0 (Vercel)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Text, code, and image/file input | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-28 |
| Beam 1.0 | $0 | 1M | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-28 |
| Glyph Cluster | $0 | 250K | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-28 |
| Nemotron 3.5 Lightning Free | $0 | 1.0M | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-28 |
| Ampersand v0.1 | $0 | 1.0M | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-28 |
| Flint | $0 | 256K | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-28 |

### Kaggle Notebooks

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Open-weight models you load (GPU runtime) | $0 | Model-dependent (16 GB P100 / 2x16 GB T4 VRAM, 29 GB RAM) | N/A | N/A | N/A | 30 GPU hours/week (resets weekly) | 2026-11-28 |

### Hugging Face Spaces

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Any Hugging Face model you load (ZeroGPU) | $0 | Model-dependent (up to 96 GB VRAM; 60s default / 120s max GPU duration per call) | Rate-limited (queue-based) | Not specified | Not specified | 5 minutes GPU time / day | 2026-11-28 |
| GLM-4.7-Flash | $0 | 195.3K | Rate-limited (queue-based) | Not specified | Not specified | 5 minutes GPU time / day | 2026-11-28 |

### Cursor (Hobby)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cursor Free Models (Agent/Chat) | $0 | Not specified | Rate-limited | Rate-limited | Rate-limited | Rate-limited | 2026-11-28 |

### Windsurf

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWE-2 Flash Medium | $0 | Standard | Not specified | Not specified | Not specified | Not specified | 2026-11-28 |
| SWE-2 | $0 (Free through November 30, 2026) | Standard | Not specified | Not specified | Not specified | Not specified | 2026-11-28 |
| SWE-2.1 | $0 (Free through December 8, 2026) | Standard | Not specified | Not specified | Not specified | Not specified | 2026-11-28 |

### Devin (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWE-2 (Free) | $0 | Not published | Light quota | Not published | Not published | Not published | 2026-11-28 |
| Limited models (auto-selected) | $0 | Not published | Light quota | Not published | Not published | Not published | 2026-11-28 |

### Qoder

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Basic models + BYO key | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |

### Antigravity CLI (Google)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini 4 Hydrogen | $0 | Standard | N/A | N/A | Not published | Not published | 2026-11-28 |
| Gemini 3.8 Flash | $0 | Standard | N/A | N/A | N/A | N/A | 2026-11-28 |

### Google Colab

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini (AI features) + GPU for your code | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |
| Lyria 3 Clip Preview | $0 | 1M | Not published | Not published | Not published | Not published | 2026-11-28 |
| Lyria 3 Pro Preview | $0 | 1M | Not published | Not published | Not published | Not published | 2026-11-28 |
| Gemma 4 31B IT | $0 | 256K | Not published | Not published | Not published | Not published | 2026-11-28 |
| Gemma 4 26B A4B IT | $0 | 256K | Not published | Not published | Not published | Not published | 2026-11-28 |

### Figma (Starter)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Figma Make | $0 (150 AI credits/day, up to 500/mo) | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |
| The Figma agent | $0 (150 AI credits/day, up to 500/mo) | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |
| GPT Image 2.5 Sunburst | $0 (2 credits/image) | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |
| Nano Banana 2 Lite | $0 (6 credits/image) | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |
| Nano Banana 2 | $0 (16 credits/image) | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |
| Nano Banana 2.1 | $0 (7 credits/image) | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |
| GPT 2.6 Flare | $0 (9 credits/image) | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |
| GPT 2.6 Image Sunburst | $0 (10 credits/image) | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |

### Canva (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Canva AI | $0 | unknown | unknown | unknown | 20 uses (monthly shared limit) | unknown | 2026-11-28 |
| Magic Media | $0 | unknown | unknown | unknown | 20 uses (monthly shared limit) | unknown | 2026-11-28 |

### Framer (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Framer Agents | $0 (500 AI credits / month) | Canvas-native web design, layout, styling, CMS, and copy generation | Not specified | Not specified | Not specified | 500 credits (one-time trial) | 2026-11-28 |

### Replit (Starter)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-28 |

### Kilo Gateway

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baidu/ernie-5.5-flash-preview:free | $0 | 1.0M | 20 | Provider-dependent | 200/day | Not published | 2026-11-28 |
| liquid/lfm-3-1.7b:free | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-11-28 |
| particle-ai/particle-1:free | $0 | 1M | 20 | Provider-dependent | 200/day | Not published | 2026-11-28 |
| recursive/flint-v1.0:free | $0 | 256K | 20 | Provider-dependent | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-3.5-super-vl:free | $0 | 1.0M | 20 | Provider-dependent | 200/day | Not published | 2026-11-28 |
| nvidia/nemotron-3.5-lightning:free | $0 | 1.0M | 20 | Provider-dependent | 200/day | Not published | 2026-11-28 |
| nvidia/nemotron-3-ultra-550b-a55b:free | $0 | 1.0M | 20 | Provider-dependent | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | $0 | 250K | 20 | Provider-dependent | Not published | Not published | 2026-11-28 |
| google/lyria-3-pro-preview | $0 | 1M | 20 | Provider-dependent | 200/day | Not published | 2026-11-28 |
| google/lyria-3-clip-preview | $0 | 1M | 20 | Provider-dependent | 200/day | Not published | 2026-11-28 |
| reflection/beam-free | $0 | 1M | 20 | Provider-dependent | Not published | Not published | 2026-11-28 |
| stealth/glyph-cluster | $0 | 250K | 20 | Provider-dependent | 200/day | Not published | 2026-11-28 |
| openrouter/bodybuilder | $0 | 125K | 20 | Provider-dependent | 200/day | Not published | 2026-11-28 |
| openrouter/pareto-code | $0 | 195.3K | 20 | Provider-dependent | 200/day | Not published | 2026-11-28 |

### Nous Portal

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| upstage/solar-mini4:free | $0 | 512K | 50 | 500K | Not published | Not published | 2026-11-28 |
| tencent/hy4-flash:free | $0 | 1M | 50 | 500K | Not published | Not published | 2026-11-28 |
| stepfun/step-3.7-flash:free | $0 | 250K | 50 | 500K | Not published | Not published | 2026-11-28 |

### Cohere

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Command A+ | $0 | N/A | 20 | N/A | N/A | N/A | 2026-11-28 |
| Command A Reasoning | $0 | N/A | 20 | N/A | N/A | N/A | 2026-11-28 |
| Command A Translate | $0 | N/A | 20 | Not published | Not published | Not published | 2026-11-28 |
| Command A Vision | $0 | N/A | 20 | Not published | Not published | Not published | 2026-11-28 |
| Command A | $0 | N/A | 20 | Not published | Not published | Not published | 2026-11-28 |
| Command R+ | $0 | N/A | 20 | N/A | N/A | N/A | 2026-11-28 |
| Command R | $0 | N/A | 20 | N/A | N/A | N/A | 2026-11-28 |
| Command R7B | $0 | N/A | 20 | N/A | N/A | N/A | 2026-11-28 |
| North Mini Code | $0 | 250K | 20 | N/A | N/A | N/A | 2026-11-28 |
| North Small Translate | $0 | 32K | 20 | N/A | N/A | N/A | 2026-11-28 |

### Requesty

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nvidia/nemotron-3.5-lightning-30b-a3b | $0 | 1M | Not published | Not published | 200/day shared | Not published | 2026-11-28 |
| nvidia/muse-glimmer-30b | $0 | 128K | Not published | Not published | 200/day shared | Not published | 2026-11-28 |
| nvidia/nemotron-3-ultra-550b-a55b | $0 | 1M | Not published | Not published | 200/day shared | Not published | 2026-11-28 |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning | $0 | 128K | Not published | Not published | 200/day shared | Not published | 2026-11-28 |
| google/gemma-4-31b-it | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-11-28 |

### OVHcloud AI Endpoints

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 free models (anonymous keyless) | $0 | Model-dependent | 2/min per IP | Not published | Not published | Not published | 2026-11-28 |
| Qwen3Guard-Gen-0.6B | $0 | 32K | 2/min per IP | Not published | Not published | Not published | 2026-11-28 |
| Qwen3Guard-Gen-8B | $0 | 32K | 2/min per IP | Not published | Not published | Not published | 2026-11-28 |
| Olala-v1.0-translate | $0 | 8K | 2/min per IP | Not published | Not published | Not published | 2026-11-28 |

### SiliconFlow

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Speech models (unspecified) | $0 (trial credits) | 43,000 minutes or 700+ hours | N/A | N/A | N/A | N/A | 2026-11-28 |

### DeepSeek Platform

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-chat | $0 (5M signup tokens) | 64K | 60 | Not published | Not published | 5M tokens grant | 2026-11-26 |
| deepseek-reasoner | $0 (5M signup tokens) | 64K | 60 | Not published | Not published | 5M tokens grant | 2026-11-26 |

### Braintrust

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-v4.1-flash | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| deepseek-v4-flash-0731 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| glm-5.3-flash | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| glm-5.2 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| kimi-k3 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| jev | $0 ($10/mo model credits) | 256K | Not published | Not published | Not published | Not published | 2026-11-28 |
| gpt-6-luna | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| gpt-6-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| gpt-6.1-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| gpt-6-astra | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| gpt-5.6-luna | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| gpt-5.6-terra | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |
| gpt-5.6-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-28 |

### Deepgram

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nova-3 | $0 (trial credits) | N/A | 150 (streaming) | N/A | N/A | N/A | 2026-11-28 |
| nova-2 | $0 (trial credits) | N/A | 150 (streaming) | N/A | N/A | N/A | 2026-11-28 |
| flux | $0 (trial credits) | N/A | 150 (streaming) | N/A | N/A | N/A | 2026-11-28 |
| aura | $0 (trial credits) | N/A | 45 (streaming) | N/A | N/A | N/A | 2026-11-28 |

### AssemblyAI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AssemblyAI-TTS-1 | $0 (trial credits) | Unknown | Not published | Not published | Not published | Not published | 2026-11-28 |
| AssemblyAI-STT-3.7 | $0 (trial credits) | Unknown | Not published | Not published | Not published | 43000 minutes | 2026-11-28 |
| Universal-2 | $0 (trial credits) | Unknown | Not published | Not published | Not published | Not published | 2026-11-28 |
| AssemblyAI-STT-3.7-Realtime-Agent | $0 (trial credits) | Unknown | Not published | Not published | Not published | Not published | 2026-11-28 |
| AssemblyAI-STT-3.7-Realtime | $0 (trial credits) | Unknown | Not published | Not published | Not published | Not published | 2026-11-28 |
| Universal-3.6 Pro Realtime | $0 (trial credits) | Unknown | Not published | Not published | Not published | Not published | 2026-11-28 |
| Dictation API | $0 (trial credits) | Unknown | Not published | Not published | Not published | Not published | 2026-11-28 |

### Dots Studio

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dots3-note-prev | $0 (free trial) | 524288 | 60 | 1500000 | Not published | Not published | 2026-11-28 |

### Liquid AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| lfm3-1.7b | $0 (trial) | 128,000 | Published on portal | Not published | Not published | Not published | 2026-11-28 |
| lfm3-vl-2b | $0 (trial) | 128,000 | Published on portal | Not published | Not published | Not published | 2026-11-28 |
| lfm3-audio-2b | $0 (trial) | 128,000 | Published on portal | Not published | Not published | Not published | 2026-11-28 |
| lfm3-omni-2b | $0 (trial) | 128,000 | Published on portal | Not published | Not published | Not published | 2026-11-28 |
| lfm2.5-24b-a2b | $0 (trial) | 128,000 | Published on portal | Not published | Not published | Not published | 2026-11-28 |
| d1.2-ultra | $0 (trial) | 65,536 | Published on portal | Not published | Not published | Not published | 2026-11-28 |
| d1.2 | $0 (trial) | 65,536 | Published on portal | Not published | Not published | Not published | 2026-11-28 |

### Speka

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-ai/deepseek-v4-flash | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| deepseek-ai/deepseek-v4-pro | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-3-super-120b-a12b | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-3-nano-30b-a3b | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/llama-3.3-nemotron-super-49b-v1.5 | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nvidia-nemotron-nano-9b-v2 | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-3-ultra-550b-a55b | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| meta/llama-3.3-70b-instruct | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| meta/llama-3.1-8b-instruct | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| meta/llama-3.2-3b-instruct | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| mistralai/mistral-nemotron | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| mistralai/mistral-medium-3.5-128b | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| z-ai/glm-5.2 | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| minimaxai/minimax-m3 | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| stepfun-ai/step-3.7-flash | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| openai/gpt-oss-120b | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| openai/gpt-oss-20b | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| poolside/laguna-xs-2.1 | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| meta/llama-3.2-90b-vision-instruct | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-nano-12b-v2-vl | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| meta/llama-3.2-11b-vision-instruct | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nv-embedqa-e5-v5 | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/llama-nemotron-embed-1b-v2 | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nemotron-3-embed-1b | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| nvidia/nv-embed-v1 | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| black-forest-labs/flux.1-dev | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |
| black-forest-labs/flux.1-schnell | $0 (lifetime credit allowance) | Model-dependent | 2 | Not published | Not published | Not published | 2026-11-28 |

### Alibaba DashScope (Bailian)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3.7 Plus | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| DeepSeek V4.1 Flash 1017 | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| GLM-5.3 | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Qwen3.6 Plus | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Wan2.7 Image | $0 (promo free tokens) | 8K | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| HappyHorse 1.1 Reference-to-Video | $0 (promo free tokens) | Model-dependent | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Qwen3.6 Flash | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Qwen3.7 Max | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| DeepSeek V4 Pro | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| MiniMax-M2.5 | $0 (promo free tokens) | 192K | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Kimi K2.6 | $0 (promo free tokens) | 256K | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Kimi K2.5 | $0 (promo free tokens) | 256K | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Kimi K2.7 Code | $0 (promo free tokens) | 256K | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| HappyHorse 1.1 Text-to-Video | $0 (promo free tokens) | Model-dependent | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Qwen Image 2.0 | $0 (promo free tokens) | 8K | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Wan2.7 Image Pro | $0 (promo free tokens) | 8K | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| HappyHorse 1.1 Image-to-Video | $0 (promo free tokens) | Model-dependent | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| DeepSeek V4 Pro 0813 | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Qwen3.8 Flash | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Qwen3.8 Max | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |
| Qwen Image 2.0 Pro | $0 (promo free tokens) | 8K | 60 | Not published | Free tier token grant | Not published | 2026-11-28 |

### ModelScope

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-ai/DeepSeek-V4-Flash-0731 | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| deepseek-ai/DeepSeek-V4-Pro | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| deepseek-ai/DeepSeek-V4-Pro-0813 | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| deepseek-ai/DeepSeek-V4.1-Flash | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| deepseek-ai/DeepSeek-V4.1-Flash-1017 | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| early-access/EA-29B-A4B | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| MedAIBase/AntAngelMed | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| meituan-longcat/LongCat-Flash-Lite | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| MiniMax/MiniMax-M1-80k | $0 | 80K | 30 | Not published | Not published | Not published | 2026-11-28 |
| MiniMax/MiniMax-M3 | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| mistralai/Mistral-Large-Instruct-2407 | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| moonshotai/Kimi-K3.1-Pro | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| MusePublic/Qwen-Image-Edit | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| nex-agi/Nex-N2.5-mini | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| nex-agi/Nex-N2.5-Pro | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| opencompass/CompassJudger-1-32B-Instruct | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| OpenGVLab/InternVL3_5-241B-A28B | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| PaddlePaddle/ERNIE-4.5-0.3B-PT | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| PaddlePaddle/ERNIE-4.5-21B-A3B-PT | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| PaddlePaddle/ERNIE-4.5-300B-A47B-PT | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| PaddlePaddle/ERNIE-4.5-VL-28B-A3B-PT | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| Qwen/Qwen3.5-122B-A10B | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| Qwen/Qwen3.5-27B | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| Qwen/Qwen3.5-35B-A3B | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| Qwen/Qwen3.5-397B-A17B | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| Qwen/Qwen3.8-27B | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| Qwen/Qwen3.8-Flash-Next | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| Shanghai_AI_Laboratory/Intern-S1 | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| Shanghai_AI_Laboratory/Intern-S1-mini | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| Shanghai_AI_Laboratory/Intern-S2-Preview | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| stepfun-ai/Step-3.5-Flash | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| stepfun-ai/Step-3.7-Flash | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| stepfun-ai/Step-5-Preview | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| XGenerationLab/XiYanSQL-QwenCoder-32B-2412 | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| XGenerationLab/XiYanSQL-QwenCoder-32B-2504 | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| ZhipuAI/GLM-4.7-Flash | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| ZhipuAI/GLM-5.2 | $0 | Not published | 30 | Not published | Not published | Not published | 2026-11-28 |
| ZhipuAI/GLM-4.6 | $0 | 198K | 30 | Not published | Not published | Not published | 2026-11-28 |
| ZhipuAI/GLM-4.5 | $0 | 128K | 30 | Not published | Not published | Not published | 2026-11-28 |
| Qwen/Qwen3-Coder-30B-A3B-Instruct | $0 | 256K | 30 | Not published | Not published | Not published | 2026-11-28 |
| Qwen/Qwen3-30B-A3B-Thinking-2507 | $0 | 256K | 30 | Not published | Not published | Not published | 2026-11-28 |
| Qwen/Qwen3-235B-A22B-Thinking-2507 | $0 | 256K | 30 | Not published | Not published | Not published | 2026-11-28 |
| Qwen/Qwen3-30B-A3B-Instruct-2507 | $0 | 256K | 30 | Not published | Not published | Not published | 2026-11-28 |
| Qwen/Qwen3-235B-A22B-Instruct-2507 | $0 | 256K | 30 | Not published | Not published | Not published | 2026-11-28 |

### AMD Developer Cloud

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MiniCPM5-2B | $0 | 128K | 30 | Not published | 1,000 | Not published | 2026-11-08 |
| Qwen3.8 Flash Next | $0 | 256K | 30 | Not published | 1,000 | Not published | 2026-11-08 |
| DeepSeek V4 Flash 0731 | $0 | 1M | 30 | Not published | 1,000 | Not published | 2026-11-08 |
| MiniCPM-V 4.7 1B | $0 | 256K | 30 | Not published | 1,000 | Not published | 2026-11-08 |
| MiniCPM-V 4.7 35B-A3B | $0 | 256K | 30 | Not published | 1,000 | Not published | 2026-11-08 |
| Qwen3.8 27B | $0 | 256K | 30 | Not published | 1,000 | Not published | 2026-11-08 |
| MiMo-V2.6-Flash | $0 | 1M | 30 | Not published | 1,000 | Not published | 2026-11-08 |
| DeepSeek V4.1 Flash | $0 | 1M | 30 | Not published | 1,000 | Not published | 2026-11-08 |
| Gemma 4 31B IT | $0 | 256K | 30 | Not published | 1,000 | Not published | 2026-11-08 |
| GLM-5.3-Flash | $0 | 256K | 30 | Not published | 1,000 | Not published | 2026-11-08 |

### InferX

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3.6 35B A3B FP8 | $0 | 255.9K | 60 | Not published | 2,000 | Not published | 2026-11-08 |
| deepseek-v4-flash | $0 | 1.0M | 60 | Not published | 2,000 | Not published | 2026-11-08 |
| Ornith-1.0-35B-FP8 | $0 | 255.9K | 60 | Not published | 2,000 | Not published | 2026-11-08 |
| Qwen3.6 27B FP8 | $0 | 256K | 60 | Not published | 2,000 | Not published | 2026-11-08 |
| mimo-v25 | $0 | 1.0M | 60 | Not published | 2,000 | Not published | 2026-11-08 |
| Qwen3 Coder Next FP8 | $0 | 250.1K | 60 | Not published | 2,000 | Not published | 2026-11-08 |
| Agents-A1 | $0 | 255.9K | 60 | Not published | 2,000 | Not published | 2026-11-08 |
| Devstral-2-123B-Instruct-2512-int4-AutoRound | $0 | 125K | 60 | Not published | 2,000 | Not published | 2026-11-08 |
| Qwen3-Embedding-8B | $0 | 32K | 60 | Not published | 2,000 | Not published | 2026-11-08 |
| Qwen3.6-35B-A3B-fp8-no-thinking | $0 | 255.9K | 60 | Not published | 2,000 | Not published | 2026-11-08 |
| Gemma 4 31B IT FP8 | $0 | 256K | 60 | Not published | 2,000 | Not published | 2026-11-08 |
| Qwen3-Coder-Next-FP8-no-thinking | $0 | 253.9K | 60 | Not published | 2,000 | Not published | 2026-11-08 |

### Kimi For Coding (Moonshot AI)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kimi K3.1 Pro Highspeed | $0 | 1M | 60 | Not published | 1,000 | Not published | 2026-11-13 |
| Kimi K3-256K | $0 | 256K | 60 | Not published | 1,000 | Not published | 2026-11-13 |
| Kimi K3.1 Pro | $0 | 1M | 60 | Not published | 1,000 | Not published | 2026-11-13 |
| Kimi K3 | $0 | 1M | 60 | Not published | 1,000 | Not published | 2026-11-13 |
| kimi-for-coding | $0 | 1M | 60 | Not published | 1,000 | Not published | 2026-11-13 |
| Kimi For Coding HighSpeed | $0 | 256K | 60 | Not published | 1,000 | Not published | 2026-11-13 |

### SCNet

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kimi K2.7 Code | $0 | 256K | 60 | Not published | 1,000 | Not published | 2026-11-14 |
| Qwen3.8 Flash | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-14 |
| MiniMax-M2.5 | $0 | 200K | 60 | Not published | 1,000 | Not published | 2026-11-14 |
| DeepSeek V4 Flash | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-14 |
| DeepSeek V4 Pro 0813 | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-14 |
| GLM-5.3 | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-14 |
| MiniMax-M3 | $0 | 1M | 60 | Not published | 1,000 | Not published | 2026-11-14 |
| MiniMax-M2.7 | $0 | 200K | 60 | Not published | 1,000 | Not published | 2026-11-14 |
| Qwen3.8 Max | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-14 |
| DeepSeek V4 Pro | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-14 |
| Kimi K2.6 | $0 | 256K | 60 | Not published | 1,000 | Not published | 2026-11-14 |
| Kimi K2.5 | $0 | 256K | 60 | Not published | 1,000 | Not published | 2026-11-14 |

### AIHubMix

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| coding-glm-5-turbo-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| coding-glm-5.3-flash-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| coding-glm-5.3-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| coding-glm-5.4-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| gemini-3-flash-preview-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| gemini-3.1-flash-image-preview-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| gpt-4.1-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| gpt-4.1-mini-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| gpt-4.1-nano-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| gpt-4o-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| k2.6-code-preview-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| qwen3.6-plus-preview-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| step-3.7-flash-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| wan3.0-video-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| wan3.0-video-prime-free | $0 | Not published | 10 | Not published | Not published | Not published | 2026-11-28 |
| Nemotron 3 Ultra 550B A55B (free) | $0 | 1.0M | 10 | Not published | Not published | Not published | 2026-11-28 |
| Gemma 4 26B A4B IT (free) | $0 | 256K | 10 | Not published | Not published | Not published | 2026-11-28 |
| GLM-4.7-Flash (free) | $0 | 195.3K | 10 | Not published | Not published | Not published | 2026-11-28 |
| Ling 3.0 Flash (free) | $0 | 256K | 10 | Not published | Not published | Not published | 2026-11-28 |
| Qwen3.8 Max (free) | $0 | 1.0M | 10 | Not published | Not published | Not published | 2026-11-28 |
| Coding GLM 5.1 (free) | $0 | 195.3K | 10 | Not published | Not published | Not published | 2026-11-28 |
| Nemotron 3.5 Content Safety (free) | $0 | 125K | 10 | Not published | Not published | Not published | 2026-11-28 |
| Nemotron 3 Nano Omni 30B A3B Reasoning (free) | $0 | 250K | 10 | Not published | Not published | Not published | 2026-11-28 |
| GLM-5.2 (Coding, free) | $0 | 1.0M | 10 | Not published | Not published | Not published | 2026-11-28 |
| Qwen3.8 Flash (free) | $0 | 1.0M | 10 | Not published | Not published | Not published | 2026-11-28 |
| Gemma 4 31B IT (free) | $0 | 256K | 10 | Not published | Not published | Not published | 2026-11-28 |
| Coding MiniMax M2.7 (Free) | $0 | 200K | 10 | Not published | Not published | Not published | 2026-11-28 |
| Nemotron 3.5 Lightning 30B A3B (free) | $0 | 256K | 10 | Not published | Not published | Not published | 2026-11-28 |
| Nemotron 3 Super 120B A12B (free) | $0 | 256K | 10 | Not published | Not published | Not published | 2026-11-28 |
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
