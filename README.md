# Free Inference

Free AI & LLM inference you can build with: an API key, a CLI login, or inference bundled inside a coding tool or builder. Speech-to-text, voice synthesis, code, vision, and reasoning. The test is whether you can ship an artifact you keep — code, an app, an audio file, a site, a design, an agent, a skill. Chat-only free tiers are excluded on purpose.

> **2026-11-07** · 41 providers · 152 free models
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
| [OpenCode Zen](https://opencode.ai/v2/docs/console/models/) | api_key | Promo free (limited time) | Big Pickle, Iceman Free, Inkling 2 Small Free, Crouton Alpha Free, GLM-5.3-Flash Free, DeepSeek V4.1 Flash Free, +7 more | [The Grant] OpenCode Zen provides a collection of zero-cost promotional and experimental models. [The Output] Users gain access to free tier inference across multiple models including text and vision variants. [The Process] Models are evaluated and identified via catalog audits and pricing data verification. [The Condition] Availability is subject to limited-time promotional windows, zero-data-retention policies, and user feedback collection requirements. |
| [OpenRouter](https://openrouter.ai/models?max_price=0) | api_key | Rate-limited free | cohere/north-mini-code:free, dots-studio/dots-3-note-preview:free, google/gemma-4-26b-a4b-it:free, google/gemma-4-31b-it:free, liquid/lfm-2.5-2.6b:free, liquid/lfm-3-1.7b:free, +7 more | OpenRouter offers 13 permanently free models (:free suffix) with 64K–500K context, translating to 50 requests/day (1,000 requests/day with + purchased credits). No credit card required. Upstream model availability determines live rate limits. |
| [Google AI Studio (Gemini API)](https://ai.google.dev/gemini-api/docs/rate-limits) | api_key | Rate-limited free | gemini-2.5-flash, gemini-2.5-flash-lite, gemini-3-flash-preview, gemini-3.1-flash-lite, gemini-3.1-flash-lite-preview, gemini-3.5-flash, +10 more | Google AI Studio offers 16 free models with up to 1M context, translating to 15–30 requests/minute (up to 1,500 requests/day per model). No credit card required. Free-tier prompts and outputs are retained for model training. |
| [Groq](https://console.groq.com/docs/rate-limits) | api_key | Rate-limited free | llama-3.3-70b-versatile, llama-3.1-8b-instant, meta-llama/llama-4-scout-17b-16e-instruct, openai/gpt-oss-120b, openai/gpt-oss-20b, qwen/qwen3.6-27b, +7 more | Groq offers 13 free models (9 LLMs, 2 Whisper STT, 2 Orpheus TTS), translating to up to 14,400 text requests/day and 2,000 audio transcriptions/day (~8 hours/day). No credit card required. Limits are pooled at organization level. |
| [Cerebras](https://inference-docs.cerebras.ai/support/rate-limits) | api_key | Trial credits | gpt-oss-120b, qwen-3.8-27b | Cerebras offers $5 trial credit across 2 models (gpt-oss-120b, qwen-3.8-27b with 8K context cap), translating to 1M tokens/day at 2,000+ tokens/sec. Credit card required. Trial credits expire in 30 days. |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/limits) | api_key | Rate-limited free | ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings), @cf/meta/llama-3.3-70b-instruct-fp8-fast, @cf/deepseek-ai/deepseek-r1-distill-qwen-32b, @cf/qwen/qwen2.5-72b-instruct, @cf/meta/llama-3.1-8b-instruct, @cf/openai/whisper | Cloudflare Workers AI offers ~80 free models (including Llama 3.3 70B, DeepSeek-R1 distills, Whisper, and FLUX), translating to 10,000 neurons/day (~hundreds of queries or audio minutes). No credit card required. Hard stop at 10,000 neurons until 00:00 UTC daily reset. |
| [Mistral La Plateforme](https://docs.mistral.ai) | api_key | Rate-limited free | mistral-tiny | Mistral provides a free tier for developers to evaluate models. The output includes access to select baseline models via API. The process involves signing up for La Plateforme and utilizing default rate limits. The condition requires compliance with terms of service and staying within specified usage thresholds. |
| [NVIDIA NIM (build.nvidia.com)](https://build.nvidia.com) | api_key | Trial credits | GLM-5, Kimi-2.5, NIM-packaged open models | NVIDIA NIM offers 1,000 free trial credits across catalog models (including Nemotron 3.5 Lightning with 1M context), translating to ~40 hours of inference testing. No credit card required; corporate email required for extended credits. Credits tie to a 90-day evaluation window. |
| [DeepInfra](https://docs.deepinfra.com/account/rate-limits) | api_key | Trial credits | deepseek-ai/DeepSeek-V3.1, Qwen/Qwen3-32B, Qwen/Qwen2.5-72B-Instruct, zai-org/GLM-4.7 | DeepInfra offers $5 signup trial credit across 185+ models (including DeepSeek-V3.1, Qwen 3 32B, and GLM-4.7), translating to ~50M tokens at 200 concurrent requests. No credit card required. Credits remain active until depleted. |
| [GitHub Copilot (Free)](https://github.com/features/copilot) | login | Rate-limited free | Auto-selected (GPT-5 mini, Claude Haiku/Sonnet, Gemini Flash line) | GitHub provides Copilot Free with limited features for individual developers to try AI-powered coding assistance. The system delivers restricted agent access and limited AI credit allowances alongside Copilot Chat on GitHub.com and mobile. The implementation uses automated web data extraction, HTML table parsing, and policy analysis scripts via bash. Users receive free access subject to specific AI model availability constraints and organization or enterprise policy governance. |
| [Kiro (AWS)](https://kiro.dev/pricing) | login | Rate-limited free | Qwen3 Coder Next, DeepSeek 3.2, MiniMax M2.1, Claude Sonnet 4.5 | Kiro offers 50 free credits/month for spec-driven agent workflows. Social account or AWS Builder ID required, no credit card required. Unused credits do not roll over to the next month. |
| [Trae (ByteDance)](https://www.trae.ai/pricing) | bundled | Trial credits | Frontier models (bundled, auto-selected) | Trae offers free inference. The free allowance includes 5,000 monthly autocompletions and a one-time $3 usage allowance. Usage is renewed monthly, and the credits are valid for 90 days. The free tier requires no credit card. |
| [Bolt.new](https://support.bolt.new/account-and-subscription/tokens) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Bolt offers 1,000,000 tokens per month with a 300,000 daily token cap, translating to bundled frontier model inference for full-stack web and code generation via the Standard agent alongside hosting for up to 333k requests. No credit card required to sign up. Daily tokens reset every 24 hours without rollover, monthly quotas reset on the 1st of each calendar month, and free plan tokens do not roll over. |
| [Lovable](https://docs.lovable.dev/introduction/credits-and-usage) | bundled | Rate-limited free | Fable 5.1 (Frontier model) | 1. The Grant: Lovable provides a rate-limited free tier for users building and iterating on applications. 2. The Output: Users get access to bundled frontier models including Fable 5.1 without direct financial cost. 3. The Process: Usage is governed by credits and rate limits determined by the platform's current policy. 4. The Condition: Availability and rate limits are subject to change as outlined in the official documentation. |
| [v0 (Vercel)](https://v0.app/docs/pricing) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | v0 offers a free plan granting 7 messages per day with bundled frontier models, plus a one-time $5 credit bonus for new accounts. Translates to 7 full-stack code and UI generations daily (~210 requests per month). No credit card required to sign up and build. Quotas reset daily at 00:00 UTC with no rollover, and custom model selection is restricted to paid plans. |
| [Kaggle Notebooks](https://www.kaggle.com/docs/efficient-gpu-usage) | login | Rate-limited free | Open-weight models you load (GPU runtime) | Kaggle offers 30 hours of free GPU accelerator quota (NVIDIA T4 x2 / P100) and 20 hours of TPU v3-8 compute per week, translating to running self-hosted open-weight model inference and fine-tuning across sessions lasting up to 12 hours. Phone verification is required to unlock accelerators and internet access; no credit card required. Compute quota resets weekly, and interactive sessions terminate after 20 to 60 minutes of idle time. |
| [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces-overview) | login | Rate-limited free | Any Hugging Face model you load (ZeroGPU) | Hugging Face Spaces offers free hosting for up to 2 ZeroGPU Gradio spaces with dynamic GPU allocation. Free account required, no credit card required. Persistent storage and dedicated hardware require a Pro tier. |
| [Cursor (Hobby)](https://cursor.com/pricing) | bundled | Rate-limited free | Composer 2, Composer 2.5, Grok 4.5, Grok 4.6, Grok 4.7 | [The Grant] Cursor provides access to bundled internal models like Composer 2 and Grok variants on the Hobby/Free tier. [The Output] Users receive rate-limited access to these bundled models without direct monetary charges. [The Process] The system evaluates user plan tiers and applies automatic rate limits to free tier requests. [The Condition] This access remains active as long as usage stays within the specified free tier rate limits and legacy or current hobby plan parameters. |
| [Windsurf](https://docs.windsurf.com/windsurf/accounts/usage) | bundled | Rate-limited free | Standard Models | Windsurf provides a free tier. Users receive a set amount of usage and standard features at no cost. The free tier operates on a rate-limited basis. Usage allowances reset periodically under standard usage conditions. |
| [Devin (Free)](https://devin.ai/pricing) | bundled | Rate-limited free | SWE-2 (Free), Limited models (auto-selected) | Devin offers a Free plan with a light quota to code with agents, free use of SWE-2, unlimited inline edits, and unlimited Tab completions. Account login required, no credit card required. Runs bundled inside the Devin interface on SWE-2 and limited models. |
| [Qoder](https://docs.qoder.com/account/pricing) | bundled | Rate-limited free | Frontier models + BYO key | Qoder offers free basic code autocompletions and limited Next-Edit-Suggestion (NES) runs. Account login required, no credit card required. Unlimited usage requires bringing your own API keys. |
| [Antigravity CLI (Google)](https://antigravity.google/pricing) | login | Rate-limited free | Gemini 3.8 Flash, Gemini 3.7 Flash, Gemini 3.6 Flash, Gemini 3.1 Pro | The free tier provides access to select base models for general inference. The output consists of standard text, code, and basic multimodal completions. The process requires standard user authentication via the Antigravity CLI without requiring payment instrument setup. The condition is subject to dynamic rate limits and potential feature restrictions across modalities. |
| [Google Colab](https://research.google.com/colaboratory/faq.html) | login | Rate-limited free | Gemini (AI features) + GPU for your code | Google Colab offers free access to hosted Jupyter notebook compute resources including shared GPUs/TPUs and integrated Gemini AI coding features, translating to interactive execution sessions of up to 12 hours with standard system memory. Google account login required (age 18+ for AI features), no credit card required. Resources and rate limits fluctuate dynamically, idle runtimes disconnect, and non-interactive background execution is disallowed. |
| [Figma (Starter)](https://www.figma.com/pricing/) | bundled | Rate-limited free | Figma AI, Make, agent | Figma Starter offers 150 free AI generation credits/day (up to 500/month). Figma account required, no credit card required. Inference runs bundled inside Figma design files for layer generation and text editing. |
| [Canva (Free)](https://www.canva.com/en/pricing/) | bundled | Rate-limited free | Canva AI, Magic Media | Free users are granted an allowance of 20 uses of standard or premium AI tools. The system outputs access to bundled models like Canva AI and Magic Media. The process enforces monthly limits on tools such as Magic Write, consuming a shared allowance. The condition strictly restricts free users from accessing ultra tools like Canva AI 2.0. |
| [Framer (Free)](https://www.framer.com/pricing) | bundled | Trial credits | Framer Agents | Framer offers 500 one-time AI trial credits on its Free plan for workspaces without active subscriptions to power Framer Agents, translating to approximately 1 to 3 page generation or design sessions. No credit card is required to sign up and use the free plan. Credits are a one-time trial allotment that does not reset monthly, and agent features pause once the credits are exhausted unless upgraded to a paid plan. |
| [Replit (Starter)](https://docs.replit.com/help/pricing-and-plans) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Starter tier grants access to basic development tools. The output includes standard cloud developer workspace capabilities. The process involves creating a free Replit account to immediately provision basic resources. The condition requires operating within standard resource limits and usage policies. |
| [Kilo Gateway](https://kilo.ai/gateway) | api_key | Rate-limited free | cohere/north-mini-code:free, poolside/laguna-s-2.1:free, poolside/laguna-xs-2.1:free, liquid/lfm-2.5-2.6b:free, dots-studio/dots-3-note-preview:free, nvidia/nemotron-3.5-lightning:free, +1 more | Confirmed active free tier with listed models |
| [Cohere](https://docs.cohere.com/docs/rate-limits) | api_key | Rate-limited free | Command A+, Command A Reasoning, Command R+, Command R, Command R7B | Cohere provides trial API keys [The Grant] allowing access to chat and embedding models [The Output] by registering an account and utilizing trial keys [The Process] subject to trial rate limits such as 20 requests per minute and 1,000 API calls per month [The Condition]. |
| [Requesty](https://www.requesty.ai/pricing) | api_key | Rate-limited free | nvidia/nemotron-3-super-120b-a12b, google/gemma-4-31b-it, poolside/laguna-xs.2 | Requesty offers 3 free models with 128K context, translating to 200 requests/day per account. Email registration required, no credit card required. Quota resets daily at 00:00 UTC. |
| [OVHcloud AI Endpoints](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/) | api_key | Rate-limited free | 10 free models (anonymous keyless) | OVHcloud offers 10 free open-source models, translating to 2 requests/minute per IP keyless (or 400 requests/minute with a registered account). No credit card required for anonymous keyless access. Quota is enforced per client IP. |
| [SiliconFlow](https://siliconflow.cn) | api_key | Trial credits | Speech models (unspecified) | The Grant: $200 in credits is provided.
The Output: Credits can be used for speech models.
The Process: Access is granted without credit card requirement.
The Condition: Credits are valid for 90 days. |
| [DeepSeek Platform](https://api-docs.deepseek.com) | api_key | Trial credits | deepseek-chat, deepseek-reasoner | The Grant: DeepSeek offers a granted balance upon account creation. The Output: Users can access API services without immediate paid top-ups. The Process: The platform automatically prioritizes using the granted balance first when both balances are available. The Condition: This applies until the granted balance is exhausted or expires, after which accounts rely on the topped-up balance. |
| [Braintrust](https://www.braintrust.dev/pricing) | api_key | Trial credits | deepseek-v4.1-flash, deepseek-v4-flash-0731, glm-5.3-flash, glm-5.2, kimi-k3, jev, +7 more | Braintrust offers $10/month recurring model credit on Starter across 13 built-in models (including GPT-6 series, DeepSeek V4.1, GLM-5.3, and Jev). Work email required, no credit card required. Model credit resets monthly with no rollover. |
| [Deepgram](https://deepgram.com/pricing) | api_key | Trial credits | nova-3, nova-2, flux, aura | [The Grant] Deepgram provides $200 in free trial credits upon sign-up. [The Output] Users gain access to public speech-to-text and text-to-speech models including Nova-3, Nova-2, Flux, and Aura. [The Process] Users register for a Pay-As-You-Go account to receive the API key and access the platform. [The Condition] The credit allows for approximately 700 hours of Nova-3 transcription, subject to standard concurrency limits for pre-recorded and streaming requests. |
| [AssemblyAI](https://www.assemblyai.com/pricing) | api_key | Trial credits | Unknown | New accounts receive $50 in credits, valid for 90 days, usable across four speech models, and requiring no credit card. |
| [Dots Studio](https://dots.ai) | api_key | Trial credits | dots-3-note-preview | - The Grant: Users receive a trial credit system accessible via an API key.
- The Output: A single available model named "dots-3-note-preview" is provided in the catalog.
- The Process: Investigation of JavaScript bundles, API parameters, and documentation revealed context limits and model naming structures.
- The Condition: Total input and output token sum cannot exceed the 524,288 token context window limit. |
| [Liquid AI](https://console.liquid.ai) | api_key | Trial credits | Liquid AI Free Model | 1. Liquid AI offers free promotional API credits to new developers upon console signup. 2. The output provides access to evaluate their models via the developer console and API. 3. The process requires creating an account on console.liquid.ai to claim the promotional allocation. 4. The condition is subject to promotional limits and potential expiration once the initial credit balance is exhausted. |
| [SambaNova Cloud](https://cloud.sambanova.ai/apis) | api_key | Trial credits | Meta-Llama-3.3-70B-Instruct, DeepSeek-V3.1 | SambaNova Cloud provides initial trial credits upon account creation. Users can access production and preview models through an API key using these credits. The platform features pay-as-you-go credit systems alongside standard and free tier rate limits. Access is subject to community support guidelines and specific developer tier restrictions. |
| [Z.AI (Zhipu)](https://z.ai) | api_key | Rate-limited free | GLM-5.1, GLM-4.5-Flash, GLM-4.7-Flash, GLM-4.6V-Flash (vision) | Z.AI offers free API access to GLM-5.1, GLM-4.7-Flash, and GLM-4.6V-Flash with 128K context, translating to 15 requests/minute. No credit card required. Shared free tier throttles during peak platform traffic hours. |
| [Nous Portal](https://portal.nousresearch.com/api-docs) | api_key | Rate-limited free | poolside/laguna-s-2.1:free, poolside/laguna-xs-2.1:free, stepfun/step-3.7-flash:free, upstage/solar-mini4:free, reflection/beam-1.0-501b-a23b:free, ornith/ornith-1.5-122b:free | Nous Portal offers 5 free Hermes and open-weight models, translating to 50 requests/minute and 500,000 tokens/minute. Free account registration required, no credit card required. Preview models may be adjusted during experimental rounds. |

## Models (per provider)

### OpenCode Zen

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Big Pickle | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| Iceman Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| Inkling 2 Small Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| Crouton Alpha Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| GLM-5.3-Flash Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| DeepSeek V4.1 Flash Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| Beam Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| Flint 40B Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| MiMo-V2.6-Flash Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| Nemotron 3 Ultra Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| Nemotron 3.5 Lightning Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| Nemotron 3.5 Super VL Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |
| Jev 1.13 Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-07 |

### OpenRouter

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cohere/north-mini-code:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| dots-studio/dots-3-note-preview:free | $0 | 500K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| google/gemma-4-26b-a4b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| google/gemma-4-31b-it:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| liquid/lfm-2.5-2.6b:free | $0 | 64K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| liquid/lfm-3-1.7b:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | $0 | 250K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| nvidia/nemotron-3-ultra-550b-a55b:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| nvidia/nemotron-3.5-lightning:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| nvidia/nemotron-3.5-super-vl:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| recursive/flint-v1.0:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| xingchen-agi/xing4.0-29b-a4b:free | $0 | 256K | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |
| meta/muse-spark-1.3-contributor:free | $0 | 1000000 | 20 | Provider-dependent | 50 (below $10 credits) / 1,000 ($10+ credits) | Not published | 2026-11-07 |

### Google AI Studio (Gemini API)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gemini-2.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-2.5-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-3-flash-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-3.1-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-3.1-flash-lite-preview | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-3.5-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-3.5-flash-lite | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-3.6-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-3.7-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-3.8-flash | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-flash-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-flash-lite-latest | $0 | 1024K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-omni-1.1-flash | $0 | 128K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemini-omni-flash-preview | $0 | 128K | Varies by account | Varies by account | Varies by account | Not published | 2026-11-07 |
| gemma-4-26b-a4b-it | $0 | 256K | 15 | 1M | 1,500 | Not published | 2026-11-07 |
| gemma-4-31b-it | $0 | 256K | 15 | 1M | 1,500 | Not published | 2026-11-07 |

### Groq

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| llama-3.3-70b-versatile | $0 | 128K | 30 | 12K | 1,000 | 100K tokens/day | 2026-11-07 |
| llama-3.1-8b-instant | $0 | 128K | 30 | 6K | 14,400 | 500K tokens/day | 2026-11-07 |
| meta-llama/llama-4-scout-17b-16e-instruct | $0 | 128K | 30 | 30K | 1,000 | 500K tokens/day | 2026-11-07 |
| openai/gpt-oss-120b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-11-07 |
| openai/gpt-oss-20b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-11-07 |
| qwen/qwen3.6-27b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-11-07 |
| qwen/qwen3.8-27b | $0 | 128K | 30 | 8K | 1,000 | 2M tokens/day | 2026-11-07 |
| meta-llama/llama-prompt-guard-2-22m | $0 | 128K | 30 | 15K | 14,400 | 500K tokens/day | 2026-11-07 |
| compound-beta | $0 | 128K | 30 | 70K | 250 | Not published | 2026-11-07 |
| whisper-large-v3-turbo | $0 | 25MB audio | 20 | 7.2K ASH (Audio sec/hr) | 2,000 | 28.8K ASD (8h audio/day) | 2026-11-07 |
| whisper-large-v3 | $0 | 25MB audio | 20 | 7.2K ASH (Audio sec/hr) | 2,000 | 28.8K ASD (8h audio/day) | 2026-11-07 |
| canopylabs/orpheus-v1-english | $0 | Text-to-speech | 10 | 1.2K ASH (Audio sec/hr) | 100 | 3.6K ASD (1h audio/day) | 2026-11-07 |
| canopylabs/orpheus-arabic-saudi | $0 | Text-to-speech | 10 | 1.2K ASH (Audio sec/hr) | 100 | 3.6K ASD (1h audio/day) | 2026-11-07 |

### Cerebras

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gpt-oss-120b | $5 trial credits (30-day, card required) | 8K cap on free tier | 5 | 30K | Not published | 1M tokens/day (per model) | 2026-11-07 |
| qwen-3.8-27b | $5 trial credits (30-day, card required) | 8K cap on free tier | 5 | 30K | Not published | 1M tokens/day (per model) | 2026-11-07 |

### Cloudflare Workers AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings) | $0 | 8K-128K+ (model-dependent) | 300 text gen (720-1,500 other tasks) | Model-dependent | Not published | 10,000 neurons/day | 2026-11-07 |
| @cf/meta/llama-3.3-70b-instruct-fp8-fast | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-07 |
| @cf/deepseek-ai/deepseek-r1-distill-qwen-32b | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-07 |
| @cf/qwen/qwen2.5-72b-instruct | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-07 |
| @cf/meta/llama-3.1-8b-instruct | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-07 |
| @cf/openai/whisper | $0 | 25MB audio | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-07 |

### Mistral La Plateforme

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mistral-tiny | $0 | 32k | Not specified | Not specified | Not specified | Not specified | 2026-11-06 |

### NVIDIA NIM (build.nvidia.com)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-5 | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-07 |
| Kimi-2.5 | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-07 |
| NIM-packaged open models | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-07 |

### DeepInfra

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-ai/DeepSeek-V3.1 | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-07 |
| Qwen/Qwen3-32B | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-07 |
| Qwen/Qwen2.5-72B-Instruct | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-07 |
| zai-org/GLM-4.7 | $0 (trial credits) | Model-dependent | ~60 (varies by model) | Not published | Not published | $5 signup credits | 2026-11-07 |

### GitHub Copilot (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Auto-selected (GPT-5 mini, Claude Haiku/Sonnet, Gemini Flash line) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-07 |

### Kiro (AWS)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3 Coder Next | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-07 |
| DeepSeek 3.2 | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-07 |
| MiniMax M2.1 | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-07 |
| Claude Sonnet 4.5 | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-07 |

### Trae (ByteDance)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-07 |

### Bolt.new

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Dynamic project context | Unspecified | Unspecified | Unspecified | 300,000 tokens/day (1,000,000 tokens/month) | 2026-11-07 |

### Lovable

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fable 5.1 (Frontier model) | $0 | Not specified | Not specified | Not specified | Not specified | Not specified | 2026-11-07 |

### v0 (Vercel)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Text, code, and image/file input | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-07 |

### Kaggle Notebooks

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Open-weight models you load (GPU runtime) | $0 | Model-dependent (16 GB P100 / 2x16 GB T4 VRAM, 29 GB RAM) | N/A | N/A | N/A | 30 GPU hours/week (resets weekly) | 2026-11-07 |

### Hugging Face Spaces

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Any Hugging Face model you load (ZeroGPU) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-07 |

### Cursor (Hobby)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Composer 2 | $0 | unknown | unknown | unknown | unknown | unknown | 2026-11-07 |
| Composer 2.5 | $0 | unknown | unknown | unknown | unknown | unknown | 2026-11-07 |
| Grok 4.5 | $0 | unknown | unknown | unknown | unknown | unknown | 2026-11-07 |
| Grok 4.6 | $0 | unknown | unknown | unknown | unknown | unknown | 2026-11-07 |
| Grok 4.7 | $0 | unknown | unknown | unknown | unknown | unknown | 2026-11-07 |

### Windsurf

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Standard Models | $0 | Standard | Not specified | Not specified | Not specified | Not specified | 2026-11-07 |

### Devin (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWE-2 (Free) | $0 | Not published | Light quota | Not published | Not published | Not published | 2026-11-07 |
| Limited models (auto-selected) | $0 | Not published | Light quota | Not published | Not published | Not published | 2026-11-07 |

### Qoder

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models + BYO key | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-07 |

### Antigravity CLI (Google)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini 3.8 Flash | $0 | Standard | N/A | N/A | N/A | N/A | 2026-11-07 |
| Gemini 3.7 Flash | $0 | Standard | N/A | N/A | N/A | N/A | 2026-11-07 |
| Gemini 3.6 Flash | $0 | Standard | N/A | N/A | N/A | N/A | 2026-11-07 |
| Gemini 3.1 Pro | $0 | Standard | N/A | N/A | N/A | N/A | 2026-11-07 |

### Google Colab

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini (AI features) + GPU for your code | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-07 |

### Figma (Starter)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Figma AI, Make, agent | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-07 |

### Canva (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Canva AI | $0 | unknown | unknown | unknown | 20 uses (monthly shared limit) | unknown | 2026-11-07 |
| Magic Media | $0 | unknown | unknown | unknown | 20 uses (monthly shared limit) | unknown | 2026-11-07 |

### Framer (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Framer Agents | $0 | Canvas-native web design, layout, styling, CMS, and copy generation | Not specified | Not specified | Not specified | 500 credits (one-time trial) | 2026-11-07 |

### Replit (Starter)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-07 |

### Kilo Gateway

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cohere/north-mini-code:free | $0 | 250K | 20 | Provider-dependent | 200/day | Not published | 2026-11-07 |
| poolside/laguna-s-2.1:free | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-11-07 |
| poolside/laguna-xs-2.1:free | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-11-07 |
| liquid/lfm-2.5-2.6b:free | $0 | 64K | 20 | Provider-dependent | 200/day | Not published | 2026-11-07 |
| dots-studio/dots-3-note-preview:free | $0 | 500K | 20 | Provider-dependent | 200/day | Not published | 2026-11-07 |
| nvidia/nemotron-3.5-lightning:free | $0 | 1000000 | 20 | Provider-dependent | 200/day | Not published | 2026-11-07 |
| nvidia/nemotron-3.5-super-vl:free | $0 | 1000000 | 20 | Provider-dependent | 200/day | Not published | 2026-11-07 |

### Cohere

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Command A+ | $0 | N/A | 20 | N/A | N/A | N/A | 2026-11-07 |
| Command A Reasoning | $0 | N/A | 20 | N/A | N/A | N/A | 2026-11-07 |
| Command R+ | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-07 |
| Command R | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-07 |
| Command R7B | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-07 |

### Requesty

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nvidia/nemotron-3-super-120b-a12b | $0 | 128K | Not published | Not published | 200/day shared | Not published | 2026-11-07 |
| google/gemma-4-31b-it | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-11-07 |
| poolside/laguna-xs.2 | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-11-07 |

### OVHcloud AI Endpoints

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 free models (anonymous keyless) | $0 | Model-dependent | 2/min per IP | Not published | Not published | Not published | 2026-11-07 |

### SiliconFlow

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Speech models (unspecified) | $0 | 43,000 minutes or 700+ hours | N/A | N/A | N/A | N/A | 2026-11-07 |

### DeepSeek Platform

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-chat | $0 (5M signup tokens) | 64K | 60 | Not published | Not published | 5M tokens grant | 2026-11-07 |
| deepseek-reasoner | $0 (5M signup tokens) | 64K | 60 | Not published | Not published | 5M tokens grant | 2026-11-07 |

### Braintrust

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-v4.1-flash | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |
| deepseek-v4-flash-0731 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |
| glm-5.3-flash | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |
| glm-5.2 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |
| kimi-k3 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |
| jev | $0 ($10/mo model credits) | 256K | Not published | Not published | Not published | Not published | 2026-11-07 |
| gpt-6-luna | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |
| gpt-6-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |
| gpt-6.1-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |
| gpt-6-astra | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |
| gpt-5.6-luna | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |
| gpt-5.6-terra | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |
| gpt-5.6-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-07 |

### Deepgram

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nova-3 | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-07 |
| nova-2 | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-07 |
| flux | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-07 |
| aura | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-07 |

### AssemblyAI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Unknown | $0 | Unknown | Unknown | Unknown | Unknown | 43000 minutes | 2026-11-07 |

### Dots Studio

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dots-3-note-preview | $0 | 524288 | N/A | N/A | N/A | N/A | 2026-11-07 |

### Liquid AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquid AI Free Model | $0 (trial) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-07 |

### SambaNova Cloud

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Meta-Llama-3.3-70B-Instruct | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-07 |
| DeepSeek-V3.1 | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-06 |

### Z.AI (Zhipu)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-5.1 | $0 | Up to 203K | 3 (burst) | Not published | 1,000 (1K RPD tier) | Not published | 2026-10-29 |
| GLM-4.5-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-10-29 |
| GLM-4.7-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-10-29 |
| GLM-4.6V-Flash (vision) | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-10-29 |

### Nous Portal

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| poolside/laguna-s-2.1:free | $0 | 256K | 50 | 500K | Not published | Not published | 2026-10-31 |
| poolside/laguna-xs-2.1:free | $0 | 256K | 50 | 500K | Not published | Not published | 2026-10-31 |
| stepfun/step-3.7-flash:free | $0 | 128K | 50 | 500K | Not published | Not published | 2026-11-07 |
| upstage/solar-mini4:free | $0 | 64K | 50 | 500K | Not published | Not published | 2026-11-07 |
| reflection/beam-1.0-501b-a23b:free | $0 | 128K | 50 | 500K | Not published | Not published | 2026-11-07 |
| ornith/ornith-1.5-122b:free | $0 | 128K | 50 | 500K | Not published | Not published | 2026-11-02 |
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
