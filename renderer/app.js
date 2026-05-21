/**
 * Turkmen'S - Renderer (Discord-vari, dinamik)
 */
(function () {
  'use strict';

  const CFG = window.TURKMENS_CONFIG || {};
  const SERVER_URL = CFG.SERVER_URL || 'http://localhost:3000';
  const TOKEN_KEY = 'turkmens.token';
  const COLORS = ['#5865F2', '#EB459E', '#FAA61A', '#43B581', '#F04747', '#9B59B6', '#1ABC9C', '#E67E22', '#3498DB', '#E74C3C'];

  // --- State ---
  let socket = null;
  let me = null;
  let myServers = [];               // [{id, name, icon, color, invite, ownerId, channels, memberCount}]
  let currentServerId = null;       // null = anasayfa
  let currentChannelId = null;
  let currentVoiceChannelId = null;
  let isMuted = false;
  let authMode = 'login';
  let updateReady = false;
  let selectedColor = COLORS[0];

  // --- DOM helpers ---
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => document.querySelectorAll(sel);

  function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
  }

  function formatTime(ts) {
    const d = new Date(ts);
    const today = new Date();
    const t = d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
    if (d.toDateString() === today.toDateString()) return `Bugün ${t}`;
    const y = new Date(today); y.setDate(y.getDate() - 1);
    if (d.toDateString() === y.toDateString()) return `Dün ${t}`;
    return `${d.toLocaleDateString('tr-TR')} ${t}`;
  }

  function initials(name) {
    if (!name) return '?';
    const parts = String(name).trim().split(/\s+/);
    if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }

  function toast(message, isError = false) {
    const t = $('#toast');
    t.textContent = message;
    t.className = 'toast' + (isError ? ' error' : '');
    setTimeout(() => t.classList.add('hidden'), 50);
    setTimeout(() => t.classList.remove('hidden'), 100);
    setTimeout(() => t.classList.add('hidden'), 3000);
  }

  // --- Token ---
  function saveToken(t) { try { localStorage.setItem(TOKEN_KEY, t); } catch (e) {} }
  function getToken() { try { return localStorage.getItem(TOKEN_KEY); } catch (e) { return null; } }
  function clearToken() { try { localStorage.removeItem(TOKEN_KEY); } catch (e) {} }

  // --- API ---
  async function api(path, options = {}) {
    const url = SERVER_URL.replace(/\/$/, '') + path;
    const headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});
    const token = getToken();
    if (token && !headers.Authorization) headers.Authorization = 'Bearer ' + token;
    let res;
    try {
      res = await fetch(url, Object.assign({}, options, { headers }));
    } catch (err) {
      throw new Error('Sunucuya ulaşılamıyor.');
    }
    let data = null;
    try { data = await res.json(); } catch (e) {}
    if (!res.ok) throw new Error((data && data.error) ? data.error : `HTTP ${res.status}`);
    return data;
  }

  // ============ Auth ============
  function showAuth() {
    $('#auth-screen').classList.remove('hidden');
    $('#app').classList.add('hidden');
    $('#reconnect-overlay').classList.add('hidden');
  }
  function hideAuth() {
    $('#auth-screen').classList.add('hidden');
    $('#app').classList.remove('hidden');
  }
  function setAuthMode(mode) {
    authMode = mode;
    $$('.auth-tab').forEach(t => t.classList.toggle('active', t.dataset.mode === mode));
    $('#password-confirm').classList.toggle('hidden', mode !== 'register');
    $('#auth-submit').textContent = mode === 'register' ? 'Hesap Oluştur' : 'Giriş Yap';
    $('#auth-subtitle').textContent = mode === 'register' ? 'Yeni bir hesap oluştur' : 'Hesabına giriş yap';
    $('#auth-error').textContent = '';
  }
  function setAuthLoading(loading) {
    $('#auth-submit').disabled = loading;
    $('#auth-loading').classList.toggle('hidden', !loading);
  }
  async function handleAuthSubmit(e) {
    if (e) e.preventDefault();
    const username = $('#username-input').value.trim();
    const password = $('#password-input').value;
    const confirm = $('#password-confirm').value;
    if (!username || username.length < 2) return $('#auth-error').textContent = 'Kullanıcı adı en az 2 karakter.';
    if (!password || password.length < 6) return $('#auth-error').textContent = 'Şifre en az 6 karakter.';
    if (authMode === 'register' && password !== confirm) return $('#auth-error').textContent = 'Şifreler eşleşmiyor.';
    $('#auth-error').textContent = '';
    setAuthLoading(true);
    try {
      const data = await api(authMode === 'register' ? '/api/auth/register' : '/api/auth/login', {
        method: 'POST', body: JSON.stringify({ username, password })
      });
      if (!data || !data.token) throw new Error('Beklenmedik yanıt.');
      saveToken(data.token);
      me = data.user;
      connectSocket();
    } catch (err) {
      $('#auth-error').textContent = err.message;
    } finally {
      setAuthLoading(false);
    }
  }
  async function tryAutoLogin() {
    if (!getToken()) return showAuth();
    try {
      const data = await api('/api/me');
      me = data.user;
      connectSocket();
    } catch (err) {
      clearToken();
      showAuth();
    }
  }
  function logout() {
    api('/api/auth/logout', { method: 'POST' }).catch(() => {});
    clearToken();
    if (socket) { try { socket.disconnect(); } catch (e) {} socket = null; }
    me = null;
    myServers = [];
    currentServerId = null; currentChannelId = null; currentVoiceChannelId = null;
    showAuth();
    $('#username-input').value = '';
    $('#password-input').value = '';
    $('#password-confirm').value = '';
  }

  // ============ Socket ============
  function connectSocket() {
    if (typeof io === 'undefined') return ($('#auth-error').textContent = 'Socket.io yüklenemedi.');
    const token = getToken();
    if (!token) return showAuth();

    try {
      socket = io(SERVER_URL, {
        auth: { token },
        reconnection: true,
        reconnectionAttempts: CFG.RECONNECT_ATTEMPTS || Infinity,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        transports: ['websocket', 'polling']
      });
    } catch (err) {
      $('#auth-error').textContent = 'Bağlantı hatası: ' + err.message;
      showAuth();
      return;
    }

    socket.on('connect', () => {
      $('#reconnect-overlay').classList.add('hidden');
    });
    socket.on('disconnect', (reason) => {
      if (reason !== 'io server disconnect' && reason !== 'io client disconnect') {
        $('#reconnect-overlay').classList.remove('hidden');
      }
    });
    socket.on('connect_error', (err) => {
      if (err.message && (err.message.includes('Token') || err.message.includes('token'))) {
        try { socket.disconnect(); } catch (e) {}
        clearToken(); me = null;
        showAuth();
        $('#auth-error').textContent = 'Oturumun sona erdi. Tekrar giriş yap.';
      }
    });

    socket.on('init', (data) => {
      me = data.user;
      myServers = data.servers || [];
      currentServerId = null;
      currentChannelId = null;
      hideAuth();
      renderUserPanel();
      renderServerSidebar();
      showHomeView();
    });

    socket.on('servers:changed', (data) => {
      myServers = data.servers || [];
      renderServerSidebar();
      if (currentServerId !== null) {
        const stillIn = myServers.find(s => s.id === currentServerId);
        if (!stillIn) {
          // Bu sunucudan atıldık/silindi
          goHome();
        } else {
          // Güncel sunucu detayını render et
          renderCurrentServer();
        }
      } else {
        renderHomeServerGrid();
      }
    });

    socket.on('server:deleted', (data) => {
      myServers = myServers.filter(s => s.id !== data.serverId);
      renderServerSidebar();
      if (currentServerId === data.serverId) {
        toast('Bu sunucu silindi.', true);
        goHome();
      } else if (currentServerId === null) {
        renderHomeServerGrid();
      }
    });

    socket.on('server:structure', (data) => {
      // Kanal eklendi/silindi
      const s = myServers.find(x => x.id === data.serverId);
      if (s) {
        s.channels = data.channels;
        if (currentServerId === data.serverId) {
          renderCurrentServer();
          // Aktif kanal silinmiş mi?
          if (currentChannelId && !data.channels.find(c => c.id === currentChannelId)) {
            const firstText = data.channels.find(c => c.type === 'text');
            if (firstText) switchChannel(firstText.id);
          }
        }
      }
    });

    socket.on('server:selected', (data) => {
      currentServerId = data.serverId;
      currentChannelId = data.channelId;
      if (data.serverId === null) {
        showHomeView();
        return;
      }
      const s = myServers.find(x => x.id === data.serverId);
      if (s) s.channels = data.channels;
      hideVoiceRoom();
      showServerView();
      renderCurrentServer();
      renderMessages(data.messages || []);
      (data.voiceChannels || []).forEach(vc => updateVoiceChannelUsers(vc.id, vc.users || []));
    });

    socket.on('channel:switched', (data) => {
      currentChannelId = data.channelId;
      renderMessages(data.messages || []);
      updateActiveChannel();
      updateChannelHeader();
      updateInputPlaceholder();
    });

    socket.on('message:new', (data) => {
      if (data.channelId === currentChannelId) appendMessage(data.message);
    });

    socket.on('users:update', (data) => {
      if (data.serverId === currentServerId) renderUserList(data.users);
    });

    socket.on('voice:update', (data) => {
      updateVoiceChannelUsers(data.channelId, data.users);
      if (isViewingVoiceRoom() && currentVoiceChannelId === data.channelId) {
        renderVoiceRoom(data.channelId, data.users);
      }
    });

    socket.on('error:rate', (data) => {
      const input = $('#message-input');
      const old = input.placeholder;
      input.placeholder = data.message;
      setTimeout(() => { input.placeholder = old; }, 3000);
    });
    socket.on('error:msg', (data) => {
      toast(data.message || 'Bir hata oluştu.', true);
    });
  }

  // ============ Server Sidebar ============
  function renderServerSidebar() {
    const c = $('#server-icons-container');
    c.innerHTML = '';
    myServers.forEach(s => {
      const el = document.createElement('div');
      el.className = 'server-item';
      if (currentServerId === s.id) {
        el.classList.add('active');
        el.style.background = s.color;
      } else {
        el.style.background = '';
      }
      el.dataset.serverId = s.id;
      el.title = s.name;
      el.textContent = s.icon || initials(s.name);
      el.addEventListener('click', () => selectServer(s.id));
      c.appendChild(el);
    });
  }

  function selectServer(serverId) {
    if (!socket || !socket.connected) return;
    socket.emit('server:select', { serverId });
  }

  function goHome() {
    if (!socket || !socket.connected) return;
    socket.emit('server:select', { serverId: null });
  }

  // ============ Home View ============
  function showHomeView() {
    currentServerId = null;
    currentChannelId = null;
    $('#home-view').classList.remove('hidden');
    $('#channel-sidebar').classList.add('hidden');
    $('#main-content').classList.add('hidden');
    $('#user-list').classList.add('hidden');
    // home btn aktif, diğerleri pasif
    $('#home-btn').classList.add('active');
    $$('#server-icons-container .server-item').forEach(el => {
      el.classList.remove('active');
      el.style.background = '';
    });
    $('#home-username').textContent = me ? me.username : '';
    renderHomeServerGrid();
  }

  function renderHomeServerGrid() {
    const grid = $('#home-server-grid');
    grid.innerHTML = '';
    if (myServers.length === 0) {
      grid.innerHTML = '<div class="empty-state">Henüz bir sunucuda değilsin. Yukarıdan oluştur veya katıl.</div>';
      return;
    }
    myServers.forEach(s => {
      const card = document.createElement('div');
      card.className = 'server-card';
      card.innerHTML = `
        <div class="server-card-icon" style="background:${escapeHtml(s.color)}">${escapeHtml(s.icon || initials(s.name))}</div>
        <div class="server-card-name">${escapeHtml(s.name)}</div>
        <div class="server-card-members">${s.memberCount || 1} üye</div>
      `;
      card.addEventListener('click', () => selectServer(s.id));
      grid.appendChild(card);
    });
  }

  // ============ Server View ============
  function showServerView() {
    $('#home-view').classList.add('hidden');
    $('#channel-sidebar').classList.remove('hidden');
    $('#main-content').classList.remove('hidden');
    $('#user-list').classList.remove('hidden');
    $('#home-btn').classList.remove('active');
    renderServerSidebar();
  }

  function renderCurrentServer() {
    const s = myServers.find(x => x.id === currentServerId);
    if (!s) return;
    $('#current-server-name').textContent = s.name;
    $$('#server-icons-container .server-item').forEach(el => {
      const isActive = parseInt(el.dataset.serverId, 10) === currentServerId;
      el.classList.toggle('active', isActive);
      el.style.background = isActive ? s.color : '';
    });
    renderChannels(s);
    updateChannelHeader();
    updateInputPlaceholder();
    // Show/hide owner-only items
    const isOwner = me && s.ownerId === me.id;
    $('#menu-add-channel').style.display = isOwner ? '' : 'none';
    // Menu leave label: owner için "Sunucuyu Sil"
    $('#menu-leave').textContent = isOwner ? 'Sunucuyu Sil' : 'Sunucudan Ayrıl';
  }

  function renderChannels(server) {
    const c = $('#channels-container');
    c.innerHTML = '';
    const isOwner = me && server.ownerId === me.id;
    const textCh = server.channels.filter(c => c.type === 'text');
    const voiceCh = server.channels.filter(c => c.type === 'voice');

    function renderCategory(label, channels, type) {
      const cat = document.createElement('div');
      cat.className = 'channel-category';
      cat.innerHTML = `<span>${escapeHtml(label)}</span>`;
      if (isOwner) {
        const addBtn = document.createElement('button');
        addBtn.className = 'add-channel-btn';
        addBtn.textContent = '+';
        addBtn.title = 'Kanal ekle';
        addBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          openCreateChannelModal(type);
        });
        cat.appendChild(addBtn);
      }
      c.appendChild(cat);

      channels.forEach(ch => {
        const el = document.createElement('div');
        el.className = 'channel-item';
        if (ch.id === currentChannelId) el.classList.add('active');
        el.dataset.channelId = ch.id;
        el.dataset.channelType = ch.type;
        el.innerHTML = `
          <span class="channel-icon">${ch.type === 'voice' ? '🔊' : '#'}</span>
          <span class="channel-name">${escapeHtml(ch.name)}</span>
        `;
        if (isOwner) {
          const del = document.createElement('button');
          del.className = 'channel-delete';
          del.textContent = '✕';
          del.title = 'Kanalı sil';
          del.addEventListener('click', async (e) => {
            e.stopPropagation();
            if (!confirm(`"${ch.name}" kanalını silmek istediğine emin misin?`)) return;
            try {
              await api('/api/channels/' + ch.id, { method: 'DELETE' });
              toast('Kanal silindi.');
            } catch (err) {
              toast(err.message, true);
            }
          });
          el.appendChild(del);
        }
        el.addEventListener('click', () => {
          if (ch.type === 'text') switchChannel(ch.id);
          else joinVoice(ch.id);
        });
        c.appendChild(el);

        if (ch.type === 'voice') {
          const usersDiv = document.createElement('div');
          usersDiv.className = 'voice-channel-users';
          usersDiv.dataset.voiceUsersFor = ch.id;
          c.appendChild(usersDiv);
        }
      });
    }

    if (textCh.length || isOwner) renderCategory('Metin Kanalları', textCh, 'text');
    if (voiceCh.length || isOwner) renderCategory('Sesli Kanallar', voiceCh, 'voice');
  }

  function switchChannel(channelId) {
    if (!socket || !socket.connected) return;
    hideVoiceRoom();
    socket.emit('channel:switch', { channelId });
  }

  function updateActiveChannel() {
    $$('.channel-item').forEach(el => el.classList.remove('active'));
    const el = document.querySelector(`.channel-item[data-channel-id="${currentChannelId}"]`);
    if (el) el.classList.add('active');
  }

  function updateChannelHeader() {
    const s = myServers.find(x => x.id === currentServerId);
    if (!s) return;
    const ch = s.channels.find(c => c.id === currentChannelId);
    if (!ch) return;
    $('#current-channel-name').textContent = ch.name;
    $('#channel-prefix').textContent = ch.type === 'voice' ? '🔊' : '#';
  }

  function updateInputPlaceholder() {
    const s = myServers.find(x => x.id === currentServerId);
    if (!s) return;
    const ch = s.channels.find(c => c.id === currentChannelId);
    if (!ch) return;
    $('#message-input').placeholder = `#${ch.name} kanalına mesaj yaz`;
  }

  // ============ Messages ============
  function renderMessages(messages) {
    const c = $('#messages');
    c.innerHTML = '';
    if (!messages || messages.length === 0) {
      c.innerHTML = '<div style="padding:40px;text-align:center;color:#72767D;">Henüz mesaj yok. İlk mesajı sen gönder!</div>';
      return;
    }
    messages.forEach(m => appendMessage(m, false));
    requestAnimationFrame(() => scrollMessagesToBottom());
  }

  function appendMessage(msg, autoScroll = true) {
    const c = $('#messages');
    const empty = c.querySelector('div[style*="text-align:center"]');
    if (empty) empty.remove();
    const el = document.createElement('div');
    el.className = 'message';
    const color = msg.author && msg.author.avatarColor ? msg.author.avatarColor : '#5865F2';
    const username = msg.author && msg.author.username ? msg.author.username : 'Bilinmeyen';
    el.innerHTML = `
      <div class="msg-avatar" style="background:${escapeHtml(color)}">${escapeHtml(initials(username))}</div>
      <div class="message-body">
        <div class="message-header">
          <span class="message-author">${escapeHtml(username)}</span>
          <span class="message-time">${escapeHtml(formatTime(msg.timestamp))}</span>
        </div>
        <div class="message-text">${escapeHtml(msg.text)}</div>
      </div>
    `;
    c.appendChild(el);
    if (autoScroll) scrollMessagesToBottom();
  }

  function scrollMessagesToBottom() {
    const c = $('#messages');
    c.scrollTop = c.scrollHeight;
  }

  function sendMessage() {
    const input = $('#message-input');
    const text = input.value.trim();
    if (!text) return;
    if (!socket || !socket.connected) return;
    socket.emit('message:send', { text });
    input.value = '';
  }

  // ============ User Panel & List ============
  function renderUserPanel() {
    if (!me) return;
    $('#my-username').textContent = me.username;
    const a = $('#my-avatar');
    a.textContent = initials(me.username);
    a.style.background = me.avatarColor || '#5865F2';
  }

  function renderUserList(users) {
    const c = $('#user-list-content');
    c.innerHTML = '';
    const order = { online: 0, idle: 1, dnd: 2, invisible: 3 };
    users.sort((a, b) => {
      const oa = order[a.status] ?? 9, ob = order[b.status] ?? 9;
      if (oa !== ob) return oa - ob;
      return a.username.localeCompare(b.username, 'tr');
    });
    $('#user-count').textContent = users.length;
    users.forEach(u => {
      const el = document.createElement('div');
      el.className = 'user-list-item';
      if (u.voiceChannel) el.classList.add('in-voice');
      el.innerHTML = `
        <div class="list-avatar" style="background:${escapeHtml(u.avatarColor || '#5865F2')}">
          ${escapeHtml(initials(u.username))}
          <span class="status-dot ${escapeHtml(u.status || 'online')}"></span>
        </div>
        <div class="list-name">${escapeHtml(u.username)}</div>
      `;
      c.appendChild(el);
    });
  }

  // ============ Voice ============
  function joinVoice(channelId) {
    if (!socket || !socket.connected) return;
    currentVoiceChannelId = channelId;
    socket.emit('voice:join', { channelId });
    showVoiceRoom(channelId);
    const s = myServers.find(x => x.id === currentServerId);
    const ch = s ? s.channels.find(c => c.id === channelId) : null;
    if (ch) {
      $('#voice-status-channel').textContent = ch.name;
      $('#voice-status').classList.remove('hidden');
    }
  }
  function leaveVoice() {
    if (!socket || !socket.connected) return;
    socket.emit('voice:leave');
    currentVoiceChannelId = null;
    $('#voice-status').classList.add('hidden');
    hideVoiceRoom();
    if (isMuted) toggleMute();
  }
  function showVoiceRoom(channelId) {
    const s = myServers.find(x => x.id === currentServerId);
    const ch = s ? s.channels.find(c => c.id === channelId) : null;
    if (!ch) return;
    $('#voice-room-title').textContent = `🔊 ${ch.name}`;
    $('#messages').classList.add('hidden');
    $('#message-input-container').classList.add('hidden');
    $('#voice-room').classList.remove('hidden');
    renderVoiceRoom(channelId, ch.users || []);
  }
  function hideVoiceRoom() {
    $('#voice-room').classList.add('hidden');
    $('#messages').classList.remove('hidden');
    $('#message-input-container').classList.remove('hidden');
  }
  function isViewingVoiceRoom() {
    return !$('#voice-room').classList.contains('hidden');
  }
  function renderVoiceRoom(channelId, users) {
    const c = $('#voice-room-users');
    c.innerHTML = '';
    if (!users || users.length === 0) {
      c.innerHTML = '<div style="color:#B9BBBE;">Bu kanalda henüz kimse yok</div>';
      return;
    }
    users.forEach(u => {
      const el = document.createElement('div');
      el.className = 'voice-room-user';
      if (u.muted) el.classList.add('muted');
      el.innerHTML = `
        <div class="big-avatar" style="background:${escapeHtml(u.avatarColor || '#5865F2')}">${escapeHtml(initials(u.username))}</div>
        <div class="vname">${escapeHtml(u.username)}</div>
        ${u.muted ? '<div class="vmute">🔇 Sessiz</div>' : ''}
      `;
      c.appendChild(el);
    });
  }
  function updateVoiceChannelUsers(channelId, users) {
    const s = myServers.find(x => x.id === currentServerId);
    if (s) {
      const ch = s.channels.find(c => c.id === channelId);
      if (ch) ch.users = users;
    }
    const div = document.querySelector(`[data-voice-users-for="${channelId}"]`);
    if (!div) return;
    div.innerHTML = '';
    (users || []).forEach(u => {
      const item = document.createElement('div');
      item.className = 'voice-user-mini';
      item.innerHTML = `
        <div class="mini-avatar" style="background:${escapeHtml(u.avatarColor || '#5865F2')}">${escapeHtml(initials(u.username))}</div>
        <span>${escapeHtml(u.username)}${u.muted ? ' 🔇' : ''}</span>
      `;
      div.appendChild(item);
    });
  }
  function toggleMute() {
    if (!currentVoiceChannelId) return;
    isMuted = !isMuted;
    const btn = $('#mute-btn');
    btn.classList.toggle('muted', isMuted);
    btn.textContent = isMuted ? '🔇' : '🎤';
    if (socket && socket.connected) socket.emit('voice:mute', { muted: isMuted });
  }

  // ============ Modals ============
  function openModal(id) {
    document.getElementById(id).classList.remove('hidden');
  }
  function closeModal(id) {
    document.getElementById(id).classList.add('hidden');
    // Reset errors/fields
    const errs = document.querySelectorAll('#' + id + ' .modal-error');
    errs.forEach(e => e.textContent = '');
  }
  function closeAllModals() {
    $$('.modal').forEach(m => m.classList.add('hidden'));
  }

  // ----- Add server (create vs join chooser) -----
  function openAddServerModal() {
    openModal('modal-add');
  }

  // ----- Create server -----
  function openCreateServerModal() {
    closeAllModals();
    openModal('modal-create');
    $('#create-server-name').value = '';
    $('#create-server-error').textContent = '';
    // Color picker
    selectedColor = COLORS[Math.floor(Math.random() * COLORS.length)];
    const cp = $('#create-color-picker');
    cp.innerHTML = '';
    COLORS.forEach(c => {
      const sw = document.createElement('div');
      sw.className = 'color-swatch' + (c === selectedColor ? ' selected' : '');
      sw.style.background = c;
      sw.dataset.color = c;
      sw.addEventListener('click', () => {
        selectedColor = c;
        $$('#create-color-picker .color-swatch').forEach(x => x.classList.remove('selected'));
        sw.classList.add('selected');
      });
      cp.appendChild(sw);
    });
    setTimeout(() => $('#create-server-name').focus(), 50);
  }

  async function handleCreateServer(e) {
    e.preventDefault();
    const name = $('#create-server-name').value.trim();
    if (!name || name.length < 2) {
      $('#create-server-error').textContent = 'Sunucu adı en az 2 karakter olmalı.';
      return;
    }
    try {
      const data = await api('/api/servers', {
        method: 'POST',
        body: JSON.stringify({ name, color: selectedColor })
      });
      closeAllModals();
      toast(`"${data.server.name}" sunucusu oluşturuldu!`);
      // myServers servers:changed event'iyle güncellenecek
      // Yine de doğrudan seçelim
      setTimeout(() => selectServer(data.server.id), 200);
    } catch (err) {
      $('#create-server-error').textContent = err.message;
    }
  }

  // ----- Join server -----
  function openJoinServerModal() {
    closeAllModals();
    openModal('modal-join');
    $('#join-invite').value = '';
    $('#join-error').textContent = '';
    setTimeout(() => $('#join-invite').focus(), 50);
  }
  async function handleJoinServer(e) {
    e.preventDefault();
    const invite = $('#join-invite').value.trim();
    if (!invite) {
      $('#join-error').textContent = 'Davet kodu girmelisin.';
      return;
    }
    try {
      const data = await api('/api/servers/join', {
        method: 'POST',
        body: JSON.stringify({ invite })
      });
      closeAllModals();
      if (data.alreadyMember) toast('Zaten bu sunucudaydın.');
      else toast(`"${data.server.name}" sunucusuna katıldın!`);
      setTimeout(() => selectServer(data.server.id), 200);
    } catch (err) {
      $('#join-error').textContent = err.message;
    }
  }

  // ----- Invite modal -----
  function openInviteModal() {
    const s = myServers.find(x => x.id === currentServerId);
    if (!s) return;
    closeAllModals();
    openModal('modal-invite');
    $('#invite-server-name').textContent = s.name;
    $('#invite-code-display').value = s.invite;
    const isOwner = me && s.ownerId === me.id;
    $('#invite-regen-btn').style.display = isOwner ? '' : 'none';
  }
  async function copyInvite() {
    const code = $('#invite-code-display').value;
    try {
      await navigator.clipboard.writeText(code);
      toast('Davet kodu kopyalandı!');
    } catch (e) {
      // Fallback
      const inp = $('#invite-code-display');
      inp.select();
      try { document.execCommand('copy'); toast('Davet kodu kopyalandı!'); }
      catch (e2) { toast('Kopyalama başarısız.', true); }
    }
  }
  async function regenerateInvite() {
    const s = myServers.find(x => x.id === currentServerId);
    if (!s) return;
    if (!confirm('Yeni davet kodu üretilecek. Eski kod artık çalışmayacak. Devam?')) return;
    try {
      const data = await api('/api/servers/' + s.id + '/regenerate-invite', { method: 'POST' });
      s.invite = data.invite;
      $('#invite-code-display').value = data.invite;
      toast('Yeni davet kodu üretildi.');
    } catch (err) {
      toast(err.message, true);
    }
  }

  // ----- Create channel -----
  let pendingChannelType = 'text';
  function openCreateChannelModal(type) {
    pendingChannelType = type || 'text';
    closeAllModals();
    openModal('modal-channel');
    $('#create-channel-name').value = '';
    $('#create-channel-error').textContent = '';
    $$('input[name="channel-type"]').forEach(r => {
      r.checked = r.value === pendingChannelType;
    });
    setTimeout(() => $('#create-channel-name').focus(), 50);
  }
  async function handleCreateChannel(e) {
    e.preventDefault();
    if (!currentServerId) return;
    const name = $('#create-channel-name').value.trim();
    const type = document.querySelector('input[name="channel-type"]:checked').value;
    if (!name) {
      $('#create-channel-error').textContent = 'Kanal adı gerekli.';
      return;
    }
    try {
      await api('/api/servers/' + currentServerId + '/channels', {
        method: 'POST',
        body: JSON.stringify({ name, type })
      });
      closeAllModals();
      toast('Kanal oluşturuldu.');
      // server:structure event'i bizi güncelleyecek
    } catch (err) {
      $('#create-channel-error').textContent = err.message;
    }
  }

  // ----- Leave/delete server -----
  async function leaveCurrentServer() {
    const s = myServers.find(x => x.id === currentServerId);
    if (!s) return;
    const isOwner = me && s.ownerId === me.id;
    const msg = isOwner
      ? `"${s.name}" sunucusu KALICI olarak silinecek. Tüm kanallar ve mesajlar yok olur. Emin misin?`
      : `"${s.name}" sunucusundan ayrılmak istediğine emin misin?`;
    if (!confirm(msg)) return;
    try {
      await api('/api/servers/' + s.id + '/leave', { method: 'POST' });
      toast(isOwner ? 'Sunucu silindi.' : 'Sunucudan ayrıldın.');
      // servers:changed event'iyle güncellenecek
      goHome();
    } catch (err) {
      toast(err.message, true);
    }
  }

  // ============ Server menu dropdown ============
  function toggleServerMenu() {
    $('#server-menu').classList.toggle('hidden');
  }
  function closeServerMenu() {
    $('#server-menu').classList.add('hidden');
  }

  // ============ Auto-update ============
  function setupUpdates() {
    if (!window.turkmens) return;
    turkmens.onUpdateAvailable((info) => {
      $('#update-banner-text').textContent = `Yeni sürüm indiriliyor: v${info.version}`;
      $('#update-banner').classList.remove('hidden');
      document.body.classList.add('with-banner');
    });
    turkmens.onUpdateProgress((p) => {
      $('#update-banner-text').textContent = `Güncelleme indiriliyor: %${p.percent}`;
      $('#update-progress-bar').style.width = p.percent + '%';
    });
    turkmens.onUpdateDownloaded((info) => {
      updateReady = true;
      $('#update-banner-text').textContent = `Sürüm v${info.version} hazır`;
      $('#update-progress-bar').style.width = '100%';
      $('#update-install-btn').classList.remove('hidden');
    });
    turkmens.onUpdateError(() => {
      $('#update-banner').classList.add('hidden');
      document.body.classList.remove('with-banner');
    });
    $('#update-install-btn').addEventListener('click', () => {
      if (updateReady && window.turkmens) window.turkmens.installUpdate();
    });
    if (window.turkmens.getVersion) {
      window.turkmens.getVersion().then(v => { $('#app-version').textContent = 'v' + v; }).catch(() => {});
    }
  }

  // ============ Event listeners ============
  function attachListeners() {
    // Auth
    $('#auth-form').addEventListener('submit', handleAuthSubmit);
    $$('.auth-tab').forEach(t => t.addEventListener('click', () => setAuthMode(t.dataset.mode)));
    $('#forget-session').addEventListener('click', (e) => {
      e.preventDefault();
      clearToken();
      $('#auth-error').textContent = 'Oturum bilgileri temizlendi.';
    });

    // Server list
    $('#home-btn').addEventListener('click', () => {
      if (currentServerId !== null) goHome();
      else showHomeView();
    });
    $('#add-server-btn').addEventListener('click', openAddServerModal);

    // Home actions
    $('#action-create').addEventListener('click', openCreateServerModal);
    $('#action-join').addEventListener('click', openJoinServerModal);

    // Add server modal
    $('#add-create-btn').addEventListener('click', openCreateServerModal);
    $('#add-join-btn').addEventListener('click', openJoinServerModal);

    // Create server modal
    $('#create-server-form').addEventListener('submit', handleCreateServer);

    // Join server modal
    $('#join-server-form').addEventListener('submit', handleJoinServer);

    // Create channel modal
    $('#create-channel-form').addEventListener('submit', handleCreateChannel);

    // Invite modal
    $('#invite-copy-btn').addEventListener('click', copyInvite);
    $('#invite-regen-btn').addEventListener('click', regenerateInvite);

    // Modal kapatma (her [data-close] elementi)
    document.addEventListener('click', (e) => {
      if (e.target.hasAttribute && e.target.hasAttribute('data-close')) {
        closeAllModals();
      }
      // Server menü dışına tıklayınca kapat
      if (!e.target.closest('#server-menu') && !e.target.closest('#server-menu-btn') && !e.target.closest('.server-header')) {
        closeServerMenu();
      }
    });

    // Escape kapatır
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeAllModals();
        closeServerMenu();
      }
    });

    // Server header menü
    $('#server-header').addEventListener('click', (e) => {
      if (e.target.closest('#server-menu')) return;
      toggleServerMenu();
    });
    $('#menu-invite').addEventListener('click', (e) => { e.stopPropagation(); closeServerMenu(); openInviteModal(); });
    $('#menu-add-channel').addEventListener('click', (e) => { e.stopPropagation(); closeServerMenu(); openCreateChannelModal('text'); });
    $('#menu-leave').addEventListener('click', (e) => { e.stopPropagation(); closeServerMenu(); leaveCurrentServer(); });

    // Messaging
    $('#send-btn').addEventListener('click', sendMessage);
    $('#message-input').addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });

    // Voice / status / user panel
    $('#status-select').addEventListener('change', (e) => {
      if (socket && socket.connected) socket.emit('status:change', { status: e.target.value });
    });
    $('#voice-leave-btn').addEventListener('click', leaveVoice);
    $('#voice-room-leave').addEventListener('click', leaveVoice);
    $('#mute-btn').addEventListener('click', toggleMute);
    $('#logout-btn').addEventListener('click', () => {
      if (confirm('Çıkış yapmak istediğine emin misin?')) logout();
    });
  }

  // ============ Boot ============
  document.addEventListener('DOMContentLoaded', () => {
    attachListeners();
    setupUpdates();
    setAuthMode('login');
    tryAutoLogin();
    $('#username-input').focus();
  });

  window.addEventListener('error', (e) => console.error('Renderer hatası:', e.error || e.message));
  window.addEventListener('unhandledrejection', (e) => console.error('Unhandled:', e.reason));
})();
