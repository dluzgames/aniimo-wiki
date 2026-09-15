// MAP API MOCK INTERCEPTOR
const origFetch = window.fetch;
window.fetch = async (url, options) => {
  const urlStr = typeof url === 'string' ? url : (url.url || '');
  if (urlStr.includes('/api/map/session')) {
    return new Response(JSON.stringify({
      session: "dluz-session-token",
      expiresIn: 86400
    }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  }
  if (urlStr.includes('/api/map/markers')) {
    let body = {};
    try {
      if (options && options.body) body = JSON.parse(options.body);
    } catch(e) {}
    if (body.pois) {
      return origFetch('/data/markers_pois.json');
    }
    return origFetch('/data/markers_species.json');
  }
  return origFetch(url, options);
};

/**
 * ANIIMO TOOLS BRASIL — CORE APPLICATION ENGINE (ENHANCED EDITION)
 * Standard Google Stitch UX/UI, i18n (PT default / EN secondary), 
 * Spotlight Search (Ctrl+K), Versus Comparator, Map Progress, Clean Deep Linking
 */

// I18N DICTIONARY
const I18N = {
  pt: {
    brand_subtitle: "Ferramentas e Banco de Dados",
    nav_home: "Início",
    nav_codes: "Códigos",
    nav_creatures: "Criaturas",
    nav_versus: "Comparador",
    nav_map: "Mapa Interativo",
    nav_type_chart: "Tabela de Tipos",
    nav_tier_list: "Tier List",
    nav_items: "Itens",
    nav_guides: "Guias",
    quick_search: "Buscar",
    hero_badge: "Lançamento Global em Setembro de 2026",
    hero_title: "O Guia e Banco de Dados Definitivo de Aniimo",
    hero_desc: "Tudo o que você precisa para explorar Idília: mapa interativo, códigos de resgate ativos, calculadora de tipos, tier list do meta e enciclopédia completa de criaturas.",
    countdown_kicker: "Tempo Restante para o Lançamento",
    days: "Dias",
    hours: "Horas",
    mins: "Min",
    secs: "Seg",
    card_codes_title: "Códigos de Resgate",
    card_codes_desc: "Resgate recompensas gratuitas como cristais de invocação, ovos raros e moedas de ouro.",
    card_creatures_title: "Registro Anii (94 Criaturas)",
    card_creatures_desc: "Consulte fraquezas, atributos base, habilidades de combate e habitats de todas as criaturas.",
    card_versus_title: "Comparador de Criaturas",
    card_versus_desc: "Compare duas criaturas lado a lado: atributos base, fraquezas elementais e sinergia de equipe.",
    card_map_title: "Mapa Interativo de Idília",
    card_map_desc: "Localize teletransportes, baús secretos, ninhos de ovos, chefes e pontos de coleta.",
    card_types_title: "Tabela de Tipos e Fraquezas",
    card_types_desc: "Descubra vantagens e fraquezas elementais com a matriz e calculadora rápida de dano.",
    card_tier_title: "Tier List do Meta",
    card_tier_desc: "Descubra as melhores criaturas para DPS, Quebra de Escudo, Cura e Suporte.",
    card_guides_title: "Guias e Requisitos",
    card_guides_desc: "Guia para iniciantes, como baixar, melhores starters e requisitos de sistema.",
    access_tool: "Acessar ferramenta →",
    active_codes: "Códigos Promocionais Ativos",
    codes_subtitle: "Códigos oficiais verificados. Clique para copiar e resgate no menu do jogo.",
    codes_filter_active: "Códigos Ativos (5)",
    codes_filter_expired: "Códigos Expirados (2)",
    copy_code: "Copiar Código",
    copied: "Copiado!",
    valid_until: "Válido até",
    source: "Origem",
    how_to_redeem: "Como Resgatar Códigos no Jogo",
    search_creatures: "Buscar criatura por nome, número ou elemento...",
    all_elements: "Todos os Elementos",
    all_roles: "Todas as Funções",
    all_stages: "Todos os Estágios",
    type_calc_title: "Calculadora de Matchup Elemental",
    attacker_element: "Elemento Atacante",
    defender_element: "Elemento Defensor",
    damage_multiplier: "Multiplicador de Dano",
    super_effective: "Super Efetivo! Causa 2x de dano.",
    normal_damage: "Dano Normal (1x).",
    not_effective: "Pouco Efetivo. Causa apenas metade do dano (0.5x).",
    immune_damage: "Sem Efeito! O defensor é imune a este elemento (0x).",
    filter_role: "Filtrar por Papel:",
    all: "Todos",
    footer_motto: "Mantenha as patas para cima, Desbravante. Nos vemos em Idília.",
    footer_disclaimer: "aniimo.dluz.com.br é um recurso não oficial feito por fãs para a comunidade de Aniimo. Todos os direitos de imagens e marcas pertencem à Pawprint Studio e FunPlus.",
    stat_hp: "Vida (HP)",
    stat_atk: "Ataque",
    stat_def: "Defesa",
    stat_spd: "Velocidade (Haste)",
    homeland_ability: "Habilidade Territorial",
    combat_skills: "Habilidades de Combate",
    habitat: "Habitats Naturais"
  },
  en: {
    brand_subtitle: "Tools & Database",
    nav_home: "Home",
    nav_codes: "Codes",
    nav_creatures: "Creatures",
    nav_versus: "Comparator",
    nav_map: "Interactive Map",
    nav_type_chart: "Type Chart",
    nav_tier_list: "Tier List",
    nav_items: "Items",
    nav_guides: "Guides",
    quick_search: "Search",
    hero_badge: "Global Launch in September 2026",
    hero_title: "The Ultimate Fan Database & Tools for Aniimo",
    hero_desc: "Everything you need to master Idylia: interactive map, active redeem codes, type chart calculator, meta tier list, and full creature database.",
    countdown_kicker: "Time Until Global Launch",
    days: "Days",
    hours: "Hours",
    mins: "Mins",
    secs: "Secs",
    card_codes_title: "Redeem Codes",
    card_codes_desc: "Claim free rewards such as summon crystals, rare eggs, and gold coins.",
    card_creatures_title: "Anii Register (94 Creatures)",
    card_creatures_desc: "Check weaknesses, base attributes, combat skills, and habitats for all Aniimos.",
    card_versus_title: "Creature Comparator",
    card_versus_desc: "Compare two Aniimos side-by-side: stats, type advantages, and team synergy.",
    card_map_title: "Interactive Map of Idylia",
    card_map_desc: "Locate teleporters, secret chests, egg nests, field bosses, and gathering nodes.",
    card_types_title: "Type Chart & Matchups",
    card_types_desc: "Discover elemental strengths and weaknesses with our 9x9 matrix and calculator.",
    card_tier_title: "Meta Tier List",
    card_tier_desc: "Find the top-tier Aniimos ranked for DPS, Shield Break, Healing, and Support.",
    card_guides_title: "Guides & Requirements",
    card_guides_desc: "Beginner starter guide, system specs, download links, and launch tips.",
    access_tool: "Open tool →",
    active_codes: "Active Redeem Codes",
    codes_subtitle: "Verified official codes. Click to copy and redeem in the in-game settings.",
    codes_filter_active: "Active Codes (5)",
    codes_filter_expired: "Expired Codes (2)",
    copy_code: "Copy Code",
    copied: "Copied!",
    valid_until: "Valid until",
    source: "Source",
    how_to_redeem: "How to Redeem Codes In-Game",
    search_creatures: "Search creatures by name, number, or element...",
    all_elements: "All Elements",
    all_roles: "All Roles",
    all_stages: "All Stages",
    type_calc_title: "Elemental Matchup Calculator",
    attacker_element: "Attacker Element",
    defender_element: "Defender Element",
    damage_multiplier: "Damage Multiplier",
    super_effective: "Super Effective! Deals 2x damage.",
    normal_damage: "Normal Damage (1x).",
    not_effective: "Not Very Effective. Deals half damage (0.5x).",
    immune_damage: "No Effect! The defender is completely immune (0x).",
    filter_role: "Filter by Role:",
    all: "All",
    footer_motto: "Keep your paws up, Pathfinder. See you in Idylia.",
    footer_disclaimer: "aniimo.dluz.com.br is an unofficial fan resource made for the Aniimo community. All trademarks and assets belong to Pawprint Studio and FunPlus.",
    stat_hp: "Health (HP)",
    stat_atk: "Attack",
    stat_def: "Defense",
    stat_spd: "Speed (Haste)",
    homeland_ability: "Homeland Ability",
    combat_skills: "Combat Skills",
    habitat: "Natural Habitats"
  }
};

// Global App State
const state = {
  lang: localStorage.getItem('aniimo_lang') || 'pt',
  theme: localStorage.getItem('aniimo_theme') || 'dark',
  creatures: [],
  codes: null,
  typeChart: null,
  tierList: null,
  mapData: null,
  items: [],
  guides: [],
  mapZoom: 1,
  mapPan: { x: 0, y: 0 },
  activeLayers: new Set(['aniimo', 'teleport', 'chest', 'boss', 'egg', 'resource']),
  foundMarkers: new Set(JSON.parse(localStorage.getItem('aniimo_found_markers') || '[]')),
  hideFoundMarkers: false,
  codeFilter: 'active',
  selectedFilterElement: 'all',
  selectedFilterRole: 'all',
  selectedFilterStage: 'all',
  searchQuery: '',
  versusCreature1: 'inferlupa',
  versusCreature2: 'celestis'
};

// INITIALIZATION
document.addEventListener('DOMContentLoaded', async () => {
  // Apply initial theme
  document.documentElement.setAttribute('data-theme', state.theme);
  
  // Load JSON Data
  await loadData();

  // Setup Event Listeners
  setupNavigation();
  setupLanguageSwitcher();
  setupThemeSwitcher();
  setupCountdown();
  setupCommandPalette();
  setupCodes();
  setupCreatures();
  setupVersusMode();
  setupMap();
  setupTypeChart();
  setupTierList();
  setupItemsAndGuides();

  // Initial Route Dispatch
  handleRouting();
});

// LOAD ALL DATA FROM DATA/ DIRECTORY
async function loadData() {
  try {
    const [creaturesRes, codesRes, typeRes, tierRes, mapRes, itemsRes, guidesRes] = await Promise.all([
      fetch('/data/creatures.json'),
      fetch('/data/codes.json'),
      fetch('/data/type_chart.json'),
      fetch('/data/tier_list.json'),
      fetch('/data/map_data.json'),
      fetch('/data/items.json'),
      fetch('/data/guides.json')
    ]);

    state.creatures = await creaturesRes.json();
    state.codes = await codesRes.json();
    state.typeChart = await typeRes.json();
    state.tierList = await tierRes.json();
    state.mapData = await mapRes.json();
    state.items = await itemsRes.json();
    state.guides = await guidesRes.json();
  } catch (err) {
    console.error("Error loading application data:", err);
  }
}

// CLEAN HTML5 NAVIGATION & ROUTING
function navigateTo(path, push = true) {
  if (push && window.location.pathname !== path) {
    history.pushState(null, '', path);
  }
  handleRouting();
}

function setupNavigation() {
  // Global click delegation for clean internal links
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="/"]');
    if (a && !a.target && !a.hasAttribute('download') && a.origin === window.location.origin) {
      e.preventDefault();
      const href = a.getAttribute('href');
      navigateTo(href);
    }
  });

  window.addEventListener('popstate', () => {
    handleRouting();
  });

  // Mobile menu toggle
  const mobileBtn = document.getElementById('mobile-toggle');
  const navLinks = document.getElementById('nav-links');
  if (mobileBtn && navLinks) {
    mobileBtn.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });

    navLinks.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        navLinks.classList.remove('open');
      });
    });
  }
}

