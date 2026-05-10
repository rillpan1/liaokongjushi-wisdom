<template>
  <div class="ai-chat-wrapper">
    <!-- ── 未登录：登录表单 ── -->
    <div v-if="!authenticated" class="login-form">
      <div class="login-card">
        <h2>AI 助手</h2>
        <p class="login-desc">基于知识库的智能问答</p>
        <form @submit.prevent="login">
          <input v-model="username" placeholder="用户名" autocomplete="username" />
          <input
            v-model="password"
            type="password"
            placeholder="密码"
            autocomplete="current-password"
          />
          <p v-if="loginError" class="error-msg">{{ loginError }}</p>
          <button type="submit" class="login-btn" :disabled="loggingIn">
            {{ loggingIn ? '登录中...' : '登录' }}
          </button>
        </form>
      </div>
    </div>

    <!-- ── 已登录：聊天界面 ── -->
    <div v-else class="chat-layout">
      <div class="chat-header">
        <span class="chat-title">AI 助手 <span class="chat-badge">基于知识库</span></span>
        <div class="header-right">
          <span class="user-name">{{ displayName }}</span>
          <button class="logout-btn" @click="logout">退出</button>
        </div>
      </div>

      <!-- Admin panel -->
      <div v-if="isAdmin" class="admin-panel">
        <button class="admin-toggle" @click="showAdmin = !showAdmin">
          ⚙ 管理 {{ showAdmin ? '▲' : '▼' }}
        </button>
        <div v-if="showAdmin" class="admin-body">
          <form @submit.prevent="createAccount" class="admin-form">
            <input v-model="newUser" placeholder="新用户名" />
            <input v-model="newPass" type="password" placeholder="新密码" />
            <button type="submit" :disabled="creating">{{ creating ? '...' : '创建用户' }}</button>
          </form>
          <p v-if="adminMsg" class="admin-msg">{{ adminMsg }}</p>
          <div v-if="userList.length" class="admin-user-list">
            <div v-for="u in userList" :key="u.username" class="admin-user-row">
              <span>{{ u.username }}</span>
              <span class="admin-user-date">{{ u.created_at }}</span>
            </div>
          </div>
          <button @click="loadUsers" class="admin-load-btn">刷新用户列表</button>
        </div>
      </div>

      <div class="chat-messages" ref="msgContainer">
        <div v-if="messages.length === 0" class="welcome-msg">
          <div class="welcome-icon">🧘</div>
          <p>你好！我是了空居士智慧的 AI 助手。</p>
          <p>你可以问我关于修行、七个核心模型、专题研究等方面的问题。</p>
          <div class="welcome-hints">
            <span class="hint" @click="input = '什么是清净心？'; send()">什么是清净心？</span>
            <span class="hint" @click="input = '如何面对焦虑？'; send()">如何面对焦虑？</span>
            <span class="hint" @click="input = '怎么开始实修？'; send()">怎么开始实修？</span>
            <span class="hint" @click="input = '天人合一的含义是什么？'; send()">天人合一的含义？</span>
          </div>
        </div>

        <div
          v-for="(msg, i) in messages"
          :key="i"
          :class="['msg', msg.role]"
        >
          <div class="bubble">
            <div v-if="msg.role === 'assistant' && msg.sources" class="source-badge">
              引用了 {{ msg.sources }} 个知识库片段
            </div>
            <div class="msg-content" v-html="renderContent(msg.content)"></div>
          </div>
        </div>

        <div v-if="streaming" class="msg assistant">
          <div class="bubble">
            <div class="msg-content streaming-cursor">{{ streamingContent }}</div>
          </div>
        </div>
      </div>

      <div class="chat-input-bar">
        <input
          v-model="input"
          placeholder="输入你的问题..."
          @keyup.enter="send"
          :disabled="streaming"
        />
        <button @click="send" :disabled="streaming || !input.trim()">发送</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'

const API = '/api'
const authenticated = ref(false)
const username = ref('')
const password = ref('')
const loginError = ref('')
const token = ref('')
const displayName = ref('')
const messages = ref([])
const input = ref('')
const streaming = ref(false)
const streamingContent = ref('')
const msgContainer = ref(null)
const isAdmin = ref(false)
const showAdmin = ref(false)
const newUser = ref('')
const newPass = ref('')
const creating = ref(false)
const adminMsg = ref('')
const userList = ref([])

function scrollToBottom() {
  nextTick(() => {
    if (msgContainer.value) {
      msgContainer.value.scrollTop = msgContainer.value.scrollHeight
    }
  })
}

function renderContent(text) {
  if (!text) return ''
  // Convert line breaks and URLs
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>')
}

