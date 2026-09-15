import json
import re
from pathlib import Path

h_copy = Path(r"H:\ollama\aniimo-wiki-copy")
creatures = json.loads((h_copy / "creatures_full.json").read_text(encoding="utf-8"))

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

# Translations dictionary for UI & lore
translations_pt = {
    # Elements
    "elements": {
        "all": "Todos",
        "holy": "Sagrado",
        "fire": "Fogo",
        "ice": "Gelo",
        "dark": "Sombra",
        "electric": "Elétrico",
        "grass": "Planta",
        "water": "Água",
        "rock": "Rocha",
        "wind": "Vento"
    },
    # Roles
    "roles": {
        "all": "Todas",
        "dps": "Dano (DPS)",
        "heal": "Cura",
        "sup": "Suporte",
        "break": "Quebra",
        "energy": "Regeneração"
    },
    # Stages
    "stages": {
        "all": "Todos",
        "Lumin Stage": "Estágio Lumin",
        "Gamma Stage": "Estágio Gamma",
        "Nova Stage": "Estágio Nova"
    },
    # UI labels
    "ui": {
        "search_placeholder": "Buscar por nome ou número...",
        "elements_label": "Elementos:",
        "roles_label": "Funções:",
        "stage_label": "Estágios:",
        "sort_no_asc": "Ordenar por Nº (Crescente)",
        "sort_no_desc": "Ordenar por Nº (Decrescente)",
        "sort_name_asc": "Ordenar por Nome (A-Z)",
        "sort_name_desc": "Ordenar por Nome (Z-A)",
        "showing": "Exibindo",
        "of": "de",
        "aniimos": "Aniimos",
        "empty_title": "Nenhum Aniimo encontrado com esses filtros.",
        "reset_filters": "Limpar Filtros",
        "back_to_wiki": "‹ Voltar para a Wiki",
        "prev": "‹ Anterior",
        "next": "Próximo ›",
        "overview": "Visão Geral",
        "attributes_total": "Total de Atributos:",
        "related_forms": "Formas Relacionadas:",
        "evolution_path": "Caminho de Evolução",
        "habitats": "Habitats",
        "homeland_ability": "Habilidade de Território",
        "skill_details": "Detalhes das Habilidades",
        "passive_trait": "Característica Passiva:",
        "physical": "Físico",
        "magic": "Mágico",
        "cost": "Custo",
        "power": "Poder"
    }
}

# Translate habitats
habitats_pt = {
    "Volcanic Caldera": "Caldeira Vulcânica",
    "Scorched Plateau": "Planalto Chamuscado",
    "Echoback Landing": "Pouso do Eco",
    "Cinder Valley": "Vale das Cinzas",
    "Azure Shoals": "Baixios Azuis",
    "Mistwoods Lagoon": "Lagoa da Floresta das Névoas",
    "The Argent Strait": "Estreito de Prata",
    "Coral Abyss": "Abismo de Coral",
    "Nimbus Fields": "Campos de Nimbos",
    "Verdant Canopy": "Dossel Verdejante",
    "Whispering Grove": "Bosque dos Sussurros",
    "Flora Reach": "Recanto da Flora",
    "Thunder Peak": "Pico do Trovão",
    "Lightning Crag": "Penhasco dos Raios",
    "Stormy Bluffs": "Escarpa Tempestuosa",
    "Frostbite Ridge": "Crista da Congelação",
    "Glacier Crest": "Cume Glacial",
    "Frozen Taiga": "Taiga Congelada",
    "Permafrost Valley": "Vale do Permafrost",
    "Highland Peaks": "Picos das Terras Altas",
    "Breezy Steppe": "Estepe Arejada",
    "Skyward Isle": "Ilha Celeste",
    "Twilight Ruins": "Ruínas do Crepúsculo",
    "Umbral Hollow": "Cova Umbrática",
    "Shadowed Vale": "Vale Sombrio",
    "Beast Fang Ridge": "Cordilheira Presa da Fera",
    "Sunlit Sanctuary": "Santuário Ensolarado",
    "Astral Ridge": "Cume Astral",
    "Luminous Pinnacle": "Pináculo Luminoso",
    "Sacred Crest": "Crista Sagrada",
    "Obsidian Quarry": "Pedreira de Obsidiana",
    "Granite Canyon": "Cânion de Granito",
    "Stony Bastion": "Bastião Pedregoso"
}