function handleRouting() {
  // Sanitize any accidental or legacy hash (e.g. /bailite#/tier-list or #/tier-list)
  if (window.location.hash) {
    const cleanFromHash = window.location.hash.replace(/^#\/?/, '').trim();
    if (cleanFromHash) {
      history.replaceState(null, '', '/' + cleanFromHash);
    } else {
      history.replaceState(null, '', window.location.pathname || '/');
    }
  }

  // Parse clean pathname (e.g. /inferlupa or /codigos)
  let raw = window.location.pathname.replace(/^\/+/, '').trim().toLowerCase();
  raw = raw.split('/')[0] || 'home';

  // Check if raw matches a creature slug directly (Deep Linking!)
  const foundCreature = state.creatures && state.creatures.find(c => c.slug.toLowerCase() === raw);
  if (foundCreature) {
    showSection('criaturas');
    openCreatureModal(foundCreature, false);
    document.title = `${foundCreature.name_pt} (${foundCreature.number}) — Aniimo Tools Brasil`;
    return;
  }

  // Normal route map
  const routeAliases = {
    '': 'home',
    'home': 'home',
    'codigos': 'codigos',
    'codes': 'codigos',
    'criaturas': 'criaturas',
    'creatures': 'criaturas',
    'comparador': 'comparador',
    'versus': 'comparador',
    'mapa': 'mapa',
    'map': 'mapa',
    'tabela-tipos': 'tabela-tipos',
    'type-chart': 'tabela-tipos',
    'tier-list': 'tier-list',
    'itens': 'itens',
    'items': 'itens',
    'guias': 'guias',
    'guides': 'guias'
  };

  const target = routeAliases[raw] || 'home';
  showSection(target);

  // Close creature modal if navigating to a normal page
  const modal = document.getElementById('creature-modal');
  if (modal && modal.classList.contains('open')) {
    modal.classList.remove('open');
  }

  // Update Page Title dynamically
  const titles = {
    'home': 'Aniimo Tools Brasil: Banco de Dados, Mapa Interativo, Códigos & Guias',
    'codigos': 'Códigos Promocionais Ativos de Aniimo — Aniimo Tools Brasil',
    'criaturas': 'Registro Anii: 94 Criaturas, Fraquezas e Stats — Aniimo Tools Brasil',
    'comparador': 'Comparador de Criaturas (Versus Mode) — Aniimo Tools Brasil',
    'mapa': 'Mapa Interativo de Idília (Planícies Ventosas) — Aniimo Tools Brasil',
    'tabela-tipos': 'Tabela de Tipos e Matchup Elemental — Aniimo Tools Brasil',
    'tier-list': 'Tier List Oficial do Meta — Aniimo Tools Brasil',
    'itens': 'Banco de Itens e Dispositivos — Aniimo Tools Brasil',
    'guias': 'Guias e Requisitos de Sistema — Aniimo Tools Brasil'
  };
  document.title = titles[target] || titles['home'];
}

function showSection(target) {
  const sections = document.querySelectorAll('.app-section');
  sections.forEach(s => s.classList.remove('active'));

  const activeSection = document.getElementById(`section-${target}`) || document.getElementById('section-home');
  if (activeSection) {
    activeSection.classList.add('active');
    if (target === 'mapa') { setTimeout(() => window.dispatchEvent(new Event('resize')), 50); }
  }

  // Update active nav link
  document.querySelectorAll('.nav-item a').forEach(a => {
    const href = a.getAttribute('href').replace(/^\/+/, '') || 'home';
    if (href === target || (target === 'home' && href === 'home')) {
      a.classList.add('active');
    } else {
      a.classList.remove('active');
    }
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// COMMAND PALETTE (CTRL+K SPOTLIGHT SEARCH)
function setupCommandPalette() {
  const overlay = document.getElementById('command-palette');
  const triggerBtn = document.getElementById('search-trigger');
  const input = document.getElementById('command-input');
  const results = document.getElementById('command-results');

  if (!overlay || !input || !results) return;

  function openPalette() {
    overlay.classList.add('open');
    input.value = '';
    renderCommandResults('');
    input.focus();
  }

  function closePalette() {
    overlay.classList.remove('open');
  }

  if (triggerBtn) triggerBtn.addEventListener('click', openPalette);

  // Global Keyboard Shortcut: Ctrl+K or Cmd+K or /
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (overlay.classList.contains('open')) closePalette();
      else openPalette();
    } else if (e.key === 'Escape' && overlay.classList.contains('open')) {
      closePalette();
    }
  });

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closePalette();
  });

  input.addEventListener('input', (e) => {
    renderCommandResults(e.target.value.toLowerCase().trim());
  });

  function renderCommandResults(query) {
    const isPt = state.lang === 'pt';
    let itemsHtml = '';

    // Quick Tool Links
    const tools = [
      { title: isPt ? 'Códigos de Resgate' : 'Redeem Codes', sub: isPt ? 'Ferramenta de códigos promocionais' : 'Redeem promo codes', path: '/codigos', icon: '🎁' },
      { title: isPt ? 'Registro Anii (Criaturas)' : 'Anii Register (Creatures)', sub: isPt ? 'Catálogo das 94 criaturas' : '94 Creatures database', path: '/criaturas', icon: '🐾' },
      { title: isPt ? 'Comparador de Criaturas' : 'Creature Comparator', sub: isPt ? 'Comparar atributos e tipos lado a lado' : 'Side-by-side stats comparison', path: '/comparador', icon: '⚔️' },
      { title: isPt ? 'Mapa Interativo' : 'Interactive Map', sub: isPt ? 'Planícies Ventosas (Breezy Plains)' : 'Explore Breezy Plains', path: '/mapa', icon: '🗺️' },
      { title: isPt ? 'Tabela de Tipos' : 'Type Chart', sub: isPt ? 'Matriz e calculadora elemental' : 'Elemental matchup calculator', path: '/tabela-tipos', icon: '🔮' },
      { title: isPt ? 'Tier List do Meta' : 'Meta Tier List', sub: isPt ? 'Rankings S+, S, A e B' : 'S+, S, A, B Rankings', path: '/tier-list', icon: '🏆' }
    ];

    const matchingTools = tools.filter(t => !query || t.title.toLowerCase().includes(query) || t.sub.toLowerCase().includes(query));
    if (matchingTools.length > 0) {
      itemsHtml += `<li style="padding:0.4rem 0.8rem; font-size:0.75rem; font-weight:800; color:var(--ink-muted); text-transform:uppercase;">${isPt ? 'Ferramentas' : 'Tools'}</li>`;
      itemsHtml += matchingTools.map(t => `
        <li class="command-item" data-action="nav" data-path="${t.path}">
          <span style="font-size:1.4rem;">${t.icon}</span>
          <div class="command-item-text">
            <div class="command-item-title">${t.title}</div>
            <div class="command-item-subtitle">${t.sub}</div>
          </div>
        </li>
      `).join('');
    }

    // Matching Creatures
    if (state.creatures.length > 0) {
      const matchingCreatures = state.creatures.filter(c => {
        const name = (isPt ? c.name_pt : c.name_en).toLowerCase();
        return !query || name.includes(query) || c.number.includes(query) || c.element_en.toLowerCase().includes(query);
      }).slice(0, 6);

      if (matchingCreatures.length > 0) {
        itemsHtml += `<li style="padding:0.4rem 0.8rem; font-size:0.75rem; font-weight:800; color:var(--ink-muted); text-transform:uppercase; margin-top:0.4rem;">${isPt ? 'Criaturas' : 'Creatures'}</li>`;
        itemsHtml += matchingCreatures.map(c => `
          <li class="command-item" data-action="creature" data-slug="${c.slug}">
            <img class="command-item-icon" src="${c.image}" alt="${c.name_pt}" />
            <div class="command-item-text">
              <div class="command-item-title">${isPt ? c.name_pt : c.name_en} (${c.number})</div>
              <div class="command-item-subtitle">${isPt ? c.element : c.element_en} • ${isPt ? c.role_pt : c.role_en} • Tier ${c.tier}</div>
            </div>
          </li>
        `).join('');
      }
    }

    results.innerHTML = itemsHtml || `<li style="padding:1.5rem; text-align:center; color:var(--ink-muted); font-weight:600;">Nenhum resultado encontrado para "${query}".</li>`;

    // Click handlers on items
    results.querySelectorAll('.command-item').forEach(li => {
      li.addEventListener('click', () => {
        closePalette();
        const action = li.getAttribute('data-action');
        if (action === 'nav') {
          navigateTo(li.getAttribute('data-path'));
        } else if (action === 'creature') {
          const slug = li.getAttribute('data-slug');
          navigateTo('/' + slug);
        }
      });
    });
  }
}