onMounted(() => {
  const saved = localStorage.getItem('ai_token')
  const savedUser = localStorage.getItem('ai_username')
  if (saved) {
    token.value = saved
    displayName.value = savedUser || ''
    fetch(`${API}/auth/check`, {
      headers: { Authorization: `Bearer ${saved}` },
    })
      .then((r) => {
        if (r.ok) {
          authenticated.value = true
          if (displayName.value === 'admin' || savedUser === 'admin') isAdmin.value = true
          // Check for pre-filled query from URL
          const params = new URLSearchParams(window.location.search)
          const q = params.get('q')
          if (q) {
            input.value = q
            nextTick(() => send())
          }
        } else {
          localStorage.removeItem('ai_token')
          localStorage.removeItem('ai_username')
        }
      })
      .catch(() => {
        localStorage.removeItem('ai_token')
        localStorage.removeItem('ai_username')
      })
  } else {
    // Even without token, check for pre-filled query to use after login
    const params = new URLSearchParams(window.location.search)
    const q = params.get('q')
    if (q) {
      input.value = q
    }
  }
})

async function login() {
  loginError.value = ''
  loggingIn.value = true
  try {
    const r = await fetch(`${API}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    })
    if (!r.ok) {
      loginError.value = '用户名或密码错误'
      return
    }
    const data = await r.json()
    token.value = data.token
    displayName.value = data.username
    localStorage.setItem('ai_token', data.token)
    localStorage.setItem('ai_username', data.username)
    authenticated.value = true
    isAdmin.value = data.username === 'admin'
  } catch {
    loginError.value = '连接服务器失败，请稍后再试'
  } finally {
    loggingIn.value = false
  }
}
const loggingIn = ref(false)

function logout() {
  localStorage.removeItem('ai_token')
  localStorage.removeItem('ai_username')
  authenticated.value = false
  token.value = ''
  messages.value = []
  streamingContent.value = ''
  isAdmin.value = false
  showAdmin.value = false
  userList.value = []
}

async function loadUsers() {
  try {
    const r = await fetch(`${API}/admin/users`, {
      headers: { Authorization: `Bearer ${token.value}` },
    })
    if (r.ok) userList.value = await r.json()
  } catch { /* ignore */ }
}

async function createAccount() {
  if (!newUser.value.trim() || !newPass.value.trim()) return
  creating.value = true
  adminMsg.value = ''
  try {
    const r = await fetch(`${API}/admin/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token.value}`,
      },
      body: JSON.stringify({ username: newUser.value, password: newPass.value }),
    })
    if (r.ok) {
      adminMsg.value = `用户 "${newUser.value}" 创建成功`
      newUser.value = ''
      newPass.value = ''
      loadUsers()
    } else {
      const data = await r.json()
      adminMsg.value = data.detail || '创建失败'
    }
  } catch {
    adminMsg.value = '请求失败'
  } finally {
    creating.value = false
  }
}

async function send() {
  const msg = input.value.trim()
  if (!msg || streaming.value) return
  input.value = ''
  messages.value.push({ role: 'user', content: msg })
  scrollToBottom()

  streaming.value = true
  streamingContent.value = ''

  try {
    const r = await fetch(`${API}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token.value}`,
      },
      body: JSON.stringify({ message: msg }),
    })

    if (!r.ok) {
      streamingContent.value = '请求失败，请重试'
      streaming.value = false
      scrollToBottom()
      return
    }

    const reader = r.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })

      const parts = buffer.split('\n\n')
      buffer = parts.pop() || ''

      for (const part of parts) {
        const lines = part.split('\n')
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6).trim()
            if (data === '[DONE]') continue
            try {
              const obj = JSON.parse(data)
              const content = obj?.content || ''
              if (content) {
                streamingContent.value += content
                scrollToBottom()
              }
            } catch {
              /* skip malformed */
            }
          }
        }
      }
    }
  } catch {
    streamingContent.value = '网络错误，请检查连接后重试'
  }

  // Finalize message
  messages.value.push({
    role: 'assistant',
    content: streamingContent.value,
  })
  streaming.value = false
  streamingContent.value = ''
  scrollToBottom()
}
</script>

<style scoped>
.ai-chat-wrapper {
  max-width: 800px;
  margin: 0 auto;
  min-height: 70vh;
  display: flex;
  flex-direction: column;
}

/* ── Login ── */
.login-form {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  padding: 40px 16px;
}
.login-card {
  width: 380px;
  max-width: 100%;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 40px 32px;
  text-align: center;
}
.login-card h2 {
  font-family: var(--serif);
  font-size: 24px;
  color: var(--navy);
  margin: 0 0 4px !important;
  padding: 0 !important;
  border: none !important;
}
.login-desc {
  color: var(--text2);
  font-size: 14px;
  margin: 0 0 28px;
}
.login-card input {
  display: block;
  width: 100%;
  padding: 10px 14px;
  margin-bottom: 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 15px;
  background: var(--bg);
  color: var(--text);
  box-sizing: border-box;
}
.login-card input:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 0 3px var(--gold-glow);
}
.error-msg {
  color: #c00;
  font-size: 13px;
  margin: 0 0 12px;
}
.login-btn {
  width: 100%;
  padding: 11px;
  background: var(--gold);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.login-btn:hover { background: #9A7209; }
.login-btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* ── Chat ── */
.chat-layout {
  flex: 1;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  background: var(--card);
  min-height: 60vh;
}
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  background: var(--navy);
  color: #fff;
}
.chat-title {
  font-weight: 700;
  font-size: 15px;
}
.chat-badge {
  font-size: 10px;
  font-weight: 400;
  background: rgba(255,255,255,.15);
  padding: 2px 8px;
  border-radius: 8px;
  margin-left: 6px;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.user-name {
  font-size: 12px;
  opacity: 0.7;
}
.logout-btn {
  background: transparent;
  border: 1px solid rgba(255,255,255,.3);
  color: rgba(255,255,255,.8);
  padding: 4px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}
.logout-btn:hover {
  background: rgba(255,255,255,.1);
  color: #fff;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  max-height: 55vh;
}

/* Welcome */
.welcome-msg {
  text-align: center;
  padding: 48px 20px;
  color: var(--text2);
}
.welcome-icon {
  font-size: 48px;
  margin-bottom: 12px;
}
.welcome-msg p {
  margin: 4px 0;
  font-size: 14px;
  line-height: 1.7;
}
.welcome-hints {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 20px;
}
.hint {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text);
}
.hint:hover {
  border-color: var(--gold);
  background: var(--gold-glow);
  color: var(--navy);
}

/* Bubbles */
.msg { margin-bottom: 16px; }
.msg.user { text-align: right; }
.msg.user .bubble {
  display: inline-block;
  background: var(--gold);
  color: #fff;
  padding: 10px 16px;
  border-radius: 16px 16px 4px 16px;
  max-width: 80%;
  text-align: left;
  font-size: 14px;
  line-height: 1.6;
}
.msg.assistant { text-align: left; }
.msg.assistant .bubble {
  display: inline-block;
  background: var(--bg2);
  padding: 12px 18px;
  border-radius: 16px 16px 16px 4px;
  max-width: 90%;
  text-align: left;
  line-height: 1.8;
  font-size: 14px;
}
.source-badge {
  font-size: 11px;
  color: var(--gold);
  font-weight: 600;
  margin-bottom: 6px;
}
.msg-content {
  white-space: pre-wrap;
  word-break: break-word;
}
.streaming-cursor::after {
  content: '▌';
  animation: blink 0.8s infinite;
  color: var(--gold);
}
@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* Input */
.chat-input-bar {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid var(--border);
}
.chat-input-bar input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 14px;
  background: var(--bg);
  color: var(--text);
}
.chat-input-bar input:focus {
  outline: none;
  border-color: var(--gold);
}
.chat-input-bar button {
  padding: 10px 24px;
  background: var(--gold);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.chat-input-bar button:hover { background: #9A7209; }
.chat-input-bar button:disabled { opacity: 0.5; cursor: not-allowed; }

/* Admin panel */
.admin-panel {
  border-bottom: 1px solid rgba(255,255,255,.1);
  background: rgba(0,0,0,.15);
}
.admin-toggle {
  width: 100%;
  padding: 8px 20px;
  background: transparent;
  border: none;
  color: rgba(255,255,255,.6);
  cursor: pointer;
  font-size: 12px;
  text-align: left;
  transition: color .2s;
}
.admin-toggle:hover { color: #fff }
.admin-body {
  padding: 0 20px 14px;
}
.admin-form {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}
.admin-form input {
  flex: 1;
  padding: 6px 10px;
  border: 1px solid rgba(255,255,255,.15);
  border-radius: 6px;
  background: rgba(255,255,255,.08);
  color: #fff;
  font-size: 13px;
}
.admin-form input:focus { outline: none; border-color: var(--gold) }
.admin-form input::placeholder { color: rgba(255,255,255,.35) }
.admin-form button {
  padding: 6px 14px;
  background: var(--gold);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
}
.admin-form button:hover { background: #9A7209 }
.admin-msg { font-size: 12px; color: rgba(255,255,255,.6); margin: 0 0 8px }
.admin-user-list { margin-bottom: 8px }
.admin-user-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
  font-size: 12px;
  color: rgba(255,255,255,.55);
  border-bottom: 1px solid rgba(255,255,255,.06);
}
.admin-user-date { font-size: 11px; opacity: .6 }
.admin-load-btn {
  background: transparent;
  border: 1px solid rgba(255,255,255,.15);
  color: rgba(255,255,255,.5);
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
}
.admin-load-btn:hover { border-color: rgba(255,255,255,.3); color: #fff }

/* Mobile */
@media (max-width: 640px) {
  .chat-layout { border-radius: 8px; min-height: 70vh; }
  .chat-messages { max-height: 55vh; }
  .msg.user .bubble, .msg.assistant .bubble { max-width: 95%; font-size: 13px; }
  .welcome-msg { padding: 32px 16px; }
}
</style>
