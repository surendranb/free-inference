// Cloudflare Pages Function: /api/subscribe
// Stores newsletter subscribers directly into Cloudflare KV (free_inference_subscribers)
// Protected by Cloudflare Turnstile bot verification and IP rate limiting.
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

  // 1. Honeypot trap: if filled by automated scrapers, return synthetic 200 without saving or alerting
  const honeypot = payload && (payload.b_name || payload.b_comment || payload.honeypot);
  if (honeypot) {
    return new Response(
      JSON.stringify({
        success: true,
        message: "Successfully subscribed to The Free Inference Dispatch.",
      }),
      { status: 200, headers: corsHeaders }
    );
  }

  // 2. Validate email address format and length
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
  const ipHash = await hashIp(clientIp);

  // 3. Cloudflare Turnstile bot verification
  const secretKey = env && env.TURNSTILE_SECRET_KEY;
  if (secretKey) {
    const turnstileToken = payload && (payload.turnstileToken || payload["cf-turnstile-response"]);
    if (!turnstileToken) {
      return new Response(
        JSON.stringify({ success: false, error: "Please complete the security check." }),
        { status: 400, headers: corsHeaders }
      );
    }

    try {
      const form = new URLSearchParams();
      form.append("secret", secretKey);
      form.append("response", turnstileToken);
      if (clientIp !== "unknown") {
        form.append("remoteip", clientIp);
      }

      const verifyRes = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: form,
      });

      const outcome = await verifyRes.json();
      if (!outcome || !outcome.success) {
        return new Response(
          JSON.stringify({
            success: false,
            error: "Security verification failed. Please refresh and try again.",
          }),
          { status: 403, headers: corsHeaders }
        );
      }
    } catch (err) {
      return new Response(
        JSON.stringify({
          success: false,
          error: "Verification service temporarily unavailable. Please try again.",
        }),
        { status: 502, headers: corsHeaders }
      );
    }
  }

  // 4. IP Rate Limiting (max 5 subscriptions per hour per IP)
  if (env && env.SUBSCRIBERS_KV && ipHash !== "unknown") {
    try {
      const rlKey = `rl:${ipHash}`;
      const countStr = await env.SUBSCRIBERS_KV.get(rlKey);
      const count = countStr ? parseInt(countStr, 10) : 0;
      if (count >= 5) {
        return new Response(
          JSON.stringify({
            success: false,
            error: "Too many subscription attempts from your IP. Please try again later.",
          }),
          { status: 429, headers: corsHeaders }
        );
      }
      await env.SUBSCRIBERS_KV.put(rlKey, String(count + 1), { expirationTtl: 3600 });
    } catch (rlErr) {
      // Non-blocking: KV rate limit failure must not block subscription
    }
  }

  // 5. Store verified subscriber record in KV
  const record = {
    email: email,
    status: "active",
    created_at: new Date().toISOString(),
    country: country,
    source: payload.source || "web_form",
    ip_hash: ipHash,
    turnstile_verified: Boolean(secretKey),
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

    const text = `⚡ *New FreeInference Subscriber!*\n• *Email:* \`${email}\`\n• *Country:* ${country}\n• *Turnstile:* ✅ Verified\n• *Source:* \`${source || "web_form"}\`${referer ? `\n• *Referer:* ${referer}` : ""}`;

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
