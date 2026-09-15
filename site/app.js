/**
 * ANIIDEX DLUZ BRASIL — CORE APPLICATION ENGINE (COMPLETE EDITION)
 * 1:1 Aniidex.com Architecture + Google Stitch UI + Full Interactive Suite
 */

// 1. I18N ELEMENT DICTIONARY
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

// 2. GLOBAL APP STATE
const state = {
  theme: localStorage.getItem('aniidex_theme') || 'dark',
  creatures: [],
  tierListData: [],
  mapData: null,
  items: [],
  builderTeam: [null, null, null, null],
  activeSlotIndex: 0,
  communityPosts: [],
  activeRegion: 'breezy-plains',
  activeTierFilter: 'all',
  activeCreatureSearch: '',
  mapZoom: 1,
  mapPan: { x: -150, y: -150 },
  activeLayers: new Set(['aniimo', 'teleport', 'chest', 'boss', 'egg', 'resource']),
  hideFoundMarkers: false,
  foundMarkers: new Set(JSON.parse(localStorage.getItem('aniidex_found_markers') || '[]')),
  selectedVoteCreature: null,
  selectedVoteTier: 'A'
};

// 3. INITIALIZATION
document.addEventListener('DOMContentLoaded', async () => {
  setupNavigation();
  setupCountdown();
  setupModals();
  
  await loadAppData();

  setupHomeFeaturedGrid();
  setupCreaturesModule();
  setupMapModule();
  setupBuilderModule();
  setupTierListModule();
  setupElementsModule();
  setupItemsModule();
  setupCommunityModule();

  handleRouting();
});

// 4. LOAD ALL DATASETS
async function loadAppData() {
  try {
    const [cRes, tRes, iRes, mRes] = await Promise.all([
      fetch('/data/creatures.json'),
      fetch('/api/tier-list/votes').catch(() => fetch('/data/tier_list_data.json')),
      fetch('/data/items.json'),
      fetch('/data/map_data.json').catch(() => null)
    ]);

    if (cRes.ok) state.creatures = await cRes.json();
    if (tRes && tRes.ok) state.tierListData = await tRes.json();
    if (iRes.ok) state.items = await iRes.json();
    if (mRes && mRes.ok) state.mapData = await mRes.json();
  } catch (e) {
    console.warn("Dataset load fallback:", e);
  }
}

// ----------------------------------------------------------------------------
// 5. ROUTING & SPA NAVIGATION
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

  const toggleBtn = document.getElementById('mobile-toggle');
  const drawerWrap = document.getElementById('mobile-drawer-wrap');
  const overlay = document.getElementById('mobile-overlay');
  const closeBtn = document.getElementById('close-drawer-btn');

  function openDrawer() { if (drawerWrap) drawerWrap.classList.add('open'); }
  function closeDrawer() { if (drawerWrap) drawerWrap.classList.remove('open'); }

  if (toggleBtn) toggleBtn.addEventListener('click', openDrawer);
  if (overlay) overlay.addEventListener('click', closeDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);

  document.querySelectorAll('.mobile-link').forEach(link => {
    link.addEventListener('click', closeDrawer);
  });
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
  document.querySelectorAll('.app-section').forEach(s => s.classList.remove('active'));
  const active = document.getElementById(`section-${target}`) || document.getElementById('section-home');
  if (active) active.classList.add('active');

  document.querySelectorAll('.nav-link, .mobile-link').forEach(link => {
    const route = link.getAttribute('data-route');
    if (route === target) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });

  // Trigger region map rendering if opening map section
  if (target === 'mapa' && state.mapData) {
    setTimeout(renderMapMarkers, 100);
  }
}