// I18N & LANGUAGE TOGGLE
function setupLanguageSwitcher() {
  const langBtn = document.getElementById('lang-toggle');
  updateTexts();

  if (langBtn) {
    langBtn.addEventListener('click', () => {
      state.lang = state.lang === 'pt' ? 'en' : 'pt';
      localStorage.setItem('aniimo_lang', state.lang);
      updateTexts();
      renderAll();
      showToast(state.lang === 'pt' ? 'Idioma alterado para Português (Brasil)' : 'Language switched to English');
    });
  }
}

function updateTexts() {
  const d = I18N[state.lang];
  const langBtn = document.getElementById('lang-toggle');
  if (langBtn) {
    langBtn.innerHTML = state.lang === 'pt' ? '🇧🇷 PT' : '🇺🇸 EN';
    langBtn.setAttribute('title', state.lang === 'pt' ? 'Mudar para Inglês' : 'Switch to Portuguese');
  }

  // Translate all [data-i18n] elements
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (d[key]) {
      el.innerHTML = d[key];
    }
  });

  // Translate placeholders
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const key = el.getAttribute('data-i18n-ph');
    if (d[key]) {
      el.setAttribute('placeholder', d[key]);
    }
  });
}

function renderAll() {
  renderCodes();
  renderCreatures();
  renderVersusMode();
  renderMap();
  renderTypeChart();
  renderTierList();
  renderItems();
  renderGuides();
}

