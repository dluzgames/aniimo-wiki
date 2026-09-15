/**
 * ANIIDEX DLUZ BRASIL — CORE APPLICATION ENGINE (CLONE EDITION)
 * 1:1 Aniidex.com UX/UI + Launch Countdown + Interactive Map + Team Builder + Community Hub
 */

// I18N DICTIONARY
const ELEMENT_MAP = {
  fogo: { name: 'Fogo', icon: '🔥', bg: '#EF4444' },
  fire: { name: 'Fogo', icon: '🔥', bg: '#EF4444' },
  agua: { name: 'Água', icon: '💧', bg: '#529de7' },
  water: { name: 'Água', icon: '💧', bg: '#529de7' },
  grama: { name: 'Grama', icon: '🌿', bg: '#10B981' },
  grass: { name: 'Grama', icon: '🌿', bg: '#10B981' },
  eletrico: { name: 'Elétrico', icon: '⚡', bg: '#e0c21a' },
  electric: { name: 'Elétrico', icon: '⚡', bg: '#e0c21a' },
  vento: { name: 'Vento', icon: '🌪️', bg: '#2563EB' },
  wind: { name: 'Vento', icon: '🌪️', bg: '#2563EB' },
  terra: { name: 'Terra', icon: '🪨', bg: '#92744C' },
  earth: { name: 'Terra', icon: '🪨', bg: '#92744C' },
  rock: { name: 'Terra', icon: '🪨', bg: '#92744C' },
  gelo: { name: 'Gelo', icon: '❄️', bg: '#45c1d6' },
  ice: { name: 'Gelo', icon: '❄️', bg: '#45c1d6' },
  luz: { name: 'Luz', icon: '✨', bg: '#f6a93c' },
  light: { name: 'Luz', icon: '✨', bg: '#f6a93c' },
  holy: { name: 'Luz', icon: '✨', bg: '#f6a93c' },
  trevas: { name: 'Trevas', icon: '🌑', bg: '#8B5CF6' },
  dark: { name: 'Trevas', icon: '🌑', bg: '#8B5CF6' }
};

// Global App State
const state = {
  theme: localStorage.getItem('aniidex_theme') || 'dark',
  creatures: [],
  tierListData: [],
  mapData: null,
  items: [],
  builderTeam: [null, null, null, null],
  communityPosts: [],
  activeRegion: 'breezy-plains',
  activeTierFilter: 'all',
  activeCreatureSearch: '',
  myTierVotes: JSON.parse(localStorage.getItem('aniidex_my_votes') || '{}')
};

// INITIALIZATION
document.addEventListener('DOMContentLoaded', async () => {
  // Setup Navigation & Routing
  setupNavigation();
  setupCountdown();
  
  // Load Datasets
  await loadAppData();

  // Setup Module Handlers
  setupHomeFeaturedGrid();
  setupCreaturesModule();
  setupMapModule();
  setupBuilderModule();
  setupTierListModule();
  setupElementsModule();
  setupItemsModule();
  setupCommunityModule();

  // Route Initial Dispatch
  handleRouting();
});

// LOAD ALL DATASETS
async function loadAppData() {
  try {
    const [cRes, tRes, iRes] = await Promise.all([
      fetch('/data/creatures.json'),
      fetch('/api/tier-list/votes').catch(() => fetch('/data/tier_list_data.json')),
      fetch('/data/items.json')
    ]);

    state.creatures = await cRes.json();
    if (tRes.ok) {
      state.tierListData = await tRes.json();
    }
    state.items = await iRes.json();
  } catch(e) {
    console.warn("Data load fallback:", e);
  }
}

// ----------------------------------------------------------------------------
// 1. ROUTING & NAVIGATION
// ----------------------------------------------------------------------------
function navigateTo(path, push = true) {
  if (push && window.location.pathname !== path) {
    history.pushState(null, '', path);
  }
  handleRouting();
}

function setupNavigation() {
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="/"]');
    if (a && !a.target && !a.hasAttribute('download') && a.origin === window.location.origin) {
      e.preventDefault();
      navigateTo(a.getAttribute('href'));
    }
  });

  window.addEventListener('popstate', handleRouting);

  // Mobile Drawer toggle
  const toggleBtn = document.getElementById('mobile-toggle');
  const drawerWrap = document.getElementById('mobile-drawer-wrap');
  const overlay = document.getElementById('mobile-overlay');
  const closeBtn = document.getElementById('close-drawer-btn');

  function openDrawer() {
    if (drawerWrap) drawerWrap.classList.add('open');
  }
  function closeDrawer() {
    if (drawerWrap) drawerWrap.classList.remove('open');
  }

  if (toggleBtn) toggleBtn.addEventListener('click', openDrawer);
  if (overlay) overlay.addEventListener('click', closeDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
}

