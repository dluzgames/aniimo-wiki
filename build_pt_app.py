import json
from pathlib import Path

h_copy = Path(r"H:\ollama\aniimo-wiki-copy")
creatures = json.loads((h_copy / "creatures_pt.json").read_text(encoding="utf-8"))

app_js_code = f"""// Official Aniimo Wiki - Compact Encyclopedia App
const CREATURES = {json.dumps(creatures, ensure_ascii=False)};

// Language dictionaries (Default: pt)
const I18N = {{
  pt: {{
    code: "PT",
    title_suffix: "Aniimo Wiki Brasil & Global | DLuz Games",
    search_placeholder: "Buscar criatura ou número...",
    elements_label: "Elementos:",
    roles_label: "Funções:",
    stage_label: "Estágios:",
    all: "Todos",
    all_f: "Todas",
    sort_no_asc: "Ordenar por Nº (Crescente)",
    sort_no_desc: "Ordenar por Nº (Decrescente)",
    sort_name_asc: "Ordenar por Nome (A-Z)",
    sort_name_desc: "Ordenar por Nome (Z-A)",
    showing: "Exibindo",
    of: "de",
    aniimos: "Aniimos",
    empty_title: "Nenhum Aniimo encontrado com esses filtros.",
    reset_filters: "Limpar Filtros",
    back_to_wiki: "‹ Voltar para a Wiki",
    prev: "‹ Anterior",
    next: "Próximo ›",
    overview: "Visão Geral",
    attributes_total: "Total de Atributos:",
    related_forms: "Formas Relacionadas:",
    evolution_path: "Caminho de Evolução",
    habitats: "Habitats",
    homeland_ability: "Habilidade de Território",
    skill_details: "Detalhes das Habilidades",
    passive_trait: "Característica Passiva:",
    physical: "Físico",
    magic: "Mágico",
    cost: "Custo",
    power: "Poder",
    elements: {{
      all: "Todos",
      holy: "Sagrado",
      fire: "Fogo",
      ice: "Gelo",
      dark: "Sombra",
      electric: "Elétrico",
      grass: "Planta",
      water: "Água",
      rock: "Rocha",
      wind: "Vento"
    }},
    roles: {{
      all: "Todas",
      dps: "Dano (DPS)",
      heal: "Cura",
      sup: "Suporte",
      break: "Quebra",
      energy: "Regeneração"
    }},
    stages: {{
      all: "Todos",
      "Lumin Stage": "Estágio Lumin",
      "Gamma Stage": "Estágio Gamma",
      "Nova Stage": "Estágio Nova"
    }}
  }},
  en: {{
    code: "EN",
    title_suffix: "Official Aniimo Wiki - Complete Aniimo Index",
    search_placeholder: "Search creatures by name or no...",
    elements_label: "Elements:",
    roles_label: "Roles:",
    stage_label: "Stage:",
    all: "All",
    all_f: "All",
    sort_no_asc: "Sort by No. in ascending order",
    sort_no_desc: "Sort by No. in descending order",
    sort_name_asc: "Sort by name (A-Z)",
    sort_name_desc: "Sort by name (Z-A)",
    showing: "Showing",
    of: "of",
    aniimos: "Aniimos",
    empty_title: "No Aniimos match the selected filters.",
    reset_filters: "Reset All Filters",
    back_to_wiki: "‹ Back to Wiki",
    prev: "‹ Prev",
    next: "Next ›",
    overview: "Overview",
    attributes_total: "Attributes Total:",
    related_forms: "Related Forms:",
    evolution_path: "Evolution Path",
    habitats: "Habitats",
    homeland_ability: "Homeland Ability",
    skill_details: "Skill Details",
    passive_trait: "Passive Trait:",
    physical: "Physical",
    magic: "Magic",
    cost: "Cost",
    power: "Power",
    elements: {{
      all: "All",
      holy: "Holy",
      fire: "Fire",
      ice: "Ice",
      dark: "Dark",
      electric: "Electric",
      grass: "Grass",
      water: "Water",
      rock: "Rock",
      wind: "Wind"
    }},
    roles: {{
      all: "All",
      dps: "DPS",
      heal: "Heal",
      sup: "Support",
      break: "BREAK",
      energy: "REGEN"
    }},
    stages: {{
      all: "All",
      "Lumin Stage": "Lumin Stage",
      "Gamma Stage": "Gamma Stage",
      "Nova Stage": "Nova Stage"
    }}
  }}
}};

// Language State (Default: pt)
let currentLang = localStorage.getItem("aniimo_lang") || "pt";
function t(key, subkey) {{
  const dict = I18N[currentLang] || I18N.pt;
  if (subkey && dict[key]) {{
    return dict[key][subkey] || subkey;
  }}
  return dict[key] || key;
}}

const state = {{
  search: "",
  element: "all",
  role: "all",
  stage: "all",
  sort: "number_asc"
}};

const app = document.querySelector("#app");
const searchInput = document.querySelector("#search");
const toTop = document.querySelector("#to-top");
const langButton = document.querySelector(".language-button");

const colors = {{
  holy: "#f6a93c",
  fire: "#e26161",
  ice: "#45c1d6",
  dark: "#a373d2",
  electric: "#e0c21a",
  grass: "#51b17a",
  water: "#529de7",
  rock: "#bea77b",
  wind: "#2a52be"
}};

const symbols = {{
  holy: "✚",
  fire: "♨",
  ice: "❄",
  dark: "☾",
  electric: "ϟ",
  grass: "✦",
  water: "≋",
  rock: "◆",
  wind: "◉"
}};

const creatureImage = (item) => `assets/creatures/Wiki_Aniimo_${{item.image}}.png`;

function parseRoute() {{
  // 1. Check path first: e.g. /inferlupa or /item/10002753
  const path = location.pathname.replace(/^\\/+|\\/+$/g, "").toLowerCase();
  if (path && path !== "index.html") {{
    const clean = path.replace(/^item\\//, "");
    const foundByPath = CREATURES.find((c) => c.slug === clean || c.id === clean || c.number === clean);
    if (foundByPath) return foundByPath;
  }}

  // 2. Check hash: e.g. #inferlupa or #item=10002753
  const hash = location.hash.replace(/^#\\/?/, "").toLowerCase();
  if (hash) {{
    const params = new URLSearchParams(hash.includes("=") ? hash : "");
    const target = params.get("item") || hash.replace(/^item\\//, "");
    const foundByHash = CREATURES.find((c) => c.slug === target || c.id === target || c.number === target);
    if (foundByHash) {{
      // Update cleanly to /slug via history.replaceState
      history.replaceState(null, "", "/" + foundByHash.slug);
      return foundByHash;
    }}
  }}

  return null;
}}

function navigateTo(slug) {{
  if (!slug) {{
    history.pushState(null, "", "/");
  }} else {{
    history.pushState(null, "", "/" + slug);
  }}
  render();
}}

function filteredItems() {{
  const query = state.search.trim().toLowerCase();
  const filtered = CREATURES.filter((item) => {{
    const matchesQuery = !query || 
      item.name.toLowerCase().includes(query) || 
      item.number.toLowerCase().includes(query) ||
      item.number.replace(/^0+/, "").includes(query) ||
      (item.slug && item.slug.includes(query));

    const matchesElement = state.element === "all" || item.element.toLowerCase() === state.element.toLowerCase();
    const matchesRole = state.role === "all" || item.role.toLowerCase() === state.role.toLowerCase();
    const matchesStage = state.stage === "all" || item.stage.toLowerCase() === state.stage.toLowerCase();

    return matchesQuery && matchesElement && matchesRole && matchesStage;
  }});

  return filtered.sort((a, b) => {{
    if (state.sort === "name_asc") return a.name.localeCompare(b.name);
    if (state.sort === "name_desc") return b.name.localeCompare(a.name);
    if (state.sort === "number_desc") return Number(b.number) - Number(a.number);
    return Number(a.number) - Number(b.number);
  }});
}}

function chip(group, value, label, visual) {{
  const active = state[group] === value;
  return `<button class="filter-chip" role="button" tabindex="0" data-filter-group="${{group}}" data-filter-value="${{value}}" aria-pressed="${{active}}">${{visual || ""}}${{label}}</button>`;
}}

function iconBadge(kind, text) {{
  const bg = colors[kind] || "#565673";
  return `<span class="dot" style="background:${{bg}}">${{text || symbols[kind] || "•"}}</span>`;
}}

function card(item) {{
  const elemBg = colors[item.element] || "#565673";
  const roleDisplay = item.role === "energy" ? "R" : item.role === "sup" ? "S" : item.role.slice(0, 1).toUpperCase();
  const elemName = t("elements", item.element);
  const roleName = t("roles", item.role);

  return `<a class="creature-card" href="/${{item.slug}}" data-slug="${{item.slug}}" aria-label="NO.${{item.number}} ${{item.name}}" tabindex="0">
    <div class="creature-image">
      <span class="creature-number">NO.${{item.number}}</span>
      <img src="${{creatureImage(item)}}" alt="${{item.name}}" loading="lazy" width="134" height="134">
      <div class="badges">
        <span class="badge" style="background:${{elemBg}}" title="${{t('elements_label')}} ${{elemName}}">${{symbols[item.element] || "•"}}</span>
        <span class="badge" style="background:#3d3d51" title="${{t('roles_label')}} ${{roleName}}">${{roleDisplay}}</span>
      </div>
    </div>
    <span class="creature-name">${{item.name}}</span>
  </a>`;
}}

function renderIndex() {{
  const items = filteredItems();
  
  if (searchInput) {{
    searchInput.placeholder = t("search_placeholder");
  }}
  if (langButton) {{
    langButton.innerHTML = currentLang === "pt" ? "🇧🇷 PT" : "🇺🇸 EN";
  }}

  app.innerHTML = `<section class="wiki-panel">
    <div class="panel-content">
      <div class="panel-header">
        <h1>Aniimo Wiki</h1>
        <button class="collapse-button" type="button" aria-label="Toggle filters" title="Expand / Collapse filters">⌃</button>
      </div>
      
      <div class="filters">
        <div class="filter-row">
          <span class="filter-label">${{t("elements_label")}}</span>
          ${{chip("element", "all", t("all"), iconBadge("all", "•"))}}
          ${{["holy", "fire", "ice", "dark", "electric", "grass", "water", "rock", "wind"].map((e) => chip("element", e, t("elements", e), iconBadge(e))).join("")}}
        </div>
        
        <div class="filter-row">
          <span class="filter-label">${{t("roles_label")}}</span>
          ${{chip("role", "all", t("all_f"), iconBadge("all", "•"))}}
          ${{Object.keys(I18N.pt.roles).filter(k => k !== "all").map((k) => chip("role", k, t("roles", k), iconBadge("all", k === "dps" ? "◆" : k === "heal" ? "✚" : k === "sup" ? "◉" : k === "break" ? "▲" : "⚡"))).join("")}}
        </div>
        
        <div class="filter-row">
          <span class="filter-label">${{t("stage_label")}}</span>
          ${{chip("stage", "all", t("all"), iconBadge("all", "•"))}}
          ${{["Lumin Stage", "Gamma Stage", "Nova Stage"].map((st) => chip("stage", st, t("stages", st), iconBadge("all", "◈"))).join("")}}
        </div>
        
        <div class="sort-row">
          <select class="sort-select" id="sort" aria-label="${{t('sort_no_asc')}}">
            <option value="number_asc">${{t("sort_no_asc")}}</option>
            <option value="number_desc">${{t("sort_no_desc")}}</option>
            <option value="name_asc">${{t("sort_name_asc")}}</option>
            <option value="name_desc">${{t("sort_name_desc")}}</option>
          </select>
          <span class="creatures-count">${{t("showing")}} ${{items.length}} ${{t("of")}} ${{CREATURES.length}} ${{t("aniimos")}}</span>
        </div>
      </div>
      
      <div class="grid">
        ${{items.length ? items.map(card).join("") : `<div class="empty"><p>${{t("empty_title")}}</p><button type="button" class="reset-filters-btn">${{t("reset_filters")}}</button></div>`}}
      </div>
    </div>
  </section>`;

  const sortEl = app.querySelector("#sort");
  if (sortEl) sortEl.value = state.sort;
}}

function statBar(name, value, maxVal = 100) {{
  const pct = Math.min(100, Math.max(10, Math.round((value / maxVal) * 100)));
  return `<div class="stat">
    <span class="stat-name">${{name}}:</span>
    <div class="stat-bar"><span style="width: ${{pct}}%"></span></div>
    <span class="stat-val">${{value}}</span>
  </div>`;
}}

function renderDetail(item) {{
  const currentIndex = CREATURES.findIndex((c) => c.id === item.id);
  const prevItem = CREATURES[(currentIndex - 1 + CREATURES.length) % CREATURES.length];
  const nextItem = CREATURES[(currentIndex + 1) % CREATURES.length];

  const related = (item.relatedIds || [item.id])
    .map((rid) => CREATURES.find((c) => c.id === rid))
    .filter(Boolean);

  const evoNodes = item.evolutionPath && item.evolutionPath.length > 0 
    ? item.evolutionPath.map((node) => CREATURES.find((c) => c.id === node.id) || node)
    : [item];

  const elemColor = colors[item.element] || "#565673";
  const elemName = t("elements", item.element);
  const roleName = t("roles", item.role);
  const stageName = t("stages", item.stage);
  const descriptionText = currentLang === "pt" && item.desc_pt ? item.desc_pt : item.desc;
  const habitatsList = currentLang === "pt" && item.habitats_pt ? item.habitats_pt : item.habitats;
  const homelandText = currentLang === "pt" && item.homeland_pt ? item.homeland_pt : item.homeland;
  const homelandDesc = currentLang === "pt" && item.homelandType_pt ? item.homelandType_pt : item.homelandType;

  if (langButton) {{
    langButton.innerHTML = currentLang === "pt" ? "🇧🇷 PT" : "🇺🇸 EN";
  }}

  app.innerHTML = `<div class="detail-wrap">
    <div class="back-row">
      <a class="nav-back" href="/" data-nav="home" aria-label="${{t('back_to_wiki')}}">${{t("back_to_wiki")}}</a>
      <span class="current-creature-title">NO.${{item.number}} ${{item.name}}</span>
      <div class="nav-pair">
        <a class="nav-step prev-btn" href="/${{prevItem.slug}}" data-slug="${{prevItem.slug}}" title="${{t('prev')}}: NO.${{prevItem.number}} ${{prevItem.name}}">${{t("prev")}} (NO.${{prevItem.number}})</a>
        <a class="nav-step next-btn" href="/${{nextItem.slug}}" data-slug="${{nextItem.slug}}" title="${{t('next')}}: NO.${{nextItem.number}} ${{nextItem.name}}">${{t("next")}} (NO.${{nextItem.number}})</a>
      </div>
    </div>

    <section class="detail-panel">
      <div class="panel-content">
        <div class="detail-hero">
          <div class="hero-art">
            <img src="${{creatureImage(item)}}" alt="${{item.name}}" width="400" height="400">
            <span class="hero-stage-badge">${{stageName}}</span>
          </div>
          
          <div class="hero-info">
            <h1 class="hero-title">
              ${{item.name}}
              <span class="tag" style="background:${{elemColor}}">${{symbols[item.element] || ""}} ${{elemName.toUpperCase()}}</span>
              <span class="tag tag-role">◉ ${{roleName.toUpperCase()}}</span>
            </h1>
            
            <h2 class="section-title">${{t("overview")}}</h2>
            <p class="hero-desc">${{descriptionText}}</p>
            
            <div class="attributes">
              <h3 class="attribute-total">${{t("attributes_total")}} ${{item.totalAttributes}}</h3>
              ${{statBar(currentLang === 'pt' ? 'VIDA (HP)' : 'HP', item.attributes?.HP || 70, 120)}}
              ${{statBar(currentLang === 'pt' ? 'ATQ. FÍSICO' : 'ATK', item.attributes?.ATK || 60, 120)}}
              ${{statBar(currentLang === 'pt' ? 'ATQ. MÁGICO' : 'M.ATK', item.attributes?.['M.ATK'] || 50, 120)}}
              ${{statBar(currentLang === 'pt' ? 'DEF. FÍSICA' : 'P.DEF', item.attributes?.['P.DEF'] || 55, 120)}}
              ${{statBar(currentLang === 'pt' ? 'DEF. MÁGICA' : 'M.DEF', item.attributes?.['M.DEF'] || 50, 120)}}
              ${{statBar(currentLang === 'pt' ? 'AGILIDADE' : 'HASTE', item.attributes?.HASTE || 65, 120)}}
            </div>
          </div>
        </div>

        ${{related.length > 1 ? `
        <div class="forms-container">
          <span class="forms-label">${{t("related_forms")}}</span>
          <div class="forms">
            ${{related.map((rel) => `<a class="form-link ${{rel.id === item.id ? "active" : ""}}" href="/${{rel.slug}}" data-slug="${{rel.slug}}">NO.${{rel.number}} ${{rel.name}}</a>`).join("")}}
          </div>
        </div>` : ""}}
      </div>
    </section>

    <section class="evolution-panel">
      <div class="panel-content">
        <div class="panel-header">
          <h2>${{t("evolution_path")}}</h2>
        </div>
        <div class="evolution-path">
          ${{evoNodes.map((node, i) => `
            ${{i > 0 ? '<span class="evo-arrow">➔</span>' : ""}}
            <a class="evo-node ${{node.id === item.id ? "active" : ""}}" href="/${{node.slug}}" data-slug="${{node.slug}}">
              <img src="${{creatureImage(node)}}" alt="${{node.name}}" width="70" height="70">
              <span class="evo-name">${{node.name}}</span>
              <small class="evo-stage">${{t("stages", node.stage)}}</small>
            </a>
          `).join("")}}
        </div>
      </div>
    </section>

    <div class="info-grid">
      <section class="info-card">
        <h2 class="section-title">${{t("habitats")}}</h2>
        <ul class="habitats-list">
          ${{(habitatsList || ["Campos de Nimbos"]).map((h) => `<li>📍 ${{h}}</li>`).join("")}}
        </ul>
        
        <h2 class="section-title" style="margin-top:22px">${{t("homeland_ability")}}</h2>
        <div class="homeland-box">
          <span class="homeland-badge">🛠️</span>
          <div>
            <strong>${{homelandText || "11 Mobilidade"}}</strong>
            <p>${{homelandDesc || "Bônus especial de exploração e sobrevivência."}}</p>
          </div>
        </div>
      </section>

      <section class="info-card">
        <h2 class="section-title">${{t("skill_details")}}</h2>
        ${{(item.skills || []).map((sk, i) => `
          <div class="skill">
            <span class="skill-icon" style="background:${{i === 0 ? elemColor : '#3d3d51'}}">${{symbols[item.element] || "⚡"}}</span>
            <div class="skill-body">
              <strong>${{sk.name}}</strong>
              <div class="skill-meta">${{sk.type === 'Physical' ? t('physical') : t('magic')}} · ${{t('cost')}} ${{sk.cost}} · ${{t('power')}} ${{sk.power}}</div>
              <p class="skill-desc">${{sk.desc}}</p>
            </div>
          </div>
        `).join("")}}
        
        ${{item.trait ? `
          <div class="skill trait-skill">
            <span class="skill-icon" style="background:#565673">✦</span>
            <div class="skill-body">
              <strong>${{t("passive_trait")}} ${{item.trait.name}}</strong>
              <p class="skill-desc">${{item.trait.desc}}</p>
            </div>
          </div>
        ` : ""}}
      </section>
    </div>
  </div>`;
}}

function render() {{
  const creature = parseRoute();
  if (creature) {{
    document.title = `${{creature.name}} (NO.${{creature.number}}) — ${{t('title_suffix')}}`;
    renderDetail(creature);
    window.scrollTo({{ top: 0, behavior: "instant" }});
    return;
  }}

  document.title = `Aniimo Wiki — ${{t('title_suffix')}}`;
  renderIndex();
  window.scrollTo({{ top: 0, behavior: "instant" }});
}}

// Click handler with SPA routing for clean /slug URLs
document.addEventListener("click", (event) => {{
  // 1. Check card or creature detail navigation link
  const link = event.target.closest("a[data-slug]");
  if (link) {{
    event.preventDefault();
    const slug = link.dataset.slug;
    navigateTo(slug);
    return;
  }}

  // 2. Check back to home link
  const homeLink = event.target.closest("a[data-nav='home'], .brand");
  if (homeLink) {{
    event.preventDefault();
    navigateTo("");
    return;
  }}

  // 3. Language toggle
  const langBtn = event.target.closest(".language-button");
  if (langBtn) {{
    currentLang = currentLang === "pt" ? "en" : "pt";
    localStorage.setItem("aniimo_lang", currentLang);
    render();
    return;
  }}

  // 4. Filters
  const chipBtn = event.target.closest(".filter-chip");
  if (chipBtn) {{
    const group = chipBtn.dataset.filterGroup;
    const val = chipBtn.dataset.filterValue;
    state[group] = val;
    renderIndex();
    return;
  }}

  const resetBtn = event.target.closest(".reset-filters-btn");
  if (resetBtn) {{
    state.search = "";
    state.element = "all";
    state.role = "all";
    state.stage = "all";
    if (searchInput) searchInput.value = "";
    renderIndex();
    return;
  }}

  const collapseBtn = event.target.closest(".collapse-button");
  if (collapseBtn) {{
    const filters = document.querySelector(".filters");
    if (filters) {{
      filters.hidden = !filters.hidden;
      collapseBtn.classList.toggle("is-collapsed", filters.hidden);
    }}
    return;
  }}
}});

// Keyboard navigation on filter chips (Enter and Space)
document.addEventListener("keydown", (event) => {{
  if (event.key === "Enter" || event.key === " ") {{
    const chipBtn = event.target.closest(".filter-chip");
    if (chipBtn) {{
      event.preventDefault();
      chipBtn.click();
    }}
  }}
}});

document.addEventListener("change", (event) => {{
  if (event.target.id === "sort") {{
    state.sort = event.target.value;
    renderIndex();
  }}
}});

if (searchInput) {{
  searchInput.addEventListener("input", () => {{
    state.search = searchInput.value;
    const currentCreature = parseRoute();
    if (currentCreature) {{
      navigateTo("");
    }} else {{
      renderIndex();
    }}
  }});
}}

window.addEventListener("popstate", render);
window.addEventListener("hashchange", render);

window.addEventListener("scroll", () => {{
  if (toTop) {{
    toTop.classList.toggle("visible", window.scrollY > 300);
  }}
}});

if (toTop) {{
  toTop.addEventListener("click", () => {{
    window.scrollTo({{ top: 0, behavior: "smooth" }});
  }});
}}

// Initial load
render();
"""

(h_copy / "app.js").write_text(app_js_code, encoding="utf-8")
print(f"Generated new PT-BR & Clean Slug app.js ({len(app_js_code)} chars)")
