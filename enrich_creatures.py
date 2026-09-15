import json
from pathlib import Path

# Load creatures_data.json
h_copy = Path(r"H:\ollama\aniimo-wiki-copy")
creatures = json.loads((h_copy / "creatures_data.json").read_text(encoding="utf-8"))

# Define canonical evolution chains
# Each chain is a list of creature numbers or names
evolution_chains = [
    ["001", "002", "003", "004"], # Emberpup -> Flameruff -> Scorchhowl -> Inferlupa
    ["005", "006"],               # Celestis -> Stellarys
    ["007", "008", "009", "010"], # Chirpi -> Tromber -> Cornet -> Tubster
    ["011", "012"],               # Iris -> Irisal
    ["014", "015", "016", "017"], # Skippy -> Pranky -> Glacy -> Leafy
    ["018", "019", "020"],        # Nimbi -> Turbo -> Dreaple
    ["021", "022", "023"],        # Hummin -> Witchin -> Tuckin
    ["024", "025", "026"],        # Budclaw -> Shrubclaw -> Geoclaw
    ["027", "028"],               # Sparki -> Flamerion
    ["029", "030", "031"],        # Flutternym -> Gracewing -> Somniwing
    ["032", "033"],               # Eko -> Eklue
    ["034", "035", "036"],        # Budsquire -> Thornblade -> Melloblum
    ["037", "038", "039"],        # Pomegg -> Dazmand -> Pomawk
    ["040", "041"],               # Dewy -> Fragrancier
    ["042", "043", "044"],        # Wisptis -> Ignitis -> Fulmintis
    ["045", "046", "047"],        # Bonesky -> Fenrier -> Glynsera
    ["048", "049"],               # Bolty -> Blazen
    ["050", "051", "052", "053"], # Susuta -> Popota -> Piopiota -> Panpanta
    ["054", "055", "056"],        # Shelly -> Sheldon -> Sherro
    ["057", "058", "059"],        # Baleetle -> Waleetle -> Bouldus
    ["060", "061"],               # Fentuft -> Fenmane
    ["062", "063", "064", "065", "066", "067", "068"], # Helmut branch
    ["069", "070"],               # Cubbo -> Grizbo
    ["071", "072", "073", "074", "075"], # Pebbling branch
    ["076", "077"],               # Cozite -> Bailite
    ["078", "079", "080"],        # Bulbly -> Veilfloat -> Luminelle
    ["081", "082"],               # Fahloo -> Erlath
    ["083"],                      # Besauce
    ["084", "085"],               # Reefish -> Coraliz
    ["086", "087"],               # Cheekie -> Wavwal
    ["088", "089"],               # Bubbeep -> Glameep
    ["090", "091"],               # Popapus -> Gachapus
    ["092", "093"],               # Malangel -> Malevsera
    ["9997"],                     # Fennelun
    ["9998"]                      # Helion
]

num_to_creature = {c["number"]: c for c in creatures}
id_to_creature = {c["id"]: c for c in creatures}

# Link evolution and related forms
for chain in evolution_chains:
    chain_creatures = [num_to_creature[n] for n in chain if n in num_to_creature]
    for c in chain_creatures:
        c["relatedIds"] = [x["id"] for x in chain_creatures]
        c["evolutionPath"] = [
            {"id": x["id"], "number": x["number"], "name": x["name"], "stage": x["stage"], "image": x["image"]}
            for x in chain_creatures
        ]

# Ensure any unlinked creature links to itself
for c in creatures:
    if "relatedIds" not in c:
        c["relatedIds"] = [c["id"]]
        c["evolutionPath"] = [{"id": c["id"], "number": c["number"], "name": c["name"], "stage": c["stage"], "image": c["image"]}]

# Habitats distribution by element
habitat_map = {
    "fire": ["Volcanic Caldera", "Scorched Plateau", "Echoback Landing", "Cinder Valley"],
    "water": ["Azure Shoals", "Mistwoods Lagoon", "The Argent Strait", "Coral Abyss"],
    "grass": ["Nimbus Fields", "Verdant Canopy", "Whispering Grove", "Flora Reach"],
    "electric": ["Thunder Peak", "Echoback Landing", "Lightning Crag", "Stormy Bluffs"],
    "ice": ["Frostbite Ridge", "Glacier Crest", "Frozen Taiga", "Permafrost Valley"],
    "wind": ["Highland Peaks", "Breezy Steppe", "The Argent Strait", "Skyward Isle"],
    "dark": ["Twilight Ruins", "Umbral Hollow", "Shadowed Vale", "Beast Fang Ridge"],
    "holy": ["Sunlit Sanctuary", "Astral Ridge", "Luminous Pinnacle", "Sacred Crest"],
    "rock": ["Beast Fang Ridge", "Obsidian Quarry", "Granite Canyon", "Stony Bastion"]
}

# Homeland ability by role
homeland_map = {
    "dps": ["12 Mobility", "Combat Instinct"],
    "break": ["14 Crushing", "Rock Shatter"],
    "heal": ["10 Gathering", "Herbal Foraging"],
    "sup": ["11 Mobility", "Target Tracking"],
    "energy": ["13 Lumbering", "Resonance Beacon"]
}

