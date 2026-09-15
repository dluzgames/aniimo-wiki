import urllib.request
import json
import re

# Fetch live wiki.aniimo.com
html_live = urllib.request.urlopen(urllib.request.Request("https://wiki.aniimo.com/", headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8")
m_live = re.search(r'<script[^>]+id="__NUXT_DATA__"[^>]*>(.*?)</script>', html_live, re.DOTALL)
live_data = json.loads(m_live.group(1))
print("Live __NUXT_DATA__ count:", len(live_data))

# Fetch live _payload.json
pl_live = json.loads(urllib.request.urlopen(urllib.request.Request("https://wiki.aniimo.com/_payload.json", headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8"))
print("Live _payload.json count:", len(pl_live))