// THEME TOGGLE (DARK / LIGHT)
function setupThemeSwitcher() {
  const themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', state.theme);
      localStorage.setItem('aniimo_theme', state.theme);
      themeBtn.innerHTML = state.theme === 'dark' ? '🌙' : '☀️';
    });
    themeBtn.innerHTML = state.theme === 'dark' ? '🌙' : '☀️';
  }
}

// COUNTDOWN TIMER
function setupCountdown() {
  const launchDate = new Date('2026-09-16T00:00:00Z').getTime();

  function update() {
    const now = new Date().getTime();
    const diff = launchDate - now;

    if (diff > 0) {
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const secs = Math.floor((diff % (1000 * 60)) / 1000);

      const dEl = document.getElementById('cd-days');
      const hEl = document.getElementById('cd-hours');
      const mEl = document.getElementById('cd-mins');
      const sEl = document.getElementById('cd-secs');

      if (dEl) dEl.textContent = String(days).padStart(2, '0');
      if (hEl) hEl.textContent = String(hours).padStart(2, '0');
      if (mEl) mEl.textContent = String(mins).padStart(2, '0');
      if (sEl) sEl.textContent = String(secs).padStart(2, '0');
    }
  }

  update();
  setInterval(update, 1000);
}

// REDEEM CODES
function setupCodes() {
  renderCodes();

  document.querySelectorAll('.code-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.code-filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.codeFilter = btn.getAttribute('data-code-filter');
      renderCodes();
    });
  });
}

function renderCodes() {
  if (!state.codes) return;
  const listEl = document.getElementById('codes-container');
  if (!listEl) return;

  const isPt = state.lang === 'pt';
  const d = I18N[state.lang];

  const items = state.codeFilter === 'active' ? state.codes.active : state.codes.expired;

  listEl.innerHTML = items.map((c, idx) => `
    <div class="code-card">
      <div class="code-info">
        <div class="code-badge-row">
          <span class="code-string">${c.code}</span>
          <span class="code-status-badge ${c.status}">${c.status === 'active' ? (isPt ? 'Ativo' : 'Active') : (isPt ? 'Expirado' : 'Expired')}</span>
          ${idx === 0 && c.status === 'active' ? `<span class="code-status-badge new">${isPt ? 'NOVO' : 'NEW'}</span>` : ''}
        </div>
        <p class="code-rewards">${isPt ? c.rewards_pt : c.rewards_en}</p>
        <p class="code-expiry">${d.valid_until}: ${c.valid_until || c.expired_at} ${c.source ? `• ${d.source}: ${c.source}` : ''}</p>
      </div>
      ${c.status === 'active' ? `
        <button class="btn-copy-code" data-code="${c.code}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
          <span>${d.copy_code}</span>
        </button>
      ` : ''}
    </div>
  `).join('');

  listEl.querySelectorAll('.btn-copy-code').forEach(btn => {
    btn.addEventListener('click', () => {
      const code = btn.getAttribute('data-code');
      navigator.clipboard.writeText(code).then(() => {
        btn.classList.add('copied');
        btn.querySelector('span').textContent = d.copied;
        showToast(isPt ? `Código ${code} copiado para a área de transferência!` : `Code ${code} copied to clipboard!`);
        setTimeout(() => {
          btn.classList.remove('copied');
          btn.querySelector('span').textContent = d.copy_code;
        }, 2000);
      });
    });
  });

  const stepsEl = document.getElementById('guide-steps');
  if (stepsEl) {
    const steps = isPt ? state.codes.instructions_pt : state.codes.instructions_en;
    stepsEl.innerHTML = steps.map(s => `<li>${s}</li>`).join('');
  }
}

// CREATURES DATABASE (ANIIMODEX)
function setupCreatures() {
  renderCreatures();

  const searchInput = document.getElementById('creature-search');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value.toLowerCase().trim();
      filterCreatures();
    });
  }

  document.querySelectorAll('.filter-chip[data-filter-group]').forEach(btn => {
    btn.addEventListener('click', () => {
      const group = btn.getAttribute('data-filter-group');
      const val = btn.getAttribute('data-filter-value');
      
      btn.parentElement.querySelectorAll('.filter-chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      if (group === 'element') state.selectedFilterElement = val;
      if (group === 'role') state.selectedFilterRole = val;
      if (group === 'stage') state.selectedFilterStage = val;

      filterCreatures();
    });
  });
}

function filterCreatures() {
  const filtered = state.creatures.filter(c => {
    const isPt = state.lang === 'pt';
    const name = (isPt ? c.name_pt : c.name_en).toLowerCase();
    const matchesSearch = !state.searchQuery || name.includes(state.searchQuery) || c.number.includes(state.searchQuery);
    const matchesElement = state.selectedFilterElement === 'all' || c.element_en.toLowerCase() === state.selectedFilterElement;
    const matchesRole = state.selectedFilterRole === 'all' || c.role_en.toLowerCase() === state.selectedFilterRole;
    const matchesStage = state.selectedFilterStage === 'all' || c.stage.toLowerCase() === state.selectedFilterStage;

    return matchesSearch && matchesElement && matchesRole && matchesStage;
  });

  const countBadge = document.getElementById('creatures-count-badge');
  if (countBadge) {
    const isPt = state.lang === 'pt';
    countBadge.textContent = isPt 
      ? `Exibindo ${filtered.length} de ${state.creatures.length} criaturas` 
      : `Showing ${filtered.length} of ${state.creatures.length} creatures`;
  }

  renderCreaturesGrid(filtered);
}

function renderCreatures() {
  filterCreatures();
}

function renderCreaturesGrid(list) {
  const grid = document.getElementById('creatures-grid');
  if (!grid) return;

  const isPt = state.lang === 'pt';

  grid.innerHTML = list.map(c => `
    <div class="creature-card" data-slug="${c.slug}">
      <span class="creature-number">${c.number}</span>
      <span class="creature-tier-badge">${c.tier}</span>
      <img class="creature-card-img" src="${c.image}" alt="${c.name_pt}" loading="lazy" />
      <h3 class="creature-card-name">${isPt ? c.name_pt : c.name_en}</h3>
      <div class="creature-card-badges">
        <span class="element-pill" style="background: var(--el-${c.element_en.toLowerCase()}, #94a3b8)">${isPt ? c.element : c.element_en}</span>
        <span class="role-pill">${isPt ? c.role_pt : c.role_en}</span>
      </div>
    </div>
  `).join('');

  grid.querySelectorAll('.creature-card').forEach(card => {
    card.addEventListener('click', () => {
      const slug = card.getAttribute('data-slug');
      const creature = state.creatures.find(c => c.slug === slug);
      if (creature) {
        openCreatureModal(creature);
        window.history.pushState(null, '', `/${creature.slug}`);
      }
    });
  });
}

