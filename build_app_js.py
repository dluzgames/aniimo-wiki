import json
from pathlib import Path

h_copy = Path(r"H:\ollama\aniimo-wiki-copy")
creatures = json.loads((h_copy / "creatures_full.json").read_text(encoding="utf-8"))

app_js_code = f"""// Official Aniimo Wiki - Compact Encyclopedia App
const CREATURES = {json.dumps(creatures, ensure_ascii=False)};

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

const roleLabels = {{
  dps: "DPS",
  heal: "Heal",
  sup: "Support",
  break: "BREAK",
  energy: "REGEN"
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
  const hash = location.hash.replace(/^#\\/?/, "");
  const searchParams = new URLSearchParams(hash.includes("=") ? hash : "");
  if (searchParams.has("item")) {{
    return searchParams.get("item");
  }}
  if (hash.startsWith("item/")) {{
    return hash.replace("item/", "");
  }}
  const pathname = location.pathname;
  const match = pathname.match(/\\/item\\/(\\d+)/);
  if (match) {{
    return match[1];
  }}
  return null;
}}

function filteredItems() {{
  const query = state.search.trim().toLowerCase();
  const filtered = CREATURES.filter((item) => {{
    const matchesQuery = !query || 
      item.name.toLowerCase().includes(query) || 
      item.number.toLowerCase().includes(query) ||
      item.number.replace(/^0+/, "").includes(query);

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
  
  return `<a class="creature-card" href="#item=${{item.id}}" aria-label="NO.${{item.number}} ${{item.name}}" tabindex="0">
    <div class="creature-image">
      <span class="creature-number">NO.${{item.number}}</span>
      <img src="${{creatureImage(item)}}" alt="${{item.name}}" loading="lazy" width="134" height="134">
      <div class="badges">
        <span class="badge" style="background:${{elemBg}}" title="Element: ${{item.element}}">${{symbols[item.element] || "•"}}</span>
        <span class="badge" style="background:#3d3d51" title="Role: ${{roleLabels[item.role] || item.role}}">${{roleDisplay}}</span>
      </div>
    </div>
    <span class="creature-name">${{item.name}}</span>
  </a>`;
}}

function renderIndex() {{
  const items = filteredItems();
  
  app.innerHTML = `<section class="wiki-panel">
    <div class="panel-content">
      <div class="panel-header">
        <h1>Aniimo Wiki</h1>
        <button class="collapse-button" type="button" aria-label="Toggle filters" title="Expand / Collapse filters">⌃</button>
      </div>
      
      <div class="filters">
        <div class="filter-row">
          <span class="filter-label">Elements:</span>
          ${{chip("element", "all", "All", iconBadge("all", "•"))}}
          ${{["holy", "fire", "ice", "dark", "electric", "grass", "water", "rock", "wind"].map((e) => chip("element", e, e, iconBadge(e))).join("")}}
        </div>
        
        <div class="filter-row">
          <span class="filter-label">Roles:</span>
          ${{chip("role", "all", "All", iconBadge("all", "•"))}}
          ${{Object.entries(roleLabels).map(([key, label]) => chip("role", key, label, iconBadge("all", key === "dps" ? "◆" : key === "heal" ? "✚" : key === "sup" ? "◉" : key === "break" ? "▲" : "⚡"))).join("")}}
        </div>
        
        <div class="filter-row">
          <span class="filter-label">Stage:</span>
          ${{chip("stage", "all", "All", iconBadge("all", "•"))}}
          ${{["Lumin Stage", "Gamma Stage", "Nova Stage"].map((st) => chip("stage", st, st, iconBadge("all", "◈"))).join("")}}
        </div>
        
        <div class="sort-row">
          <select class="sort-select" id="sort" aria-label="Sort creatures">
            <option value="number_asc">Sort by No. in ascending order</option>
            <option value="number_desc">Sort by No. in descending order</option>
            <option value="name_asc">Sort by name (A-Z)</option>
            <option value="name_desc">Sort by name (Z-A)</option>
          </select>
          <span class="creatures-count">Showing ${{items.length}} of ${{CREATURES.length}} Aniimos</span>
        </div>
      </div>
      
      <div class="grid">
        ${{items.length ? items.map(card).join("") : '<div class="empty"><p>No Aniimos match the selected filters.</p><button type="button" class="reset-filters-btn">Reset All Filters</button></div>'}}
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

  app.innerHTML = `<div class="detail-wrap">
    <div class="back-row">
      <a class="nav-back" href="#" aria-label="Back to catalog">‹ Back to Wiki</a>
      <span class="current-creature-title">NO.${{item.number}} ${{item.name}}</span>
      <div class="nav-pair">
        <a class="nav-step prev-btn" href="#item=${{prevItem.id}}" title="Previous: NO.${{prevItem.number}} ${{prevItem.name}}">‹ NO.${{prevItem.number}}</a>
        <a class="nav-step next-btn" href="#item=${{nextItem.id}}" title="Next: NO.${{nextItem.number}} ${{nextItem.name}}">NO.${{nextItem.number}} ›</a>
      </div>
    </div>

    <section class="detail-panel">
      <div class="panel-content">
        <div class="detail-hero">
          <div class="hero-art">
            <img src="${{creatureImage(item)}}" alt="${{item.name}}" width="400" height="400">
            <span class="hero-stage-badge">${{item.stage}}</span>
          </div>
          
          <div class="hero-info">
            <h1 class="hero-title">
              ${{item.name}}
              <span class="tag" style="background:${{elemColor}}">${{symbols[item.element] || ""}} ${{item.element.toUpperCase()}}</span>
              <span class="tag tag-role">◉ ${{roleLabels[item.role] || item.role.toUpperCase()}}</span>
            </h1>
            
            <h2 class="section-title">Overview</h2>
            <p class="hero-desc">${{item.desc}}</p>
            
            <div class="attributes">
              <h3 class="attribute-total">Attributes Total: ${{item.totalAttributes}}</h3>
              ${{statBar("HP", item.attributes?.HP || 70, 120)}}
              ${{statBar("ATK", item.attributes?.ATK || 60, 120)}}
              ${{statBar("M.ATK", item.attributes?.["M.ATK"] || 50, 120)}}
              ${{statBar("P.DEF", item.attributes?.["P.DEF"] || 55, 120)}}
              ${{statBar("M.DEF", item.attributes?.["M.DEF"] || 50, 120)}}
              ${{statBar("HASTE", item.attributes?.HASTE || 65, 120)}}
            </div>
          </div>
        </div>

        ${{related.length > 1 ? `
        <div class="forms-container">
          <span class="forms-label">Related Forms:</span>
          <div class="forms">
            ${{related.map((rel) => `<a class="form-link ${{rel.id === item.id ? "active" : ""}}" href="#item=${{rel.id}}">NO.${{rel.number}} ${{rel.name}}</a>`).join("")}}
          </div>
        </div>` : ""}}
      </div>
    </section>

    <section class="evolution-panel">
      <div class="panel-content">
        <div class="panel-header">
          <h2>Evolution Path</h2>
        </div>
        <div class="evolution-path">
          ${{evoNodes.map((node, i) => `
            ${{i > 0 ? '<span class="evo-arrow">➔</span>' : ""}}
            <a class="evo-node ${{node.id === item.id ? "active" : ""}}" href="#item=${{node.id}}">
              <img src="${{creatureImage(node)}}" alt="${{node.name}}" width="70" height="70">
              <span class="evo-name">${{node.name}}</span>
              <small class="evo-stage">${{node.stage}}</small>
            </a>
          `).join("")}}
        </div>
      </div>
    </section>

    <div class="info-grid">
      <section class="info-card">
        <h2 class="section-title">Habitats</h2>
        <ul class="habitats-list">
          ${{(item.habitats || ["Nimbus Fields"]).map((h) => `<li>📍 ${{h}}</li>`).join("")}}
        </ul>
        
        <h2 class="section-title" style="margin-top:22px">Homeland Ability</h2>
        <div class="homeland-box">
          <span class="homeland-badge">🛠️</span>
          <div>
            <strong>${{item.homeland || "11 Mobility"}}</strong>
            <p>${{item.homelandType || "Specialized survival and exploration perk."}}</p>
          </div>
        </div>
      </section>

      <section class="info-card">
        <h2 class="section-title">Skill Details</h2>
        ${{(item.skills || []).map((sk, i) => `
          <div class="skill">
            <span class="skill-icon" style="background:${{i === 0 ? elemColor : '#3d3d51'}}">${{symbols[item.element] || "⚡"}}</span>
            <div class="skill-body">
              <strong>${{sk.name}}</strong>
              <div class="skill-meta">${{sk.type}} · Cost ${{sk.cost}} · Power ${{sk.power}}</div>
              <p class="skill-desc">${{sk.desc}}</p>
            </div>
          </div>
        `).join("")}}
        
        ${{item.trait ? `
          <div class="skill trait-skill">
            <span class="skill-icon" style="background:#565673">✦</span>
            <div class="skill-body">
              <strong>Passive Trait: ${{item.trait.name}}</strong>
              <p class="skill-desc">${{item.trait.desc}}</p>
            </div>
          </div>
        ` : ""}}
      </section>
    </div>
  </div>`;
}}

function render() {{
  const itemId = parseRoute();
  if (itemId) {{
    const creature = CREATURES.find((c) => c.id === itemId || c.number === itemId);
    if (creature) {{
      document.title = `${{creature.name}} (NO.${{creature.number}}) — Aniimo Wiki`;
      renderDetail(creature);
      window.scrollTo({{ top: 0, behavior: "instant" }});
      return;
    }}
  }}

  document.title = "Official Aniimo Wiki - Complete Aniimo Index | DLuz";
  renderIndex();
  window.scrollTo({{ top: 0, behavior: "instant" }});
}}

// Keyboard and click interaction for filters
document.addEventListener("click", (event) => {{
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
    const currentItem = parseRoute();
    if (currentItem) {{
      location.hash = "";
    }} else {{
      renderIndex();
    }}
  }});
}}

window.addEventListener("hashchange", render);
window.addEventListener("popstate", render);

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
print(f"Updated H:\\ollama\\aniimo-wiki-copy\\app.js ({len(app_js_code)} chars)")
