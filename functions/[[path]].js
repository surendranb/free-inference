// Content negotiation & server-side GA4 telemetry for agents, CLI hits, and raw data requests.
const GA_ID = "G-CFXWNKBD7G";

const CORS_HEADERS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, POST, OPTIONS, HEAD",
  "access-control-allow-headers": "*",
};

// Static assets to bypass from edge telemetry logging (FI_EVENTS & GA4)
const STATIC_ASSET = /^\/logos\/|\.(svg|png|jpg|jpeg|gif|webp|ico|css|js|map|woff|woff2|ttf|webmanifest)$/i;

const CHAT_GUIDANCE = {
  error: {
    message: "FreeInference.dev is an open verified catalog and directory of $0 free inference providers, not an API proxy or inference gateway. Direct inference requests (POST /v1/chat/completions) are not executed on this domain. To run free inference, query our catalog at /v1/models to select a provider, and route your requests directly to that provider's base_url (e.g. Groq, SambaNova, Google AI Studio, Cerebras).",
    type: "catalog_only_directory",
    code: "method_not_allowed",
    param: null,
  },
  catalog: {
    directory_url: "https://freeinference.dev",
    models_endpoint: "https://freeinference.dev/v1/models",
    raw_json: "https://freeinference.dev/data/providers.json",
    llms_txt: "https://freeinference.dev/llms.txt",
    documentation: "https://freeinference.dev/free-openai-compatible-api/",
  },
  skill: {
    name: "free-inference",
    description: "Official Agent Skill for Cursor, Claude Code, Cline, and LLM agent loops to automatically query, filter, and configure verified $0 endpoints and rate limits.",
    install_url: "https://freeinference.dev/skill.md",
    canonical_url: "https://freeinference.dev/skills/free-inference/SKILL.md",
    instructions: "Download or reference https://freeinference.dev/skill.md in your agent prompt to dynamically discover active free models.",
  },
  newsletter: {
    name: "FreeInference Weekly Dispatch",
    description: "Weekly automated email digest tracking new free models, quota changes, and verified $0 provider drops.",
    web_archive: "https://freeinference.dev/newsletter/",
    api_subscribe: {
      endpoint: "https://freeinference.dev/api/subscribe",
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: { email: "developer@example.com" },
      curl_example: "curl -X POST https://freeinference.dev/api/subscribe -H 'Content-Type: application/json' -d '{\"email\": \"you@example.com\"}'",
    },
  },
  feed: {
    atom_feed: "https://freeinference.dev/feed.xml",
    description: "Atom / RSS syndication feed for automated catalog aggregators, RSS readers, and agent monitors.",
  },
  quick_drop_in_providers: [
    {
      provider: "SambaNova Cloud",
      base_url: "https://api.sambanova.ai/v1",
      recommended_model: "DeepSeek-V3.2",
      free_tier: "Free API key, 0 credit card, 131k context window",
      signup_url: "https://cloud.sambanova.ai",
    },
    {
      provider: "Groq",
      base_url: "https://api.groq.com/openai/v1",
      recommended_model: "llama-3.3-70b-versatile",
      free_tier: "Free API key, 0 credit card, ultra-low latency LPU",
      signup_url: "https://console.groq.com",
    },
    {
      provider: "Google AI Studio",
      base_url: "https://generativelanguage.googleapis.com/v1beta/openai/",
      recommended_model: "gemini-3.5-flash-lite",
      free_tier: "15 RPM, 500 RPD permanently free, 1,000,000 token context window",
      signup_url: "https://aistudio.google.com",
    },
    {
      provider: "Cerebras",
      base_url: "https://api.cerebras.ai/v1",
      recommended_model: "llama-3.3-70b",
      free_tier: "Free trial credits, 2,000+ tokens/sec throughput",
      signup_url: "https://cloud.cerebras.ai",
    },
  ],
};