function openCreatureModal(c) {
  const modal = document.getElementById('creature-modal');
  if (!modal) return;

  const isPt = state.lang === 'pt';

  document.getElementById('modal-title').textContent = `${isPt ? c.name_pt : c.name_en} (${c.number})`;
  document.getElementById('modal-img').src = c.image;
  document.getElementById('modal-element').textContent = isPt ? c.element : c.element_en;
  document.getElementById('modal-element').style.background = `var(--el-${c.element_en.toLowerCase()}, #94a3b8)`;
  document.getElementById('modal-role').textContent = isPt ? c.role_pt : c.role_en;
  document.getElementById('modal-desc').textContent = isPt ? c.description_pt : c.description_en;
  document.getElementById('modal-habitat').textContent = isPt ? c.habitat_pt : c.habitat_en;
  document.getElementById('modal-homeland').textContent = isPt ? c.homeland_pt : c.homeland_en;

  document.getElementById('stat-hp').textContent = c.stats.HP || 80;
  document.getElementById('stat-atk').textContent = c.stats.ATK || 85;
  document.getElementById('stat-def').textContent = c.stats.P_DEF || 70;
  document.getElementById('stat-spd').textContent = c.stats.HASTE || 65;

  const skillsList = isPt ? c.skills_pt : c.skills_en;
  const skillsContainer = document.getElementById('modal-skills');
  if (skillsContainer) {
    skillsContainer.innerHTML = skillsList.map(s => `
      <div style="margin-bottom:0.6rem; padding:0.5rem 0.75rem; background:var(--surface-2); border-radius:var(--radius-md); border:1px solid var(--border);">
        <strong>${s.name}</strong> • <small style="color:var(--accent-strong)">${s.type} (Poder: ${s.power})</small>
        <p style="font-size:0.85rem; color:var(--ink-soft); margin-top:0.2rem;">${s.desc}</p>
      </div>
    `).join('');
  }

  modal.classList.add('open');
}

// VERSUS COMPARATOR MODE
function setupVersusMode() {
  const sel1 = document.getElementById('versus-select-1');
  const sel2 = document.getElementById('versus-select-2');
  if (!sel1 || !sel2) return;

  renderVersusMode();

  sel1.addEventListener('change', (e) => {
    state.versusCreature1 = e.target.value;
    updateVersusDisplay();
  });

  sel2.addEventListener('change', (e) => {
    state.versusCreature2 = e.target.value;
    updateVersusDisplay();
  });
}

function renderVersusMode() {
  const sel1 = document.getElementById('versus-select-1');
  const sel2 = document.getElementById('versus-select-2');
  if (!sel1 || !sel2 || state.creatures.length === 0) return;

  const isPt = state.lang === 'pt';
  const opts = state.creatures.map(c => `<option value="${c.slug}">${c.number} - ${isPt ? c.name_pt : c.name_en}</option>`).join('');

  sel1.innerHTML = opts;
  sel2.innerHTML = opts;

  sel1.value = state.versusCreature1;
  sel2.value = state.versusCreature2;

  updateVersusDisplay();
}

function updateVersusDisplay() {
  const c1 = state.creatures.find(c => c.slug === state.versusCreature1) || state.creatures[0];
  const c2 = state.creatures.find(c => c.slug === state.versusCreature2) || state.creatures[1];
  if (!c1 || !c2) return;

  const isPt = state.lang === 'pt';

  // Update C1
  document.getElementById('versus-name-1').textContent = isPt ? c1.name_pt : c1.name_en;
  document.getElementById('versus-img-1').src = c1.image;
  document.getElementById('versus-elem-1').textContent = isPt ? c1.element : c1.element_en;
  document.getElementById('versus-elem-1').style.background = `var(--el-${c1.element_en.toLowerCase()}, #94a3b8)`;
  document.getElementById('versus-role-1').textContent = isPt ? c1.role_pt : c1.role_en;
  
  const hp1 = c1.stats.HP || 80, atk1 = c1.stats.ATK || 85, def1 = c1.stats.P_DEF || 70, spd1 = c1.stats.HASTE || 65;
  document.getElementById('vs1-hp').textContent = hp1;
  document.getElementById('vs1-atk').textContent = atk1;
  document.getElementById('vs1-def').textContent = def1;
  document.getElementById('vs1-spd').textContent = spd1;
  document.getElementById('bar1-hp').style.width = `${Math.min(hp1, 140) / 1.4}%`;
  document.getElementById('bar1-atk').style.width = `${Math.min(atk1, 140) / 1.4}%`;
  document.getElementById('bar1-def').style.width = `${Math.min(def1, 140) / 1.4}%`;
  document.getElementById('bar1-spd').style.width = `${Math.min(spd1, 140) / 1.4}%`;

  // Update C2
  document.getElementById('versus-name-2').textContent = isPt ? c2.name_pt : c2.name_en;
  document.getElementById('versus-img-2').src = c2.image;
  document.getElementById('versus-elem-2').textContent = isPt ? c2.element : c2.element_en;
  document.getElementById('versus-elem-2').style.background = `var(--el-${c2.element_en.toLowerCase()}, #94a3b8)`;
  document.getElementById('versus-role-2').textContent = isPt ? c2.role_pt : c2.role_en;

  const hp2 = c2.stats.HP || 80, atk2 = c2.stats.ATK || 85, def2 = c2.stats.P_DEF || 70, spd2 = c2.stats.HASTE || 65;
  document.getElementById('vs2-hp').textContent = hp2;
  document.getElementById('vs2-atk').textContent = atk2;
  document.getElementById('vs2-def').textContent = def2;
  document.getElementById('vs2-spd').textContent = spd2;
  document.getElementById('bar2-hp').style.width = `${Math.min(hp2, 140) / 1.4}%`;
  document.getElementById('bar2-atk').style.width = `${Math.min(atk2, 140) / 1.4}%`;
  document.getElementById('bar2-def').style.width = `${Math.min(def2, 140) / 1.4}%`;
  document.getElementById('bar2-spd').style.width = `${Math.min(spd2, 140) / 1.4}%`;

  // Calculate Elemental Advantage
  const matrix = state.typeChart ? state.typeChart.matrix : {};
  const mult1to2 = (matrix[c1.element] && matrix[c1.element][c2.element] !== undefined) ? matrix[c1.element][c2.element] : 1.0;
  const mult2to1 = (matrix[c2.element] && matrix[c2.element][c1.element] !== undefined) ? matrix[c2.element][c1.element] : 1.0;

  const verdictEl = document.getElementById('versus-verdict');
  if (verdictEl) {
    if (mult1to2 > mult2to1) {
      verdictEl.innerHTML = isPt 
        ? `🔥 <strong style="color:var(--accent-strong);">${c1.name_pt}</strong> tem grande vantagem elemental (${mult1to2}x de dano em ${c2.name_pt})!` 
        : `🔥 <strong style="color:var(--accent-strong);">${c1.name_en}</strong> has major elemental advantage (${mult1to2}x damage against ${c2.name_en})!`;
    } else if (mult2to1 > mult1to2) {
      verdictEl.innerHTML = isPt 
        ? `🔥 <strong style="color:var(--accent-strong);">${c2.name_pt}</strong> tem grande vantagem elemental (${mult2to1}x de dano em ${c1.name_pt})!` 
        : `🔥 <strong style="color:var(--accent-strong);">${c2.name_en}</strong> has major elemental advantage (${mult2to1}x damage against ${c1.name_en})!`;
    } else {
      verdictEl.innerHTML = isPt 
        ? `⚖️ Duelo neutro: ambos possuem multiplicadores equivalentes (${mult1to2}x vs ${mult2to1}x). A vitória dependerá dos atributos brutos e sinergia!` 
        : `⚖️ Neutral matchup: both deal balanced damage (${mult1to2}x vs ${mult2to1}x). Raw stats and team synergy will decide the battle!`;
    }
  }
}

