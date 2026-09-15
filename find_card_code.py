from pathlib import Path
import re

nuxt_dir = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site\_nuxt")

for f in nuxt_dir.glob("*.js"):
    text = f.read_text(encoding="utf-8", errors="ignore")
    if "aniimo-item-top-image" in text:
        print(f"Found in {f.name} (length {len(text)})")
        idx = text.find("aniimo-item-top-image")
        start = max(0, idx - 500)
        end = min(len(text), idx + 800)
        print("SNIPPET:")
        print(text[start:end])