# Translate Homeland types
homeland_pt = {
    "12 Mobility": "12 Mobilidade",
    "Combat Instinct": "Instinto de Combate",
    "14 Crushing": "14 Esmagamento",
    "Rock Shatter": "Quebra-Rochas",
    "10 Gathering": "10 Coleta",
    "Herbal Foraging": "Colheita de Ervas",
    "11 Mobility": "11 Mobilidade",
    "Target Tracking": "Rastreamento de Alvos",
    "13 Lumbering": "13 Corte de Lenha",
    "Resonance Beacon": "Farol de Ressonância",
    "Exploration": "Exploração Avançada"
}

# Descriptions translations dictionary
desc_pt_map = {
    "Emberpup": "Criaturas animadas que adoram seguir os Flameruffs. Quando sua pelagem fumegante começa a queimar, tornam-se incrivelmente ativas e velozes.",
    "Flameruff": "Um Aniimo leal cuja juba arde com chamas contínuas. Protege ferozmente seu bando e domina ataques físicos de fogo.",
    "Scorchhowl": "Uiva para inflamar as chamas ao seu redor. Sua temperatura corporal pode derreter rochas quando entra em frenesi de batalha.",
    "Inferlupa": "Um Flameruff veterano que desafiou os mais fortes e sobreviveu, absorvendo a essência ardente de seus companheiros caídos. Move-se com fúria implacável.",
    "Celestis": "Uma criatura enigmática envolta em sombras estelares. Move-se silenciosamente pela escuridão absorvendo energia cósmica.",
    "Stellarys": "Possui orbes celestiais que brilham fracamente sob a noite. Dizem que seus ataques distorcem o próprio tecido das sombras.",
    "Chirpi": "Pequeno pássaro dos ventos que flutua nas correntes de ar. Emite melodias cristalinas que acalmam seus aliados.",
    "Tromber": "Seu bico ressonante amplifica rajadas de vento poderosas, capazes de desorientar predadores a longas distâncias.",
    "Cornet": "Voa em espirais cortantes com precisão milimétrica. Usa o vento para acelerar seus ataques até que se tornem invisíveis ao olho humano.",
    "Tubster": "Um defensor pesado dos céus. Suas asas criam barreiras de pressão atmosférica que barram até os projéteis mais densos.",
    "Iris": "Um ser floral delicado que floresce em solo fértil. Libera pólen curativo e chicotes vegetais velozes.",
    "Irisal": "A forma evoluída de Iris, com pétalas laminadas capazes de desferir cortes precisos de energia vegetal.",
    "Skippy": "Saltador aquático ágil que navega pelos baixios com facilidade. Suas bolhas refrescantes restauram as forças da equipe.",
    "Pranky": "Travesso e brincalhão, usa jatos de água inesperados para desestabilizar adversários enquanto cura seus companheiros.",
    "Glacy": "Uma criatura límpida cujas águas começam a se cristalizar em gelo puro, concedendo bênçãos regenerativas.",
    "Leafy": "Possui uma cauda com folhas largas que absorvem luz solar pura, convertendo-a em energia vital contínua.",
    "Nimbi": "Nuvem viva e graciosa que paira sobre colinas. Gera brisas suaves que amplificam a mobilidade de seus aliados.",
    "Turbo": "Acelera as correntes de ar ao seu redor, criando vórtices que impulsionam companheiros e afastam ameaças.",
    "Dreaple": "Um espírito sombrio dos ventos que desvia a atenção dos adversários com ilusões de névoa e sombras.",
    "Hummin": "Um pequeno colibri veloz que bate as asas com frequência ensurdecedora, quebrando a guarda de oponentes.",
    "Witchin": "Canaliza magia obscura das florestas antigas para drenar a vitalidade de inimigos desavisados.",
    "Tuckin": "Enrola-se em uma couraça impenetrável de cipós rígidos para absorver impactos devastadores.",
    "Budclaw.": "Possui garras pétreas que perfuram minerais densos. Escava túneis com facilidade invejável.",
    "Shrubclaw": "Garras revestidas de raízes fossilizadas. Desfere golpes pesados que quebram escudos rochosos.",
    "Geoclaw": "Seu corpo cristalizou-se em gelo e pedra, transformando-o em uma força avassaladora de quebra de guarda.",
    "Sparki": "Chispas incandescentes pulsam em seu dorso. Gera energia térmica abundante em qualquer clima.",
    "Flamerion": "Uma fera de pura brasa cujos rugidos liberam ondas de calor que abastecem os poderes dos aliados.",
    "Flutternym": "Borboleta etérea que dispersa orvalho suave, trazendo tranquilidade e cura profunda para quem está próximo.",
    "Gracewing": "Asas translúcidas que refratam a luz, criando auras calmantes que aceleram a regeneração de ferimentos.",
    "Somniwing": "Suas asas induzem um transe tranquilo, restaurando continuamente o foco e a energia de todo o time.",
    "Eko": "Curioso e atento a rastros e pistas. Consegue captar vibrações ultrassônicas à distância.",
    "Eklue": "O anel em sua cauda amplifica ondas ultrassônicas, revelando a localização de qualquer inimigo oculto.",
    "Budsquire": "Jovem guerreiro botânico que empunha galhos afiados com postura impecável e disciplina marcial.",
    "Thornblade": "Suas lâminas de espinhos cortam com veneno vegetal, punindo qualquer um que se aproxime.",
    "Melloblum": "Guardião sereno que projeta barreiras de pétalas aromáticas para proteger os mais jovens do grupo.",
    "Pomegg": "Semente protegida por casca ultrarresistente. Rebota contra agressores para interromper seus ataques.",
    "Dazmand": "Carregado de estática pulsante, atrai descargas elétricas para alimentar as habilidades da equipe.",
    "Pomawk": "A forma final da semente, agora uma árvore robusta com espinhos de combate para demolição de defesas.",
    "Dewy": "Gotas escuras condensam-se em seu corpo, gerando campos gravitacionais sutis que auxiliam a equipe.",
    "Fragrancier": "Exala perfumes exóticos das sombras que confundem sentidos e reduzem a precisão inimiga.",
    "Wisptis": "Fogo-fátuo espectral que vagueia por noites escuras atacando com labaredas sombrias.",
    "Ignitis": "Suas labaredas negras ardem mesmo submersas, consumindo as defesas mágicas dos alvos.",
    "Fulmintis": "Fundiu a sombra ao relâmpago, disparando trovões negros que cortam o campo de batalha.",
    "Bonesky": "Um filhote enérgico com orelhas pontiagudas e um laço de osso congelado no peito. Odeia quem invade seu espaço pessoal.",
    "Fenrier": "Lobo ártico imponente cujo sopro congela a relva. Lidera caçadas nas neves eternas.",
    "Glynsera": "Monarca do gelo cujos olhos congelam o coração dos invasores com apenas um olhar sereno.",
    "Bolty": "Cheio de centelhas e curiosidade, salta contra oponentes quebrando escudos com estática intensa.",
    "Blazen": "Descargas voltaicas percorrem seu corpo veloz, rompendo barreiras defensivas em segundos.",
    "Susuta": "Pequeno ser aquático anfíbio que suporta pressões submarinas extremas.",
    "Popota": "Expele bolhas de alta pressão capazes de rachar rochas sedimentares e proteger seu refúgio.",
    "Piopiota": "Navega suavemente nas profundezas marinhas guiando seus companheiros com luzes bioluminescentes.",
    "Panpanta": "Guerreiro couraçado dos mares, suas investidas quebram as defesas mais resistentes.",
    "Shelly": "Carrega uma concha iridescente afiada que usa como projétil nos recifes de coral.",
    "Sheldon": "Concha reforçada por madrepérola impenetrável. Lança rajadas cortantes de água a grande distância.",
    "Sherro": "Guerreiro temível dos oceanos cujos dardos perfuram o casco de navios antigos.",
    "Baleetle": "Besouro com carapaça de arenito resistente. Usa chifres pesados para investidas contundentes.",
    "Waleetle": "Suas placas rochosas suportam quedas de desfiladeiros sem sofrer um único arranhão.",
    "Bouldus": "Montanha ambulante em miniatura, ancora-se no chão para apoiar a linha de frente.",
    "Fentuft": "Pelagem felpuda que acumula eletricidade estática até explodir em faíscas velozes.",
    "Fenmane": "Leão elétrico de juba dourada. Cada salto gera estrondos de trovão no horizonte.",
    "Helmut": "Usa um elmo antigo encontrado em ruínas. Bate a cabeça com determinação inabalável.",
    "Pawney": "Pequeno estrategista de sombras que calcula cada movimento antes de dar o bote fatal.",
    "Rookey": "Torre sólida de escuridão que avança em linha reta desmantelando posições inimigas.",
    "Jawling": "Mandíbulas de vento que mordem o ar criando vórtices cortantes ao redor dos alvos.",
    "Helmwhelp": "Jovem dragão encouraçado que testa a resistência de seus chifres contra rochas gigantes.",
    "Helgon": "Dragão alado dos vendavais que destrói fortificações com investidas aéreas maciças.",
    "Infergon": "A lendária forma dragônica de fogo, cujas asas flamejantes incendeiam montanhas inteiras.",
    "Cubbo": "Ursinho rechonchudo de pedra que rola pelas colinas quebrando galhos e rochas.",
    "Grizbo": "Urso das cavernas gigantesco que despedaça blocos de granito com patadas sísmicas.",
    "Pebbling": "Seixo vivo que se agrupa em desmoronamentos para afastar intrusos de sua mina natal.",
    "Lavazar": "Magma incandescente escorre por suas fissuras, quebrando resistências com calor extremo.",
    "Magmarex": "Rei dos fluxos piroclásticos, pisa no chão transformando pedra em lava derretida.",
    "Geodeback": "Suas costas abrigam cristais reluzentes de quartzo que desviam golpes de impacto.",
    "Minespine": "Espinhos de minério puro brotam de sua espinha para perfurar qualquer agressor.",
    "Cozite": "Pequeno cristal flutuante que emite frequências harmônicas reconfortantes para aliados.",
    "Bailite": "Bateria mineral orgânica que estabiliza o fluxo de mana e fortalece ataques amigos.",
    "Bulbly": "Globo luminoso que levita emitindo sinais elétricos suaves pela penumbra.",
    "Veilfloat": "Medusa aérea que canaliza energia estática para erguer campos de força protetores.",
    "Luminelle": "Lanterna celestial dos céus que ilumina áreas inteiras com bênçãos elétricas.",
    "Fahloo": "Espírito das águas profundas que acumula mana límpida para recarregar aliados.",
    "Erlath": "Fontanela viva que purifica e revitaliza a energia vital de todo o esquadrão.",
    "Besauce": "Gerador vivo de eletricidade constante que acelera a prontidão de habilidades da equipe.",
    "Reefish": "Peixe fóssil ancestral que nada em correntes profundas filtrando minerais vitais.",
    "Coraliz": "Recife vivo pulsante que absorve impactos e recarrega os poderes do time.",
    "Cheekie": "Foca ártica divertida que desliza no gelo quebrando barreiras com o corpo rígido.",
    "Wavwal": "Morsa imponente cujas presas de gelo quebram geleiras com um único golpe.",
    "Bubbeep": "Ovelha floral cuja lã de algodão e folhas tem propriedades cicatrizantes milagrosas.",
    "Glameep": "Lã aveludada de aroma doce que restaura grandes quantidades de vida aos companheiros.",
    "Popapus": "Polvo brincalhão que cospe tinta colorida de alta velocidade em seus oponentes.",
    "Gachapus": "Gira seus tentáculos em redemoinhos aquáticos que causam dano massivo e contínuo.",
    "Malangel": "Anjo de gelo de aura austera que dispara lanças congeladas contra o mal.",
    "Malevsera": "Soberana gélida que rege as tempestades de neve com poder destrutivo incomparável.",
    "Fennelun": "Guardiã sagrada da lua radiante que purifica corrupções com luz celestial.",
    "Helion": "Avatar solar imortal que banha o mundo em brilho sagrado e poder absoluto."
}