// INTERACTIVE MAP WITH WHEEL ZOOM, PAN & PROGRESS
function setupMap() {
  renderMap();

  const viewport = document.getElementById('map-viewport');
  const container = document.getElementById('map-container');
  const zoomIn = document.getElementById('map-zoom-in');
  const zoomOut = document.getElementById('map-zoom-out');
  const zoomReset = document.getElementById('map-zoom-reset');
  const zoomBadge = document.getElementById('map-zoom-badge');
  const filterUnfoundBtn = document.getElementById('map-filter-unfound');
  const resetProgressBtn = document.getElementById('map-reset-progress');
  const selectAllBtn = document.getElementById('map-select-all-layers');
  const deselectAllBtn = document.getElementById('map-deselect-all-layers');
  const detailCard = document.getElementById('map-detail-card');
  const detailCloseBtn = document.getElementById('map-detail-close');

  if (!viewport || !container) return;

  function updateTransform() {
    container.style.transform = `translate(${state.mapPan.x}px, ${state.mapPan.y}px) scale(${state.mapZoom})`;
    if (zoomBadge) {
      zoomBadge.textContent = `${Math.round(state.mapZoom * 100)}%`;
    }
  }

  // Initial center of map inside viewport
  function centerMapInitially() {
    const vpRect = viewport.getBoundingClientRect();
    if (vpRect.width > 0 && vpRect.height > 0) {
      // center around the main island / starter region (x: ~500px, y: ~400px)
      state.mapPan.x = (vpRect.width / 2) - 450 * state.mapZoom;
      state.mapPan.y = (vpRect.height / 2) - 380 * state.mapZoom;
      updateTransform();
    }
  }
  setTimeout(centerMapInitially, 100);

  // 1. MOUSE WHEEL ZOOM (Centered at cursor)
  viewport.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
    const oldZoom = state.mapZoom;
    const newZoom = Math.min(Math.max(oldZoom * zoomFactor, 0.4), 3.5);
    if (newZoom === oldZoom) return;

    const rect = viewport.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    state.mapPan.x = mouseX - (mouseX - state.mapPan.x) * (newZoom / oldZoom);
    state.mapPan.y = mouseY - (mouseY - state.mapPan.y) * (newZoom / oldZoom);
    state.mapZoom = newZoom;
    updateTransform();
  }, { passive: false });

  // 2. MOUSE DRAGGING (PAN)
  let isDragging = false;
  let startX = 0;
  let startY = 0;

  viewport.addEventListener('mousedown', (e) => {
    if (e.target.closest('.map-marker') || e.target.closest('.map-controls') || e.target.closest('.map-detail-card')) return;
    isDragging = true;
    startX = e.clientX - state.mapPan.x;
    startY = e.clientY - state.mapPan.y;
    viewport.style.cursor = 'grabbing';
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    state.mapPan.x = e.clientX - startX;
    state.mapPan.y = e.clientY - startY;
    updateTransform();
  });

  window.addEventListener('mouseup', () => {
    if (isDragging) {
      isDragging = false;
      viewport.style.cursor = 'grab';
    }
  });

  // 3. TOUCH PAN & PINCH-TO-ZOOM (Mobile / Tablet)
  let initialTouchDist = null;
  let initialTouchZoom = 1;

  viewport.addEventListener('touchstart', (e) => {
    if (e.target.closest('.map-marker') || e.target.closest('.map-controls') || e.target.closest('.map-detail-card')) return;
    if (e.touches.length === 1) {
      isDragging = true;
      startX = e.touches[0].clientX - state.mapPan.x;
      startY = e.touches[0].clientY - state.mapPan.y;
    } else if (e.touches.length === 2) {
      isDragging = false;
      initialTouchDist = Math.hypot(
        e.touches[0].clientX - e.touches[1].clientX,
        e.touches[0].clientY - e.touches[1].clientY
      );
      initialTouchZoom = state.mapZoom;
    }
  }, { passive: true });

  viewport.addEventListener('touchmove', (e) => {
    if (e.touches.length === 1 && isDragging) {
      state.mapPan.x = e.touches[0].clientX - startX;
      state.mapPan.y = e.touches[0].clientY - startY;
      updateTransform();
    } else if (e.touches.length === 2 && initialTouchDist) {
      const dist = Math.hypot(
        e.touches[0].clientX - e.touches[1].clientX,
        e.touches[0].clientY - e.touches[1].clientY
      );
      const factor = dist / initialTouchDist;
      state.mapZoom = Math.min(Math.max(initialTouchZoom * factor, 0.4), 3.5);
      updateTransform();
    }
  }, { passive: true });

  viewport.addEventListener('touchend', () => {
    isDragging = false;
    initialTouchDist = null;
  });

  // 4. ZOOM BUTTONS
  if (zoomIn) {
    zoomIn.addEventListener('click', () => {
      const oldZoom = state.mapZoom;
      state.mapZoom = Math.min(state.mapZoom + 0.25, 3.5);
      const rect = viewport.getBoundingClientRect();
      const cx = rect.width / 2;
      const cy = rect.height / 2;
      state.mapPan.x = cx - (cx - state.mapPan.x) * (state.mapZoom / oldZoom);
      state.mapPan.y = cy - (cy - state.mapPan.y) * (state.mapZoom / oldZoom);
      updateTransform();
    });
  }

  if (zoomOut) {
    zoomOut.addEventListener('click', () => {
      const oldZoom = state.mapZoom;
      state.mapZoom = Math.max(state.mapZoom - 0.25, 0.4);
      const rect = viewport.getBoundingClientRect();
      const cx = rect.width / 2;
      const cy = rect.height / 2;
      state.mapPan.x = cx - (cx - state.mapPan.x) * (state.mapZoom / oldZoom);
      state.mapPan.y = cy - (cy - state.mapPan.y) * (state.mapZoom / oldZoom);
      updateTransform();
    });
  }

  if (zoomReset) {
    zoomReset.addEventListener('click', () => {
      state.mapZoom = 1;
      centerMapInitially();
    });
  }

  // 5. LAYER TOGGLE BUTTONS
  if (selectAllBtn) {
    selectAllBtn.addEventListener('click', () => {
      if (state.mapData) {
        state.mapData.categories.forEach(c => state.activeLayers.add(c.id));
        renderMap();
      }
    });
  }

  if (deselectAllBtn) {
    deselectAllBtn.addEventListener('click', () => {
      state.activeLayers.clear();
      renderMap();
    });
  }

  if (filterUnfoundBtn) {
    filterUnfoundBtn.addEventListener('click', () => {
      state.hideFoundMarkers = !state.hideFoundMarkers;
      filterUnfoundBtn.classList.toggle('active', state.hideFoundMarkers);
      filterUnfoundBtn.textContent = state.hideFoundMarkers 
        ? (state.lang === 'pt' ? 'Mostrar Todos' : 'Show All') 
        : (state.lang === 'pt' ? 'Ocultar Encontrados' : 'Hide Found');
      renderMarkers();
    });
  }

  if (resetProgressBtn) {
    resetProgressBtn.addEventListener('click', () => {
      if (confirm(state.lang === 'pt' ? 'Deseja resetar o progresso dos marcadores encontrados?' : 'Reset found markers progress?')) {
        state.foundMarkers.clear();
        localStorage.removeItem('aniimo_found_markers');
        updateMapProgress();
        renderMarkers();
        showToast(state.lang === 'pt' ? 'Progresso do mapa resetado.' : 'Map progress reset.');
      }
    });
  }

  // 6. DETAIL CARD CLOSE
  if (detailCloseBtn) {
    detailCloseBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      detailCard.classList.remove('visible');
    });
  }

  // Clicking viewport canvas closes detail card
  viewport.addEventListener('click', (e) => {
    if (!e.target.closest('.map-marker') && !e.target.closest('.map-detail-card') && !e.target.closest('.map-controls')) {
      if (detailCard) detailCard.classList.remove('visible');
    }
  });
}

