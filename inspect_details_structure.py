import json
from pathlib import Path

payload_path = Path(r"C:\Users\dluzgg\.gemini\antigravity\scratch\aniimo-wiki\site\item\10002688\_payload.json")
data = json.loads(payload_path.read_text(encoding="utf-8"))

def resolve(val):
    if isinstance(val, int) and 0 <= val < len(data):
        return data[val]
    return val

# Print top-level keys or structures
print("Total entries in payload:", len(data))
# Search for skill, homeland, habitat, attributes
for i, item in enumerate(data[:100]):
    if isinstance(item, dict):
        print(f"[{i}]: dict keys -> {list(item.keys())}")
    elif isinstance(item, str) and len(item) < 80:
        if any(k in item.lower() for k in ["homeland", "mobility", "habitat", "evolution", "skill", "trait"]):
            print(f"[{i}]: string -> {item}")
