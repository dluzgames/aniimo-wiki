from pathlib import Path

js_path = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site\_nuxt\gHvmXFGl.js")
text = js_path.read_text(encoding="utf-8")

idx = text.find("return(o,d)=>{const k=ne;return i(),O(k,")
print("=== RENDER FUNCTION ===")
print(text[idx:idx+1500])