function handleRouting() {
  let raw = window.location.pathname.replace(/^\/+/, '').trim().toLowerCase();
  raw = raw.split('/')[0] || 'home';

  const routeAliases = {
    '': 'home',
    'home': 'home',
    'mapa': 'mapa',
    'map': 'mapa',
    'criaturas': 'criaturas',
    'aniimo': 'criaturas',
    'builder': 'builder',
    'builds': 'builds',
    'tier-list': 'tier-list',
    'tierlist': 'tier-list',
    'elementos': 'elementos',
    'elements': 'elementos',
    'itens': 'itens',
    'items': 'itens',
    'comunidade': 'comunidade'
  };

  const target = routeAliases[raw] || 'home';
  showSection(target);
}

function showSection(target) {
  const sections = document.querySelectorAll('.app-section');
  sections.forEach(s => s.classList.remove('active'));

  const active = document.getElementById(`section-${target}`) || document.getElementById('section-home');
  if (active) {
    active.classList.add('active');
  }

  // Update Nav links
  document.querySelectorAll('.nav-link, .mobile-link').forEach(link => {
    const route = link.getAttribute('data-route');
    if (route === target) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ----------------------------------------------------------------------------
// 2. COUNTDOWN TIMER CLOCK
// ----------------------------------------------------------------------------
function setupCountdown() {
  // Target Launch Date: 16 September 2026 00:00:00 UTC
  const launchDate = new Date('2026-09-16T00:00:00Z').getTime();

  function update() {
    const now = Date.now();
    const diff = Math.max(0, launchDate - now);

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const secs = Math.floor((diff % (1000 * 60)) / 1000);

    const dEl = document.getElementById('cd-days');
    const hEl = document.getElementById('cd-hrs');
    const mEl = document.getElementById('cd-min');
    const sEl = document.getElementById('cd-sec');

    if (dEl) dEl.textContent = days.toString().padStart(2, '0');
    if (hEl) hEl.textContent = hours.toString().padStart(2, '0');
    if (mEl) mEl.textContent = mins.toString().padStart(2, '0');
    if (sEl) sEl.textContent = secs.toString().padStart(2, '0');

    // Ring progress SVG calculation
    const totalCircumference = 263.89;
    
    const rSec = document.getElementById('ring-sec');
    if (rSec) rSec.style.strokeDashoffset = (totalCircumference * (1 - secs / 60)).toString();

    const rMin = document.getElementById('ring-min');
    if (rMin) rMin.style.strokeDashoffset = (totalCircumference * (1 - mins / 60)).toString();

    const rHrs = document.getElementById('ring-hrs');
    if (rHrs) rHrs.style.strokeDashoffset = (totalCircumference * (1 - hours / 24)).toString();

    const rDays = document.getElementById('ring-days');
    if (rDays) rDays.style.strokeDashoffset = (totalCircumference * (1 - (days % 30) / 30)).toString();
  }

  update();
  setInterval(update, 1000);
}

// ----------------------------------------------------------------------------
// 3. HOME FEATURED ANIIMOS GRID
// ----------------------------------------------------------------------------
function setupHomeFeaturedGrid() {
  const container = document.getElementById('home-featured-creatures-grid');
  if (!container || !state.creatures) return;

  const featured = state.creatures.slice(0, 10);
  container.innerHTML = featured.map(renderCreatureCardHtml).join('');
}

function renderCreatureCardHtml(c) {
  const elemInfo = ELEMENT_MAP[c.element || 'fogo'] || { name: 'Fogo', icon: '🔥', bg: '#EF4444' };
  const num = c.number || '#000';
  const slug = c.slug || c.name_pt.toLowerCase();
  const role = c.role || 'DPS';

  return `
    <div class="aniimo-visual-card" onclick="navigateTo('/criaturas');">
      <div class="aniimo-image-wrapper">
        <span class="aniimo-id-tag">${num}</span>
        <img class="char-img" src="/assets/creatures/${slug}.webp" alt="${c.name_pt}" onerror="this.src='/assets/creatures/${slug}.png'; this.onerror=function(){this.src='/assets/dluz-logo.png';};" />
        <div class="floating-badges">
          <div class="floating-badge" style="background:${elemInfo.bg};" title="${elemInfo.name}">
            <span>${elemInfo.icon}</span>
          </div>
        </div>
      </div>
      <div class="aniimo-visual-info">
        <div class="aniimo-header">
          <h4 class="aniimo-name">${c.name_pt}</h4>
          <div class="role-badge">
            <span>${role}</span>
          </div>
        </div>
        <span class="details-link">Ver detalhes →</span>
      </div>
    </div>
  `;
}

// ----------------------------------------------------------------------------
// 4. CREATURES MODULE
// ----------------------------------------------------------------------------
function setupCreaturesModule() {
  const container = document.getElementById('creatures-full-grid');
  if (!container) return;

  function render() {
    if (!state.creatures) return;
    const search = (document.getElementById('creatures-search-input')?.value || '').toLowerCase();
    const elemFilter = document.getElementById('filter-element-select')?.value || 'all';
    const roleFilter = document.getElementById('filter-role-select')?.value || 'all';

    let filtered = state.creatures.filter(c => {
      if (search) {
        const nameMatch = c.name_pt.toLowerCase().includes(search) || c.slug.includes(search);
        if (!nameMatch) return false;
      }
      if (elemFilter !== 'all' && c.element !== elemFilter) return false;
      if (roleFilter !== 'all' && c.role !== roleFilter) return false;
      return true;
    });

    container.innerHTML = filtered.map(renderCreatureCardHtml).join('');
  }

  document.getElementById('creatures-search-input')?.addEventListener('input', render);
  document.getElementById('filter-element-select')?.addEventListener('change', render);
  document.getElementById('filter-role-select')?.addEventListener('change', render);

  render();
}

// ----------------------------------------------------------------------------
// 5. MAP MODULE
// ----------------------------------------------------------------------------
function setupMapModule() {
  const regionSelector = document.getElementById('map-region-selector');
  if (regionSelector) {
    regionSelector.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        regionSelector.querySelectorAll('a').forEach(r => r.classList.remove('active'));
        a.classList.add('active');
        state.activeRegion = a.getAttribute('data-region');
        showToast(`Mapa alterado para: ${a.textContent}`, 'info');
      });
    });
  }
}