function detectAgentFamily(ua) {
  const u = (ua || "").toLowerCase();
  if (u.includes("claude") || u.includes("anthropic")) return "Claude / Anthropic";
  if (u.includes("chatgpt") || u.includes("gptbot") || u.includes("openai") || u.includes("oai-searchbot")) return "ChatGPT / OpenAI";
  if (u.includes("perplexity")) return "Perplexity";
  if (u.includes("cursor")) return "Cursor";
  if (u.includes("cline")) return "Cline";
  if (u.includes("antigravity") || u.includes("gemini") || u.includes("google-extended")) return "Google Gemini / Antigravity";
  if (u.includes("langchain")) return "LangChain";
  if (u.includes("llamaindex")) return "LlamaIndex";
  if (u.includes("python") || u.includes("requests") || u.includes("httpx") || u.includes("urllib") || u.includes("aiohttp")) return "Python Script";
  if (u.includes("curl")) return "cURL";
  if (u.includes("httpie")) return "HTTPie";
  if (u.includes("wget")) return "Wget";
  if (u.includes("node-fetch") || u.includes("axios") || u.includes("undici") || u.includes("go-http-client")) return "Backend HTTP Client";
  if (/googlebot|bingbot|duckduckbot|yandex|slurp|exasearch|petalbot|bytespider|baiduspider|sogou|bot|crawl|spider|headless/.test(u)) return "Search Crawler";
  if (u.includes("mozilla") || u.includes("chrome") || u.includes("safari") || u.includes("edge") || u.includes("firefox")) return "Browser";
  return "Custom / Unnamed Client";
}

function classifyClient(ua) {
  ua = (ua || "").toLowerCase();
  if (ua.includes("curl") || ua.includes("httpie") || ua.includes("wget")) return "cli";
  if (ua.includes("python") || ua.includes("requests") || ua.includes("urllib") || ua.includes("aiohttp") || ua.includes("httpx") || ua.includes("node-fetch") || ua.includes("axios") || ua.includes("go-http-client")) return "script";
  if (ua.includes("claude") || ua.includes("gpt") || ua.includes("agent") || ua.includes("llm") || ua.includes("langchain") || ua.includes("llama") || ua.includes("anthropic") || ua.includes("openai") || ua.includes("perplexity") || ua.includes("cursor")) return "agent";
  if (/bot|crawl|spider|slurp|headless|exasearch|petalbot|bytespider|googlebot|bingbot|yandex|baiduspider|duckduckbot/.test(ua)) return "crawler";
  if (ua.includes("mozilla") || ua.includes("chrome") || ua.includes("safari") || ua.includes("firefox") || ua.includes("edge")) return "browser";
  return "other";
}

// Deeper event sink: Analytics Engine dataset `freeinference_events` (binding FI_EVENTS).
// One data point per request; guarded so a missing binding never breaks delivery.
function consumerClass(ua, org) {
  const u = (ua || "").toLowerCase();
  if (u.includes("opencode")) return "harness_opencode";
  if (u.includes("claude")) return "harness_claude";
  if (/nexus-agent|free-api-catalog|freewaybot|free-ops|daedalus|freeairouter|modelscout|hatchfeed|webapp-mapper|sonarprime/.test(u)) return "directory";
  if (/palo alto|secleak|nameserver-checker|google-display-ads|google-lens|discordbot|icon\.horse|censys|shodan/.test(u)) return "scanner";
  if (/jev-readiness|hermes-ecosystem|forgeandco/.test(u)) return "self";
  if (/chatgpt|openai|oai-searchbot|perplexity|cursor/.test(u)) return "assistant";
  if (/python|httpx|curl|wget|node|undici|bun|go-http|axios|requests|urllib/.test(u)) return "script";
  if (/bot|crawl|spider|slurp|headless|exasearch|petalbot|bytespider|googlebot|bingbot|yandex|baiduspider|duckduckbot/.test(u)) return "crawler";
  if (/mozilla|chrome|safari|firefox|edge/.test(u)) return "browser";
  return "unclassified";
}

