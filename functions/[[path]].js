// Content negotiation & server-side GA4 telemetry for agents, CLI hits, and raw data requests.
const GA_ID = "G-CFXWNKBD7G";

function detectAgentFamily(ua) {
  const u = (ua || "").toLowerCase();
  if (u.includes("claude") || u.includes("anthropic")) return "Claude / Anthropic";
  if (u.includes("chatgpt") || u.includes("gptbot") || u.includes("openai") || u.includes("oai-searchbot")) return "ChatGPT / OpenAI";
  if (u.includes("perplexity")) return "Perplexity";
  if (u.includes("cursor")) return "Cursor";
  if (u.includes("google-extended") || u.includes("gemini")) return "Google Gemini / Vertex";
  if (u.includes("langchain")) return "LangChain";
  if (u.includes("llamaindex")) return "LlamaIndex";
  if (u.includes("python") || u.includes("requests") || u.includes("httpx") || u.includes("urllib") || u.includes("aiohttp")) return "Python Script";
  if (u.includes("curl")) return "cURL";
  if (u.includes("httpie")) return "HTTPie";
  if (u.includes("wget")) return "Wget";
  if (u.includes("node-fetch") || u.includes("axios") || u.includes("undici") || u.includes("go-http-client")) return "Backend HTTP Client";
  if (u.includes("googlebot") || u.includes("bingbot") || u.includes("duckduckbot") || u.includes("yandex") || u.includes("slurp")) return "Search Crawler";
  if (u.includes("mozilla") || u.includes("chrome") || u.includes("safari") || u.includes("edge")) return "Browser";
  return "Custom / Unnamed Client";
}

function classifyClient(ua) {
  ua = (ua || "").toLowerCase();
  if (ua.includes("curl") || ua.includes("httpie") || ua.includes("wget")) return "cli";
  if (ua.includes("python") || ua.includes("requests") || ua.includes("urllib") || ua.includes("aiohttp") || ua.includes("httpx") || ua.includes("node-fetch") || ua.includes("axios") || ua.includes("go-http-client")) return "script";
  if (ua.includes("claude") || ua.includes("gpt") || ua.includes("agent") || ua.includes("llm") || ua.includes("langchain") || ua.includes("llama") || ua.includes("anthropic") || ua.includes("openai") || ua.includes("perplexity") || ua.includes("cursor")) return "agent";
  if (ua.includes("bot") || ua.includes("crawl") || ua.includes("spider")) return "crawler";
  if (ua.includes("mozilla") || ua.includes("chrome") || ua.includes("safari")) return "browser";
  return "other";
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
    const cid = Math.abs(hash) + "." + Math.floor(Date.now() / 1000);

    const params = new URLSearchParams({
      v: "2",
      tid: GA_ID,
      cid: cid,
      en: "agent_asset_hit",
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
      headers: { "user-agent": ua }
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

  // 1. Content negotiation for markdown on root
  if (pathname === "/" && accept.includes("text/markdown")) {
    if (context.waitUntil) {
      context.waitUntil(sendGaHit(req, "/index.md", "markdown"));
    }
    const res = await context.env.ASSETS.fetch(new URL("/index.md", req.url));
    if (res.ok) {
      return new Response(res.body, {
        status: 200,
        headers: { "content-type": "text/markdown; charset=utf-8", vary: "Accept" },
      });
    }
  }

  // 2. Track hits to llms.txt, index.md, and all data JSON files
  let fileType = null;
  if (pathname === "/llms.txt") {
    fileType = "llms.txt";
  } else if (pathname === "/index.md") {
    fileType = "markdown";
  } else if (pathname.startsWith("/data/") && pathname.endsWith(".json")) {
    fileType = "json";
  }

  if (fileType && context.waitUntil) {
    context.waitUntil(sendGaHit(req, pathname, fileType));
  }

  const res = await context.next();
  res.headers.set("Vary", "Accept");
  return res;
}