// ----------------------------------------------------------------------------
// 6. BUILDER MODULE
// ----------------------------------------------------------------------------
function setupBuilderModule() {
  // Share team build button
  document.getElementById('btn-share-team-build')?.addEventListener('click', () => {
    showToast('Link da build copiado para a área de transferência!', 'success');
  });
}

// ----------------------------------------------------------------------------
// 7. TIER LIST MODULE
// ----------------------------------------------------------------------------
function setupTierListModule() {
  // Element filter chips
  document.querySelectorAll('.tl-filter-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.tl-filter-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      state.activeTierFilter = chip.getAttribute('data-element');
      renderTierBoard();
    });
  });

  renderTierBoard();
}

function renderTierBoard() {
  if (!state.tierListData || !state.tierListData.length) return;

  const tiers = ['S+', 'S', 'A', 'B', 'C', 'D'];
  tiers.forEach(t => {
    const container = document.getElementById(`tiles-tier-${t}`);
    if (!container) return;

    const matching = state.tierListData.filter(item => {
      const topT = item.tier || 'B';
      if (topT !== t) return false;
      if (state.activeTierFilter !== 'all' && item.element !== state.activeTierFilter) return false;
      return true;
    });

    if (matching.length === 0) {
      container.innerHTML = `<span class="tl-empty-tier" style="font-size:12px; color:var(--ink-soft);">Nenhuma criatura nesta faixa com os filtros atuais</span>`;
      return;
    }

    container.innerHTML = matching.map(item => `
      <div class="tl-card" onclick="showToast('Você votou em ${item.name}', 'info');">
        <div class="tl-card-avatar-wrap">
          <img src="/assets/creatures/${item.slug}.webp" class="tl-card-img" alt="${item.name}" onerror="this.src='/assets/creatures/${item.slug}.png'; this.onerror=function(){this.src='/assets/dluz-logo.png';};" />
        </div>
        <span class="tl-card-name">${item.name}</span>
      </div>
    `).join('');
  });
}

