from pathlib import Path
import re

html = (Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site") / "index.html").read_text(encoding="utf-8")
for m in re.finditer(r'.{0,50}kg-web-cdn\.akamaized\.net.{0,50}', html):
    print(m.group(0))
