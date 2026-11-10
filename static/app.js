function modelRow(m) {
  return `<tr><td>${m.name}</td><td>${m.cost}</td><td>${m.context}</td>
    <td>${m.rpm}</td><td>${m.tpm}</td><td>${m.rpd}</td>
    <td>${m.tpd}</td><td>${m.verified}</td></tr>`;
}

function trackMcpCall(toolName, params) {
  if (typeof window.gtag === "function") {
    window.gtag("event", "webmcp_tool_call", {
      tool_name: toolName,
      search_query: params.query || "",
      provider_param: params.provider_name || params.provider || "",
      model_count: Array.isArray(params.model_names) ? params.model_names.length : undefined
    });
  }
}

const tools = {
  search_models: {
    name: "search_models",
    description: "Search free LLM models by keyword, minimum context length, provider name, or free tier type.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search query across model name or provider" },
        min_context_k: { type: "number", description: "Minimum context window in thousands (e.g. 128 for 128K+)" },
        provider: { type: "string", description: "Filter by provider name (partial or exact)" },
        free_type: { type: "string", description: "Filter by free tier type (e.g. 'Rate-limited free', 'Promo free (limited time)', 'Trial credits')" }
      }
    },
    execute: async (params = {}) => {
      trackMcpCall("search_models", params);
      const q = (params.query || "").toLowerCase();
      const pFilter = (params.provider || "").toLowerCase();
      const ftFilter = (params.free_type || "").toLowerCase();
      const minCtx = params.min_context_k || 0;
      const results = [];
      for (const prov of DATA.providers) {
        if (pFilter && !prov.name.toLowerCase().includes(pFilter)) continue;
        if (ftFilter && !prov.free_type.toLowerCase().includes(ftFilter)) continue;
        for (const m of prov.models) {
          const nameMatch = !q || m.name.toLowerCase().includes(q) || prov.name.toLowerCase().includes(q);
          let ctxNum = 0;
          const ctxMatch = String(m.context).match(/(\d+)K?/i);
          if (ctxMatch) {
            ctxNum = parseInt(ctxMatch[1], 10);
            if (!String(m.context).toUpperCase().includes("K") && ctxNum > 1000) ctxNum = Math.floor(ctxNum / 1024);
          }
          const passCtx = minCtx === 0 || ctxNum >= minCtx;
          if (nameMatch && passCtx) {
            results.push({
              provider: prov.name,
              free_type: prov.free_type,
              model: m.name,
              cost: m.cost,
              context: m.context,
              rpm: m.rpm,
              tpm: m.tpm,
              rpd: m.rpd,
              tpd: m.tpd,
              verified: m.verified
            });
          }
        }
      }
      return results;
    }
  },
  get_provider: {
    name: "get_provider",
    description: "Get comprehensive details and model inventory for a specific free inference provider.",
    inputSchema: {
      type: "object",
      properties: {
        provider_name: { type: "string", description: "Exact or partial provider name (e.g. 'Google', 'Groq', 'OpenRouter', 'OpenCode Zen')" }
      },
      required: ["provider_name"]
    },
    execute: async (params = {}) => {
      trackMcpCall("get_provider", params);
      const target = (params.provider_name || "").toLowerCase();
      const found = DATA.providers.find(p => p.name.toLowerCase().includes(target));
      if (!found) return { error: `Provider '${params.provider_name}' not found in catalog.` };
      return found;
    }
  },
  list_providers: {
    name: "list_providers",
    description: "List all free LLM inference providers with summary metadata, free tier type, and model counts.",
    inputSchema: {
      type: "object",
      properties: {
        free_type: { type: "string", description: "Optional filter by free tier type" }
      }
    },
    execute: async (params = {}) => {
      trackMcpCall("list_providers", params);
      const ft = (params.free_type || "").toLowerCase();
      return DATA.providers
        .filter(p => !ft || p.free_type.toLowerCase().includes(ft))
        .map(p => ({
          name: p.name,
          url: p.url,
          free_type: p.free_type,
          model_count: p.models.length,
          verified: p.verified,
          verified_method: p.verified_method,
          notes: p.notes
        }));
    }
  },
  compare_models: {
    name: "compare_models",
    description: "Compare rate limits and specs of specific models across providers.",
    inputSchema: {
      type: "object",
      properties: {
        model_names: { type: "array", items: { type: "string" }, description: "Array of model names to compare" }
      },
      required: ["model_names"]
    },
    execute: async (params = {}) => {
      trackMcpCall("compare_models", params);
      const names = (params.model_names || []).map(n => n.toLowerCase());
      const matches = [];
      for (const p of DATA.providers) {
        for (const m of p.models) {
          if (names.some(n => m.name.toLowerCase().includes(n) || n.includes(m.name.toLowerCase()))) {
            matches.push({
              provider: p.name,
              model: m.name,
              cost: m.cost,
              context: m.context,
              rpm: m.rpm,
              tpm: m.tpm,
              rpd: m.rpd,
              tpd: m.tpd,
              verified: m.verified
            });
          }
        }
      }
      return matches;
    }
  }
};