function logEvent(context, req, pathname, fileType, res) {
  try {
    if (!context.env || !context.env.FI_EVENTS) return;
    const h = req.headers;
    const cf = req.cf || {};
    const ua = h.get("user-agent") || "";
    const conditional = h.get("if-none-match") ? 1 : 0;
    context.env.FI_EVENTS.writeDataPoint({
      indexes: [consumerClass(ua, cf.asOrganization)],
      blobs: [
        pathname,
        req.method,
        ua,
        h.get("accept") || "",
        h.get("referer") || "",
        cf.asOrganization || "",
        cf.country || "",
        cf.city || "",
        cf.colo || "",
        cf.httpProtocol || "",
        h.get("sec-fetch-mode") || "",
        h.get("sec-fetch-dest") || "",
        h.get("sec-purpose") || h.get("purpose") || "",
        fileType || "html",
        res ? (res.headers.get("content-type") || "") : "",
        res ? String(res.status) : "",
      ],
      doubles: [
        cf.asn || 0,
        res ? res.status : 0,
        res && res.headers.get("content-length") ? Number(res.headers.get("content-length")) : 0,
        cf.clientTcpRtt || 0,
        conditional,
      ],
    });
  } catch (e) {
    // never degrade delivery for telemetry
  }
}

async function sendGaHit(req, pathname, fileType) {
  try {
    const ua = req.headers.get("user-agent") || "unknown";
    const referer = req.headers.get("referer") || "";
    const accept = req.headers.get("accept") || "*/*";
    const country = req.headers.get("cf-ipcountry") || "unknown";
    const asnOrg = (req.cf && req.cf.asOrganization) ? req.cf.asOrganization : "unknown";
    
    const clientType = classifyClient(ua);
    const agentFamily = detectAgentFamily(ua);

    const ip = req.headers.get("cf-connecting-ip") || "anonymous";
    let hash = 0;
    const str = ip + ua;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }
    const cid = String(Math.abs(hash));

    const params = new URLSearchParams({
      v: "2",
      tid: GA_ID,
      cid: cid,
      en: "agent_asset_hit",
      uip: ip,
      ua: ua,
      "ep.path": pathname,
      "ep.file_type": fileType,
      "ep.agent_name": agentFamily,
      "ep.client_type": clientType,
      "ep.user_agent": ua.slice(0, 100),
      "ep.asn_org": asnOrg.slice(0, 100),
      "ep.country_code": country,
      "ep.accept_type": accept.slice(0, 100),
      dl: req.url,
      dr: referer
    });

    await fetch("https://www.google-analytics.com/g/collect?" + params.toString(), {
      method: "POST",
      headers: {
        "user-agent": ua,
        "x-forwarded-for": ip
      }
    });
  } catch (e) {
    // Non-blocking: telemetry failures must never degrade asset delivery
  }
}

