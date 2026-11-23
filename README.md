# Free Inference

Free AI & LLM inference you can build with: an API key, a CLI login, or inference bundled inside a coding tool or builder. Speech-to-text, voice synthesis, code, vision, and reasoning. The test is whether you can ship an artifact you keep — code, an app, an audio file, a site, a design, an agent, a skill. Chat-only free tiers are excluded on purpose.

> **2026-11-23** · 50 providers · 355 models
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
| [Synap by Linkrra](https://synap402.com/ai/account.html) | api_key | Rate-limited free | qwen3-coder-30b | Synap provides a no-card free tier for qwen3-coder-30b through an OpenAI-compatible API. Google or email sign-in grants 100,000 tokens and 50 requests per day, with a 10 requests/minute per-key limit. Prompts and completions are not stored or used for training. Allowances reset daily at 00:00 UTC and are limited per account and network address. |
| [OpenCode (Free)](https://opencode.ai/pricing) | bundled | Rate-limited free | Big Pickle, Iceman Free, Inkling 2 Small Free, Crouton Alpha Free, GLM-5.3-Flash Free, DeepSeek V4.1 Flash Free, +11 more | OpenCode provides built-in free tier inference across open models directly within the OpenCode CLI and editor. Users authenticate via client login without entering a payment method or adding console credits. Access is subject to client rate limits. |
| [OpenRouter](https://openrouter.ai/models?max_price=0) | api_key | Rate-limited free | inclusionai/ling-3.2-flash:free, baidu/ernie-5.5-flash-preview:free, liquid/lfm-3-1.7b:free, particle-ai/particle-1:free, recursive/flint-v1.0:free, nvidia/nemotron-3.5-super-vl:free, +6 more | OpenRouter offers 13 permanently free models (:free suffix) with 64K–500K context, translating to 50 requests/day (1,000 requests/day with + purchased credits). No credit card required. Upstream model availability determines live rate limits. |
| [Google AI Studio (Gemini API)](https://ai.google.dev/gemini-api/docs/rate-limits) | api_key | Rate-limited free | gemini-3.5-flash-lite, gemini-3.1-flash-lite, gemma-4-26b-a4b-it, gemma-4-31b-it, gemini-3.5-flash, gemini-3-flash-preview, +15 more | Google AI Studio offers 16 free models with up to 1M context. Flagship light models (Gemini 3.5 Flash-Lite, 3.1 Flash-Lite) offer 500 RPD, 15 RPM, and 250K TPM, while open-weight Gemma 4 models (26B, 31B) provide 14.4K RPD, 30 RPM, and 16K TPM. No credit card required. Free-tier prompts and outputs are retained for model training. |
| [Groq](https://console.groq.com/docs/rate-limits) | api_key | Rate-limited free | llama-3.3-70b-versatile, llama-3.1-8b-instant, meta-llama/llama-4-scout-17b-16e-instruct, openai/gpt-oss-120b, openai/gpt-oss-20b, qwen/qwen3.6-27b, +9 more | Groq offers 13 free models (9 LLMs, 2 Whisper STT, 2 Orpheus TTS), translating to up to 14,400 text requests/day and 2,000 audio transcriptions/day (~8 hours/day). No credit card required. Limits are pooled at organization level. |
| [Cerebras](https://inference-docs.cerebras.ai/support/rate-limits) | api_key | Trial credits | gpt-oss-120b, qwen-3.8-27b | Cerebras offers $5 trial credit across 2 models (gpt-oss-120b, qwen-3.8-27b with 8K context cap), translating to 1M tokens/day at 2,000+ tokens/sec. Credit card required. Trial credits expire in 30 days. |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/limits) | api_key | Rate-limited free | ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings), @cf/meta/llama-3.3-70b-instruct-fp8-fast, @cf/deepseek-ai/deepseek-r1-distill-qwen-32b, @cf/qwen/qwen2.5-72b-instruct, @cf/meta/llama-3.1-8b-instruct, @cf/openai/whisper | Cloudflare Workers AI is Generally Available with ~80 free models (including Llama 3.3 70B, DeepSeek-R1 distills, Whisper, and FLUX), translating to 10,000 neurons/day (~hundreds of queries or audio minutes). No credit card required. Hard stop at 10,000 neurons until 00:00 UTC daily reset. |
| [Mistral La Plateforme](https://docs.mistral.ai) | api_key | Rate-limited free | mistral-small-latest, codestral-latest, open-mistral-nemo | Mistral provides a rate-limited free tier on La Plateforme for developers evaluating frontier and open models. Access is available via direct API key upon account registration with no credit card required upfront. Usage is bounded by default platform rate limits and standard evaluation terms of service. |
| [SambaNova Cloud](https://cloud.sambanova.ai/apis) | api_key | Trial credits | Meta-Llama-3.3-70B-Instruct | SambaNova Cloud provides a free developer tier with initial pay-as-you-go exploratory credits for ultra-fast SN40L inference. Developers access production open-weights models including Llama 3.3 70B via an OpenAI-compatible endpoint. API keys are generated directly in the developer portal with no credit card required, subject to platform concurrency caps. |
| [NVIDIA NIM (build.nvidia.com)](https://build.nvidia.com) | api_key | Trial credits | GLM-5, Kimi-2.5, NIM-packaged open models, MiniMax-M3.1-Flash, Whisper Large v3, GPT OSS 20B, +34 more | NVIDIA NIM offers 1,000 free trial credits across catalog models (including Nemotron 3.5 Lightning with 1M context), translating to ~40 hours of inference testing. No credit card required; corporate email required for extended credits. Credits tie to a 90-day evaluation window. |
| [Z.AI (Zhipu)](https://z.ai) | api_key | Rate-limited free | GLM-5.1, GLM-4.5-Flash, GLM-4.7-Flash, GLM-4.6V-Flash (vision), GLM-4.6V-Flash | Z.AI offers free API access to GLM-5.1, GLM-4.7-Flash, and GLM-4.6V-Flash with 128K context, translating to 15 requests/minute. No credit card required. Shared free tier throttles during peak platform traffic hours. |
| [DeepInfra](https://docs.deepinfra.com/account/rate-limits) | api_key | Trial credits | deepseek-ai/DeepSeek-V3.1, Qwen/Qwen3-32B, Qwen/Qwen2.5-72B-Instruct, zai-org/GLM-4.7 | DeepInfra offers $5 signup trial credit across 185+ models (including DeepSeek-V3.1, Qwen 3 32B, and GLM-4.7), translating to ~50M tokens at 200 concurrent requests. No credit card required. Credits remain active until depleted. |
| [GitHub Copilot (Free)](https://github.com/features/copilot) | login | Rate-limited free | Auto-selected (GPT-5 mini, Claude Haiku/Sonnet, Gemini Flash line) | GitHub provides Copilot Free with limited features for individual developers to try AI-powered coding assistance. The system delivers restricted agent access and limited AI credit allowances alongside Copilot Chat on GitHub.com and mobile. The implementation uses automated web data extraction, HTML table parsing, and policy analysis scripts via bash. Users receive free access subject to specific AI model availability constraints and organization or enterprise policy governance. |
| [Kiro (AWS)](https://kiro.dev/pricing) | login | Rate-limited free | Qwen3 Coder Next, DeepSeek 3.2, MiniMax M2.1, Claude Sonnet 4.5 | Kiro offers 50 free credits/month for spec-driven agent workflows. Social account or AWS Builder ID required, no credit card required. Unused credits do not roll over to the next month. |
| [Trae (ByteDance)](https://www.trae.ai/pricing) | bundled | Trial credits | Frontier models (bundled, auto-selected) | Trae offers free inference. The free allowance includes 5,000 monthly autocompletions and a one-time $3 usage allowance. Usage is renewed monthly, and the credits are valid for 90 days. The free tier requires no credit card. |
| [Bolt.new](https://support.bolt.new/account-and-subscription/tokens) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Bolt offers 1,000,000 tokens per month with a 300,000 daily token cap, translating to bundled frontier model inference for full-stack web and code generation via the Standard agent alongside hosting for up to 333k requests. No credit card required to sign up. Daily tokens reset every 24 hours without rollover, monthly quotas reset on the 1st of each calendar month, and free plan tokens do not roll over. |
| [Lovable](https://docs.lovable.dev/introduction/credits-and-usage) | bundled | Rate-limited free | Fable 5.1 (Frontier model) | Lovable provides a rate-limited free plan for developers building full-stack web applications. Users receive bundled access to frontier models including Fable 5.1 directly within the development workspace without upfront subscription cost. Access is managed through daily workspace credits and standard platform usage limits. |
| [v0 (Vercel)](https://v0.app/docs/pricing) | bundled | Rate-limited free | Frontier models (bundled, auto-selected), Beam 1.0, Beam 1.0 (Free), Glyph Cluster, Nemotron 3.5 Lightning Free, Ampersand v0.1, +1 more | v0 offers a free plan granting 7 messages per day with bundled frontier models, plus a one-time $5 credit bonus for new accounts. Translates to 7 full-stack code and UI generations daily (~210 requests per month). No credit card required to sign up and build. Quotas reset daily at 00:00 UTC with no rollover, and custom model selection is restricted to paid plans. |
| [Kaggle Notebooks](https://www.kaggle.com/docs/efficient-gpu-usage) | login | Rate-limited free | Open-weight models you load (GPU runtime) | Kaggle offers 30 hours of free GPU accelerator quota (NVIDIA T4 x2 / P100) and 20 hours of TPU v3-8 compute per week, translating to running self-hosted open-weight model inference and fine-tuning across sessions lasting up to 12 hours. Phone verification is required to unlock accelerators and internet access; no credit card required. Compute quota resets weekly, and interactive sessions terminate after 20 to 60 minutes of idle time. |
| [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces-overview) | login | Rate-limited free | Any Hugging Face model you load (ZeroGPU), GLM-4.7-Flash | Hugging Face Spaces provides 5 minutes of daily ZeroGPU compute on dynamic NVIDIA RTX Pro 6000 Blackwell GPUs (48 GB to 96 GB VRAM) along with free hosting for up to 2 Gradio Spaces. This allows users to deploy and run inference on any compatible Hugging Face model across text, vision, audio, and multimodal tasks with execution limits of 60 to 120 seconds per function call. Access requires creating and logging into a free Hugging Face account with a verified email address, with no credit card required. The 5-minute GPU quota resets 24 hours after the first GPU usage, spaces auto-sleep when inactive, and hosting personal ZeroGPU demos requires an account older than 30 days in good standing. |
| [Cursor (Hobby)](https://cursor.com/pricing) | bundled | Rate-limited free | Cursor Free Models (Agent/Chat) | Cursor provides a complimentary Hobby tier for developers evaluating AI-assisted code editing. Users access bundled agent and inline chat completions directly within the IDE without an upfront subscription. Free access is subject to monthly request allowances and rate limits defined in the editor settings. |
| [Windsurf](https://docs.windsurf.com/windsurf/accounts/usage) | bundled | Rate-limited free | Standard Models | Windsurf provides a free tier. Users receive a set amount of usage and standard features at no cost. The free tier operates on a rate-limited basis. Usage allowances reset periodically under standard usage conditions. |
| [Devin (Free)](https://devin.ai/pricing) | bundled | Rate-limited free | SWE-2 (Free), Limited models (auto-selected) | Devin offers a Free plan with a light quota to code with agents, free use of SWE-2, unlimited inline edits, and unlimited Tab completions. Account login required, no credit card required. Runs bundled inside the Devin interface on SWE-2 and limited models. |
| [Qoder](https://docs.qoder.com/account/pricing) | bundled | Rate-limited free | Frontier models + BYO key | Qoder offers free basic code autocompletions and limited Next-Edit-Suggestion (NES) runs. Account login required, no credit card required. Unlimited usage requires bringing your own API keys. |
| [Antigravity CLI (Google)](https://antigravity.google/pricing) | login | Rate-limited free | Gemini 3.8 Flash, Gemini 3.7 Flash, Gemini 3.6 Flash, Gemini 3.1 Pro | Antigravity CLI provides free developer inference for base and multimodal foundation models. Users run text, code, and reasoning tasks through local CLI and terminal workflows. Authentication is handled directly via Google account login without requiring a payment instrument, subject to dynamic request rate limits. |
| [Google Colab](https://research.google.com/colaboratory/faq.html) | login | Rate-limited free | Gemini (AI features) + GPU for your code, Lyria 3 Clip Preview, Lyria 3 Pro Preview, Gemma 4 31B IT, Gemma 4 26B A4B IT | Google Colab offers free access to hosted Jupyter notebook compute resources including shared GPUs/TPUs and integrated Gemini AI coding features, translating to interactive execution sessions of up to 12 hours with standard system memory. Google account login required (age 18+ for AI features), no credit card required. Resources and rate limits fluctuate dynamically, idle runtimes disconnect, and non-interactive background execution is disallowed. |
| [Figma (Starter)](https://www.figma.com/pricing/) | bundled | Rate-limited free | Figma AI, Make, agent | Figma Starter offers 150 free AI generation credits/day (up to 500/month). Figma account required, no credit card required. Inference runs bundled inside Figma design files for layer generation and text editing. |
| [Canva (Free)](https://www.canva.com/en/pricing/) | bundled | Rate-limited free | Canva AI, Magic Media | Canva provides free users with a recurring monthly allowance of 20 generations across standard AI creative tools. Users access bundled Magic Media and text generation features directly within the design canvas without a paid plan. Free usage consumes a shared monthly credit pool and excludes premium enterprise AI tools. |
| [Framer (Free)](https://www.framer.com/pricing) | bundled | Trial credits | Framer Agents | Framer offers 500 one-time AI trial credits on its Free plan for workspaces without active subscriptions to power Framer Agents, translating to approximately 1 to 3 page generation or design sessions. No credit card is required to sign up and use the free plan. Credits are a one-time trial allotment that does not reset monthly, and agent features pause once the credits are exhausted unless upgraded to a paid plan. |
| [Replit (Starter)](https://docs.replit.com/help/pricing-and-plans) | bundled | Rate-limited free | Frontier models (bundled, auto-selected) | Replit provides a free Starter tier for developers prototyping and deploying cloud software. Users gain access to standard workspace environments with bundled AI assistance features. Accounts are created instantly with email or GitHub without entering billing details, subject to shared CPU and memory limits. |
| [Kilo Gateway](https://kilo.ai/gateway) | api_key | Rate-limited free | cohere/north-mini-code:free, poolside/laguna-s-2.1:free, poolside/laguna-xs-2.1:free, liquid/lfm-2.5-2.6b:free, dots-studio/dots-3-note-preview:free, nvidia/nemotron-3.5-lightning:free, +23 more | Kilo Gateway offers 7 free models with 64K–256K context, translating to 200 requests/hour per IP address. No credit card required. Model availability reflects upstream provider quotas. |
| [Nous Portal](https://portal.nousresearch.com/api-docs) | api_key | Rate-limited free | upstage/solar-mini4:free, tencent/hy4-flash:free, stepfun/step-3.7-flash:free, qwen/qwen4-max:free, meituan/longcat-2.5:free | Nous Portal offers 5 free Hermes and open-weight models, translating to 50 requests/minute and 500,000 tokens/minute. Free account registration required, no credit card required. Preview models may be adjusted during experimental rounds. |
| [Cohere](https://docs.cohere.com/docs/rate-limits) | api_key | Rate-limited free | Command A+, Command A Reasoning, Command R+, Command R, Command R7B, North Small Translate, +1 more | Cohere provides free trial API keys for developers building with Command A and embedding models. Users register an account to instantly retrieve trial credentials without entering a payment method. Usage is bounded by trial rate limits of 20 requests per minute and 1,000 API calls per month. |
| [Requesty](https://www.requesty.ai/pricing) | api_key | Rate-limited free | nvidia/nemotron-3-super-120b-a12b, google/gemma-4-31b-it, poolside/laguna-xs.2, Gemma 4 31B IT, ling-3.0-tiny, Muse Glimmer 30B, +7 more | Requesty offers 3 free models with 128K context, translating to 200 requests/day per account. Email registration required, no credit card required. Quota resets daily at 00:00 UTC. |
| [OVHcloud AI Endpoints](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/) | api_key | Rate-limited free | 10 free models (anonymous keyless), Qwen3Guard-Gen-0.6B, Qwen3Guard-Gen-8B | OVHcloud offers 10 free open-source models, translating to 2 requests/minute per IP keyless (or 400 requests/minute with a registered account). No credit card required for anonymous keyless access. Quota is enforced per client IP. |
| [SiliconFlow](https://siliconflow.cn) | api_key | Trial credits | Speech models (unspecified) | SiliconFlow provides $200 in free trial credits upon developer account registration. Credits can be applied across speech, text, and multimodal open-source models through an OpenAI-compatible API. Users create an account to generate API keys with no credit card required, with credits remaining valid for 90 days. |
| [DeepSeek Platform](https://api-docs.deepseek.com) | api_key | Deprecated | deepseek-chat, deepseek-reasoner | [DEPRECATED 2026-11-23] DeepSeek Platform documentation indicates that deepseek-chat and deepseek-reasoner models were retired on April 24, 2026. |
| [Braintrust](https://www.braintrust.dev/pricing) | api_key | Trial credits | deepseek-v4.1-flash, deepseek-v4-flash-0731, glm-5.3-flash, glm-5.2, kimi-k3, jev, +7 more | Braintrust offers $10/month recurring model credit on Starter across 13 built-in models (including GPT-6 series, DeepSeek V4.1, GLM-5.3, and Jev). Work email required, no credit card required. Model credit resets monthly with no rollover. |
| [Deepgram](https://deepgram.com/pricing) | api_key | Trial credits | nova-3, nova-2, flux, aura | Deepgram provides $200 in free trial credits upon registration, unlocking public speech-to-text and text-to-speech models including Nova-3, Flux, and Aura. Developers register an account to obtain an API key with no credit card required upfront. The allowance yields roughly 700 hours of audio transcription, subject to a 90-day expiry window and standard streaming concurrency caps. |
| [AssemblyAI](https://www.assemblyai.com/pricing) | api_key | Trial credits | Unknown | New accounts receive $50 in credits, valid for 90 days, usable across four speech models, and requiring no credit card. |
| [Dots Studio](https://dots.ai) | api_key | Trial credits | dots-3-note-preview | Dots Studio provides a developer trial credit system for querying its proprietary reasoning preview models. Developers access the dots-3-note-preview model via direct API key integration without upfront billing. Requests are constrained by a 524,288 token context window limit and trial usage quotas. |
| [Liquid AI](https://console.liquid.ai) | api_key | Trial credits | Liquid AI Free Model | Liquid AI provides promotional developer API credits upon registration in the Liquid developer console. Users evaluate liquid foundation models via OpenAI-compatible completion endpoints. Access is provisioned upon account creation at console.liquid.ai without upfront card requirements, subject to promotional credit balance limits. |
| [Speka](https://speka.me) | api_key | Permanent $0 | deepseek-ai/deepseek-v4-flash, deepseek-ai/deepseek-v4-pro, meta/llama-3.1-8b-instruct, meta/llama-3.2-3b-instruct, meta/llama-3.2-11b-vision-instruct, meta/llama-3.2-90b-vision-instruct, +21 more | Speka provides a recurring $1.00 monthly credit allowance that resets on the first of each month. Developers query all open catalog models (DeepSeek, Llama 3.2) via an OpenAI-compatible endpoint with a single API key created at signup without a credit card. Usage is capped at 10 RPM and billed at standard per-token rates, returning HTTP 402 once exhausted until the next monthly refresh. |
| [Alibaba DashScope (Bailian)](https://www.alibabacloud.com/help/en/model-studio/developer-reference/get-api-key) | api_key | Trial / Free tokens | Qwen3.7 Plus, DeepSeek V4.1 Flash 1017, GLM-5.3, Qwen3.6 Plus, Wan2.7 Image, HappyHorse 1.1 Reference-to-Video, +15 more | Alibaba Cloud Model Studio (Bailian/DashScope) provides free token allotments upon account activation across its Qwen and DeepSeek model fleet. Developers access high-throughput OpenAI-compatible endpoints with up to 1M token context windows. API keys are generated in the Model Studio console after account registration, with promotional free tokens valid during designated trial windows. |
| [ModelScope](https://modelscope.cn/docs/api-inference) | api_key | Rate-limited free | Qwen3 30B A3B Thinking 2507, Qwen3 235B A22B Instruct 2507, Qwen3 30B A3B Instruct 2507, Qwen3-235B-A22B-Thinking-2507, Qwen3 Coder 30B A3B Instruct, GLM-4.5, +1 more | ModelScope (Alibaba's open-source model community) offers free hosted inference for community and Qwen open-weights models. Users query standard OpenAI-compatible completion endpoints with context windows up to 262K tokens. Access is activated by creating a ModelScope account to retrieve an API access token, subject to fair-share community queuing and rate limits. |
| [AMD Developer Cloud](https://cloud.amd.com/) | api_key | Free Developer Tier | MiniCPM5-2B, Qwen3.8 Flash Next, DeepSeek V4 Flash 0731, MiniCPM-V 4.7 1B, MiniCPM-V 4.7 35B-A3B, Qwen3.8 27B, +4 more | AMD Developer Cloud provides free inference access to open frontier models running on AMD Instinct ROCm GPU clusters. Developers query OpenAI-compatible chat endpoints supporting DeepSeek, Qwen, and MiniCPM variants. Access is provisioned by registering an AMD Developer account to reach the API console, subject to cluster capacity and fair-use developer quotas. |
| [InferX](https://model.inferx.net/endpoints) | api_key | Free Developer Tier | Qwen3.6 35B A3B FP8, deepseek-v4-flash, Ornith-1.0-35B-FP8, Qwen3.6 27B FP8, mimo-v25, Qwen3 Coder Next FP8, +6 more | InferX provides zero-cost inference endpoints for open models including Qwen 3.6, Gemma 4, and DeepSeek variants. Developers access low-latency OpenAI-compatible completions with streaming and structured output support. Keys are provisioned instantly upon user sign-in without upfront payment, subject to community prototyping rate limits. |
| [Kimi For Coding (Moonshot AI)](https://www.kimi.ai/code/docs/en/kimi-code/models.html) | api_key | Free Developer Tier | Kimi K3.1 Pro Highspeed, Kimi K3-256K, Kimi K3.1 Pro, Kimi K3, kimi-for-coding, Kimi For Coding HighSpeed | Moonshot AI provides free developer inference for Kimi K3 and coding models with context windows up to 1M tokens. Developers query OpenAI-compatible coding endpoints supporting deep reasoning and agentic workflows. Credentials are retrieved via the Kimi coding portal, subject to community rate limits and peak-period concurrency throttling. |
| [SCNet](https://www.scnet.cn) | api_key | Free Developer Tier | Kimi K2.7 Code, Qwen3.8 Flash, MiniMax-M2.5, DeepSeek V4 Flash, DeepSeek V4 Pro 0813, GLM-5.3, +6 more | SCNet provides national high-performance computing open inference tokens for domestic LLMs including Qwen 3.8 and DeepSeek V4 Flash. Developers access OpenAI-compatible chat endpoints with up to 1M token context windows. Registration on the SCNet developer portal provisions API keys upon identity verification, subject to national computing quota rules. |
| [AIHubMix](https://aihubmix.com) | api_key | Promo free | GLM-4.7-Flash (free), Nemotron 3 Ultra 550B A55B (free), Nemotron 3.5 Content Safety (free), Qwen3.8 Max (free), GLM-5.2 (Coding, free), Ling 3.0 Flash (free), +10 more | AIHubMix provides a suite of zero-cost promotional models including GLM-4.7 Flash, Nemotron 3 Ultra, and Qwen 3.8 Max. Developers query OpenAI-compatible completion endpoints with long context support up to 1M tokens. Free API credentials are generated upon account signup without credit cards, subject to promotional token availability and rate limits. |

## Models (per provider)

### Synap by Linkrra

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen3-coder-30b | $0 (100,000 tokens/day account allowance) | 98.3K | 10 | Not published | 50 | 100,000 | 2026-11-23 |

### OpenCode (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Big Pickle | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| Iceman Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| Inkling 2 Small Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| Crouton Alpha Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| GLM-5.3-Flash Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| DeepSeek V4.1 Flash Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| Beam Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| Flint 40B Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| MiMo-V2.6-Flash Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| Nemotron 3 Ultra Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| Nemotron 3.5 Lightning Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| Nemotron 3.5 Super VL Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| Jev 1.13 Free | $0 | Unknown | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| MiniMax M3.1 Flash Free | $0 | 1.0M | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| LongCat 2.5 Free | $0 | 1.0M | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| Hy4 flash Free | $0 | 1M | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |
| Tidepool Alpha Free | $0 | 1M | Unknown | Unknown | Unknown | Unknown | 2026-11-23 |

### OpenRouter

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| inclusionai/ling-3.2-flash:free | 0 | 1048576 | Not published | Not published | Not published | Not published | 2026-11-23 |
| baidu/ernie-5.5-flash-preview:free | 0 | 1024000 | Not published | Not published | Not published | Not published | 2026-11-23 |
| liquid/lfm-3-1.7b:free | 0 | 262144 | Not published | Not published | Not published | Not published | 2026-11-23 |
| particle-ai/particle-1:free | 0 | 1048576 | Not published | Not published | Not published | Not published | 2026-11-23 |
| recursive/flint-v1.0:free | 0 | 262144 | Not published | Not published | Not published | Not published | 2026-11-23 |
| nvidia/nemotron-3.5-super-vl:free | 0 | 1000000 | Not published | Not published | Not published | Not published | 2026-11-23 |
| dots-studio/dots-3-note-preview:free | 0 | 512000 | Not published | Not published | Not published | Not published | 2026-11-23 |
| nvidia/nemotron-3.5-lightning:free | 0 | 1000000 | Not published | Not published | Not published | Not published | 2026-11-23 |
| nvidia/nemotron-3-ultra-550b-a55b:free | 0 | 1000000 | Not published | Not published | Not published | Not published | 2026-11-23 |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | 0 | 256000 | Not published | Not published | Not published | Not published | 2026-11-23 |
| google/gemma-4-26b-a4b-it:free | 0 | 262144 | Not published | Not published | Not published | Not published | 2026-11-23 |
| google/gemma-4-31b-it:free | 0 | 262144 | Not published | Not published | Not published | Not published | 2026-11-23 |

### Google AI Studio (Gemini API)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gemini-3.5-flash-lite | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-3.1-flash-lite | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemma-4-26b-a4b-it | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemma-4-31b-it | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-3.5-flash | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-3-flash-preview | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-3.1-flash-lite-preview | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-3.6-flash | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-3.7-flash | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-3.8-flash | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-flash-latest | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-flash-lite-latest | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-2.5-flash | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-2.5-flash-lite | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-omni-1.1-flash | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-omni-flash-preview | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-omni-1.2-flash | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-4-argon | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-4-carbon | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-4-hydrogen | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| gemini-4-neon | 0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |

### Groq

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| llama-3.3-70b-versatile | $0 | 128K | 30 | 12K | 1,000 | 100K tokens/day | 2026-11-23 |
| llama-3.1-8b-instant | $0 | 128K | 30 | 6K | 14,400 | 500K tokens/day | 2026-11-23 |
| meta-llama/llama-4-scout-17b-16e-instruct | $0 | 128K | 30 | 30K | 1,000 | 500K tokens/day | 2026-11-23 |
| openai/gpt-oss-120b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-11-23 |
| openai/gpt-oss-20b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-11-23 |
| qwen/qwen3.6-27b | $0 | 128K | 30 | 8K | 1,000 | 200K tokens/day | 2026-11-23 |
| qwen/qwen3.8-27b | $0 | 128K | 30 | 8K | 1,000 | 2M tokens/day | 2026-11-23 |
| meta-llama/llama-prompt-guard-2-22m | $0 | 128K | 30 | 15K | 14,400 | 500K tokens/day | 2026-11-23 |
| compound-beta | $0 | 128K | 30 | 70K | 250 | Not published | 2026-11-23 |
| whisper-large-v3-turbo | $0 | 25MB audio | 20 | 7.2K ASH (Audio sec/hr) | 2,000 | 28.8K ASD (8h audio/day) | 2026-11-23 |
| whisper-large-v3 | $0 | 25MB audio | 20 | 7.2K ASH (Audio sec/hr) | 2,000 | 28.8K ASD (8h audio/day) | 2026-11-23 |
| canopylabs/orpheus-v1-english | $0 | Text-to-speech | 10 | 1.2K ASH (Audio sec/hr) | 100 | 3.6K ASD (1h audio/day) | 2026-11-23 |
| canopylabs/orpheus-arabic-saudi | $0 | Text-to-speech | 10 | 1.2K ASH (Audio sec/hr) | 100 | 3.6K ASD (1h audio/day) | 2026-11-23 |
| ALLaM-2-7b | $0 | 4K | 30 | 12K | 1,000 | 100K tokens/day | 2026-11-23 |
| meta-llama/llama-prompt-guard-2-86m | $0 | 128K | 30 | 15K | 14,400 | 500K tokens/day | 2026-11-23 |

### Cerebras

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gpt-oss-120b | $0 | 65k | 5 | 30K uncached (90K total) | Not published | 1M | 2026-11-23 |
| qwen-3.8-27b | $0 | 64k | 300 | 150K uncached (750K total) | Not published | No daily cap (N/A) | 2026-11-23 |

### Cloudflare Workers AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ~80 free models (Llama 3.x/4, Qwen, Gemma, DeepSeek-R1 distills, FLUX, Whisper, BGE embeddings) | $0 | 8K-128K+ (model-dependent) | 300 text gen (720-1,500 other tasks) | Model-dependent | Not published | 10,000 neurons/day | 2026-11-22 |
| @cf/meta/llama-3.3-70b-instruct-fp8-fast | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-22 |
| @cf/deepseek-ai/deepseek-r1-distill-qwen-32b | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-22 |
| @cf/qwen/qwen2.5-72b-instruct | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-22 |
| @cf/meta/llama-3.1-8b-instruct | $0 | 128K | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-22 |
| @cf/openai/whisper | $0 | 25MB audio | 300 | Model-dependent | Not published | 10,000 neurons/day | 2026-11-22 |

### Mistral La Plateforme

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mistral-small-latest | $0 | 128K | 60 | 500K | Not published | Not published | 2026-11-22 |
| codestral-latest | $0 | 256K | 30 | 300K | Not published | Not published | 2026-11-22 |
| open-mistral-nemo | $0 | 128K | 60 | 500K | Not published | Not published | 2026-11-22 |

### SambaNova Cloud

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Meta-Llama-3.3-70B-Instruct | $0 (trial credits) | unknown | unknown | unknown | unknown | unknown | 2026-11-07 |

### NVIDIA NIM (build.nvidia.com)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-5 | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Kimi-2.5 | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| NIM-packaged open models | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| MiniMax-M3.1-Flash | $0 (trial credits) | 256K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Whisper Large v3 | $0 (trial credits) | 448 | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| GPT OSS 20B | $0 (trial credits) | 128K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Qwen Image | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Qwen Image Edit | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Llama Guard 4 12B | $0 (trial credits) | 160K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Llama-3.2-90B-Vision-Instruct | $0 (trial credits) | 125K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Muse Glimmer 30B | $0 (trial credits) | 128K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Llama 3.2 11b Vision Instruct | $0 (trial credits) | 125K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Gemma-4-31B-IT | $0 (trial credits) | 250K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| DiffusionGemma 26B A4B IT | $0 (trial credits) | 244.1K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| paligemma | $0 (trial credits) | 125K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| DeepSeek V4.1 Flash | $0 (trial credits) | 1.0M | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| FLUX.1-dev | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| FLUX.2 Klein 4B | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| FLUX.1-Kontext-dev | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| FLUX.1-schnell | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Laguna XS 2.1 | $0 (trial credits) | 256K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| magpie-tts-zeroshot | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| cosmos-transfer2.5-2b | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| llama-nemotron-embed-vl-1b-v2 | $0 (trial credits) | 8K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Nemotron 3.5 Lightning 30B A3B | $0 (trial credits) | 256K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Active Speaker Detection | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| llama-nemotron-rerank-vl-1b-v2 | $0 (trial credits) | 10K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Nemotron 3 Ultra 550B A55B | $0 (trial credits) | 1.0M | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Nemotron 3 Nano Omni | $0 (trial credits) | 250K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| llama-3.1-nemotron-safety-guard-8b-v3 | $0 (trial credits) | 125K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| nemotron-voicechat | $0 (trial credits) | 125K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| streampetr | $0 (trial credits) | 125K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| bevformer | $0 (trial credits) | 125K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Nemotron 3.5 Content Safety | $0 (trial credits) | 125K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| sparsedrive | $0 (trial credits) | 125K | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Nemotron 3.5 Super VL 120B A12B | $0 (trial credits) | 1M | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| synthetic-video-detector | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| studiovoice | $0 (trial credits) | Model-dependent | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| GLM-5.3-Flash | $0 (trial credits) | 1.0M | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |
| Step 5 Preview | $0 (trial credits) | 1M | ~40 | Not published | Not published | ~1,000 credits at signup (up to ~5,000) | 2026-11-23 |

### Z.AI (Zhipu)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-5.1 | $0 | Up to 203K | 3 (burst) | Not published | 1,000 (1K RPD tier) | Not published | 2026-11-22 |
| GLM-4.5-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-11-22 |
| GLM-4.7-Flash | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-11-22 |
| GLM-4.6V-Flash (vision) | $0 | Up to 203K | 3 (burst) | Not published | 1,000 | Not published | 2026-11-22 |
| GLM-4.6V-Flash | $0 | 125K | 3 (burst) | Not published | 1,000 (1K RPD tier) | Not published | 2026-11-22 |

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
| Auto-selected (GPT-5 mini, Claude Haiku/Sonnet, Gemini Flash line) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-22 |

### Kiro (AWS)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3 Coder Next | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-22 |
| DeepSeek 3.2 | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-22 |
| MiniMax M2.1 | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-22 |
| Claude Sonnet 4.5 | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-22 |

### Trae (ByteDance)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 (trial credits) | Not published | Not published | Not published | Not published | Not published | 2026-11-21 |

### Bolt.new

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Dynamic project context | Unspecified | Unspecified | Unspecified | 300,000 tokens/day (1,000,000 tokens/month) | 2026-11-22 |

### Lovable

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fable 5.1 (Frontier model) | $0 | Not specified | Not specified | Not specified | Not specified | Not specified | 2026-11-23 |

### v0 (Vercel)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Text, code, and image/file input | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-22 |
| Beam 1.0 | $0 | 1M | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-22 |
| Beam 1.0 (Free) | $0 | 1M | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-22 |
| Glyph Cluster | $0 | 250K | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-22 |
| Nemotron 3.5 Lightning Free | $0 | 1.0M | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-22 |
| Ampersand v0.1 | $0 | 1.0M | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-22 |
| Flint | $0 | 256K | unspecified | unspecified | 7 requests/day | unspecified | 2026-11-22 |

### Kaggle Notebooks

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Open-weight models you load (GPU runtime) | $0 | Model-dependent (16 GB P100 / 2x16 GB T4 VRAM, 29 GB RAM) | N/A | N/A | N/A | 30 GPU hours/week (resets weekly) | 2026-11-23 |

### Hugging Face Spaces

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Any Hugging Face model you load (ZeroGPU) | $0 | Model-dependent (up to 96 GB VRAM; 60s default / 120s max GPU duration per call) | Rate-limited (queue-based) | Not specified | Not specified | 5 minutes GPU time / day | 2026-11-22 |
| GLM-4.7-Flash | $0 | 195.3K | Rate-limited (queue-based) | Not specified | Not specified | 5 minutes GPU time / day | 2026-11-22 |

### Cursor (Hobby)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cursor Free Models (Agent/Chat) | $0 | Not specified | Rate-limited | Rate-limited | Rate-limited | Rate-limited | 2026-11-23 |

### Windsurf

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Standard Models | $0 | Standard | Not specified | Not specified | Not specified | Not specified | 2026-11-22 |

### Devin (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWE-2 (Free) | $0 | Not published | Light quota | Not published | Not published | Not published | 2026-11-22 |
| Limited models (auto-selected) | $0 | Not published | Light quota | Not published | Not published | Not published | 2026-11-22 |

### Qoder

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models + BYO key | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-22 |

### Antigravity CLI (Google)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini 3.8 Flash | $0 | Standard | N/A | N/A | N/A | N/A | 2026-11-23 |
| Gemini 3.7 Flash | $0 | Standard | N/A | N/A | N/A | N/A | 2026-11-23 |
| Gemini 3.6 Flash | $0 | Standard | N/A | N/A | N/A | N/A | 2026-11-23 |
| Gemini 3.1 Pro | $0 | Standard | N/A | N/A | N/A | N/A | 2026-11-23 |

### Google Colab

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini (AI features) + GPU for your code | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |
| Lyria 3 Clip Preview | $0 | 1M | Not published | Not published | Not published | Not published | 2026-11-23 |
| Lyria 3 Pro Preview | $0 | 1M | Not published | Not published | Not published | Not published | 2026-11-23 |
| Gemma 4 31B IT | $0 | 256K | Not published | Not published | Not published | Not published | 2026-11-23 |
| Gemma 4 26B A4B IT | $0 | 256K | Not published | Not published | Not published | Not published | 2026-11-23 |

### Figma (Starter)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Figma AI, Make, agent | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |

### Canva (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Canva AI | $0 | unknown | unknown | unknown | 20 uses (monthly shared limit) | unknown | 2026-11-23 |
| Magic Media | $0 | unknown | unknown | unknown | 20 uses (monthly shared limit) | unknown | 2026-11-23 |

### Framer (Free)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Framer Agents | $0 (trial credits) | Canvas-native web design, layout, styling, CMS, and copy generation | Not specified | Not specified | Not specified | 500 credits (one-time trial) | 2026-11-23 |

### Replit (Starter)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frontier models (bundled, auto-selected) | $0 | Not published | Not published | Not published | Not published | Not published | 2026-11-23 |

### Kilo Gateway

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cohere/north-mini-code:free | $0 | 250K | 20 | Provider-dependent | 200/day | Not published | 2026-11-07 |
| poolside/laguna-s-2.1:free | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-10-31 |
| poolside/laguna-xs-2.1:free | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-10-31 |
| liquid/lfm-2.5-2.6b:free | $0 | 64K | 20 | Provider-dependent | 200/day | Not published | 2026-11-03 |
| dots-studio/dots-3-note-preview:free | $0 | 500K | 20 | Provider-dependent | 200/day | Not published | 2026-11-07 |
| nvidia/nemotron-3.5-lightning:free | $0 | 1000000 | 20 | Provider-dependent | 200/day | Not published | 2026-11-07 |
| nvidia/nemotron-3.5-super-vl:free | $0 | 1000000 | 20 | Provider-dependent | 200/day | Not published | 2026-11-07 |
| Reflection: Beam 1.0 (free) | $0 | 1M | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| Crouton Alpha | $0 | 1M | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| Stealth: Glyph Cluster (free) | $0 | 250K | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| Auto Free | $0 | 250K | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| Lyria 3 Clip Preview | $0 | 1M | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| Lyria 3 Pro Preview | $0 | 1M | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| LiquidAI: LFM3-1.7B (free) | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| NVIDIA: Nemotron 3 Nano Omni (free) | $0 | 250K | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| NVIDIA: Nemotron 3 Ultra (free) | $0 | 1.0M | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| Body Builder (beta) | $0 | 125K | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| OpenRouter Free Models Router | $0 | 195.3K | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| Pareto Code Router | $0 | 195.3K | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| Auto Router | $0 | 1.9M | 20 | Provider-dependent | 200/day | Not published | 2026-11-08 |
| Thinking Machines: Inkling 2 Small (free) | $0 | 1M | 20 | Provider-dependent | 200/day | Not published | 2026-11-10 |
| Baidu: ERNIE-5.5-Flash-Preview (free) | $0 | 1.0M | 20 | Provider-dependent | 200/day | Not published | 2026-11-12 |
| Glyph Cluster | $0 | 250K | 20 | Provider-dependent | 200/day | Not published | 2026-11-13 |
| Ampersand v0.1 | $0 | 1.0M | 20 | Provider-dependent | 200/day | Not published | 2026-11-13 |
| Particle AI: Particle-1 (free) | $0 | 1M | 20 | Provider-dependent | 200/day | Not published | 2026-11-13 |
| Apodex: Apodex 1.1 Mini (free) | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-11-13 |
| inclusionAI: Ling 3.2 Flash (free) | $0 | 1M | 20 | Provider-dependent | 200/day | Not published | 2026-11-14 |
| Recursive: Flint | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-11-17 |
| Recursive: Flint (free) | $0 | 256K | 20 | Provider-dependent | 200/day | Not published | 2026-11-19 |

### Nous Portal

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| upstage/solar-mini4:free | Free | 524288 | Not published | Not published | Not published | Not published | 2026-11-23 |
| tencent/hy4-flash:free | Free | 1048576 | Not published | Not published | Not published | Not published | 2026-11-23 |
| stepfun/step-3.7-flash:free | Free | 256000 | Not published | Not published | Not published | Not published | 2026-11-23 |
| qwen/qwen4-max:free | Free | 1000000 | Not published | Not published | Not published | Not published | 2026-11-23 |
| meituan/longcat-2.5:free | Free | 1048576 | Not published | Not published | Not published | Not published | 2026-11-23 |

### Cohere

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Command A+ | $0 | N/A | 20 | N/A | N/A | N/A | 2026-11-22 |
| Command A Reasoning | $0 | N/A | 20 | N/A | N/A | N/A | 2026-11-22 |
| Command R+ | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-22 |
| Command R | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-22 |
| Command R7B | $0 | N/A | N/A | N/A | N/A | N/A | 2026-11-22 |
| North Small Translate | $0 | 32K | 20 | N/A | N/A | N/A | 2026-11-22 |
| North Mini Code | $0 | 250K | 20 | N/A | N/A | N/A | 2026-11-22 |

### Requesty

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nvidia/nemotron-3-super-120b-a12b | $0 | 128K | Not published | Not published | 200/day shared | Not published | 2026-11-07 |
| google/gemma-4-31b-it | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-11-07 |
| poolside/laguna-xs.2 | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-11-07 |
| Gemma 4 31B IT | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-11-08 |
| ling-3.0-tiny | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-11-08 |
| Muse Glimmer 30B | $0 | 128K | Not published | Not published | 200/day shared | Not published | 2026-11-08 |
| Nemotron 3.5 Lightning 30B A3B | $0 | 1M | Not published | Not published | 200/day shared | Not published | 2026-11-08 |
| leanstral-1-5 | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-11-08 |
| Nemotron 3 Ultra 550B A55B | $0 | 1M | Not published | Not published | 200/day shared | Not published | 2026-11-08 |
| Nemotron 3 Nano Omni 30B A3B Reasoning | $0 | 128K | Not published | Not published | 200/day shared | Not published | 2026-11-08 |
| leanstral-1-5@eu | $0 | 256K | Not published | Not published | 200/day shared | Not published | 2026-11-08 |
| Nemotron 3 Super 120B A12B | $0 | 1M | Not published | Not published | 200/day shared | Not published | 2026-11-08 |
| Nemotron 3.5 Content Safety | $0 | 128K | Not published | Not published | 200/day shared | Not published | 2026-11-08 |

### OVHcloud AI Endpoints

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 free models (anonymous keyless) | $0 | Model-dependent | 2/min per IP | Not published | Not published | Not published | 2026-11-07 |
| Qwen3Guard-Gen-0.6B | $0 | 32K | 2/min per IP | Not published | Not published | Not published | 2026-11-08 |
| Qwen3Guard-Gen-8B | $0 | 32K | 2/min per IP | Not published | Not published | Not published | 2026-11-08 |

### SiliconFlow

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Speech models (unspecified) | $0 (trial credits) | 43,000 minutes or 700+ hours | N/A | N/A | N/A | N/A | 2026-11-23 |

### DeepSeek Platform

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-chat | $0 (5M signup tokens) | 64K | 60 | Not published | Not published | 5M tokens grant | 2026-11-22 |
| deepseek-reasoner | $0 (5M signup tokens) | 64K | 60 | Not published | Not published | 5M tokens grant | 2026-11-22 |

### Braintrust

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-v4.1-flash | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |
| deepseek-v4-flash-0731 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |
| glm-5.3-flash | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |
| glm-5.2 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |
| kimi-k3 | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |
| jev | $0 ($10/mo model credits) | 256K | Not published | Not published | Not published | Not published | 2026-11-22 |
| gpt-6-luna | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |
| gpt-6-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |
| gpt-6.1-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |
| gpt-6-astra | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |
| gpt-5.6-luna | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |
| gpt-5.6-terra | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |
| gpt-5.6-sol | $0 ($10/mo model credits) | 128K | Not published | Not published | Not published | Not published | 2026-11-22 |

### Deepgram

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nova-3 | $0 (trial credits) | N/A | N/A | N/A | N/A | N/A | 2026-11-22 |
| nova-2 | $0 (trial credits) | N/A | N/A | N/A | N/A | N/A | 2026-11-22 |
| flux | $0 (trial credits) | N/A | N/A | N/A | N/A | N/A | 2026-11-22 |
| aura | $0 (trial credits) | N/A | N/A | N/A | N/A | N/A | 2026-11-22 |

### AssemblyAI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Unknown | $0 (trial credits) | Unknown | Unknown | Unknown | Unknown | 43000 minutes | 2026-11-22 |

### Dots Studio

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dots-3-note-preview | $0 (trial credits) | 524288 | N/A | N/A | N/A | N/A | 2026-11-23 |

### Liquid AI

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquid AI Free Model | $0 (trial) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |

### Speka

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek-ai/deepseek-v4-flash | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| deepseek-ai/deepseek-v4-pro | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| meta/llama-3.1-8b-instruct | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| meta/llama-3.2-3b-instruct | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| meta/llama-3.2-11b-vision-instruct | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| meta/llama-3.2-90b-vision-instruct | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| meta/llama-3.3-70b-instruct | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| mistralai/mistral-nemotron | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| mistralai/mistral-medium-3.5-128b | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| mistralai/mistral-large-4-1t-a52b | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| nvidia/nemotron-3-nano-30b-a3b | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| nvidia/nemotron-3-super-120b-a12b | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| nvidia/nemotron-3-ultra-550b-a55b | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| nvidia/nemotron-3.5-bolt-e4b | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| nvidia/nemotron-3.5-lightning-30b-a3b | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| nvidia/nemotron-3-embed-1b | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| nvidia/nemotron-nano-9b-v2 | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| nvidia/nemotron-nano-12b-v2-vl | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| nvidia/llama-3.3-nemotron-super-49b-v1.5 | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| openai/gpt-oss-20b | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| openai/gpt-oss-120b | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| poolside/laguna-xs-2.1 | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| stepfun-ai/step-3.7-flash | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| stepfun-ai/step-5-preview | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| minimaxai/minimax-m3 | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| z-ai/glm-5.2 | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |
| black-forest-labs/flux.1-dev | $0 (monthly credit allowance) | Model-dependent | Published on portal | Not published | Not published | Not published | 2026-11-22 |

### Alibaba DashScope (Bailian)

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3.7 Plus | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| DeepSeek V4.1 Flash 1017 | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| GLM-5.3 | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Qwen3.6 Plus | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Wan2.7 Image | $0 (promo free tokens) | 8K | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| HappyHorse 1.1 Reference-to-Video | $0 (promo free tokens) | Model-dependent | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Qwen3.6 Flash | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Qwen3.7 Max | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| DeepSeek V4 Pro | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| MiniMax-M2.5 | $0 (promo free tokens) | 192K | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Kimi K2.6 | $0 (promo free tokens) | 256K | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Kimi K2.5 | $0 (promo free tokens) | 256K | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Kimi K2.7 Code | $0 (promo free tokens) | 256K | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| HappyHorse 1.1 Text-to-Video | $0 (promo free tokens) | Model-dependent | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Qwen Image 2.0 | $0 (promo free tokens) | 8K | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Wan2.7 Image Pro | $0 (promo free tokens) | 8K | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| HappyHorse 1.1 Image-to-Video | $0 (promo free tokens) | Model-dependent | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| DeepSeek V4 Pro 0813 | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Qwen3.8 Flash | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Qwen3.8 Max | $0 (promo free tokens) | 1.0M | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |
| Qwen Image 2.0 Pro | $0 (promo free tokens) | 8K | 60 | Not published | Free tier token grant | Not published | 2026-11-23 |

### ModelScope

| Model | Cost | Context | RPM | TPM | RPD | Day tokens | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3 30B A3B Thinking 2507 | $0 | 256K | 30 | Not published | 500 | Not published | 2026-11-08 |
| Qwen3 235B A22B Instruct 2507 | $0 | 256K | 30 | Not published | 500 | Not published | 2026-11-08 |
| Qwen3 30B A3B Instruct 2507 | $0 | 256K | 30 | Not published | 500 | Not published | 2026-11-08 |
| Qwen3-235B-A22B-Thinking-2507 | $0 | 256K | 30 | Not published | 500 | Not published | 2026-11-08 |
| Qwen3 Coder 30B A3B Instruct | $0 | 256K | 30 | Not published | 500 | Not published | 2026-11-08 |
| GLM-4.5 | $0 | 128K | 30 | Not published | 500 | Not published | 2026-11-08 |
| GLM-4.6 | $0 | 198K | 30 | Not published | 500 | Not published | 2026-11-08 |

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
| GLM-4.7-Flash (free) | $0 | 195.3K | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Nemotron 3 Ultra 550B A55B (free) | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Nemotron 3.5 Content Safety (free) | $0 | 125K | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Qwen3.8 Max (free) | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| GLM-5.2 (Coding, free) | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Ling 3.0 Flash (free) | $0 | 256K | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Coding MiniMax M2.7 (Free) | $0 | 200K | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Nemotron 3.5 Lightning 30B A3B (free) | $0 | 256K | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| GLM-5.3 (Coding, free) | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Qwen3.8 Flash (free) | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Nemotron 3 Nano Omni 30B A3B Reasoning (free) | $0 | 250K | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Coding GLM 5.1 (free) | $0 | 195.3K | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| GLM-5.3-Flash (Coding, free) | $0 | 1.0M | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Nemotron 3 Super 120B A12B (free) | $0 | 256K | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Gemma 4 31B IT (free) | $0 | 256K | 60 | Not published | 1,000 | Not published | 2026-11-19 |
| Gemma 4 26B A4B IT (free) | $0 | 256K | 60 | Not published | 1,000 | Not published | 2026-11-19 |
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