function updateMapProgress() {
  if (!state.mapData) return;
  const total = state.mapData.markers.length;
  const found = state.foundMarkers.size;
  const pct = Math.round((found / total) * 100);

  const fillEl = document.getElementById('map-progress-bar-fill');
  const textEl = document.getElementById('map-progress-text');
  if (fillEl) fillEl.style.width = `${pct}%`;
  if (textEl) textEl.textContent = `${found} / ${total} (${pct}%)`;
}

function renderMap() {
  if (!state.mapData) return;
  const layersEl = document.getElementById('map-layers-list');
  const isPt = state.lang === 'pt';

  if (layersEl) {
    layersEl.innerHTML = state.mapData.categories.map(cat => {
      const count = state.mapData.markers.filter(m => m.cat === cat.id).length;
      const isChecked = state.activeLayers.has(cat.id);
      return `
        <li class="map-layer-item ${isChecked ? 'active' : ''}" data-layer="${cat.id}">
          <span>${cat.icon} ${isPt ? cat.name_pt : cat.name_en}</span>
          <span class="map-layer-count">(${count})</span>
          <input type="checkbox" ${isChecked ? 'checked' : ''} />
        </li>
      `;
    }).join('');

    layersEl.querySelectorAll('.map-layer-item').forEach(li => {
      li.addEventListener('click', () => {
        const id = li.getAttribute('data-layer');
        if (state.activeLayers.has(id)) {
          state.activeLayers.delete(id);
          li.classList.remove('active');
          li.querySelector('input').checked = false;
        } else {
          state.activeLayers.add(id);
          li.classList.add('active');
          li.querySelector('input').checked = true;
        }
        renderMarkers();
      });
    });
  }

  updateMapProgress();
  renderMarkers();
}

function renderMarkers() {
  const container = document.getElementById('map-markers-container');
  if (!container || !state.mapData) return;

  const isPt = state.lang === 'pt';
  const visibleMarkers = state.mapData.markers.filter(m => {
    const layerActive = state.activeLayers.has(m.cat);
    const notHiddenByFound = !state.hideFoundMarkers || !state.foundMarkers.has(m.id);
    return layerActive && notHiddenByFound;
  });

  container.innerHTML = visibleMarkers.map(m => {
    const cat = state.mapData.categories.find(c => c.id === m.cat) || {};
    const isFound = state.foundMarkers.has(m.id);
    return `
      <div class="map-marker ${isFound ? 'found' : ''}" style="left:${m.x}%; top:${m.y}%; --marker-color:${cat.color || '#38bdf8'}" data-marker-id="${m.id}" title="${isPt ? m.name_pt : m.name_en}">
        ${cat.icon || '📍'}
      </div>
    `;
  }).join('');

  container.querySelectorAll('.map-marker').forEach(mEl => {
    mEl.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = mEl.getAttribute('data-marker-id');
      const marker = state.mapData.markers.find(m => m.id === id);
      if (marker) openMarkerDetail(marker);
    });
  });
}

function openMarkerDetail(m) {
  const card = document.getElementById('map-detail-card');
  if (!card) return;

  const isPt = state.lang === 'pt';
  const cat = state.mapData.categories.find(c => c.id === m.cat) || {};

  card.querySelector('.map-detail-title').textContent = isPt ? m.name_pt : m.name_en;
  card.querySelector('.map-detail-category').innerHTML = `<span style="color:${cat.color}; font-weight:800;">${cat.icon} ${isPt ? cat.name_pt : cat.name_en}</span> • <span style="font-family:var(--font-mono); font-size:0.75rem; color:var(--ink-muted);">${m.x.toFixed(1)}%, ${m.y.toFixed(1)}%</span>`;
  card.querySelector('.map-detail-desc').textContent = isPt ? m.desc_pt : m.desc_en;

  const foundBtn = card.querySelector('#btn-mark-found');
  const isFound = state.foundMarkers.has(m.id);
  foundBtn.textContent = isFound ? (isPt ? '✓ Encontrado' : '✓ Found') : (isPt ? 'Marcar como Encontrado' : 'Mark as Found');

  foundBtn.onclick = (e) => {
    e.stopPropagation();
    if (state.foundMarkers.has(m.id)) {
      state.foundMarkers.delete(m.id);
      foundBtn.textContent = isPt ? 'Marcar como Encontrado' : 'Mark as Found';
    } else {
      state.foundMarkers.add(m.id);
      foundBtn.textContent = isPt ? '✓ Encontrado' : '✓ Found';
    }
    localStorage.setItem('aniimo_found_markers', JSON.stringify(Array.from(state.foundMarkers)));
    updateMapProgress();
    renderMarkers();
  };

  card.classList.add('visible');

  // Center marker smoothly in view
  centerMarkerInView(m);
}

function centerMarkerInView(m) {
  const viewport = document.getElementById('map-viewport');
  const container = document.getElementById('map-container');
  if (!viewport || !container) return;
  const rect = viewport.getBoundingClientRect();
  const markerPxX = (m.x / 100) * 1000;
  const markerPxY = (m.y / 100) * 1000;
  state.mapPan.x = (rect.width / 2) - (markerPxX * state.mapZoom);
  state.mapPan.y = (rect.height / 2) - (markerPxY * state.mapZoom);
  container.style.transform = `translate(${state.mapPan.x}px, ${state.mapPan.y}px) scale(${state.mapZoom})`;
}