export async function onRequest(context) {
  const req = context.request;
  const url = new URL(req.url);
  const pathname = url.pathname;
  const accept = req.headers.get("accept") || "";

  // 0. CORS preflight for all endpoints
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  // 0b. Path normalization for /v1/models (stripping markdown backticks, URL-encoded %60, trailing quotes, /api/v1/models)
  let decodedPath = pathname;
  try {
    decodedPath = decodeURIComponent(pathname);
  } catch (e) {}
  const cleanPath = decodedPath.replace(/[`'"]+$/, "").trim();
  if (cleanPath === "/v1/models" || cleanPath === "/models" || cleanPath === "/api/v1/models") {
    if (context.waitUntil) context.waitUntil(sendGaHit(req, "/v1/models", "models_api"));
    const res = await context.env.ASSETS.fetch(new URL("/v1/models", req.url));
    if (res.ok) {
      logEvent(context, req, "/v1/models", "models_api", res);
      return new Response(res.body, {
        status: 200,
        headers: {
          "content-type": "application/json; charset=utf-8",
          ...CORS_HEADERS,
          "cache-control": "public, max-age=300",
        },
      });
    }
  }

  // 0c. Direct inference & chat completion interception: Developer Guidance
  const isChatInference = /^\/(v1\/)?chat(\/completions)?\/?$/.test(pathname)
    || /^\/(api\/)?(v1\/)?messages\/?$/.test(pathname)
    || /^\/api\/chat(\/completions)?\/?$/.test(pathname)
    || pathname.endsWith("/v1/chat/completions")
    || pathname.endsWith("/api/chat")
    || pathname.endsWith("/api/chat/completions");

  if (isChatInference) {
    const status = (req.method === "GET" || req.method === "HEAD") ? 200 : 405;
    if (context.waitUntil) {
      context.waitUntil(sendGaHit(req, pathname, status === 405 ? "guidance_405" : "chat_guidance"));
    }
    logEvent(context, req, pathname, "guidance_405", { status });
    return new Response(JSON.stringify(CHAT_GUIDANCE, null, 2) + "\n", {
      status: status,
      headers: {
        "content-type": "application/json; charset=utf-8",
        ...CORS_HEADERS,
        "allow": "GET, HEAD, OPTIONS",
        "cache-control": "no-store",
      },
    });
  }

  // 1. Content negotiation for markdown on root
  if (pathname === "/" && accept.includes("text/markdown")) {
    if (context.waitUntil) {
      context.waitUntil(sendGaHit(req, "/index.md", "markdown"));
    }
    const res = await context.env.ASSETS.fetch(new URL("/index.md", req.url));
    if (res.ok) {
      logEvent(context, req, "/index.md", "markdown", res);
      return new Response(res.body, {
        status: 200,
        headers: { "content-type": "text/markdown; charset=utf-8", vary: "Accept" },
      });
    }
  }

  // 1b. Content negotiation for markdown on provider pages (/providers/<slug>/ or /providers/<slug>)
  const providerMatch = pathname.match(/^\/providers\/([^/]+)\/?$/);
  if (providerMatch && accept.includes("text/markdown")) {
    const mdPath = `/providers/${providerMatch[1]}/index.md`;
    if (context.waitUntil) {
      context.waitUntil(sendGaHit(req, mdPath, "markdown"));
    }
    const res = await context.env.ASSETS.fetch(new URL(mdPath, req.url));
    if (res.ok) {
      logEvent(context, req, mdPath, "markdown", res);
      return new Response(res.body, {
        status: 200,
        headers: { "content-type": "text/markdown; charset=utf-8", vary: "Accept" },
      });
    }
  }

  // 1c. Content negotiation or alias for skill
  if (pathname === "/skill" || pathname === "/skills") {
    const res = await context.env.ASSETS.fetch(new URL("/skill.md", req.url));
    if (res.ok) {
      if (context.waitUntil) {
        context.waitUntil(sendGaHit(req, "/skill.md", "skill"));
      }
      logEvent(context, req, "/skill.md", "skill", res);
      return new Response(res.body, {
        status: 200,
        headers: { "content-type": "text/markdown; charset=utf-8", "access-control-allow-origin": "*", vary: "Accept" },
      });
    }
  }

  // 2. Track hits to llms.txt, index.md, provider markdown, data JSON, skills, feeds, and models API
  let fileType = null;
  if (pathname === "/llms.txt") {
    fileType = "llms.txt";
  } else if (pathname === "/index.md" || /^\/providers\/[^/]+\/index\.md$/.test(pathname)) {
    fileType = "markdown";
  } else if (pathname.startsWith("/data/") && pathname.endsWith(".json")) {
    fileType = "json";
  } else if (pathname === "/skill.md" || pathname.startsWith("/skills/")) {
    fileType = "skill";
  } else if (pathname === "/feed.xml" || pathname === "/changelog.xml") {
    fileType = "feed";
  } else if (pathname === "/v1/models" || pathname === "/models") {
    fileType = "models_api";
  } else if (pathname.startsWith("/api/")) {
    fileType = "api";
  }

  if (fileType && context.waitUntil) {
    context.waitUntil(sendGaHit(req, pathname, fileType));
  }

  // 3. Data-gap coverage: agents don't run gtag, so their HTML page reads
  // would otherwise exist nowhere. Browsers skipped — gtag covers them.
  if (!fileType && !STATIC_ASSET.test(pathname) && context.waitUntil
      && (pathname === "/" || /^\/providers\/[^/]+\/?$/.test(pathname) || /^\/free-[^/]+\/?$/.test(pathname))
      && classifyClient(req.headers.get("user-agent")) !== "browser") {
    context.waitUntil(sendGaHit(req, pathname, "html"));
  }

  const res = await context.next();
  // Bypass static assets (/logos/*, *.svg, *.png, *.ico, *.css, *.js) from edge telemetry sink
  if (!STATIC_ASSET.test(pathname)) {
    logEvent(context, req, pathname, fileType || "html", res);
  }
  try {
    res.headers.set("Vary", "Accept");
  } catch (e) {
    // ignore immutable header errors
  }
  return res;
}
