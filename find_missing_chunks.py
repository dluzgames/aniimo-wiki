from pathlib import Path
import re

nuxt_dir = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site\_nuxt")

all_js = set()
for f in nuxt_dir.glob("*.js"):
    text = f.read_text(encoding="utf-8", errors="ignore")
    matches = re.findall(r'([a-zA-Z0-9_-]{5,20}\.js)', text)
    for m in matches:
        all_js.add(m)

print(f"Total potential JS chunk names found: {len(all_js)}")
missing = []
for js in sorted(list(all_js)):
    local = nuxt_dir / js
    if not local.exists():
        missing.append(js)

print(f"Missing JS files: {len(missing)}")
for m in missing[:30]:
    print("  ->", m)
