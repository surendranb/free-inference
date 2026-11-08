// Test suite for functions/api/subscribe.js
import assert from "node:assert/strict";
import { onRequestPost } from "../functions/api/subscribe.js";

async function runTests() {
  console.log("--> Running subscribe function tests...");

  // Mock KV
  class MockKV {
    constructor() {
      this.store = new Map();
    }
    async get(k) {
      return this.store.get(k) || null;
    }
    async put(k, v) {
      this.store.set(k, v);
    }
  }

  // 1. Invalid JSON body -> 400
  {
    const req = new Request("https://freeinference.dev/api/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: "not-json",
    });
    const res = await onRequestPost({ request: req, env: {} });
    assert.equal(res.status, 400);
    const data = await res.json();
    assert.equal(data.error, "Invalid JSON body");
    console.log("  ✓ Invalid JSON rejected with 400");
  }

  // 2. Honeypot trap -> silent 200 without KV put
  {
    const kv = new MockKV();
    const req = new Request("https://freeinference.dev/api/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: "bot@spam.com", b_name: "I am a bot" }),
    });
    const res = await onRequestPost({ request: req, env: { SUBSCRIBERS_KV: kv } });
    assert.equal(res.status, 200);
    const data = await res.json();
    assert.equal(data.success, true);
    assert.equal(kv.store.size, 0, "KV should have 0 entries for honeypot bot trap");
    console.log("  ✓ Honeypot trap returned synthetic 200 with 0 KV writes");
  }

  // 3. Invalid email -> 400
  {
    const req = new Request("https://freeinference.dev/api/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: "invalid-email" }),
    });
    const res = await onRequestPost({ request: req, env: {} });
    assert.equal(res.status, 400);
    const data = await res.json();
    assert.match(data.error, /valid email/);
    console.log("  ✓ Invalid email rejected with 400");
  }

  // 4. Missing Turnstile token when secret key is configured -> 400
  {
    const req = new Request("https://freeinference.dev/api/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: "user@example.com" }),
    });
    const res = await onRequestPost({ request: req, env: { TURNSTILE_SECRET_KEY: "secret-123" } });
    assert.equal(res.status, 400);
    const data = await res.json();
    assert.match(data.error, /security check/i);
    console.log("  ✓ Missing Turnstile token rejected with 400");
  }

  // 5. Failed Turnstile verification -> 403
  {
    const originalFetch = globalThis.fetch;
    globalThis.fetch = async (url) => {
      if (String(url).includes("siteverify")) {
        return new Response(JSON.stringify({ success: false, "error-codes": ["invalid-input-response"] }));
      }
      return originalFetch(url);
    };

    const req = new Request("https://freeinference.dev/api/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: "user@example.com", turnstileToken: "bad-token" }),
    });
    const res = await onRequestPost({ request: req, env: { TURNSTILE_SECRET_KEY: "secret-123" } });
    assert.equal(res.status, 403);
    const data = await res.json();
    assert.match(data.error, /Security verification failed/i);
    console.log("  ✓ Invalid Turnstile token rejected with 403");

    globalThis.fetch = originalFetch;
  }

  // 6. Successful Turnstile verification -> 200 and saved to KV
  {
    const originalFetch = globalThis.fetch;
    let slackNotified = false;
    globalThis.fetch = async (url, opts) => {
      if (String(url).includes("siteverify")) {
        return new Response(JSON.stringify({ success: true, challenge_ts: new Date().toISOString() }));
      }
      if (String(url).includes("slack.com")) {
        slackNotified = true;
        return new Response(JSON.stringify({ ok: true }));
      }
      return originalFetch(url, opts);
    };

    const kv = new MockKV();
    const req = new Request("https://freeinference.dev/api/subscribe", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "cf-connecting-ip": "1.2.3.4",
        "cf-ipcountry": "US",
      },
      body: JSON.stringify({ email: "tester@example.com", turnstileToken: "valid-token" }),
    });
    const res = await onRequestPost({
      request: req,
      env: {
        TURNSTILE_SECRET_KEY: "secret-123",
        SUBSCRIBERS_KV: kv,
        SLACK_BOT_TOKEN: "mock-token",
      },
    });
    assert.equal(res.status, 200);
    const data = await res.json();
    assert.equal(data.success, true);
    assert.ok(kv.store.has("sub:tester@example.com"), "Record saved in KV");
    const saved = JSON.parse(kv.store.get("sub:tester@example.com"));
    assert.equal(saved.email, "tester@example.com");
    assert.equal(saved.country, "US");
    assert.equal(saved.turnstile_verified, true);
    assert.ok(slackNotified, "Slack notification sent");
    console.log("  ✓ Valid subscription passed with 200, saved to KV, and notified Slack");

    globalThis.fetch = originalFetch;
  }

  // 7. Rate limiting after 5 attempts -> 429
  {
    const originalFetch = globalThis.fetch;
    globalThis.fetch = async (url) => {
      if (String(url).includes("siteverify")) {
        return new Response(JSON.stringify({ success: true }));
      }
      return new Response(JSON.stringify({ ok: true }));
    };

    const kv = new MockKV();
    const env = {
      TURNSTILE_SECRET_KEY: "secret-123",
      SUBSCRIBERS_KV: kv,
    };

    for (let i = 0; i < 5; i++) {
      const req = new Request("https://freeinference.dev/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json", "cf-connecting-ip": "9.9.9.9" },
        body: JSON.stringify({ email: `user${i}@example.com`, turnstileToken: "token" }),
      });
      const res = await onRequestPost({ request: req, env });
      assert.equal(res.status, 200);
    }

    // 6th attempt from same IP should get 429
    const req6 = new Request("https://freeinference.dev/api/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json", "cf-connecting-ip": "9.9.9.9" },
      body: JSON.stringify({ email: "user6@example.com", turnstileToken: "token" }),
    });
    const res6 = await onRequestPost({ request: req6, env });
    assert.equal(res6.status, 429);
    const data6 = await res6.json();
    assert.match(data6.error, /too many subscription attempts/i);
    console.log("  ✓ 6th attempt from same IP rate-limited with 429");

    globalThis.fetch = originalFetch;
  }

  console.log("--> ALL 7 SUBSCRIBE FUNCTION TESTS PASSED!");
}

runTests().catch((e) => {
  console.error(e);
  process.exit(1);
});