// ----------------------------------------------------------------------------
// 6. LAUNCH COUNTDOWN TIMER
// ----------------------------------------------------------------------------
function setupCountdown() {
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
// 7. HOME FEATURED CREATURES GRID
// ----------------------------------------------------------------------------
function setupHomeFeaturedGrid() {
  const container = document.getElementById('home-featured-creatures-grid');
  if (!container || !state.creatures.length) return;

  const featured = state.creatures.slice(0, 10);
  container.innerHTML = featured.map(renderCreatureCardHtml).join('');
}

function renderCreatureCardHtml(c) {
  const elemInfo = ELEMENT_MAP[c.element || 'fogo'] || { name: 'Fogo', icon: '🔥', bg: '#EF4444' };
  const num = c.number || '#000';
  const slug = c.slug || (c.name_pt || '').toLowerCase();
  const role = c.role || 'DPS';

  return `
    <div class="aniimo-visual-card" onclick="navigateTo('/criaturas');">
      <div class="aniimo-image-wrapper">
        <span class="aniimo-id-tag">${num}</span>
        <img class="char-img" src="/assets/creatures/${slug}.webp" alt="${c.name_pt || c.name}" onerror="this.src='/assets/creatures/${slug}.png'; this.onerror=function(){this.src='/assets/dluz-logo.png';};" />
        <div class="floating-badges">
          <div class="floating-badge" style="background:${elemInfo.bg};" title="${elemInfo.name}">
            <span>${elemInfo.icon}</span>
          </div>
        </div>
      </div>
      <div class="aniimo-visual-info">
        <div class="aniimo-header">
          <h4 class="aniimo-name">${c.name_pt || c.name}</h4>
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
// 8. CREATURES DATABASE MODULE
// ----------------------------------------------------------------------------
function setupCreaturesModule() {
  const container = document.getElementById('creatures-full-grid');
  if (!container) return;

  function render() {
    if (!state.creatures.length) return;
    const search = (document.getElementById('creatures-search-input')?.value || '').toLowerCase();
    const elemFilter = document.getElementById('filter-element-select')?.value || 'all';
    const roleFilter = document.getElementById('filter-role-select')?.value || 'all';

    const filtered = state.creatures.filter(c => {
      if (search) {
        const namePt = (c.name_pt || '').toLowerCase();
        const slug = (c.slug || '').toLowerCase();
        if (!namePt.includes(search) && !slug.includes(search)) return false;
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
// 9. INTERACTIVE MAP ENGINE MODULE
// ----------------------------------------------------------------------------
function setupMapModule() {
  const viewport = document.getElementById('imap-viewport-container');
  const container = document.getElementById('imap-container');
  const bg = document.getElementById('imap-canvas-bg');
  const zoomIn = document.getElementById('map-zoom-in');
  const zoomOut = document.getElementById('map-zoom-out');
  const zoomReset = document.getElementById('map-reset-view');
  const searchInput = document.getElementById('map-search-input');
  const toggleFoundBtn = document.getElementById('btn-toggle-found-markers');
  const regionSelector = document.getElementById('map-region-selector');

  const regionBackgrounds = {
    'breezy-plains': '/images/map/map_3000_full.webp',
    'astra': '/assets/map/astra.webp',
    'whisperwake-isles': '/assets/map/whisperwake-isles.webp'
  };

  function updateRegion(region) {
    state.activeRegion = region;
    const bgUrl = regionBackgrounds[region] || regionBackgrounds['breezy-plains'];
    if (bg) {
      bg.style.backgroundImage = `url('${bgUrl}')`;
    }
    renderMapMarkers();
  }

  // Set initial background
  updateRegion('breezy-plains');

  if (regionSelector) {
    regionSelector.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        regionSelector.querySelectorAll('a').forEach(r => r.classList.remove('active'));
        a.classList.add('active');
        const reg = a.getAttribute('data-region');
        updateRegion(reg);
        showToast(`Mapa alternado para: ${a.textContent}`, 'info');
      });
    });
  }

  function updateTransform() {
    if (container) {
      container.style.transform = `translate(${state.mapPan.x}px, ${state.mapPan.y}px) scale(${state.mapZoom})`;
    }
  }

  if (viewport) {
    // Center map initially
    const vpRect = viewport.getBoundingClientRect();
    if (vpRect.width > 0 && vpRect.height > 0) {
      state.mapPan.x = (vpRect.width / 2) - 1100 * state.mapZoom;
      state.mapPan.y = (vpRect.height / 2) - 1100 * state.mapZoom;
      updateTransform();
    }

    // Drag Pan
    let isDragging = false;
    let startX = 0, startY = 0;

    viewport.addEventListener('mousedown', (e) => {
      if (e.target.closest('.map-marker') || e.target.closest('.imap-zoom-controls')) return;
      isDragging = true;
      startX = e.clientX - state.mapPan.x;
      startY = e.clientY - state.mapPan.y;
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      state.mapPan.x = e.clientX - startX;
      state.mapPan.y = e.clientY - startY;
      updateTransform();
    });

    window.addEventListener('mouseup', () => { isDragging = false; });

    // Mouse Wheel Zoom
    viewport.addEventListener('wheel', (e) => {
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.88;
      const oldZoom = state.mapZoom;
      const newZoom = Math.min(Math.max(oldZoom * zoomFactor, 0.4), 3.0);
      if (newZoom === oldZoom) return;

      const rect = viewport.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      state.mapPan.x = mouseX - (mouseX - state.mapPan.x) * (newZoom / oldZoom);
      state.mapPan.y = mouseY - (mouseY - state.mapPan.y) * (newZoom / oldZoom);
      state.mapZoom = newZoom;
      updateTransform();
    }, { passive: false });
  }

  // Controls
  if (zoomIn) zoomIn.addEventListener('click', () => {
    state.mapZoom = Math.min(state.mapZoom * 1.25, 3.0);
    updateTransform();
  });
  if (zoomOut) zoomOut.addEventListener('click', () => {
    state.mapZoom = Math.max(state.mapZoom * 0.8, 0.4);
    updateTransform();
  });
  if (zoomReset) zoomReset.addEventListener('click', () => {
    state.mapZoom = 1;
    if (viewport) {
      const vpRect = viewport.getBoundingClientRect();
      state.mapPan.x = (vpRect.width / 2) - 1100;
      state.mapPan.y = (vpRect.height / 2) - 1100;
    }
    updateTransform();
    showToast('Visualização do mapa centralizada!', 'info');
  });

  // Layer toggles
  document.querySelectorAll('.filter-checkbox input').forEach(input => {
    input.addEventListener('change', () => {
      const layer = input.getAttribute('data-layer');
      if (input.checked) {
        state.activeLayers.add(layer);
      } else {
        state.activeLayers.delete(layer);
      }
      renderMapMarkers();
    });
  });

  // Search filter
  if (searchInput) {
    searchInput.addEventListener('input', renderMapMarkers);
  }

  // Toggle found markers
  if (toggleFoundBtn) {
    toggleFoundBtn.addEventListener('click', () => {
      state.hideFoundMarkers = !state.hideFoundMarkers;
      toggleFoundBtn.textContent = state.hideFoundMarkers
        ? '👁️ Mostrar Marcadores Encontrados'
        : '👁️ Ocultar Marcadores Encontrados';
      renderMapMarkers();
    });
  }

  renderMapMarkers();
}

function renderMapMarkers() {
  const container = document.getElementById('imap-markers-layer');
  if (!container || !state.mapData || !state.mapData.markers) return;

  const query = (document.getElementById('map-search-input')?.value || '').toLowerCase();

  const visibleMarkers = state.mapData.markers.filter(m => {
    if (!state.activeLayers.has(m.cat)) return false;
    if (state.hideFoundMarkers && state.foundMarkers.has(m.id)) return false;
    if (query) {
      const name = (m.name_pt || m.name_en || '').toLowerCase();
      if (!name.includes(query)) return false;
    }
    return true;
  });

  const catMap = {};
  (state.mapData.categories || []).forEach(c => { catMap[c.id] = c; });

  container.innerHTML = visibleMarkers.map(m => {
    const cat = catMap[m.cat] || { icon: '📍', color: '#38bcef' };
    const isFound = state.foundMarkers.has(m.id);
    return `
      <div class="map-marker ${isFound ? 'found' : ''}" 
           style="left:${m.x}%; top:${m.y}%; --marker-color:${cat.color};" 
           data-id="${m.id}" 
           title="${m.name_pt || m.name_en}">
        ${cat.icon}
      </div>
    `;
  }).join('');

  // Marker click handler
  container.querySelectorAll('.map-marker').forEach(mEl => {
    mEl.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = mEl.getAttribute('data-id');
      const marker = state.mapData.markers.find(m => m.id === id);
      if (!marker) return;

      const isFound = state.foundMarkers.has(id);
      if (isFound) {
        state.foundMarkers.delete(id);
        mEl.classList.remove('found');
        showToast(`Marcador '${marker.name_pt}' desmarcado.`, 'info');
      } else {
        state.foundMarkers.add(id);
        mEl.classList.add('found');
        showToast(`Marcador '${marker.name_pt}' marcado como coletado!`, 'success');
      }
      localStorage.setItem('aniidex_found_markers', JSON.stringify([...state.foundMarkers]));
    });
  });
}

// ----------------------------------------------------------------------------
// 10. TEAM BUILDER MODULE
// ----------------------------------------------------------------------------
function setupBuilderModule() {
  const slots = [1, 2, 3, 4];
  slots.forEach(slotNum => {
    const card = document.querySelector(`.builder-slot-card[data-slot="${slotNum}"]`);
    const body = document.getElementById(`slot-body-${slotNum}`);
    const clearBtn = card?.querySelector('.btn-clear-slot');

    if (body) {
      body.addEventListener('click', () => {
        state.activeSlotIndex = slotNum - 1;
        openBuilderPicker();
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        state.builderTeam[slotNum - 1] = null;
        renderBuilderSlot(slotNum);
        updateBuilderSynergy();
        showToast(`Slot ${slotNum} esvaziado.`, 'info');
      });
    }
  });

  document.getElementById('btn-share-team-build')?.addEventListener('click', () => {
    const slugs = state.builderTeam.map(c => c ? c.slug : '').join(',');
    const url = `${window.location.origin}/builder?team=${slugs}`;
    navigator.clipboard.writeText(url).then(() => {
      showToast('🔗 Link da build copiado para a área de transferência!', 'success');
    }).catch(() => {
      showToast('Build compartilhada!', 'success');
    });
  });

  // Restore team from URL if present
  const params = new URLSearchParams(window.location.search);
  const teamParam = params.get('team');
  if (teamParam) {
    const slugs = teamParam.split(',');
    slugs.forEach((slug, idx) => {
      if (slug && idx < 4) {
        const found = state.creatures.find(c => c.slug === slug);
        if (found) state.builderTeam[idx] = found;
      }
    });
    slots.forEach(renderBuilderSlot);
    updateBuilderSynergy();
  }
}

function openBuilderPicker() {
  const modal = document.getElementById('modal-builder-picker');
  if (!modal) return;
  modal.classList.add('open');

  const searchInput = document.getElementById('picker-search-input');
  const elemFilter = document.getElementById('picker-element-filter');
  const grid = document.getElementById('picker-creatures-grid');
  const closeBtn = document.getElementById('modal-picker-close');

  if (closeBtn) closeBtn.onclick = () => modal.classList.remove('open');

  function renderPicker() {
    if (!grid || !state.creatures.length) return;
    const search = (searchInput?.value || '').toLowerCase();
    const elem = elemFilter?.value || 'all';

    const filtered = state.creatures.filter(c => {
      if (search && !(c.name_pt || '').toLowerCase().includes(search) && !c.slug.includes(search)) return false;
      if (elem !== 'all' && c.element !== elem) return false;
      return true;
    });

    grid.innerHTML = filtered.map(c => {
      const elemInfo = ELEMENT_MAP[c.element || 'fogo'] || { name: 'Fogo', icon: '🔥', bg: '#EF4444' };
      return `
        <div class="picker-card" data-slug="${c.slug}" style="background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.1); border-radius:10px; padding:8px; cursor:pointer; text-align:center; transition:all 0.2s;">
          <img src="/assets/creatures/${c.slug}.webp" style="width:54px; height:54px; object-fit:contain; margin:0 auto;" onerror="this.src='/assets/dluz-logo.png';" />
          <div style="font-size:12px; font-weight:800; color:#f8fafc; margin-top:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${c.name_pt}</div>
          <span style="display:inline-block; font-size:10px; padding:1px 6px; border-radius:4px; background:${elemInfo.bg}; color:#fff; margin-top:2px;">${elemInfo.icon} ${elemInfo.name}</span>
        </div>
      `;
    }).join('');

    grid.querySelectorAll('.picker-card').forEach(card => {
      card.addEventListener('click', () => {
        const slug = card.getAttribute('data-slug');
        const creature = state.creatures.find(c => c.slug === slug);
        if (creature) {
          state.builderTeam[state.activeSlotIndex] = creature;
          renderBuilderSlot(state.activeSlotIndex + 1);
          updateBuilderSynergy();
          modal.classList.remove('open');
          showToast(`${creature.name_pt} adicionado à equipe!`, 'success');
        }
      });
    });
  }

  if (searchInput) searchInput.oninput = renderPicker;
  if (elemFilter) elemFilter.onchange = renderPicker;

  renderPicker();
}

function renderBuilderSlot(slotNum) {
  const card = document.querySelector(`.builder-slot-card[data-slot="${slotNum}"]`);
  const body = document.getElementById(`slot-body-${slotNum}`);
  if (!card || !body) return;

  const creature = state.builderTeam[slotNum - 1];
  if (!creature) {
    card.classList.remove('filled');
    body.innerHTML = `
      <span class="slot-plus">+</span>
      <span>Selecionar Aniimo</span>
    `;
    return;
  }

  card.classList.add('filled');
  const elemInfo = ELEMENT_MAP[creature.element || 'fogo'] || { name: 'Fogo', icon: '🔥', bg: '#EF4444' };
  body.innerHTML = `
    <img src="/assets/creatures/${creature.slug}.webp" style="height:90px; width:auto; object-fit:contain; filter:drop-shadow(0 4px 10px rgba(0,0,0,0.6));" onerror="this.src='/assets/dluz-logo.png';" />
    <strong style="font-size:15px; color:#f8fafc; margin-top:6px;">${creature.name_pt}</strong>
    <div style="display:flex; gap:6px; margin-top:4px;">
      <span style="font-size:11px; font-weight:800; padding:2px 8px; border-radius:99px; background:${elemInfo.bg}; color:#fff;">${elemInfo.icon} ${elemInfo.name}</span>
      <span style="font-size:11px; font-weight:700; padding:2px 8px; border-radius:99px; background:rgba(255,255,255,0.1); color:#94a3b8;">${creature.role || 'DPS'}</span>
    </div>
  `;
}

function updateBuilderSynergy() {
  const container = document.getElementById('builder-synergy-analysis');
  if (!container) return;

  const team = state.builderTeam.filter(Boolean);
  if (!team.length) {
    container.innerHTML = `<p style="color:var(--ink-soft);">Selecione criaturas nos slots acima para visualizar as vantagens e fraquezas de sua equipe.</p>`;
    return;
  }

  const allElements = ['fogo', 'agua', 'grama', 'eletrico', 'vento', 'terra', 'gelo', 'luz', 'trevas'];
  const coverage = {};
  allElements.forEach(e => { coverage[e] = 0; });
  team.forEach(c => {
    if (coverage[c.element] !== undefined) coverage[c.element]++;
  });

  const coveredCount = Object.values(coverage).filter(v => v > 0).length;
  const ratingScore = Math.round((coveredCount / 9) * 100);

  container.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
      <div>
        <strong style="font-size:1.1rem; color:#f8fafc;">Cobertura Elemental da Equipe</strong>
        <span style="display:block; font-size:12px; color:#94a3b8;">${team.length}/4 Criaturas Selecionadas • ${coveredCount} de 9 Elementos Cobertos</span>
      </div>
      <div style="text-align:right;">
        <span style="font-size:1.4rem; font-weight:900; color:#38bcef;">${ratingScore}%</span>
        <span style="display:block; font-size:10px; text-transform:uppercase; color:#64748b; font-weight:800;">Sinergia</span>
      </div>
    </div>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(100px, 1fr)); gap:10px;">
      ${allElements.map(e => {
        const info = ELEMENT_MAP[e];
        const count = coverage[e];
        const isCovered = count > 0;
        return `
          <div style="background:${isCovered ? 'rgba(56,188,239,0.15)' : 'rgba(15,23,42,0.6)'}; border:1px solid ${isCovered ? '#38bcef' : 'rgba(255,255,255,0.06)'}; border-radius:8px; padding:8px; text-align:center;">
            <span style="font-size:1.2rem;">${info.icon}</span>
            <span style="display:block; font-size:11px; font-weight:700; color:${isCovered ? '#fff' : '#64748b'}; margin-top:2px;">${info.name}</span>
            <span style="display:block; font-size:10px; font-weight:800; color:${isCovered ? '#10B981' : '#475569'};">${count}x</span>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

// ----------------------------------------------------------------------------
// 11. TIER LIST MODULE & COMMUNITY VOTING
// ----------------------------------------------------------------------------
function setupTierListModule() {
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
      container.innerHTML = `<span style="font-size:12px; color:var(--ink-soft); padding:8px;">Nenhuma criatura nesta faixa com os filtros ativos</span>`;
      return;
    }

    container.innerHTML = matching.map(item => `
      <div class="tl-card" data-slug="${item.slug}">
        <div class="tl-card-avatar-wrap">
          <img src="/assets/creatures/${item.slug}.webp" class="tl-card-img" alt="${item.name}" onerror="this.src='/assets/creatures/${item.slug}.png'; this.onerror=function(){this.src='/assets/dluz-logo.png';};" />
        </div>
        <span class="tl-card-name">${item.name}</span>
      </div>
    `).join('');

    container.querySelectorAll('.tl-card').forEach(card => {
      card.addEventListener('click', () => {
        const slug = card.getAttribute('data-slug');
        const item = state.tierListData.find(i => i.slug === slug);
        if (item) openTierVoteModal(item);
      });
    });
  });
}

