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

// Deeper event sink: Analytics Engine dataset `freeinference_events` (binding FI_EVENTS).
// One data point per request; guarded so a missing binding never breaks delivery.
function consumerClass(ua, org) {
  const u = (ua || "").toLowerCase();
  if (u.includes("opencode")) return "harness_opencode";
  if (u.includes("claude")) return "harness_claude";
  if (/nexus-agent|free-api-catalog|freewaybot|free-ops|daedalus|freeairouter|modelscout|hatchfeed|webapp-mapper|sonarprime/.test(u)) return "directory";
  if (/palo alto|secleak|nameserver-checker|google-display-ads|google-lens|discordbot|icon\.horse/.test(u)) return "scanner";
  if (/jev-readiness|hermes-ecosystem|forgeandco/.test(u)) return "self";
  if (/chatgpt|openai|oai-searchbot|perplexity|cursor/.test(u)) return "assistant";
  if (/python|httpx|curl|wget|node|undici|bun|go-http/.test(u)) return "script";
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

  // 2. Track hits to llms.txt, index.md, provider markdown, and all data JSON files
  let fileType = null;
  if (pathname === "/llms.txt") {
    fileType = "llms.txt";
  } else if (pathname === "/index.md" || /^\/providers\/[^/]+\/index\.md$/.test(pathname)) {
    fileType = "markdown";
  } else if (pathname.startsWith("/data/") && pathname.endsWith(".json")) {
    fileType = "json";
  }

  if (fileType && context.waitUntil) {
    context.waitUntil(sendGaHit(req, pathname, fileType));
  }

  // 3. Data-gap coverage: agents don't run gtag, so their HTML page reads
  // would otherwise exist nowhere. Browsers skipped — gtag covers them.
  if (!fileType && context.waitUntil
      && (pathname === "/" || /^\/providers\/[^/]+\/?$/.test(pathname))
      && classifyClient(req.headers.get("user-agent")) !== "browser") {
    context.waitUntil(sendGaHit(req, pathname, "html"));
  }

  const res = await context.next();
  logEvent(context, req, pathname, fileType || "html", res);
  res.headers.set("Vary", "Accept");
  return res;
}