// TYPE CHART & CALCULATOR
function setupTypeChart() {
  renderTypeChart();

  const atkSel = document.getElementById('calc-attacker');
  const defSel = document.getElementById('calc-defender');
  if (atkSel && defSel) {
    atkSel.addEventListener('change', calculateTypeMatchup);
    defSel.addEventListener('change', calculateTypeMatchup);
  }
}

function renderTypeChart() {
  if (!state.typeChart) return;

  const isPt = state.lang === 'pt';
  const elements = isPt ? state.typeChart.elements_pt : state.typeChart.elements_en;
  const matrix = state.typeChart.matrix;

  const atkSel = document.getElementById('calc-attacker');
  const defSel = document.getElementById('calc-defender');
  if (atkSel && defSel) {
    const opts = elements.map(e => `<option value="${e}">${e}</option>`).join('');
    atkSel.innerHTML = opts;
    defSel.innerHTML = opts;
    defSel.selectedIndex = 1;
    calculateTypeMatchup();
  }

  const table = document.getElementById('type-matrix-table');
  if (table) {
    let html = `<thead><tr><th>Atacante \\ Defensor</th>${elements.map(e => `<th>${e}</th>`).join('')}</tr></thead><tbody>`;
    
    elements.forEach(atk => {
      html += `<tr><th>${atk}</th>`;
      elements.forEach(def => {
        const mult = (matrix[atk] && matrix[atk][def] !== undefined) ? matrix[atk][def] : 1.0;
        let cellClass = 'cell-normal';
        if (mult === 2.0) cellClass = 'cell-super';
        else if (mult === 0.5) cellClass = 'cell-weak';
        else if (mult === 0.0) cellClass = 'cell-immune';

        html += `<td class="${cellClass}">${mult}x</td>`;
      });
      html += `</tr>`;
    });

    html += `</tbody>`;
    table.innerHTML = html;
  }
}

function calculateTypeMatchup() {
  const atk = document.getElementById('calc-attacker').value;
  const def = document.getElementById('calc-defender').value;
  const multEl = document.getElementById('type-multiplier');
  const descEl = document.getElementById('type-calc-desc');
  const d = I18N[state.lang];

  if (!state.typeChart || !multEl) return;

  const matrix = state.typeChart.matrix;
  const mult = (matrix[atk] && matrix[atk][def] !== undefined) ? matrix[atk][def] : 1.0;

  multEl.textContent = `${mult}x`;
  multEl.className = 'type-result-mult';

  if (mult === 2.0) {
    multEl.classList.add('super');
    descEl.textContent = d.super_effective;
  } else if (mult === 0.5) {
    multEl.classList.add('weak');
    descEl.textContent = d.not_effective;
  } else if (mult === 0.0) {
    multEl.classList.add('immune');
    descEl.textContent = d.immune_damage;
  } else {
    multEl.classList.add('normal');
    descEl.textContent = d.normal_damage;
  }
}

// TIER LIST
function setupTierList() {
  renderTierList();

  document.querySelectorAll('.tier-role-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tier-role-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const role = btn.getAttribute('data-role');
      filterTierList(role);
    });
  });
}

function filterTierList(role) {
  if (!state.tierList) return;
  const filtered = role === 'all' 
    ? state.tierList.items 
    : state.tierList.items.filter(i => i.role.toLowerCase() === role.toLowerCase());
  renderTierRows(filtered);
}

function renderTierList() {
  if (!state.tierList) return;
  renderTierRows(state.tierList.items);
}

function renderTierRows(items) {
  const tiers = ["S+", "S", "A", "B"];
  tiers.forEach(t => {
    const container = document.getElementById(`tier-content-${t.replace('+', '-plus').toLowerCase()}`);
    if (!container) return;

    const tierItems = items.filter(i => i.tier === t);
    container.innerHTML = tierItems.map(item => `
      <div class="tier-creature-item" data-slug="${item.slug}">
        <img class="tier-creature-img" src="/assets/creatures/${item.slug}.webp" alt="${item.name}" />
        <span class="tier-creature-name">${item.name}</span>
        <small style="font-size:0.68rem; color:var(--ink-muted)">${item.role}</small>
      </div>
    `).join('');

    container.querySelectorAll('.tier-creature-item').forEach(card => {
      card.addEventListener('click', () => {
        const slug = card.getAttribute('data-slug');
        const c = state.creatures.find(cr => cr.slug === slug);
        if (c) openCreatureModal(c);
      });
    });
  });
}

// ITEMS & GUIDES
function setupItemsAndGuides() {
  renderItems();
  renderGuides();
}

function renderItems() {
  const container = document.getElementById('items-container');
  if (!container || !state.items) return;

  const isPt = state.lang === 'pt';
  container.innerHTML = state.items.map(item => `
    <div class="tool-card" style="cursor:default;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span class="role-pill">${isPt ? item.category_pt : item.category_en}</span>
        <span style="color:#eab308; font-weight:800;">${'★'.repeat(item.rarity)}</span>
      </div>
      <h3 class="tool-card-title" style="font-size:1.15rem;">${isPt ? item.name_pt : item.name_en}</h3>
      <p class="tool-card-desc">${isPt ? item.desc_pt : item.desc_en}</p>
    </div>
  `).join('');
}

function renderGuides() {
  const container = document.getElementById('guides-container');
  if (!container || !state.guides) return;

  const isPt = state.lang === 'pt';
  container.innerHTML = state.guides.map(g => `
    <article class="guide-box" style="margin:0 0 2rem 0; max-width:100%;">
      <span class="brand-badge">${isPt ? g.category_pt : g.category_en} • ${g.read_time}</span>
      <h2 class="section-title" style="font-size:1.6rem; text-align:left; margin-top:0.5rem;">${isPt ? g.title_pt : g.title_en}</h2>
      <p style="color:var(--ink-soft); margin-bottom:1.25rem;">${isPt ? g.summary_pt : g.summary_en}</p>
      <div style="white-space:pre-line; color:var(--ink); font-size:0.95rem; line-height:1.7;">${g.content_pt}</div>
    </article>
  `).join('');
}

// TOAST HELPER
function showToast(msg) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = msg;
  container.appendChild(toast);
  setTimeout(() => { toast.remove(); }, 3000);
}

// MODAL CLOSE LISTENERS & KEYBOARD ESCAPE
function closeCreatureModal() {
  const modal = document.getElementById('creature-modal');
  if (modal && modal.classList.contains('open')) {
    modal.classList.remove('open');
    const segment = window.location.pathname.replace(/^\/+/, '').split('/')[0].toLowerCase();
    const isCreature = state.creatures && state.creatures.some(c => c.slug.toLowerCase() === segment);
    if (isCreature) {
      history.pushState(null, '', '/criaturas');
      document.title = 'Registro Anii: 94 Criaturas, Fraquezas e Stats — Aniimo Tools Brasil';
    }
  }
}

window.addEventListener('click', (e) => {
  const modal = document.getElementById('creature-modal');
  if (e.target === modal || e.target.closest('.modal-close-btn')) {
    closeCreatureModal();
  }
});

window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeCreatureModal();
    const mapCard = document.getElementById('map-detail-card');
    if (mapCard) mapCard.classList.remove('visible');
  }
});