function registerWebMcp() {
  const mc = navigator.modelContext || window.modelContext || (typeof document !== "undefined" && document.modelContext);
  if (mc && typeof mc.registerTool === "function") {
    for (const tool of Object.values(tools)) {
      try {
        mc.registerTool({
          name: tool.name,
          description: tool.description,
          inputSchema: tool.inputSchema,
          execute: tool.execute,
          annotations: { readOnlyHint: true }
        });
      } catch (e) {
        console.warn("WebMCP registration failed:", tool.name, e);
      }
    }
  }
}

window.freeInferenceTools = tools;
window.webmcp = tools;
registerWebMcp();

const AM = {api_key:"API key", login:"Login", bundled:"Bundled"};
const plural = (n, one) => n + " " + one + (n === 1 ? "" : "s");

function render(app) {
  const list = DATA.providers;
  let activeIdx = 0, filter = "", rows = [...list];
  const sidebar = document.createElement("div");
  sidebar.className = "sidebar";
  const panel = document.createElement("div");
  panel.className = "panel";
  app.append(sidebar, panel);

  sidebar.innerHTML = `<input id="filter" type="text" placeholder="Filter provider or model…" autocomplete="off">
    <div id="providers"></div>`;
  const providersEl = sidebar.querySelector("#providers");
  const filterEl = sidebar.querySelector("#filter");

  function drawSidebar() {
    rows = list.filter(p => !filter ||
      (p.name + " " + p.models.map(m => m.name).join(" ")).toLowerCase().includes(filter.toLowerCase()));
    providersEl.innerHTML = rows.map((p, i) => {
      const active = list.indexOf(p) === activeIdx ? " active" : "";
      const dead = p.dead ? ` <span class="dead">• dead</span>` : "";
      return `<button class="prow${active}" data-i="${i}">
        <span class="pname"><img src="/logos/${LOGOS[p.name]}" class="prow-logo" width="16" height="16" alt="" onerror="this.style.display='none'"> ${p.name}${dead}</span>
        <span class="pmeta">${p.free_type} · ${plural(p.models.length, "free model")} · ${AM[p.access_method] || p.access_method}</span></button>`;
    }).join("");
    providersEl.querySelectorAll(".prow").forEach(b =>
      b.addEventListener("click", () => { activeIdx = list.indexOf(rows[+b.dataset.i]); drawPanel(); drawSidebar(); }));
    if (!rows.length) providersEl.innerHTML = `<div class="empty">No match.</div>`;
  }

  function drawPanel() {
    const p = list[activeIdx];
    const dead = p.dead ? `<div class="pnotes"><strong class="dead">Probe flags this provider unreachable — verify before relying on it.</strong></div>` : "";
    panel.innerHTML = `<div class="panel-head">
      <div class="provider-title-row">
        <img src="/logos/${LOGOS[p.name]}" class="panel-logo" width="28" height="28" alt="" onerror="this.style.display='none'">
        <h2 style="display:inline;margin:0;">${p.name}</h2>
        <span class="ftype">${p.free_type}</span><span class="amchip">${AM[p.access_method] || p.access_method}</span>
      </div>
      <a class="purl" href="${p.url}" target="_blank" rel="noopener" style="display:inline-block;margin-top:4px;">${p.url}</a>
      <div class="pnotes">${p.notes}</div>
      <div class="pnotes"><strong>Last updated: ${p.verified}</strong>${p.verified_method === "docs" ? " · verified against official public documentation" : " · verified nightly via automated probe"}</div>${dead}
    </div>
    <div class="table-wrap"><table>
      <thead><tr><th data-k="name">Model</th><th data-k="cost">Cost</th><th data-k="context">Context</th>
      <th data-k="rpm">RPM</th><th data-k="tpm">TPM</th><th data-k="rpd">RPD</th>
      <th data-k="tpd">Day tokens</th><th data-k="verified">Verified</th></tr></thead>
      <tbody id="mtbody">${p.models.map(modelRow).join("")}</tbody>
    </table></div>`;

    let asc = true, lastKey = "";
    panel.querySelectorAll("th").forEach(th => th.addEventListener("click", () => {
      const k = th.dataset.k;
      if (lastKey === k) asc = !asc; else { lastKey = k; asc = true; }
      const ms = [...p.models].sort((a, b) =>
        String(a[k]).localeCompare(String(b[k]), undefined, { numeric: true }));
      if (!asc) ms.reverse();
      panel.querySelector("#mtbody").innerHTML = ms.map(modelRow).join("");
    }));
  }

  filterEl.addEventListener("input", () => { filter = filterEl.value.trim(); drawSidebar(); });
  drawSidebar(); drawPanel();
}

document.addEventListener("DOMContentLoaded", () => render(document.getElementById("app")));

const m = document.getElementById("about");
document.getElementById("aboutlink").addEventListener("click", e => { e.preventDefault(); m.classList.add("open"); });
m.querySelector(".close").addEventListener("click", () => m.classList.remove("open"));
m.addEventListener("click", e => { if (e.target === m) m.classList.remove("open"); });
document.addEventListener("keydown", e => { if (e.key === "Escape") m.classList.remove("open"); });
