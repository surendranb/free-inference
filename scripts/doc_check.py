#!/usr/bin/env python3
"""Vision doc-check: screenshot each provider's docs page, have Gemini quote the
free-tier limits verbatim, compare quoted numbers against catalog values.

REPORT-ONLY: never writes data/providers.json. A mismatch is a flag for human
verification, not an auto-update. Exit 0 always.
"""
import base64
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = json.loads((ROOT / "data" / "providers.json").read_text())
UA = {"User-Agent": "free-inference-doccheck/0.1"}
MODEL = "gemini-2.5-flash"

PROMPT = """You are auditing documentation for a free-tier API rate-limit catalog.
Screenshot is of {name} ({url}).
Quote VERBATIM (copy exact text, do not infer or compute) every statement about
free-tier limits: requests per minute/day, tokens per minute/day, context caps,
daily token pools, credits. Return ONLY a JSON array:
[{{"scope":"model name or 'free tier'","metric":"RPM|TPM|RPD|TPD|tokens|credits|context","value_verbatim":"exact quoted text"}}]
If nothing about free-tier limits appears, return []"""


def shot(page, url, path):
    page.goto(url, timeout=45000, wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    page.screenshot(path=path, full_page=True)
    return Path(path).read_bytes()


def ask_gemini(png_bytes, name, url, key):
    body = {
        "contents": [{"parts": [
            {"text": PROMPT.format(name=name, url=url)},
            {"inline_data": {"mime_type": "image/png", "data": base64.b64encode(png_bytes).decode()}},
        ]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.load(r)
    text = d["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)


def nums(s):
    return {int(x) for x in re.findall(r"\d[\d,]*", str(s)) if int(x.replace(",", "") or 0) > 0}


def catalog_numbers(prov):
    out = set()
    for m in prov["models"]:
        for k in ("rpm", "tpm", "rpd", "tpd"):
            out |= nums(m.get(k))
    return out


def main():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("no GEMINI_API_KEY; skipping")
        return
    targets = [p for p in DATA["providers"] if p.get("docs_url")]
    report = [f"# Vision doc-check {__import__('datetime').date.today().isoformat()}", ""]
    diffs = 0
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed; skipping")
        return
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1200})
        tmp = Path("/tmp/free-inference-shots")
        tmp.mkdir(exist_ok=True)
        for prov in targets:
            slug = re.sub(r"[^a-z0-9]+", "-", prov["name"].lower()).strip("-")
            png = tmp / f"{slug}.png"
            try:
                quotes = ask_gemini(shot(page, prov["docs_url"], png), prov["name"], prov["docs_url"], key)
            except Exception as e:
                report += [f"## {prov['name']}", f"- ERROR: {e}", ""]
                continue
            if not quotes:
                report += [f"## {prov['name']}", "- no limit statements found on page — page may have moved or redesigned", ""]
                continue
            cat = catalog_numbers(prov)
            lines = []
            for q in quotes:
                qn = {n for n in nums(q["value_verbatim"])}
                status = "ok" if qn & cat else ("**DIFF**" if qn else "?")
                if status == "**DIFF**":
                    diffs += 1
                lines.append(f'- `{q["value_verbatim"]}` ({q["metric"]}, {q["scope"]}) → {status}')
            report += [f"## {prov['name']}", *lines, ""]
        browser.close()
    text = "\n".join(report)
    print(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        Path(summary).write_text(text + "\n")
    print(f"\ndiffs flagged: {diffs} (report-only — nothing written to catalog)")


if __name__ == "__main__":
    main()
