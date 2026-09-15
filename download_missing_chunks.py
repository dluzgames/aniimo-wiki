import urllib.request
from pathlib import Path
import re

AKAMAI_BASE = "https://kg-web-cdn.akamaized.net/master/worldx/wiki-frontend/_nuxt"
WIKI_BASE = "https://wiki.aniimo.com"

NUXT_DIR = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site\_nuxt")
SITE_DIR = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site")

chunks_to_try = [
    "BOgH26SG.js",
    "Bnv3wCaE.js",
    "BwIWVvy6.js",
    "CGMV5hdQ.js",
    "DPJjYUI-.js",
    "DQpwj2T7.js",
    "DpHUHgHl.js",
    "DyK3sV5L.js",
    "YLXfFP3I.js"
]

# 1. Download missing JS chunks
for chunk in chunks_to_try:
    dest = NUXT_DIR / chunk
    if not dest.exists():
        url = f"{AKAMAI_BASE}/{chunk}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                dest.write_bytes(data)
                print(f"✅ Downloaded {chunk} ({len(data)} bytes)")
        except Exception as e:
            print(f"❌ Failed to download {chunk}: {e}")

# 2. Download _i18n message bundles
locales = ["en", "ja", "ko", "tw", "zh"]
for loc in locales:
    dest = SITE_DIR / "_i18n" / "OTeKV1Z6" / loc / "messages.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"{WIKI_BASE}/_i18n/OTeKV1Z6/{loc}/messages.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            dest.write_bytes(data)
            print(f"✅ Downloaded _i18n messages for {loc} ({len(data)} bytes)")
    except Exception as e:
        print(f"❌ Failed _i18n for {loc}: {e}")

# 3. Check if newly downloaded JS chunks reference even more chunks!
new_js = set()
for chunk in chunks_to_try:
    dest = NUXT_DIR / chunk
    if dest.exists():
        text = dest.read_text(encoding="utf-8", errors="ignore")
        for m in re.findall(r'([a-zA-Z0-9_-]{5,20}\.js)', text):
            new_js.add(m)

more_missing = [m for m in new_js if not (NUXT_DIR / m).exists()]
print(f"\nMore missing chunks found: {len(more_missing)}")
for m in more_missing:
    url = f"{AKAMAI_BASE}/{m}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            (NUXT_DIR / m).write_bytes(data)
            print(f"✅ Downloaded {m} ({len(data)} bytes)")
    except Exception as e:
        pass
