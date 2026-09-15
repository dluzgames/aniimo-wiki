import json
from pathlib import Path

h_copy = Path(r"H:\ollama\aniimo-wiki-copy")
data = json.loads((h_copy / "creatures_data.json").read_text(encoding="utf-8"))

missing = []
for c in data:
    img_name = "Wiki_Aniimo_" + str(c["image"]) + ".png"
    img_path = h_copy / "assets" / "creatures" / img_name
    if not img_path.exists():
        missing.append(img_name)

print(f"Total creatures: {len(data)}")
print(f"Missing images: {len(missing)}")
if not missing:
    print("✅ All 94 local creature images are present in H:\\ollama\\aniimo-wiki-copy\\assets\\creatures!")
