// Content negotiation & server-side GA4 telemetry for agents, CLI hits, and raw data requests.
const GA_ID = "G-CFXWNKBD7G";

function classifyClient(ua) {
  ua = (ua || "").toLowerCase();
  if (ua.includes("curl") || ua.includes("httpie") || ua.includes("wget")) return "cli";
  if (ua.includes("python") || ua.includes("requests") || ua.includes("urllib") || ua.includes("aiohttp") || ua.includes("node-fetch") || ua.includes("axios") || ua.includes("go-http-client")) return "script";
  if (ua.includes("claude") || ua.includes("gpt") || ua.includes("agent") || ua.includes("llm") || ua.includes("langchain") || ua.includes("llama") || ua.includes("anthropic") || ua.includes("openai")) return "agent";
  if (ua.includes("bot") || ua.includes("crawl") || ua.includes("spider")) return "crawler";
  if (ua.includes("mozilla") || ua.includes("chrome") || ua.includes("safari")) return "browser";
  return "other";
}

async function sendGaHit(req, pathname, fileType) {
  try {
    const ua = req.headers.get("user-agent") || "unknown";
    const referer = req.headers.get("referer") || "";
    const clientType = classifyClient(ua);

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
      "ep.client_type": clientType,
      "ep.user_agent": ua.slice(0, 100),
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
