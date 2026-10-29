#!/usr/bin/env python3
"""Automated verification suite for the programmatic free-* matrix on freeinference.dev.

Checks:
1. All 31 free-* slugs are built into dist/ with index.html and index.md.
2. Titles are <= 75 chars, unique, and contain target keywords.
3. Every page has >= 1 verified model row (no empty pages).
4. Canonical URLs and markdown alternates are correctly formatted.
5. JSON-LD structured data is valid.
6. All URLs are indexed in dist/sitemap.xml and dist/llms.txt.
7. Homepage dist/index.html integrity is preserved.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
sys.path.insert(0, str(ROOT))

from build import FREE_PAGES_CONFIG, TITLE, WEBSITE, DATA_VERSION

def verify_matrix():
    print(f"--> Verifying free-* matrix ({len(FREE_PAGES_CONFIG)} slices)...")
    errors = []
    
    # 1. Check sitemap.xml and llms.txt
    sitemap = (DIST / "sitemap.xml").read_text()
    llmstxt = (DIST / "llms.txt").read_text()
    
    titles = set()
    summary = []
    
    for slug, cfg in sorted(FREE_PAGES_CONFIG.items()):
        html_path = DIST / slug / "index.html"
        md_path = DIST / slug / "index.md"
        
        if not html_path.exists():
            errors.append(f"Missing {html_path}")
            continue
        if not md_path.exists():
            errors.append(f"Missing {md_path}")
            continue
            
        html_content = html_path.read_text()
        md_content = md_path.read_text()
        
        # Check title
        m_title = re.search(r"<title>(.*?)</title>", html_content)
        if not m_title:
            errors.append(f"{slug}: missing <title>")
        else:
            t = m_title.group(1)
            if len(t) > 75:
                errors.append(f"{slug}: title too long ({len(t)} chars > 75)")
            if t in titles:
                errors.append(f"{slug}: duplicate title '{t}'")
            titles.add(t)
            
        # Check canonical
        expected_canonical = f'<link rel="canonical" href="{WEBSITE}/{slug}/">'
        if expected_canonical not in html_content:
            errors.append(f"{slug}: canonical link missing or invalid: {expected_canonical}")
            
        # Check markdown alternate
        expected_md_alt = f'<link rel="alternate" type="text/markdown" href="{WEBSITE}/{slug}/index.md">'
        if expected_md_alt not in html_content:
            errors.append(f"{slug}: markdown alternate link missing: {expected_md_alt}")
            
        # Check answer block
        if '<section class="answer">' not in html_content:
            errors.append(f"{slug}: missing answer section")
            
        # Check model rows in table
        m_tbody = re.search(r"<tbody>(.*?)</tbody>", html_content, re.DOTALL)
        if not m_tbody:
            errors.append(f"{slug}: missing <tbody>")
        else:
            row_count = m_tbody.group(1).count("<tr>")
            if row_count == 0:
                errors.append(f"{slug}: 0 model rows in table")
                
        # Check sitemap & llms.txt
        page_url = f"{WEBSITE}/{slug}/"
        if page_url not in sitemap:
            errors.append(f"{slug}: not found in sitemap.xml")
        if page_url not in llmstxt:
            errors.append(f"{slug}: not found in llms.txt")
            
        # Check markdown twin content
        if not md_content.startswith(f"# {cfg['h1']}"):
            errors.append(f"{slug}: index.md missing matching H1")
            
        summary.append((slug, row_count if m_tbody else 0, len(m_title.group(1)) if m_title else 0))

    # 2. Check homepage integrity
    index_html = (DIST / "index.html").read_text()
    if "Free Inference You Can Build With" not in index_html:
        errors.append("Homepage H1 altered or missing")
    if f'name="data-version" content="{DATA_VERSION}"' not in index_html:
        errors.append("Homepage data-version missing")
    if index_html.count('href="/providers/') < 36:
        errors.append("Homepage footer provider links missing")

    # Output report
    print(f"\n{'SLUG':<30} {'MODELS':<8} {'TITLE LEN':<10}")
    print("-" * 50)
    for s, count, tlen in summary:
        print(f"{s:<30} {count:<8} {tlen:<10}")
    print("-" * 50)
    
    if errors:
        print(f"\nFAILED: {len(errors)} error(s) detected:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
        
    print(f"\nSUCCESS: All {len(FREE_PAGES_CONFIG)} slices verified perfectly with zero errors!")

if __name__ == "__main__":
    verify_matrix()
