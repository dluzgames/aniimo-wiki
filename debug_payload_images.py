import json
import re

# Inspect site/_payload.json
payload = json.loads(open(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site\_payload.json", "r", encoding="utf-8").read())

print("Total elements in site/_payload.json:", len(payload))
image_urls = []
for i, item in enumerate(payload):
    if isinstance(item, str) and ("Wiki_Aniimo" in item or "/cdn/" in item or "worldx" in item):
        image_urls.append((i, item))

print(f"Found {len(image_urls)} image references in _payload.json. First 10:")
for idx, u in image_urls[:10]:
    print(f" [{idx}]: {u}")

# Also check index.html Nuxt data
html = open(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site\index.html", "r", encoding="utf-8").read()
m = re.search(r'<script[^>]+id="__NUXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
if m:
    nuxt_data = json.loads(m.group(1))
    print(f"\nTotal elements in index.html __NUXT_DATA__: {len(nuxt_data)}")
    nuxt_images = []
    for i, item in enumerate(nuxt_data):
        if isinstance(item, str) and ("Wiki_Aniimo" in item or "/cdn/" in item or "worldx" in item):
            nuxt_images.append((i, item))
    print(f"Found {len(nuxt_images)} image references in __NUXT_DATA__. First 10:")
    for idx, u in nuxt_images[:10]:
        print(f" [{idx}]: {u}")