# Update each creature
for c in creatures:
    raw_name = c["name"].replace(".", "").strip()
    c["slug"] = slugify(raw_name)
    c["nameClean"] = raw_name
    
    # PT Lore description
    if raw_name in desc_pt_map:
        c["desc_pt"] = desc_pt_map[raw_name]
    else:
        c["desc_pt"] = f"Criatura nativa de Aniimo com afinidade para o elemento {translations_pt['elements'].get(c['element'], c['element'])} e estilo de combate focado em {translations_pt['roles'].get(c['role'], c['role'])}."

    # Habitats in PT
    c["habitats_pt"] = [habitats_pt.get(h, h) for h in c.get("habitats", [])]
    
    # Homeland in PT
    c["homeland_pt"] = homeland_pt.get(c.get("homeland", ""), c.get("homeland", ""))
    c["homelandType_pt"] = homeland_pt.get(c.get("homelandType", ""), c.get("homelandType", ""))

    # Update evolution path with slugs and clean names
    if "evolutionPath" in c:
        for node in c["evolutionPath"]:
            n_clean = node["name"].replace(".", "").strip()
            node["slug"] = slugify(n_clean)
            node["nameClean"] = n_clean

print(f"Sample creature with slug and PT data: {creatures[0]['name']} -> slug: {creatures[0]['slug']}")
inferlupa = next((c for c in creatures if c['slug'] == 'inferlupa'), None)
if inferlupa:
    print(f"Inferlupa verified: slug={inferlupa['slug']}, number={inferlupa['number']}, desc_pt={inferlupa['desc_pt'][:60]}...")

(h_copy / "creatures_pt.json").write_text(json.dumps(creatures, indent=2, ensure_ascii=False), encoding="utf-8")
print("Saved creatures_pt.json!")
