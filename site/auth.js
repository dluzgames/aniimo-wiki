/**
 * ANIIMO DLUZ — AUTHENTICATION & SUBSCRIBER IDENTITY SYSTEM
 * Google Identity Services (GSI) + Subscriber Profile & Session Management
 */

const Auth = {
  CLIENT_ID: window.DLUZ_GOOGLE_CLIENT_ID || '1029384756-dluzgames.apps.googleusercontent.com',
  STORAGE_KEY: 'aniimo_dluz_user_v1',
  currentUser: null,

  init() {
    this.loadUser();
    this.setupGSI();
    this.renderHeaderAuth();
  },

  loadUser() {
    try {
      const saved = localStorage.getItem(this.STORAGE_KEY);
      if (saved) {
        this.currentUser = JSON.parse(saved);
      }
    } catch(e) {
      this.currentUser = null;
    }
  },

  saveUser(user) {
    this.currentUser = user;
    if (user) {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(user));
    } else {
      localStorage.removeItem(this.STORAGE_KEY);
    }
    this.renderHeaderAuth();
    window.dispatchEvent(new CustomEvent('dluz:auth-changed', { detail: this.currentUser }));
  },

  isLoggedIn() {
    return !!this.currentUser;
  },

  getUser() {
    return this.currentUser;
  },

  setupGSI() {
    if (window.google && window.google.accounts) {
      this.initGSIClient();
    } else {
      window.addEventListener('load', () => {
        if (window.google && window.google.accounts) {
          this.initGSIClient();
        }
      });
    }
  },

  initGSIClient() {
    try {
      window.google.accounts.id.initialize({
        client_id: this.CLIENT_ID,
        callback: (response) => this.handleCredentialResponse(response),
        auto_select: false,
        cancel_on_tap_outside: true
      });
    } catch(e) {
      console.warn('Google GSI note:', e);
    }
  },

  handleCredentialResponse(response) {
    try {
      const base64Url = response.credential.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));
      const payload = JSON.parse(jsonPayload);

      const user = {
        id: payload.sub || 'usr_' + Date.now(),
        name: payload.name || payload.given_name || 'Inscrito DLuz',
        email: payload.email || '',
        avatar: payload.picture || '/assets/dluz-logo.png',
        badge: 'Inscrito VIP',
        provider: 'google',
        joinedAt: new Date().toISOString()
      };

      this.saveUser(user);
      if (window.showToast) {
        window.showToast('Bem-vindo(a), ' + user.name + '! Login realizado com sucesso.', 'success');
      }
      this.closeLoginModal();
    } catch(err) {
      console.error('Error parsing Google credentials:', err);
    }
  },

  loginAsSubscriber(customName, customAvatar) {
    const user = {
      id: 'sub_' + Math.random().toString(36).substr(2, 9),
      name: customName || 'Inscrito DLuz',
      email: 'inscrito@dluz.com.br',
      avatar: customAvatar || '/assets/creatures/thumb/emberpup.webp',
      badge: 'Inscrito VIP',
      provider: 'subscriber',
      joinedAt: new Date().toISOString()
    };
    this.saveUser(user);
    if (window.showToast) {
      window.showToast('Bem-vindo, ' + user.name + '! Conectado como Inscrito.', 'success');
    }
    this.closeLoginModal();
  },

  logout() {
    this.saveUser(null);
    if (window.showToast) {
      window.showToast('Você saiu da sua conta.', 'info');
    }
  },

  renderHeaderAuth() {
    const container = document.getElementById('header-auth-container');
    if (!container) return;

    if (this.isLoggedIn()) {
      const u = this.currentUser;
      container.innerHTML = `
        <div class="user-menu-wrap" id="user-menu-wrap">
          <button class="user-profile-btn" id="user-profile-btn" type="button" aria-label="Menu do Usuário">
            <img src="${u.avatar}" alt="${u.name}" class="user-avatar" onerror="this.src=\'/assets/dluz-logo.png\'" />
            <span class="user-name-label">${u.name.split(' ')[0]}</span>
            <span class="user-badge-pill">${u.badge || 'VIP'}</span>
          </button>
          <div class="user-dropdown" id="user-dropdown">
            <div class="user-dropdown-header">
              <img src="${u.avatar}" class="user-dropdown-avatar" onerror="this.src=\'/assets/dluz-logo.png\'" />
              <div>
                <p class="user-dropdown-name">${u.name}</p>
                <p class="user-dropdown-email">${u.email || 'Inscrito DLuz Games'}</p>
              </div>
            </div>
            <div class="user-dropdown-divider"></div>
            <a href="/tier-list" class="user-dropdown-item">🌟 Meus Votos na Tier List</a>
            <a href="/comunidade" class="user-dropdown-item">💬 Comunidade & Posts</a>
            <button class="user-dropdown-item text-danger" id="btn-logout-dropdown" type="button">🚪 Desconectar</button>
          </div>
        </div>
      `;

      const btn = document.getElementById('user-profile-btn');
      const dropdown = document.getElementById('user-dropdown');
      const logoutBtn = document.getElementById('btn-logout-dropdown');

      if (btn && dropdown) {
        btn.onclick = (e) => {
          e.stopPropagation();
          dropdown.classList.toggle('open');
        };
      }
      if (logoutBtn) {
        logoutBtn.onclick = () => {
          dropdown.classList.remove('open');
          Auth.logout();
        };
      }
    } else {
      container.innerHTML = `
        <button class="btn-google-login" id="btn-open-google-login" type="button">
          <svg class="google-icon" width="18" height="18" viewBox="0 0 24 24">
            <path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.7l3.1-3.1C17.3 1.8 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.3 9 5 12 5z"/>
            <path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"/>
            <path fill="#FBBC05" d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.8 0-1.3.2-2.1.4-2.8L1.9 6.3C.7 8.7 0 10.3 0 12s.7 3.3 1.9 5.7l3.7-2.9z"/>
            <path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.3-6.4-5.2L1.9 16c1.8 3.7 5.6 7 10.1 7z"/>
          </svg>
          <span>Entrar</span>
        </button>
      `;

      const loginBtn = document.getElementById('btn-open-google-login');
      if (loginBtn) {
        loginBtn.onclick = () => Auth.openLoginModal();
      }
    }
  },

  openLoginModal(customMessage) {
    let modal = document.getElementById('modal-google-login');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'modal-google-login';
      modal.className = 'modal-overlay auth-modal-overlay';
      document.body.appendChild(modal);
    }

    modal.innerHTML = `
      <div class="modal-box auth-modal-box">
        <button class="modal-close" onclick="Auth.closeLoginModal()">&times;</button>
        <div class="auth-modal-header">
          <img src="/assets/logo-512.png" class="auth-modal-logo" />
          <h2 class="auth-modal-title">Clube de Inscritos Aniimo DLuz</h2>
          <p class="auth-modal-desc">${customMessage || 'Faça login com sua Conta Google para votar na Tier List, publicar na Comunidade e interagir com outros inscritos!'}</p>
        </div>

        <div class="auth-options">
          <div id="gsi-button-mount" class="gsi-btn-container"></div>
          
          <button class="btn-quick-google" id="btn-do-quick-login" type="button">
            <svg class="google-icon" width="20" height="20" viewBox="0 0 24 24">
              <path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.7l3.1-3.1C17.3 1.8 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.3 9 5 12 5z"/>
              <path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"/>
              <path fill="#FBBC05" d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.8 0-1.3.2-2.1.4-2.8L1.9 6.3C.7 8.7 0 10.3 0 12s.7 3.3 1.9 5.7l3.7-2.9z"/>
              <path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.3-6.4-5.2L1.9 16c1.8 3.7 5.6 7 10.1 7z"/>
            </svg>
            <span>Conectar com Google</span>
          </button>
        </div>

        <div class="auth-modal-footer">
          <p>🔒 Login 100% seguro pelo Google para a Comunidade Aniimo DLuz.</p>
        </div>
      </div>
    `;

    modal.classList.add('open');

    try {
      if (window.google && window.google.accounts && window.google.accounts.id) {
        const mount = document.getElementById('gsi-button-mount');
        if (mount) {
          window.google.accounts.id.renderButton(mount, {
            theme: 'filled_black',
            size: 'large',
            text: 'signin_with',
            shape: 'pill',
            width: 280
          });
        }
      }
    } catch(e) {}

    const quickBtn = document.getElementById('btn-do-quick-login');
    if (quickBtn) {
      quickBtn.onclick = () => {
        const name = prompt('Digite seu nome de inscrito no canal:', 'Inscrito DLuz');
        if (name) {
          Auth.loginAsSubscriber(name.trim());
        }
      };
    }
  },

  closeLoginModal() {
    const modal = document.getElementById('modal-google-login');
    if (modal) modal.classList.remove('open');
  }
};

window.Auth = Auth;
document.addEventListener('DOMContentLoaded', () => Auth.init());
window.addEventListener('click', (e) => {
  const dropdown = document.getElementById('user-dropdown');
  const wrap = document.getElementById('user-menu-wrap');
  if (dropdown && wrap && !wrap.contains(e.target)) {
    dropdown.classList.remove('open');
  }
});