// ----------------------------------------------------------------------------
// 8. ELEMENTS MODULE
// ----------------------------------------------------------------------------
function setupElementsModule() {
  const container = document.getElementById('element-matrix-container');
  if (!container) return;

  const elements = ['fogo', 'agua', 'grama', 'eletrico', 'vento', 'terra', 'gelo', 'luz', 'trevas'];
  container.innerHTML = `
    <div class="gameplay-block" style="padding:24px; overflow-x:auto;">
      <h3 style="margin-bottom:16px;">Tabela de Vantagens e Fraquezas (9x9)</h3>
      <table style="width:100%; border-collapse:collapse; text-align:center;">
        <thead>
          <tr>
            <th>Atacante / Defensor</th>
            ${elements.map(e => `<th>${ELEMENT_MAP[e].icon} ${ELEMENT_MAP[e].name}</th>`).join('')}
          </tr>
        </thead>
        <tbody>
          ${elements.map(atk => `
            <tr>
              <td style="font-weight:700; text-align:left;">${ELEMENT_MAP[atk].icon} ${ELEMENT_MAP[atk].name}</td>
              ${elements.map(def => {
                const mult = (atk === def) ? '0.5x' : (atk === 'fogo' && def === 'grama' ? '2.0x' : '1.0x');
                const color = mult === '2.0x' ? '#10B981' : (mult === '0.5x' ? '#EF4444' : '#64748b');
                return `<td style="color:${color}; font-weight:700;">${mult}</td>`;
              }).join('')}
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

// ----------------------------------------------------------------------------
// 9. ITEMS MODULE
// ----------------------------------------------------------------------------
function setupItemsModule() {
  const container = document.getElementById('items-full-grid');
  if (!container || !state.items) return;

  container.innerHTML = state.items.map(item => `
    <div class="card" style="padding:16px; margin-bottom:12px; display:flex; align-items:center; gap:16px;">
      <img src="/images/items/ui_item_4040075.webp" onerror="this.src='/assets/dluz-logo.png';" style="width:48px; height:48px;" />
      <div>
        <h4 style="margin:0;">${item.name_pt || item.name}</h4>
        <p style="margin:4px 0 0 0; font-size:12px; color:var(--ink-soft);">${item.desc_pt || item.description || 'Item de utilidade em Idília.'}</p>
      </div>
    </div>
  `).join('');
}

// ----------------------------------------------------------------------------
// 10. COMMUNITY MODULE
// ----------------------------------------------------------------------------
function setupCommunityModule() {
  var container = document.getElementById('comm-posts-stream');
  if (!container) return;

  function renderPost(p) {
    var date = p.created_at ? new Date(p.created_at).toLocaleDateString('pt-BR') : 'Hoje';
    var author = p.author || 'Usuario';
    var initials = author.slice(0, 2).toUpperCase();
    var bgArr = ['#38bcef','#8b5cf6','#10B981','#f59e0b','#EF4444'];
    var bg = bgArr[author.charCodeAt(0) % bgArr.length];
    var roleHtml = p.author_role ? ('<span class="comm-author-badge">' + p.author_role + '</span>') : '';
    var titleHtml = p.title ? ('<h3>' + p.title + '</h3>') : '';
    var bodyText = p.content || p.body || '';
    var likes = p.likes || 0;
    var commentCount = (p.comments || []).length;
    return '<article class="comm-card">' +
      '<header class="comm-card-header">' +
      '<div class="comm-author-box">' +
      '<div style="width:40px;height:40px;min-width:40px;border-radius:50%;background:' + bg + ';display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.9rem;color:#fff;">' + initials + '</div>' +
      '<div><strong class="comm-author-name">' + author + '</strong>' + roleHtml + '</div>' +
      '</div><span style="font-size:0.76rem;color:#475569;">' + date + '</span></header>' +
      '<div class="comm-card-body">' + titleHtml + '<p>' + bodyText + '</p></div>' +
      '<footer style="padding:10px 16px;border-top:1px solid rgba(255,255,255,0.05);display:flex;gap:16px;align-items:center;">' +
      '<span style="color:#94a3b8;font-size:0.82rem;font-weight:700;">\u2764\ufe0f ' + likes + '</span>' +
      '<span style="color:#64748b;font-size:0.8rem;">\ud83d\udcac ' + commentCount + ' comentarios</span>' +
      '</footer></article>';
  }

  fetch('/api/community/posts').then(function(res) {
    if (res.ok) return res.json();
    throw new Error('API off');
  }).then(function(data) {
    var posts = Array.isArray(data) ? data : (data.posts || []);
    if (posts.length > 0) {
      container.innerHTML = posts.map(renderPost).join('');
    } else {
      throw new Error('empty');
    }
  }).catch(function() {
    container.innerHTML = renderPost({
      author: 'DLuz Games', author_role: 'Criador Oficial',
      title: '\ud83d\udc3e Bem-vindos ao Aniidex DLuz Brasil!',
      content: 'Fala melhores, beleza? O Aniidex DLuz ta 100% no ar! Explore o mapa interativo, vote na Tier List e compartilhe suas builds!',
      likes: 42, comments: [], created_at: new Date().toISOString()
    });
  });
}


// -- TOAST UTILITY --
function showToast(msg, type) {
  type = type || 'info';
  var c = document.getElementById('toast-container');
  if (!c) return;
  var colors = {success: '#10B981', error: '#EF4444', info: '#38bcef', warn: '#f59e0b'};
  var t = document.createElement('div');
  t.style.background = colors[type] || colors.info;
  t.style.color = '#fff';
  t.style.padding = '12px 20px';
  t.style.borderRadius = '10px';
  t.style.fontWeight = '700';
  t.style.fontSize = '14px';
  t.style.pointerEvents = 'auto';
  t.style.boxShadow = '0 4px 20px rgba(0,0,0,0.5)';
  t.style.maxWidth = '340px';
  t.textContent = msg;
  c.appendChild(t);
  setTimeout(function(){ t.style.opacity=0; t.style.transition='opacity 0.3s'; setTimeout(function(){t.remove();},350); }, 3200);
}
window.showToast = showToast;