function openTierVoteModal(item) {
  state.selectedVoteCreature = item;
  state.selectedVoteTier = item.tier || 'A';

  const modal = document.getElementById('modal-tier-vote');
  if (!modal) return;
  modal.classList.add('open');

  const img = document.getElementById('vote-creature-img');
  const name = document.getElementById('vote-creature-name');
  const meta = document.getElementById('vote-creature-meta');
  const bars = document.getElementById('vote-distribution-bars');
  const closeBtn = document.getElementById('modal-vote-close');

  if (img) img.src = `/assets/creatures/${item.slug}.webp`;
  if (name) name.textContent = item.name;
  if (meta) meta.textContent = `Elemento: ${item.element || 'Normal'} • Tier Atual: ${item.tier || 'A'}`;

  // Update distribution bars
  const totalVotes = Object.values(item.votes || {}).reduce((a, b) => a + b, 0) || 1;
  const tiers = ['S+', 'S', 'A', 'B', 'C', 'D'];

  if (bars) {
    bars.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:6px;">
        ${tiers.map(t => {
          const count = (item.votes && item.votes[t]) || 0;
          const pct = Math.round((count / totalVotes) * 100);
          return `
            <div style="display:flex; align-items:center; gap:8px; font-size:12px;">
              <strong style="width:24px; color:#cbd5e1;">${t}</strong>
              <div style="flex:1; height:8px; background:rgba(255,255,255,0.08); border-radius:99px; overflow:hidden;">
                <div style="height:100%; width:${pct}%; background:#38bcef; border-radius:99px;"></div>
              </div>
              <span style="width:36px; text-align:right; color:#94a3b8; font-weight:700;">${pct}%</span>
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  // Tier buttons selection
  document.querySelectorAll('.vote-tier-opt').forEach(btn => {
    btn.classList.toggle('selected', btn.getAttribute('data-tier') === state.selectedVoteTier);
    btn.onclick = () => {
      document.querySelectorAll('.vote-tier-opt').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      state.selectedVoteTier = btn.getAttribute('data-tier');
    };
  });

  if (closeBtn) closeBtn.onclick = () => modal.classList.remove('open');

  const submitBtn = document.getElementById('btn-submit-tier-vote');
  if (submitBtn) {
    submitBtn.onclick = async () => {
      if (!state.selectedVoteCreature) return;
      const targetTier = state.selectedVoteTier;
      
      // Update locally
      if (!item.votes) item.votes = {};
      item.votes[targetTier] = (item.votes[targetTier] || 0) + 1;
      
      // Recalculate top tier
      let maxVotes = 0;
      let topTier = targetTier;
      for (const [t, v] of Object.entries(item.votes)) {
        if (v > maxVotes) {
          maxVotes = v;
          topTier = t;
        }
      }
      item.tier = topTier;

      // Post to backend API
      try {
        await fetch('/api/tier-list/vote', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            slug: item.slug,
            creatureSlug: item.slug,
            tier: targetTier,
            user: { name: 'Inscrito VIP DLuz' }
          })
        });
      } catch(e) {}

      modal.classList.remove('open');
      renderTierBoard();
      showToast(`🎉 Seu voto oficial em ${item.name} (${targetTier}) foi computado com sucesso!`, 'success');
    };
  }
}

// ----------------------------------------------------------------------------
// 12. ELEMENTS MATCHUP MATRIX MODULE
// ----------------------------------------------------------------------------
function setupElementsModule() {
  const container = document.getElementById('element-matrix-container');
  if (!container) return;

  const elements = ['fogo', 'agua', 'grama', 'eletrico', 'vento', 'terra', 'gelo', 'luz', 'trevas'];
  container.innerHTML = `
    <div class="gameplay-block" style="padding:24px; overflow-x:auto;">
      <h3 style="margin-bottom:16px; color:#f8fafc;">Tabela de Vantagens e Fraquezas (9x9)</h3>
      <table style="width:100%; border-collapse:collapse; text-align:center;">
        <thead>
          <tr style="border-bottom:1px solid rgba(255,255,255,0.1);">
            <th style="padding:10px; text-align:left; color:#94a3b8;">Atacante \\ Defensor</th>
            ${elements.map(e => `<th style="padding:10px; color:#cbd5e1;">${ELEMENT_MAP[e].icon} ${ELEMENT_MAP[e].name}</th>`).join('')}
          </tr>
        </thead>
        <tbody>
          ${elements.map(atk => `
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
              <td style="padding:10px; font-weight:800; text-align:left; color:#f8fafc;">${ELEMENT_MAP[atk].icon} ${ELEMENT_MAP[atk].name}</td>
              ${elements.map(def => {
                let mult = '1.0x';
                let color = '#64748b';
                if (atk === 'fogo' && (def === 'grama' || def === 'gelo')) { mult = '2.0x'; color = '#10B981'; }
                else if (atk === 'agua' && (def === 'fogo' || def === 'terra')) { mult = '2.0x'; color = '#10B981'; }
                else if (atk === 'grama' && (def === 'agua' || def === 'terra')) { mult = '2.0x'; color = '#10B981'; }
                else if (atk === 'eletrico' && (def === 'agua' || def === 'vento')) { mult = '2.0x'; color = '#10B981'; }
                else if (atk === 'luz' && def === 'trevas') { mult = '2.0x'; color = '#10B981'; }
                else if (atk === 'trevas' && def === 'luz') { mult = '2.0x'; color = '#10B981'; }
                else if (atk === def) { mult = '0.5x'; color = '#EF4444'; }
                return `<td style="padding:10px; color:${color}; font-weight:800;">${mult}</td>`;
              }).join('')}
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

// ----------------------------------------------------------------------------
// 13. ITEMS DATABASE MODULE
// ----------------------------------------------------------------------------
function setupItemsModule() {
  const container = document.getElementById('items-full-grid');
  if (!container || !state.items.length) return;

  container.innerHTML = state.items.slice(0, 48).map(item => `
    <div class="card" style="padding:16px; display:flex; align-items:center; gap:16px; background:rgba(15,23,42,0.75);">
      <img src="/images/items/ui_item_4040075.webp" onerror="this.src='/assets/dluz-logo.png';" style="width:48px; height:48px; object-fit:contain;" />
      <div>
        <h4 style="margin:0; color:#f8fafc; font-size:14px; font-weight:800;">${item.name_pt || item.name}</h4>
        <p style="margin:4px 0 0 0; font-size:12px; color:#94a3b8; line-height:1.4;">${item.desc_pt || item.description || 'Item essencial de aventura em Idília.'}</p>
      </div>
    </div>
  `).join('');
}

// ----------------------------------------------------------------------------
// 14. COMMUNITY MODULE & POSTS STREAM
// ----------------------------------------------------------------------------
function setupCommunityModule() {
  const container = document.getElementById('comm-posts-stream');
  if (!container) return;

  function renderPost(p) {
    const date = p.created_at ? new Date(p.created_at).toLocaleDateString('pt-BR') : 'Hoje';
    const author = p.author || 'Inscrito DLuz';
    const initials = author.slice(0, 2).toUpperCase();
    const bgArr = ['#38bcef','#8b5cf6','#10B981','#f59e0b','#EF4444'];
    const bg = bgArr[author.charCodeAt(0) % bgArr.length];
    const roleHtml = p.author_role ? `<span class="comm-author-badge">${p.author_role}</span>` : '';
    const titleHtml = p.title ? `<h3>${p.title}</h3>` : '';
    const bodyText = p.content || p.body || '';
    const likes = p.likes || 0;
    const commentsCount = (p.comments || []).length;

    return `
      <article class="comm-card">
        <header class="comm-card-header">
          <div class="comm-author-box">
            <div style="width:40px; height:40px; min-width:40px; border-radius:50%; background:${bg}; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:0.9rem; color:#fff;">
              ${initials}
            </div>
            <div>
              <strong class="comm-author-name">${author}</strong>
              ${roleHtml}
            </div>
          </div>
          <span style="font-size:0.76rem; color:#475569;">${date}</span>
        </header>
        <div class="comm-card-body">
          ${titleHtml}
          <p>${bodyText}</p>
        </div>
        <footer style="padding:10px 16px; border-top:1px solid rgba(255,255,255,0.05); display:flex; gap:16px; align-items:center;">
          <button class="btn-like-post" onclick="this.dataset.liked ? null : (this.querySelector('.lc').textContent = parseInt(this.querySelector('.lc').textContent)+1, this.dataset.liked='1', showToast('Você curtiu esta publicação!', 'success'));" style="background:none; border:none; color:#94a3b8; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:4px;">
            ❤️ <span class="lc">${likes}</span>
          </button>
          <span style="color:#64748b; font-size:0.8rem;">💬 ${commentsCount} comentários</span>
        </footer>
      </article>
    `;
  }

  async function loadPosts() {
    try {
      const res = await fetch('/api/community/posts');
      if (res.ok) {
        const data = await res.json();
        const posts = Array.isArray(data) ? data : (data.posts || []);
        if (posts.length > 0) {
          container.innerHTML = posts.map(renderPost).join('');
          return;
        }
      }
    } catch(e) {}

    // Seed fallback post
    container.innerHTML = renderPost({
      author: 'DLuz Games',
      author_role: 'Criador Oficial',
      title: '🐾 Bem-vindos ao Aniidex DLuz Brasil!',
      content: 'Fala melhores, beleza? O Aniidex DLuz tá 100% no ar com o clone fiel do Aniidex.com! Explore o mapa interativo completo, vote na Tier List oficial do meta e monte suas equipes no Builder!',
      likes: 42,
      comments: [],
      created_at: new Date().toISOString()
    });
  }

  loadPosts();
}

// ----------------------------------------------------------------------------
// 15. MODAL HELPERS & AUTH DIALOG
// ----------------------------------------------------------------------------
function setupModals() {
  const loginBtn = document.getElementById('btn-header-login');
  const loginModal = document.getElementById('modal-login');
  const loginClose = document.getElementById('modal-login-close');

  if (loginBtn && loginModal) {
    loginBtn.addEventListener('click', () => loginModal.classList.add('open'));
  }
  if (loginClose && loginModal) {
    loginClose.addEventListener('click', () => loginModal.classList.remove('open'));
  }

  // Quick Subscriber Login
  document.getElementById('btn-login-quick-sub')?.addEventListener('click', () => {
    if (loginModal) loginModal.classList.remove('open');
    showToast('🚀 Conectado com sucesso como Inscrito VIP DLuz!', 'success');
    const headerAuth = document.getElementById('header-auth-container');
    if (headerAuth) {
      headerAuth.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px;">
          <div style="width:32px; height:32px; border-radius:50%; background:#38bcef; color:#07090e; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:12px;">DL</div>
          <span style="font-size:13px; font-weight:800; color:#f8fafc;">Inscrito VIP</span>
        </div>
      `;
    }
  });
}

// ----------------------------------------------------------------------------
// 16. TOAST NOTIFICATION UTILITY
// ----------------------------------------------------------------------------
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const colors = { success: '#10B981', error: '#EF4444', info: '#38bcef', warn: '#f59e0b' };
  const toast = document.createElement('div');
  toast.style.cssText = `
    background: ${colors[type] || colors.info};
    color: #fff; padding: 12px 20px; border-radius: 10px;
    font-weight: 700; font-size: 14px; pointer-events: auto;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    max-width: 340px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    transition: opacity 0.3s ease, transform 0.3s ease;
  `;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 350);
  }, 3200);
}
window.showToast = showToast;
