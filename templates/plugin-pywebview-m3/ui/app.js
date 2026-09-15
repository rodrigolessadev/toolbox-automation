/**
 * {{PLUGIN_NAME}} Plugin - Frontend Application Logic
 */

let state = {
  items: [],
};

// Fallback Mock para desenvolvimento em navegador sem pywebview
const mockApi = {
  get_items: async () => ({
    success: true,
    items: [
      { id: 'item_1', title: 'Item de Exemplo 1', created_at: '2026-09-15 12:00:00' },
      { id: 'item_2', title: 'Item de Exemplo 2', created_at: '2026-09-15 12:30:00' }
    ]
  }),
  add_item: async (title, details = '') => {
    const item = {
      id: 'item_' + Math.random().toString(36).substr(2, 6),
      title,
      details,
      created_at: new Date().toISOString().replace('T', ' ').substr(0, 19)
    };
    state.items.unshift(item);
    return { success: true, item, items: state.items };
  },
  delete_item: async (id) => {
    state.items = state.items.filter(i => i.id !== id);
    return { success: true, items: state.items };
  },
  get_plugin_version: async () => ({ success: true, version: '1.0.0' }),
};

function getApi() {
  if (window.pywebview && window.pywebview.api) {
    return window.pywebview.api;
  }
  return mockApi;
}

document.addEventListener('DOMContentLoaded', async () => {
  initTheme();
  setupListeners();

  if (window.pywebview) {
    window.addEventListener('pywebviewready', async () => {
      await loadInitialData();
    });
  } else {
    setTimeout(async () => {
      await loadInitialData();
    }, 150);
  }
});

async function loadInitialData() {
  const api = getApi();
  try {
    const verRes = await api.get_plugin_version();
    if (verRes && verRes.version) {
      const badge = document.getElementById('versionBadge');
      if (badge) badge.textContent = `v${verRes.version}`;
    }

    const res = await api.get_items();
    if (res && res.success) {
      state.items = res.items || [];
    }
  } catch (err) {
    console.error('Erro ao carregar dados:', err);
  }
  renderItems();
  if (window.renderIcons) window.renderIcons();
}

function setupListeners() {
  const input = document.getElementById('itemInput');
  if (input) {
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        handleAddItem();
      }
    });
  }
}

function renderItems() {
  const container = document.getElementById('itemsContainer');
  const countEl = document.getElementById('itemsCount');
  if (!container) return;

  if (countEl) countEl.textContent = state.items.length;

  if (state.items.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div data-icon="box" style="width: 36px; height: 36px; color: var(--border);"></div>
        <div style="font-weight: 600;">Nenhum item cadastrado</div>
        <div style="font-size: 11px;">Use o formulário acima para adicionar itens.</div>
      </div>
    `;
    if (window.renderIcons) window.renderIcons();
    return;
  }

  container.innerHTML = state.items.map(item => `
    <div class="item-card" id="card_${item.id}">
      <div style="display: flex; flex-direction: column; gap: 2px;">
        <span style="font-weight: 600; color: var(--fg);">${escapeHtml(item.title)}</span>
        <span style="font-size: 10px; color: var(--fg-muted);">${escapeHtml(item.created_at || '')}</span>
      </div>
      <button
        type="button"
        class="btn btn-secondary btn-sm"
        onclick="handleDeleteItem('${item.id}')"
        title="Excluir item"
      >
        <span data-icon="trash-2"></span>
      </button>
    </div>
  `).join('');

  if (window.renderIcons) window.renderIcons();
}

async function handleAddItem() {
  const input = document.getElementById('itemInput');
  if (!input) return;
  const title = (input.value || '').trim();
  if (!title) return;

  const api = getApi();
  try {
    const res = await api.add_item(title);
    if (res && res.success) {
      state.items = res.items;
      input.value = '';
      renderItems();
    }
  } catch (err) {
    console.error('Erro ao adicionar item:', err);
  }
}

async function handleDeleteItem(itemId) {
  const api = getApi();
  try {
    const res = await api.delete_item(itemId);
    if (res && res.success) {
      state.items = res.items;
      renderItems();
    }
  } catch (err) {
    console.error('Erro ao excluir item:', err);
  }
}

function initTheme() {
  const saved = localStorage.getItem('toolbox-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeIcon(saved);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'dark';
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('toolbox-theme', next);
  updateThemeIcon(next);
}

function updateThemeIcon(theme) {
  const icon = document.getElementById('themeIcon');
  if (!icon) return;
  icon.setAttribute('data-icon', theme === 'dark' ? 'sun' : 'moon');
  if (window.renderIcons) window.renderIcons();
}

function escapeHtml(str) {
  return String(str ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

window.handleAddItem = handleAddItem;
window.handleDeleteItem = handleDeleteItem;
window.toggleTheme = toggleTheme;