# Skill sets by element
skill_templates = {
    "fire": [
        {"name": "Flame Strike", "type": "Physical", "cost": 0, "power": 75, "desc": "Lashes out with burning claws, dealing Fire damage to the target."},
        {"name": "Blazing Nova", "type": "Magic", "cost": 15, "power": 120, "desc": "Unleashes a surge of intense heat that scorches all nearby foes."},
        {"trait": "Kindled Fury", "desc": "Increases Fire damage by 20% when facing foes weak to Fire."}
    ],
    "water": [
        {"name": "Aqua Jet", "type": "Magic", "cost": 0, "power": 70, "desc": "Fires a concentrated pressurized stream of water at high velocity."},
        {"name": "Surging Torrent", "type": "Magic", "cost": 12, "power": 110, "desc": "Conjures a tidal rush that restores allies and pushes back enemies."},
        {"trait": "Aquatic Harmony", "desc": "Heals the party for 5% max HP when triggering an elemental reaction."}
    ],
    "grass": [
        {"name": "Vine Whip", "type": "Physical", "cost": 0, "power": 72, "desc": "Strikes fiercely with hardened floral vines."},
        {"name": "Verdant Bloom", "type": "Magic", "cost": 10, "power": 105, "desc": "Sprouts radiant flora that saps enemy defenses and grants Regen."},
        {"trait": "Photosynthesis", "desc": "Regenerates energy over time while in sunlit or grassy terrain."}
    ],
    "electric": [
        {"name": "Volt Jab", "type": "Physical", "cost": 0, "power": 78, "desc": "Discharges an electric punch that shocks the opponent."},
        {"name": "Thunderstorm Wrath", "type": "Magic", "cost": 18, "power": 130, "desc": "Calls down a devastating lightning strike from above."},
        {"trait": "Static Charge", "desc": "Has a 25% chance to paralyze the attacker on contact."}
    ],
    "ice": [
        {"name": "Frost Fang", "type": "Physical", "cost": 0, "power": 74, "desc": "Bites with freezing fangs, lowering the enemy's move speed."},
        {"name": "Glacial Blizzard", "type": "Magic", "cost": 14, "power": 115, "desc": "Freezes the battlefield in a harsh howling blizzard."},
        {"trait": "Permafrost Shield", "desc": "Reduces incoming Physical and Magic damage by 15%."}
    ],
    "wind": [
        {"name": "Gale Slash", "type": "Physical", "cost": 0, "power": 73, "desc": "Slices forward with razor-sharp gusts of compressed wind."},
        {"name": "Cyclone Spiral", "type": "Magic", "cost": 12, "power": 108, "desc": "Spins into a whirlwind that lifts and scatters enemy formations."},
        {"trait": "Tailwind Grace", "desc": "Increases haste and evasion for the entire squad."}
    ],
    "dark": [
        {"name": "Shadow Bite", "type": "Physical", "cost": 0, "power": 76, "desc": "Engulfs the target in shadows, inflicting Break damage."},
        {"name": "Abyssal Rift", "type": "Magic", "cost": 16, "power": 125, "desc": "Opens a dark vortex that consumes enemy buffs."},
        {"trait": "Nightfall Stalker", "desc": "Increases Critical Strike rate by 25% during combat."}
    ],
    "holy": [
        {"name": "Luminous Beam", "type": "Magic", "cost": 0, "power": 80, "desc": "Channels sacred light to pierce through enemy barriers."},
        {"name": "Astral Judgement", "type": "Magic", "cost": 20, "power": 140, "desc": "Summons celestial stars to smite darkness across the area."},
        {"trait": "Divine Resonance", "desc": "Grants complete immunity to debuffs for 5 seconds upon entry."}
    ],
    "rock": [
        {"name": "Boulder Crash", "type": "Physical", "cost": 0, "power": 82, "desc": "Slams with stony mass, dealing massive Break damage."},
        {"name": "Terra Tremor", "type": "Physical", "cost": 15, "power": 120, "desc": "Shatters the ground below, staggering all surrounding foes."},
        {"trait": "Solid Bastion", "desc": "Grants high resistance against staggering and knockdown."}
    ]
}

for c in creatures:
    elem = c["element"].lower()
    role = c["role"].lower()
    c["habitats"] = habitat_map.get(elem, ["Nimbus Fields", "Beast Fang Ridge"])
    c["homeland"] = homeland_map.get(role, ["11 Mobility", "Exploration"])[0]
    c["homelandType"] = homeland_map.get(role, ["11 Mobility", "Exploration"])[1]
    
    st = skill_templates.get(elem, skill_templates["fire"])
    c["skills"] = [
        {"name": st[0]["name"], "type": st[0]["type"], "cost": st[0]["cost"], "power": st[0]["power"], "desc": st[0]["desc"]},
        {"name": f"{c['name']} {st[1]['name']}", "type": st[1]["type"], "cost": st[1]["cost"], "power": st[1]["power"], "desc": st[1]["desc"]}
    ]
    c["trait"] = {"name": st[2]["trait"], "desc": st[2]["desc"]}

print("Sample creature with full data:")
print(json.dumps(creatures[0], indent=2))

(h_copy / "creatures_full.json").write_text(json.dumps(creatures, indent=2, ensure_ascii=False), encoding="utf-8")
print("Saved creatures_full.json in H:\\ollama\\aniimo-wiki-copy")
