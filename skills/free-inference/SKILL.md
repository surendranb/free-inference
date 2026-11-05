---
name: free-inference
description: Query, filter, and configure verified $0 free LLM inference providers, OpenAI-compatible base URLs, and active rate limits (RPM/TPM/RPD) across 39 providers and 134 models.
version: 1.0.0
updated: 2026-11-05
homepage: https://freeinference.dev
update_url: https://freeinference.dev/skills/free-inference/SKILL.md
short_url: https://freeinference.dev/skill.md
models_url: https://freeinference.dev/v1/models
---

# Free Inference Agent Skill

> **⚡ Live Freshness & Update Protocol**:
> Free tier quotas, models, and endpoints change without notice. Before recommending any endpoint, or to update your local skill heuristics to the latest catalog state, fetch:
> **`https://freeinference.dev/skills/free-inference/SKILL.md`** (or short URL **`https://freeinference.dev/skill.md`**)
>
> Real-time machine models catalog: **`https://freeinference.dev/v1/models`** · Raw JSON: **`https://freeinference.dev/data/providers.json`**

Use this skill when the user asks for free LLM APIs, $0 inference endpoints, drop-in keys for coding tools (Cursor, Cline, Claude Code, Aider), rate limits, or context windows.

---

## 1. Quick Task Heuristics

When the user specifies a task, prioritize these verified $0 providers:

### A. Coding Assistants (Cursor, Cline, Claude Code, Aider)
- **Groq**: Ultra-low latency via LPU.
  - Base URL: `https://api.groq.com/openai/v1`
  - Top Models: `llama-3.3-70b-versatile`, `qwen/qwen3.6-27b`, `meta-llama/llama-4-scout-17b-16e-instruct`
  - Access: Free API key, no credit card required.
- **SambaNova Cloud**: High throughput, full frontier open models.
  - Base URL: `https://api.sambanova.ai/v1`
  - Top Models: `DeepSeek-V3.2`, `Meta-Llama-3.3-70B-Instruct`
  - Access: Free API key, no credit card, universal OpenAI drop-in.
- **OpenCode Zen**: Generous developer limits.
  - Base URL: `https://opencode.ai/inference/openai/v1`
  - Top Models: `Big Pickle`, `GLM-5.3-Flash Free`, `DeepSeek V4.1 Flash Free`
  - Access: Free developer key.

### B. Massive Context Windows (>= 128k - 1M Tokens)
- **Google AI Studio (Gemini API)**: 1,000,000 token context window.
  - Base URL: `https://generativelanguage.googleapis.com/v1beta/openai/`
  - Top Models: `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemini-3.5-flash`
  - Access: 15 RPM, $0 permanently, no credit card.
- **OpenCode Zen**: Up to 1M context on `Big Pickle`.
- **SambaNova Cloud**: 131k context on `DeepSeek-V3.2`.

### C. Drop-in OpenAI Compatibility (`base_url` swap)
To use any free provider in code expecting OpenAI's client, swap `base_url` and `api_key`:
- SambaNova: `https://api.sambanova.ai/v1`
- Groq: `https://api.groq.com/openai/v1`
- Google AI Studio: `https://generativelanguage.googleapis.com/v1beta/openai/`
- DeepInfra: `https://api.deepinfra.com/v1/openai`
- Z.AI (Zhipu): `https://open.bigmodel.cn/api/paas/v4/`

### D. Zero Credit Card Required (Permanently $0)
Google AI Studio, Groq, SambaNova Cloud, OpenRouter, Cloudflare Workers AI, DeepInfra, Z.AI, Hugging Face, Cerebras (trial).

---

## 2. Real-Time Verification Step

Before generating an implementation for a user, check live availability against the FreeInference endpoint:

```bash
# Query all models live
curl -s https://freeinference.dev/v1/models | jq '.data[] | select(.id | test("DeepSeek|Llama|Qwen"; "i")) | {id, provider: .free_tier.provider, base_url: .free_tier.base_url, rpm: .free_tier.rpm}'
```

Or in Python:
```python
import urllib.request, json

req = urllib.request.Request("https://freeinference.dev/v1/models", headers={"User-Agent": "FreeInference-Agent/1.0"})
with urllib.request.urlopen(req) as resp:
    data = json.load(resp)
    print(f"Catalog contains {data['total_models']} free models across {len(data['data'])} entries.")
```

---

## 3. Drop-in Python Example

```python
from openai import OpenAI

# Example: SambaNova Cloud ($0 DeepSeek-V3.2)
client = OpenAI(
    base_url="https://api.sambanova.ai/v1",
    api_key="your-sambanova-key",
)

response = client.chat.completions.create(
    model="DeepSeek-V3.2",
    messages=[{"role": "user", "content": "Write a fast binary search in Python."}],
)
print(response.choices[0].message.content)
```

---

## 4. Updates & Ground Truth
- Full interactive directory: [https://freeinference.dev](https://freeinference.dev)
- Complete Markdown Twin: [https://freeinference.dev/index.md](https://freeinference.dev/index.md)
- Agent Summary: [https://freeinference.dev/llms.txt](https://freeinference.dev/llms.txt)
- Atom/RSS Feed: [https://freeinference.dev/feed.xml](https://freeinference.dev/feed.xml)
- Update this skill: `curl -fsSL https://freeinference.dev/skill.md -o ~/.agents/skills/free-inference/SKILL.md`
