// Cloudflare Pages Function: /api/subscribe
// Stores newsletter subscribers directly into Cloudflare KV (free_inference_subscribers)
// Zero third-party dependencies, 100% Cloudflare Free Tier.

const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "86400",
    },
  });
}

export async function onRequestPost(context) {
  const req = context.request;
  const env = context.env;

  const corsHeaders = {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
  };

  let payload;
  try {
    payload = await req.json();
  } catch (e) {
    return new Response(
      JSON.stringify({ success: false, error: "Invalid JSON body" }),
      { status: 400, headers: corsHeaders }
    );
  }

  const email = (payload && payload.email ? String(payload.email) : "").trim().toLowerCase();

  if (!email || !EMAIL_REGEX.test(email) || email.length > 254) {
    return new Response(
      JSON.stringify({ success: false, error: "Please enter a valid email address." }),
      { status: 400, headers: corsHeaders }
    );
  }

  const clientIp = req.headers.get("cf-connecting-ip") || "unknown";
  const country = req.headers.get("cf-ipcountry") || "unknown";
  const userAgent = req.headers.get("user-agent") || "";
  const referer = req.headers.get("referer") || "";

  const record = {
    email: email,
    status: "active",
    created_at: new Date().toISOString(),
    country: country,
    source: payload.source || "web_form",
    ip_hash: await hashIp(clientIp),
  };

  try {
    if (env && env.SUBSCRIBERS_KV) {
      await env.SUBSCRIBERS_KV.put(`sub:${email}`, JSON.stringify(record));
    } else {
      console.warn("SUBSCRIBERS_KV binding not found on environment");
    }

    if (context.waitUntil) {
      context.waitUntil(notifySlack(env, { email, country, source: record.source, referer }));
    } else {
      notifySlack(env, { email, country, source: record.source, referer });
    }

    return new Response(
      JSON.stringify({
        success: true,
        message: "Successfully subscribed to The Free Inference Dispatch.",
      }),
      { status: 200, headers: corsHeaders }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ success: false, error: "Failed to save subscription. Please try again." }),
      { status: 500, headers: corsHeaders }
    );
  }
}

async function notifySlack(env, { email, country, source, referer }) {
  try {
    const token = env && env.SLACK_BOT_TOKEN;
    const webhook = env && env.SLACK_WEBHOOK_URL;
    const channel = (env && env.SLACK_CHANNEL_ID) || "C0BLW648J3T"; // #build

    if (!token && !webhook) return;

    const text = `⚡ *New FreeInference Subscriber!*\n• *Email:* \`${email}\`\n• *Country:* ${country}\n• *Source:* \`${source || "web_form"}\`${referer ? `\n• *Referer:* ${referer}` : ""}`;

    if (webhook) {
      await fetch(webhook, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
    } else if (token) {
      await fetch("https://slack.com/api/chat.postMessage", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify({
          channel: channel,
          text: text,
        }),
      });
    }
  } catch (e) {
    // Non-blocking: Slack alert failure must never degrade subscription response
  }
}

async function hashIp(ip) {
  try {
    const encoder = new TextEncoder();
    const data = encoder.encode(ip + "freeinference-salt");
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("").slice(0, 16);
  } catch (e) {
    return "unknown";
  }
}
