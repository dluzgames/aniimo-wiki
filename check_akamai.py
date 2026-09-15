import re
from pathlib import Path

html = (Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site") / "index.html").read_text(encoding="utf-8")
matches = re.findall(r'https?://[^\s"\'`<>]*akamaized[^\s"\'`<>]*', html)
print("Akamai matches in index.html:")
for m in set(matches):
    print(" ", m)
