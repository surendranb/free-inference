# Free Inference

Free AI & LLM inference you can build with: an API key, a CLI login, or inference bundled inside a coding tool or builder. Speech-to-text, voice synthesis, code, vision, and reasoning. The test is whether you can ship an artifact you keep — code, an app, an audio file, a site, a design, an agent, a skill. Chat-only free tiers are excluded on purpose.

> **2026-11-06** · 40 providers · 148 free models
> Interactive site: https://freeinference.dev · Agent summary: https://freeinference.dev/llms.txt · Machine data: https://freeinference.dev/data/providers.json (validate against https://freeinference.dev/data/schema.json)

### Quick Navigation & Machine Access

- 🤖 **Agent Skill (`SKILL.md`)**: [https://freeinference.dev/skill.md](https://freeinference.dev/skill.md) (install: `curl -fsSL https://freeinference.dev/skill.md -o ~/.agents/skills/free-inference/SKILL.md`)
- 📋 **OpenAI Catalog Endpoint**: `GET https://freeinference.dev/v1/models`
- 📡 **Changelog RSS/Atom Feed**: [https://freeinference.dev/feed.xml](https://freeinference.dev/feed.xml)
- 📬 **Weekly Dispatch (Newsletter)**: [https://freeinference.dev/newsletter/](https://freeinference.dev/newsletter/)
- 💳 **No Credit Card or Subscription**: [https://freeinference.dev/free-llm-api-no-credit-card/](https://freeinference.dev/free-llm-api-no-credit-card/)
- ⚡ **OpenAI-Compatible Drop-in Endpoints**: [https://freeinference.dev/free-openai-compatible-api/](https://freeinference.dev/free-openai-compatible-api/)
- 🛠 **Free Coding & Cursor / Cline Keys**: [https://freeinference.dev/free-coding-api/](https://freeinference.dev/free-coding-api/) · [https://freeinference.dev/free-cursor-api/](https://freeinference.dev/free-cursor-api/)
- 🧠 **Top Model Guides**: [DeepSeek V3.2](https://freeinference.dev/free-deepseek-api/) · [Llama 3.3 70B](https://freeinference.dev/free-llama-api/) · [Qwen 3.8](https://freeinference.dev/free-qwen-api/) · [Gemini 2.5 Flash](https://freeinference.dev/free-gemini-api/) · [GLM-5 / 4.7](https://freeinference.dev/free-glm-api/)

## Providers

| Provider | Access | Free tier | Notable models | Notes |
| --- | --- | --- | --- | --- |
| [OpenCode Zen](https://opencode.ai/v2/docs/console/models/) | api_key | Promo free (limited time) | Big Pickle, GLM-5.3-Flash Free, DeepSeek V4.1 Flash Free, MiMo-V2.6-Flash Free, Beam Free, Flint 40B Free, +6 more | OpenCode Zen offers 12 free models with 256K–1M context (including Big Pickle, Jev 1.13, Flint 40B, and Crouton). No credit card required. Free-tier prompts are retained for model training. |
| [OpenRouter](https://openrouter.ai/models?max_price=0) | api_key | Rate-limited free | cohere/north-mini-code:free, dots-studio/dots-3-note-preview:free, google/gemma-4-26b-a4b-it:free, google/gemma-4-31b-it:free, liquid/lfm-2.5-2.6b:free, nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free, +7 more | OpenRouter offers 13 permanently free models (:free suffix) with 64K–500K context, translating to 50 requests/day (1,000 requests/day with + purchased credits). No credit card required. Upstream model availability determines live rate limits. |
| [Google AI Studio (Gemini API)](https://ai.google.dev/gemini-api/docs/rate-limits) | api_key | Rate-limited free | gemini-2.5-flash, gemini-2.5-flash-lite, gemini-3-flash-preview, gemini-3.1-flash-lite, gemini-3.1-flash-lite-preview, gemini-3.5-flash, +10 more | Google AI Studio offers 16 free models with up to 1M context, translating to 15–30 requests/minute (up to 1,500 requests/day per model). No credit card required. Free-tier prompts and outputs are retained for model training. |
| [Groq](https://console.groq.com/docs/rate-limits) | api_key | Rate-limited free | llama-3.3-70b-versatile, llama-3.1-8b-instant, meta-llama/llama-4-scout-17b-16e-instruct, openai/gpt-oss-120b, openai/gpt-oss-20b, qwen/qwen3.6-27b, +7 more | Groq offers 13 free models (9 LLMs, 2 Whisper STT, 2 Orpheus TTS), translating to up to 14,400 text requests/day and 2,000 audio transcriptions/day (~8 hours/day). No credit card required. Limits are pooled at organization level. |
| [Cerebras](https://inference-docs.cerebras.ai/support/rate-limits) | api_key | Trial credits | gpt-oss-120b, qwen-3.8-27b | Cerebras offers $5 trial credit across 2 models (gpt-oss-120b, qwen-3.8-27b with 8K context cap), translating to 1M tokens/day at 2,000+ tokens/sec. Credit card required. Trial credits expire in 30 days. |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/limits) | api_key | Rate-limited free | ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings), @cf/meta/llama-3.3-70b-instruct-fp8-fast, @cf/deepseek-ai/deepseek-r1-distill-qwen-32b, @cf/qwen/qwen2.5-72b-instruct, @cf/meta/llama-3.1-8b-instruct, @cf/openai/whisper | Cloudflare Workers AI offers ~80 free models (including Llama 3.3 70B, DeepSeek-R1 distills, Whisper, and FLUX), translating to 10,000 neurons/day (~hundreds of queries or audio minutes). No credit card required. Hard stop at 10,000 neurons until 00:00 UTC daily reset. |
| [Mistral La Plateforme](https://docs.mistral.ai) | api_key | Rate-limited free (Experiment) | Mistral Large, Codestral, All API models (Experiment tier) | Mistral offers free evaluation API access across 4 models (including Codestral and Mistral Small), translating to 1B free tokens/month on Experiment tier. Phone verification required; no credit card required. Restricted to evaluation and non-production prototyping. |
| [SambaNova Cloud](https://cloud.sambanova.ai/apis) | api_key | Trial credits | DeepSeek-V3.1, DeepSeek-V3.2, Meta-Llama-3.3-70B-Instruct, gemma-4-31B-it, gpt-oss-120b | [The Grant] Free tier. [The Output] Allows free access to models. [The Process] Does not require a credit card, but requires account creation. [The Condition] Credits expire in 90 days. |
| [NVIDIA NIM (build.nvidia.com)](https://build.nvidia.com) | api_key | Trial credits | GLM-5, Kimi-2.5, NIM-packaged open models | NVIDIA NIM offers 1,000 free trial credits across catalog models (including Nemotron 3.5 Lightning with 1M context), translating to ~40 hours of inference testing. No credit card required; corporate email required for extended credits. Credits tie to a 90-day evaluation window. |
| [Z.AI (Zhipu)](https://z.ai) | api_key | Rate-limited free | GLM-5.1, GLM-4.5-Flash, GLM-4.7-Flash, GLM-4.6V-Flash (vision) | Z.AI offers free API access to GLM-5.1, GLM-4.7-Flash, and GLM-4.6V-Flash with 128K context, translating to 15 requests/minute. No credit card required. Shared free tier throttles during peak platform traffic hours. |
| [DeepInfra](https://docs.deepinfra.com/account/rate-limits) | api_key | Trial credits | deepseek-ai/DeepSeek-V3.1, Qwen/Qwen3-32B, Qwen/Qwen2.5-72B-Instruct, zai-org/GLM-4.7 | DeepInfra offers $5 signup trial credit across 185+ models (including DeepSeek-V3.1, Qwen 3 32B, and GLM-4.7), translating to ~50M tokens at 200 concurrent requests. No credit card required. Credits remain active until depleted. |
| [GitHub Copilot (Free)](https://github.com/features/copilot) | login | Rate-limited free | Auto-selected (GPT-5 mini, Claude Haiku/Sonnet, Gemini Flash line) | GitHub Copilot Free offers 2,000 code completions/month and 50 chat messages/month. GitHub account required, no credit card required. Models are auto-selected by GitHub and run bundled inside the editor. |
| [Kiro (AWS)](https://kiro.dev/pricing) | login | Rate-limited free | Qwen3 Coder Next, DeepSeek 3.2, MiniMax M2.1, Claude Sonnet 4.5 | Kiro offers 50 free credits/month for spec-driven agent workflows. Social account or AWS Builder ID required, no credit card required. Unused credits do not roll over to the next month. |
| [Trae (ByteDance)](https://www.trae.ai/pricing) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Trae offers 5,000 free code completions/month plus standard-queue access to Claude 3.5 Sonnet and GPT-4o. Account login required, no credit card required. Inference runs bundled inside the Trae IDE. |
| [Bolt.new](https://support.bolt.new/account-and-subscription/tokens) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Bolt.new offers 1M free tokens/month with a 300K tokens/day daily cap for full-stack web generation. Account login required, no credit card required. Credits reset on the first of each month. |
| [Lovable](https://docs.lovable.dev/introduction/credits-and-usage) | bundled | Rate-limited free | Frontier models (bundled, Fable 5.1) | Lovable offers 5 daily build credits (up to 30/month) plus 20 cloud and 4 AI edit credits/month. Account login required, no credit card required. Inference runs bundled inside the Lovable web builder. |
| [v0 (Vercel)](https://v0.app/docs/pricing) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | v0 offers $5/month in free credits plus 7 messages/day for UI component generation. Account login required, no credit card required. Credits reset monthly with no rollover. |
| [Kaggle Notebooks](https://www.kaggle.com/docs/efficient-gpu-usage) | login | Rate-limited free | Open-weight models you load (GPU runtime) | Kaggle offers 30 GPU-hours/week (NVIDIA P100 or 2xT4) in 12-hour maximum execution sessions. Phone verification required for GPU access; no credit card required. GPU quota resets weekly. |
| [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces-overview) | login | Rate-limited free | Any Hugging Face model you load (ZeroGPU) | Hugging Face Spaces offers free hosting for up to 2 ZeroGPU Gradio spaces with dynamic GPU allocation. Free account required, no credit card required. Persistent storage and dedicated hardware require a Pro tier. |
| [Cursor (Hobby)](https://cursor.com/pricing) | bundled | Rate-limited free | Composer 2 (own), Auto (auto-selected, limited frontier) | Cursor Hobby offers 2,000 free completion edits and limited agent requests. Account login required, no credit card required. Quota is metered per user account with frontier models auto-selected. |
| [Windsurf](https://docs.windsurf.com/windsurf/accounts/usage) | bundled | Rate-limited free | Frontier models (via Auto) | Windsurf offers unlimited inline code edits/Tab completions plus a limited starter quota of Cascade agent prompts. Account login required, no credit card required. Advanced frontier routing requires a paid plan. |
| [Qoder](https://docs.qoder.com/account/pricing) | bundled | Rate-limited free | Frontier models + BYO key | Qoder offers free basic code autocompletions and limited Next-Edit-Suggestion (NES) runs. Account login required, no credit card required. Unlimited usage requires bringing your own API keys. |
| [Antigravity CLI (Google)](https://antigravity.google/pricing) | login | Rate-limited free | Gemini 3.8/3.7/3.6 Flash, Gemini 3.1 Pro, Claude Sonnet/Opus 4.6, gpt-oss-120b | Antigravity CLI offers free weekly quotas for terminal and editor agent tasks. Google account login required, no credit card required. Quotas reset weekly; rate limits apply during high-load periods. |
| [Google Colab](https://research.google.com/colaboratory/faq.html) | login | Rate-limited free | Gemini (AI features) + GPU for your code | Google Colab offers free access to shared T4 GPUs and TPUs with 12-hour maximum runtime sessions. Google account required, no credit card required. Compute resources are dynamically allocated and idle sessions disconnect. |
| [Figma (Starter)](https://www.figma.com/pricing/) | bundled | Rate-limited free | Figma AI, Make, agent | Figma Starter offers 150 free AI generation credits/day (up to 500/month). Figma account required, no credit card required. Inference runs bundled inside Figma design files for layer generation and text editing. |
| [Canva (Free)](https://www.canva.com/en/pricing/) | bundled | Rate-limited free | Canva AI, Magic Media | Canva Free offers 20 free AI design uses/month and 50 lifetime Magic Media text-to-image generations. Canva account required, no credit card required. Monthly generation allowance resets on the first of each month. |
| [Framer (Free)](https://www.framer.com/pricing) | bundled | Trial credits | Framer Agents | Framer Free offers 500 one-time AI page generation credits plus a free Framer subdomain. Account login required, no credit card required. Projects are limited to non-commercial personal use. |
| [Replit (Starter)](https://docs.replit.com/help/pricing-and-plans) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Replit Starter offers a limited daily Replit Agent allowance plus free hosting for 1 published app. Replit account required, no credit card required. Container runs sleep after periods of inactivity. |
| [Kilo Gateway](https://kilo.ai/gateway) | api_key | Rate-limited free | cohere/north-mini-code:free, poolside/laguna-s-2.1:free, poolside/laguna-xs-2.1:free, liquid/lfm-2.5-2.6b:free, dots-studio/dots-3-note-preview:free, nvidia/nemotron-3.5-lightning:free, +1 more | Kilo Gateway offers 7 free models with 64K–256K context, translating to 200 requests/hour per IP address. No credit card required. Model availability reflects upstream provider quotas. |
| [Nous Portal](https://portal.nousresearch.com/api-docs) | api_key | Rate-limited free | poolside/laguna-s-2.1:free, poolside/laguna-xs-2.1:free, stepfun/step-3.7-flash:free, upstage/solar-mini4:free, reflection/beam-1.0-501b-a23b:free, ornith/ornith-1.5-122b:free | Nous Portal offers 5 free Hermes and open-weight models, translating to 50 requests/minute and 500,000 tokens/minute. Free account registration required, no credit card required. Preview models may be adjusted during experimental rounds. |
| [Cohere](https://docs.cohere.com/docs/rate-limits) | api_key | Rate-limited free | Command A, Command R+, Command R7B | Cohere offers free trial developer access across 5 models, translating to 1,000 API calls/month (20 requests/minute for Command R+, 2,000 inputs/minute for Embed). No credit card required. Restricted to evaluation and non-production testing. |
| [Requesty](https://www.requesty.ai/pricing) | api_key | Rate-limited free | nvidia/nemotron-3-super-120b-a12b, google/gemma-4-31b-it, poolside/laguna-xs.2 | Requesty offers 3 free models with 128K context, translating to 200 requests/day per account. Email registration required, no credit card required. Quota resets daily at 00:00 UTC. |
| [OVHcloud AI Endpoints](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/) | api_key | Rate-limited free | 10 free models (anonymous keyless) | OVHcloud offers 10 free open-source models, translating to 2 requests/minute per IP keyless (or 400 requests/minute with a registered account). No credit card required for anonymous keyless access. Quota is enforced per client IP. |
| [SiliconFlow](https://siliconflow.cn) | api_key | Rate-limited free | deepseek-ai/DeepSeek-R1-Distill-Qwen-7B, deepseek-ai/DeepSeek-V3, Qwen/Qwen2.5-7B-Instruct, THUDM/glm-4-9b-chat | SiliconFlow offers 4 permanently free models (including DeepSeek-V3 and GLM-4 9B) plus 14M free signup tokens. Account registration required, no credit card required. Platform tokens apply across non-free catalog models until depleted. |
| [DeepSeek Platform](https://api-docs.deepseek.com) | api_key | Trial credits | deepseek-chat, deepseek-reasoner | DeepSeek Platform offers 5M free signup tokens across deepseek-chat and deepseek-reasoner with 64K context. Account registration required, no credit card required. Free token grant expires 30 days after account creation. |
| [TypeSafe AI](https://typesafe.ai/) | api_key | Trial credits | typesafe/jev-1.13 | TypeSafe AI offers $5 free signup credit on Jev 1.13 with 256K context, translating to ~120M input tokens. Account registration required, no credit card required. Credits remain active until depleted. |
| [Braintrust](https://www.braintrust.dev/pricing) | api_key | Trial credits | deepseek-v4.1-flash, deepseek-v4-flash-0731, glm-5.3-flash, glm-5.2, kimi-k3, jev, +7 more | Braintrust offers $10/month recurring model credit on Starter across 13 built-in models (including GPT-6 series, DeepSeek V4.1, GLM-5.3, and Jev). Work email required, no credit card required. Model credit resets monthly with no rollover. |
| [Deepgram](https://deepgram.com/pricing) | api_key | Trial credits | nova-3, nova-2, aura | Deepgram offers $200 free credit across 3 models, translating to ~43,000 minutes (700+ hours) of speech transcription and TTS. Account registration required, no credit card required. Free credits do not expire. |
| [AssemblyAI](https://www.assemblyai.com/pricing) | api_key | Trial credits | universal-1, conformer-2 | AssemblyAI offers $50 free credit across 2 models, translating to ~135 hours of audio transcription and streaming speech-to-text. Account registration required, no credit card required. Free credits do not expire. |
| [Dots Studio](https://dots.ai) | api_key | Trial credits | dots-3-note-preview | Dots Studio offers free trial API credits and inference testing on Dots-3 Note and open-weight models. No credit card required. Trial credits are intended for evaluation and prototype development. |

## Models (per provider)

### OpenCode Zen

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Big Pickle | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |
| GLM-5.3-Flash Free | $0 (promo) | 128K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |
| DeepSeek V4.1 Flash Free | $0 (promo) | 128K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |
| MiMo-V2.6-Flash Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |
| Beam Free | $0 (promo) | 128K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |
| Flint 40B Free | $0 (promo) | 128K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |
| Nemotron 3 Ultra Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |
| Nemotron 3.5 Lightning Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |
| Nemotron 3.5 Super VL Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |
| Jev 1.13 Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |
| Crouton Alpha Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |
| Pulse Alpha Free | $0 (promo) | 256K - 1M | Not published | Not published | Not published | Not published | 2026-11-06 |

### OpenRouter

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cohere/north-mini-code:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| dots-studio/dots-3-note-preview:free | $0 | 500K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| google/gemma-4-26b-a4b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| google/gemma-4-31b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| liquid/lfm-2.5-2.6b:free | $0 | 64K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| nvidia/nemotron-3-ultra-550b-a55b:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| nvidia/nemotron-3.5-content-safety:free | $0 | 125K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| nvidia/nemotron-3.5-lightning:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| nvidia/nemotron-3.5-super-vl:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| recursive/flint-v1.0:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| xingchen-agi/xing4.0-29b-a4b:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |
| meta/muse-spark-1.3-contributor:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-06 |

### Google AI Studio (Gemini API)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gemini-2.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-2.5-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-3-flash-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-3.1-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-3.1-flash-lite-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-3.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-3.5-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-3.6-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-3.7-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-3.8-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-flash-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-flash-lite-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-omni-1.1-flash | $0 | 128K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemini-omni-flash-preview | $0 | 128K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-06 |
| gemma-4-26b-a4b-it | $0 | 256K | 15 | 1M | 1,500 | Not published | 2026-11-06 |
| gemma-4-31b-it | $0 | 256K | 15 | 1M | 1,500 | Not published | 2026-11-06 |

### Groq

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| llama-3.3-70b-versatile | $0 | 128K | 30 | 12K | 1,000 | 100K tokens/day | 2026-11-06 |
| llama-3.1-8b-instant | $0 | 128K | 30 | 6K | 14,400 | 500K tokens/day | 2026-11-06 |
| meta-llama/llama-4-scout-17b-16e-instruct | $0 | 128K | 30 | 30K | 1,000 | 500K tokens/day | 2026-11-06 |
| openai/gpt-oss-120b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-11-06 |
| openai/gpt-oss-20b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-11-06 |
| qwen/qwen3.6-27b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-11-06 |
| qwen/qwen3.8-27b | $0 | 128K | 30 | 8K | 1,000 | 2M tokens/day | 2026-11-06 |
| meta-llama/llama-prompt-guard-2-22m | $0 | 128K | 30 | 15K | 14,400 | 500K tokens/day | 2026-11-06 |
| compound-beta | $0 | 128K | 30 | 70K | 250 | Not published | 2026-11-06 |
| whisper-large-v3-turbo | $0 | 25MB audio | 20 | 7.2K ASH (Audio sec/hr) | 2,000 | 28.8K ASD (8h audio/day) | 2026-11-06 |
| whisper-large-v3 | $0 | 25MB audio | 20 | 7.2K ASH (Audio sec/hr) | 2,000 | 28.8K ASD (8h audio/day) | 2026-11-06 |
| canopylabs/orpheus-v1-english | $0 | Text-to-speech | 10 | 1.2K ASH (Audio sec/hr) | 100 | 3.6K ASD (1h audio/day) | 2026-11-06 |
| canopylabs/orpheus-arabic-saudi | $0 | Text-to-speech | 10 | 1.2K ASH (Audio sec/hr) | 100 | 3.6K ASD (1h audio/day) | 2026-11-06 |

### Cerebras

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gpt-oss-120b | $5 trial credits (30-day, card required) | 8K cap on free tier | 5 | 30K | Not published | 1M tokens/day (per model) | 2026-11-01 |
| qwen-3.8-27b | $5 trial credits (30-day, card required) | 8K cap on free tier | 5 | 30K | Not published | 1M tokens/day (per model) | 2026-11-01 |

### Cloudflare Workers AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings) | $0 | 8K-128K+ (model-dependent) | 300 text gen (720-1,500 other tasks) | Model-dependent | Not published | 10,000 neurons/day | 2026-08-30 |
| @cf/meta/llama-3.3-70b-instruct-fp8-fast | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-10-29 |
| @cf/deepseek-ai/deepseek-r1-distill-qwen-32b | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-10-29 |
| @cf/qwen/qwen2.5-72b-instruct | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-10-29 |
| @cf/meta/llama-3.1-8b-instruct | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-10-29 |
| @cf/openai/whisper | $0 | 25MB audio | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-05 |

### Mistral La Plateforme

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mistral Large | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-10-29 |
| Codestral | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-10-29 |
| All API models (Experiment tier) | $0 (Experiment) | Model-dependent | ~1 req/sec | Not published | Not published | ~1B tokens/month | 2026-10-29 |

### SambaNova Cloud

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DeepSeek-V3.1 | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-11-06 |
| DeepSeek-V3.2 | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-11-06 |
| Meta-Llama-3.3-70B-Instruct | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-11-06 |
| gemma-4-31B-it | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-11-06 |
| gpt-oss-120b | $0 | 128K | 20 | Not published | 20 | 200K tokens/day | 2026-11-06 |

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

### DeepInfra

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-ai/DeepSeek-V3.1 | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-06 |
| Qwen/Qwen3-32B | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-06 |
| Qwen/Qwen2.5-72B-Instruct | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-06 |
| zai-org/GLM-4.7 | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-06 |

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
| cohere/north-mini-code:free | $0 | 250K | 20 | Provider-dependent | 200/day | Not published | 2026-11-06 |
| poolside/laguna-s-2.1:free | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-10-31 |
| poolside/laguna-xs-2.1:free | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-10-31 |
| liquid/lfm-2.5-2.6b:free | $0 | 64K | 20 | Provider-dependent | 200/day | Not published | 2026-11-03 |
| dots-studio/dots-3-note-preview:free | $0 | 500K | 20 | Provider-dependent | 200/day | Not published | 2026-11-06 |
| nvidia/nemotron-3.5-lightning:free | $0 | 1000000 | 20 | Provider-dependent | 200/day | Not published | 2026-11-06 |
| nvidia/nemotron-3.5-super-vl:free | $0 | 1000000 | 20 | Provider-dependent | 200/day | Not published | 2026-11-06 |

### Nous Portal

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| poolside/laguna-s-2.1:free | $0 | 256K | 50 | 500K | Not published | Not published | 2026-10-31 |
| poolside/laguna-xs-2.1:free | $0 | 256K | 50 | 500K | Not published | Not published | 2026-10-31 |
| stepfun/step-3.7-flash:free | $0 | 128K | 50 | 500K | Not published | Not published | 2026-11-06 |
| upstage/solar-mini4:free | $0 | 64K | 50 | 500K | Not published | Not published | 2026-11-06 |
| reflection/beam-1.0-501b-a23b:free | $0 | 128K | 50 | 500K | Not published | Not published | 2026-11-06 |
| ornith/ornith-1.5-122b:free | $0 | 128K | 50 | 500K | Not published | Not published | 2026-11-02 |

### Cohere

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Command A | $0 | 256K | 20 | Not published | Not published | Not published | 2026-11-01 |
| Command R+ | $0 | 128K | 20 | Not published | Not published | Not published | 2026-11-01 |
| Command R7B | $0 | 128K | 20 | Not published | Not published | Not published | 2026-11-01 |

### Requesty

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nvidia/nemotron-3-super-120b-a12b | $0 | 128K | Not published | Not published | 200/day shared | Not published | 2026-11-06 |
| google/gemma-4-31b-it | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-11-06 |
| poolside/laguna-xs.2 | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-11-06 |

### OVHcloud AI Endpoints

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 free models (anonymous keyless) | $0 | Model-dependent | 2/min per IP | Not published | Not published | Not published | 2026-11-06 |

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

### TypeSafe AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| typesafe/jev-1.13 | $0 ($5 signup credits) | 256K | 60 | Not published | Not published | Not published | 2026-11-05 |

### Braintrust

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-v4.1-flash | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |
| deepseek-v4-flash-0731 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |
| glm-5.3-flash | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |
| glm-5.2 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |
| kimi-k3 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |
| jev | $0 ($10/mo model credits) | 256K | Not published | Not published | Not published | Not published | 2026-11-05 |
| gpt-6-luna | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |
| gpt-6-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |
| gpt-6.1-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |
| gpt-6-astra | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |
| gpt-5.6-luna | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |
| gpt-5.6-terra | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |
| gpt-5.6-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-05 |

### Deepgram

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nova-3 | $0 ($200 credit grant) | 43K min audio | 100 | Not published | Not published | 700+ hours grant | 2026-11-05 |
| nova-2 | $0 ($200 credit grant) | 43K min audio | 100 | Not published | Not published | 700+ hours grant | 2026-11-05 |
| aura | $0 ($200 credit grant) | Text-to-speech | 100 | Not published | Not published | $200 credit grant | 2026-11-05 |

### AssemblyAI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| universal-1 | $0 ($50 credit grant) | Pre-recorded &amp; streaming audio | 100 | Not published | Not published | $50 credit grant | 2026-11-05 |
| conformer-2 | $0 ($50 credit grant) | Speech-to-text audio | 100 | Not published | Not published | $50 credit grant | 2026-11-05 |

### Dots Studio

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dots-3-note-preview | $0 (trial) | 128K | 60 | Not published | Not published | Not published | 2026-11-06 |
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
