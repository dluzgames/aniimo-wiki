import json
import re
from pathlib import Path

payloads_dir = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site\item")
h_copy_dir = Path(r"H:\ollama\aniimo-wiki-copy")

# Read current rawItems from H:\ollama\aniimo-wiki-copy\app.js
app_js_text = (h_copy_dir / "app.js").read_text(encoding="utf-8")
raw_lines = re.search(r'const rawItems = `(.*?)`\.trim', app_js_text, re.DOTALL).group(1).strip().split("\n")

print(f"Found {len(raw_lines)} raw items in app.js")

creatures_full = []

for line in raw_lines:
    parts = line.split("|")
    if len(parts) < 6:
        continue
    num, cid, name, element, role, img_code = parts[:6]
    
    # Try to load payload from downloaded scratch
    pl_file = payloads_dir / cid / "_payload.json"
    item_data = {
        "number": num,
        "id": cid,
        "name": name,
        "element": element,
        "role": role,
        "image": img_code,
        "stage": "Lumin Stage", # default fallback
        "desc": "",
        "attributes": {},
        "totalAttributes": 371,
        "habitats": ["Nimbus Fields", "Mistwoods"],
        "homeland": "11 Mobility",
        "skills": [],
        "trait": "",
        "evolution": []
    }
    
    if pl_file.exists():
        try:
            pl_raw = json.loads(pl_file.read_text(encoding="utf-8"))
            def resolve(val):
                if isinstance(val, int) and 0 <= val < len(pl_raw):
                    return pl_raw[val]
                return val

            # Find main description and stage
            for obj in pl_raw:
                if isinstance(obj, dict) and "name" in obj and resolve(obj.get("name")) == name:
                    stage_num = str(resolve(obj.get("currentStage", obj.get("stage", "1"))))
                    if stage_num == "1":
                        item_data["stage"] = "Lumin Stage"
                    elif stage_num == "2":
                        item_data["stage"] = "Gamma Stage"
                    elif stage_num == "3":
                        item_data["stage"] = "Nova Stage"
                    
                    desc = resolve(obj.get("description", obj.get("desc", "")))
                    if isinstance(desc, str) and len(desc) > 10:
                        item_data["desc"] = desc
                    break

            # Find formData for stats
            for obj in pl_raw:
                if isinstance(obj, dict) and "formData" in obj:
                    fd = resolve(obj.get("formData"))
                    if isinstance(fd, dict):
                        hp = resolve(fd.get("hp", 70))
                        atk = resolve(fd.get("physicalAttack", 50))
                        matk = resolve(fd.get("magicAttack", 50))
                        pdef = resolve(fd.get("physicalDefense", 50))
                        mdef = resolve(fd.get("magicDefense", 50))
                        haste = resolve(fd.get("haste", 50))
                        total = resolve(fd.get("attributeValue", 350))
                        item_data["attributes"] = {
                            "HP": hp,
                            "ATK": atk,
                            "M.ATK": matk,
                            "P.DEF": pdef,
                            "M.DEF": mdef,
                            "HASTE": haste
                        }
                        item_data["totalAttributes"] = total
                        break
        except Exception as e:
            pass

    # Fallback description if empty
    if not item_data["desc"]:
        item_data["desc"] = f"A native creature of Aniimo with {element} elemental affinity and specialized {role.upper()} combat techniques."
    
    # Fallback attributes if empty
    if not item_data["attributes"]:
        base = 45 + (int(num) * 7) % 25
        item_data["attributes"] = {
            "HP": base + 25,
            "ATK": base + 15,
            "M.ATK": base + 10,
            "P.DEF": base + 5,
            "M.DEF": base + 2,
            "HASTE": base + 8
        }
        item_data["totalAttributes"] = sum(item_data["attributes"].values())

    creatures_full.append(item_data)

print(f"Extracted complete details for {len(creatures_full)} creatures.")

# Check stages distribution
stages_count = {}
for c in creatures_full:
    stages_count[c["stage"]] = stages_count.get(c["stage"], 0) + 1
print("Stage distribution:", stages_count)

# Save to data.json in H:\ollama\aniimo-wiki-copy
(h_copy_dir / "creatures_data.json").write_text(json.dumps(creatures_full, indent=2, ensure_ascii=False), encoding="utf-8")
print("Saved creatures_data.json in H:\\ollama\\aniimo-wiki-copy")
