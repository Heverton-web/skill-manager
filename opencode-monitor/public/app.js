const statusDot = document.getElementById('statusDot')
const statusText = document.getElementById('statusText')
const contextModel = document.getElementById('contextModel')
const contextFill = document.getElementById('contextFill')
const contextText = document.getElementById('contextText')
const sessionFill = document.getElementById('sessionFill')
const sessionText = document.getElementById('sessionText')
const statEvents = document.getElementById('statEvents')
const statTools = document.getElementById('statTools')
const statTokens = document.getElementById('statTokens')
const statCost = document.getElementById('statCost')
const statTps = document.getElementById('statTps')
const statDuration = document.getElementById('statDuration')
const statStatus = document.getElementById('statStatus')
const statSession = document.getElementById('statSession')
const timeline = document.getElementById('timeline')
const eventsLog = document.getElementById('eventsLog')
const toolsGrid = document.getElementById('toolsGrid')
const skillsPanel = document.getElementById('skillsPanel')

let eventCount = 0
let startTime = null
let eventSource = null
let currentInput = null
let lastApiPoll = 0
let flowResetTimer = null

function connect() {
  eventSource = new EventSource('/events')

  eventSource.onopen = () => {
    statusDot.classList.add('connected')
    statusText.textContent = 'Conectado'
  }

  eventSource.onerror = () => {
    statusDot.classList.remove('connected')
    statusText.textContent = 'Reconectando...'
    setTimeout(connect, 3000)
  }

  eventSource.onmessage = (msg) => {
    const event = JSON.parse(msg.data)
    handleEvent(event)
  }
}

function handleEvent(event) {
  if (event.type === 'connected') return

  if (event.type === 'session-status') {
    updateFromSessionStatus(event)
    return
  }

  eventCount++
  statEvents.textContent = eventCount

  if (!startTime) {
    startTime = event.timestamp
    statSession.textContent = event.sessionId?.slice(0, 8) || event.properties?.sessionID?.slice(0, 8) || '-'
  }

  const elapsed = ((event.timestamp - startTime) / 1000).toFixed(0)
  statDuration.textContent = elapsed + 's'

  updateFlowDiagram(event)
  addTimelineEntry(event)
  addLogEntry(event)
  fetchSessionStatus()
}

function updateFromSessionStatus(state) {
  if (state.totalTokens > 0) statTokens.textContent = formatNumber(state.totalTokens)
  if (state.totalCost > 0) statCost.textContent = '$' + state.totalCost.toFixed(4)
  if (state.tokensPerSecond > 0) statTps.textContent = state.tokensPerSecond
  if (state.sessionStatus) statStatus.textContent = state.sessionStatus
  if (state.sessionId) statSession.textContent = state.sessionId.slice(0, 8)
  if (state.lastModel) contextModel.textContent = state.lastModel

  updateContextBars(state)
  updateFlowFromStatus(state.sessionStatus)

  if (state.toolCount > 0) statTools.textContent = state.toolCount

  const elapsed = state.startTime ? ((Date.now() - state.startTime) / 1000).toFixed(0) : 0
  if (elapsed > 0) statDuration.textContent = elapsed + 's'
}

function updateContextBars(state) {
  const sessionUsed = (state.sessionInputTokens || 0) + (state.sessionOutputTokens || 0) + (state.sessionReasoningTokens || 0)
  const allUsed = state.allSessionsTokens || state.totalTokens || 0
  const limit = state.contextLimit?.input || 0

  if (limit > 0) {
    const sessionPct = Math.min(100, (sessionUsed / limit) * 100)
    const allPct = Math.min(100, (allUsed / limit) * 100)

    contextFill.style.width = allPct + '%'
    applyBarColor(contextFill, allPct)
    contextText.textContent = formatNumber(allUsed) + ' (' + Math.round(allPct) + '%)'

    sessionFill.style.width = sessionPct + '%'
    applyBarColor(sessionFill, sessionPct)
    sessionText.textContent = formatNumber(sessionUsed) + ' (' + Math.round(sessionPct) + '%)'
  } else if (allUsed > 0) {
    contextFill.style.width = '100%'
    contextFill.style.background = 'linear-gradient(90deg, #3b82f6, #2563eb)'
    contextText.textContent = formatNumber(allUsed) + ' tokens'

    sessionFill.style.width = '100%'
    sessionFill.style.background = 'linear-gradient(90deg, #3b82f6, #2563eb)'
    sessionText.textContent = formatNumber(sessionUsed) + ' tokens'
  } else {
    contextFill.style.width = '0%'
    contextText.textContent = '0 tokens (0%)'
    sessionFill.style.width = '0%'
    sessionText.textContent = '0 tokens (0%)'
  }
}

function applyBarColor(fill, pct) {
  if (pct > 90) {
    fill.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)'
  } else if (pct > 70) {
    fill.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)'
  } else {
    fill.style.background = 'linear-gradient(90deg, #3b82f6, #2563eb)'
  }
}

function updateFlowFromStatus(status) {
  if (status === 'idle') {
    document.querySelectorAll('.flow-node').forEach(n => n.classList.remove('active'))
    document.querySelectorAll('.flow-arrow').forEach(a => a.classList.remove('active'))
  }
}

function updateFlowDiagram(event) {
  if (flowResetTimer) clearTimeout(flowResetTimer)

  const t = event.type

  if (t === 'chat.message' || t === 'session:prompt') {
    document.querySelectorAll('.flow-node').forEach(n => {
      n.classList.remove('active')
      n.classList.remove('done')
    })
    document.querySelectorAll('.flow-arrow').forEach(a => a.classList.remove('active'))

    document.getElementById('node-user').classList.add('active')
    const agent = event.properties?.agent || event.agent
    if (agent) {
      document.getElementById('agentLabel').textContent = agent
      document.getElementById('agentLabel2').textContent = agent
    }

    flowResetTimer = setTimeout(() => {
      document.getElementById('node-user').classList.remove('active')
      document.getElementById('node-user').classList.add('done')
      document.getElementById('arrow-1').classList.add('active')
      document.getElementById('node-harness').classList.add('active')
    }, 300)

  } else if (t === 'tool.execute.before' || t === 'tool:call') {
    document.getElementById('node-harness').classList.remove('active')
    document.getElementById('node-harness').classList.add('done')
    document.getElementById('arrow-2').classList.add('active')
    document.getElementById('node-llm').classList.add('active')
    document.getElementById('arrow-3').classList.add('active')
    document.getElementById('node-tools').classList.add('active')

    const tool = event.properties?.tool || event.tool
    if (tool) document.getElementById('toolLabel').textContent = tool

  } else if (t === 'tool.execute.after' || t === 'tool:result') {
    document.getElementById('node-tools').classList.remove('active')
    document.getElementById('node-tools').classList.add('done')

  } else if (t === 'message.updated' || t === 'session:response') {
    const msg = event.properties?.info || event.properties
    if (msg?.role === 'assistant') {
      document.getElementById('node-harness').classList.remove('active')
      document.getElementById('node-harness').classList.add('done')
      document.getElementById('node-llm').classList.remove('active')
      document.getElementById('node-llm').classList.add('done')
      document.getElementById('arrow-4').classList.add('active')
      document.getElementById('node-response').classList.add('active')

      const model = msg.modelID || msg.model || ''
      if (model) document.getElementById('modelLabel').textContent = model.split('/').pop()

      flowResetTimer = setTimeout(() => {
        document.getElementById('node-response').classList.remove('active')
        document.getElementById('node-response').classList.add('done')
      }, 1500)
    }

  } else if (t === 'message.part.updated') {
    const part = event.properties?.part
    if (part?.type === 'tool') {
      document.getElementById('node-tools').classList.add('active')
    } else if (part?.type === 'text') {
      document.getElementById('node-harness').classList.remove('active')
      document.getElementById('node-harness').classList.add('done')
      document.getElementById('node-llm').classList.add('active')
      document.getElementById('arrow-2').classList.add('active')
      document.getElementById('arrow-3').classList.remove('active')
      document.getElementById('node-tools').classList.remove('active')
    }

  } else if (t === 'session.status') {
    const status = event.properties?.status?.type
    if (status) updateFlowFromStatus(status)
  }
}

function addTimelineEntry(event) {
  if (timeline.querySelector('.no-events')) {
    timeline.innerHTML = ''
  }

  const t = event.type
  const isUserInput = t === 'chat.message' || t === 'session:prompt'

  if (isUserInput) {
    const group = document.createElement('div')
    group.className = 'timeline-group'

    const header = document.createElement('div')
    header.className = 'timeline-group-header'

    const userText = event.properties?.parts?.find(p => p.type === 'text')?.text
      || event.prompt
      || ''

    const time = new Date(event.timestamp).toLocaleTimeString('pt-BR')
    header.innerHTML =
      '<span class="user-icon">\uD83D\uDC64</span>' +
      '<span class="user-text">' + escapeHtml(userText.slice(0, 120) + (userText.length > 120 ? '...' : '')) + '</span>' +
      '<span class="group-time">' + time + '</span>'

    group.appendChild(header)
    timeline.prepend(group)
    currentInput = group
    return
  }

  if (!currentInput) {
    const group = document.createElement('div')
    group.className = 'timeline-group'
    const header = document.createElement('div')
    header.className = 'timeline-group-header'
    header.innerHTML = '<span class="user-icon">\uD83D\uDCE1</span><span class="user-text">System Events</span>'
    group.appendChild(header)
    timeline.prepend(group)
    currentInput = group
  }

  const item = document.createElement('div')
  item.className = 'timeline-item active'

  const time = new Date(event.timestamp).toLocaleTimeString('pt-BR')
  let detail = ''
  const props = event.properties || {}

  if (t === 'tool.execute.before') {
    detail = props.tool + '(' + JSON.stringify(props.args || {}).slice(0, 60) + ')'
  } else if (t === 'tool.execute.after') {
    detail = props.tool + ' \u2192 ' + (props.title || 'OK')
  } else if (t === 'message.updated') {
    const msg = props.info || props
    detail = (msg.role || '?') + ' \u2014 ' + (msg.modelID || msg.model || '').slice(0, 30)
  } else if (t === 'message.part.updated') {
    const part = props.part || {}
    detail = part.type + ': ' + (part.text || part.tool || '').slice(0, 60)
  } else if (t === 'session.status') {
    detail = 'status: ' + (props.status?.type || '?')
  } else {
    detail = JSON.stringify(props).slice(0, 80)
  }

  const typeClass = t.split('.')[0].split(':')[0]
  item.innerHTML =
    '<span class="event-time">' + time + '</span> ' +
    '<span class="event-type ' + typeClass + '">' + escapeHtml(t) + '</span> ' +
    '<div class="event-detail">' + escapeHtml(detail) + '</div>'

  currentInput.prepend(item)
}

function addLogEntry(event) {
  if (eventsLog.querySelector('.no-events')) {
    eventsLog.innerHTML = ''
  }

  const row = document.createElement('div')
  row.className = 'event-row'

  const time = new Date(event.timestamp).toLocaleTimeString('pt-BR')
  const t = event.type
  const typeClass = t.split('.')[0].split(':')[0]
  let detail = JSON.stringify(event).slice(0, 150)

  row.innerHTML =
    '<span class="event-time">' + time + '</span> ' +
    '<span class="event-type ' + typeClass + '">' + escapeHtml(t) + '</span> ' +
    '<span class="event-detail">' + escapeHtml(detail) + '</span>'

  eventsLog.prepend(row)
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

async function fetchSessionStatus() {
  const now = Date.now()
  if (now - lastApiPoll < 2500) return
  lastApiPoll = now

  try {
    const res = await fetch('/api/session-status')
    const state = await res.json()

    if (state.totalTokens > 0) statTokens.textContent = formatNumber(state.totalTokens)
    if (state.totalCost > 0) statCost.textContent = '$' + state.totalCost.toFixed(4)
    if (state.tokensPerSecond > 0) statTps.textContent = state.tokensPerSecond
    if (state.sessionStatus) statStatus.textContent = state.sessionStatus
    if (state.sessionId) statSession.textContent = state.sessionId.slice(0, 8)
    if (state.lastModel) contextModel.textContent = state.lastModel

    updateContextBars(state)

    if (state.toolCount > 0) statTools.textContent = state.toolCount

    const elapsed = state.startTime ? ((Date.now() - state.startTime) / 1000).toFixed(0) : 0
    if (elapsed > 0) statDuration.textContent = elapsed + 's'

  } catch {
    // Server might be down
  }
}

function formatNumber(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'K'
  return n.toString()
}

function showNotice(msg) {
  let notice = document.getElementById('global-notice')
  if (!notice) {
    notice = document.createElement('div')
    notice.id = 'global-notice'
    notice.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#e2e8f0;padding:12px 24px;border-radius:8px;border:1px solid #334155;font-size:14px;z-index:9999;box-shadow:0 4px 12px rgba(0,0,0,.4);transition:opacity .3s'
    document.body.appendChild(notice)
  }
  notice.textContent = msg
  notice.style.opacity = '1'
  clearTimeout(notice._timer)
  notice._timer = setTimeout(() => { notice.style.opacity = '0' }, 4000)
}



document.addEventListener('click', e => {
  const cmdBtn = e.target.closest('.cmd-btn')
  if (cmdBtn) {
    const cmd = cmdBtn.dataset.cmd
    if (cmd) {
      navigator.clipboard.writeText(cmd).then(() => {
        showNotice('Copiado: ' + cmd)
        cmdBtn.classList.add('copied')
        setTimeout(() => cmdBtn.classList.remove('copied'), 1500)
      }).catch(() => {
        showNotice('Erro ao copiar. Tente novamente.')
      })
    }
    return
  }

  const skillHeader = e.target.closest('.skill-header')
  if (skillHeader) {
    const card = skillHeader.closest('.skill-card')
    if (card) card.classList.toggle('open')
    return
  }

  const skillCopyBtn = e.target.closest('.skill-copy-btn')
  if (skillCopyBtn) {
    e.stopPropagation()
    const cmd = skillCopyBtn.dataset.cmd
    if (cmd) {
      navigator.clipboard.writeText(cmd).then(() => {
        showNotice('Copiado: ' + cmd)
        skillCopyBtn.classList.add('copied')
        const original = skillCopyBtn.innerHTML
        skillCopyBtn.innerHTML = '&#x2705; Copiado!'
        setTimeout(() => {
          skillCopyBtn.classList.remove('copied')
          skillCopyBtn.innerHTML = original
        }, 1500)
      }).catch(() => {
        showNotice('Erro ao copiar. Tente novamente.')
      })
    }
  }
})

setInterval(fetchSessionStatus, 3000)

async function fetchTools() {
  try {
    const res = await fetch('/api/tools')
    const data = await res.json()
    const grid = toolsGrid
    grid.innerHTML = ''

    if (data.usedTools && data.usedTools.length > 0) {
      const usedSection = document.createElement('div')
      usedSection.className = 'tools-section'
      usedSection.innerHTML = '<div class="tools-section-title">Em uso nesta sessao</div>'
      for (const tool of data.usedTools) {
        const chip = document.createElement('span')
        chip.className = 'tool-chip active'
        chip.textContent = tool
        usedSection.appendChild(chip)
      }
      grid.appendChild(usedSection)
    }

    if (data.mcp && data.mcp.length > 0) {
      const mcpSection = document.createElement('div')
      mcpSection.className = 'tools-section'
      mcpSection.innerHTML = '<div class="tools-section-title">MCP Servers</div>'
      for (const mcp of data.mcp) {
        const chip = document.createElement('span')
        chip.className = 'tool-chip mcp'
        chip.textContent = mcp.name + (mcp.enabled ? '' : ' (disabled)')
        if (!mcp.enabled) chip.style.opacity = '0.5'
        mcpSection.appendChild(chip)
      }
      grid.appendChild(mcpSection)
    }

    if (grid.children.length === 0) {
      grid.innerHTML = '<div class="no-events">Nenhuma ferramenta detectada</div>'
    }

    renderSkills(data.skills || [])
  } catch {
    toolsGrid.innerHTML = '<div class="no-events">Erro ao carregar ferramentas</div>'
  }
}

const SKILLS_INITIAL = 6
let allSkills = []
let skillsShowingAll = false

function renderSkills(skills) {
  if (!skillsPanel) return
  skillsPanel.innerHTML = ''
  allSkills = skills || []
  skillsShowingAll = false

  if (allSkills.length === 0) {
    skillsPanel.innerHTML = '<div class="no-events" style="padding:12px;font-size:0.75rem">Nenhuma skill detectada</div>'
    return
  }

  const search = document.createElement('input')
  search.className = 'skills-search'
  search.type = 'text'
  search.placeholder = 'Buscar skill...'
  skillsPanel.appendChild(search)

  const list = document.createElement('div')
  list.className = 'skills-list'
  skillsPanel.appendChild(list)

  renderSkillList(allSkills, list, search)
  setupSkillsSearch()
}

function renderSkillList(skills, container, searchInput) {
  container.innerHTML = ''
  const query = searchInput ? searchInput.value.toLowerCase() : ''
  const filtered = query ? skills.filter(s => s.name.toLowerCase().includes(query)) : skills
  const limited = (!skillsShowingAll && !query) ? filtered.slice(0, SKILLS_INITIAL) : filtered

  for (const skill of limited) {
    const card = document.createElement('div')
    card.className = 'skill-card'

    const desc = skill.description || 'Skill disponivel no OpenCode'
    const cmd = '/skill:' + skill.name

    card.innerHTML =
      '<div class="skill-header">' +
        '<span class="skill-name">' + escapeHtml(skill.name) + '</span>' +
        '<span class="skill-arrow">&#x25BC;</span>' +
      '</div>' +
      '<div class="skill-body">' +
        '<p class="skill-desc">' + escapeHtml(desc) + '</p>' +
        '<button class="skill-copy-btn" data-cmd="' + escapeHtml(cmd) + '">' +
          '&#x1F4CB; Copiar trigger' +
        '</button>' +
      '</div>'

    container.appendChild(card)
  }

  const existingToggle = container.parentNode.querySelector('.skills-toggle')
  if (existingToggle) existingToggle.remove()

  if (filtered.length > SKILLS_INITIAL && !query) {
    const btn = document.createElement('button')
    btn.className = 'skills-toggle'
    btn.textContent = skillsShowingAll
      ? 'Recolher'
      : 'Mostrar todas (' + filtered.length + ')'
    btn.addEventListener('click', () => {
      skillsShowingAll = !skillsShowingAll
      renderSkillList(skills, container, searchInput)
    })
    container.parentNode.appendChild(btn)
  }
}

function setupSkillsSearch() {
  const search = skillsPanel.querySelector('.skills-search')
  if (!search) return
  let debounce = null
  search.addEventListener('input', () => {
    clearTimeout(debounce)
    debounce = setTimeout(() => {
      const list = skillsPanel.querySelector('.skills-list')
      if (list) renderSkillList(allSkills, list, search)
    }, 200)
  })
}

setInterval(fetchTools, 10000)

connect()
fetchSessionStatus()
fetchTools()

// Card collapse/expand functionality
const STORAGE_KEY = 'opencode-monitor-collapsed'

function initCardCollapse() {
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')

  document.querySelectorAll('.card[data-card]').forEach(card => {
    const key = card.dataset.card
    if (saved[key]) {
      card.classList.add('collapsed')
    }
  })

  document.addEventListener('click', e => {
    const header = e.target.closest('.card-header')
    if (!header) return

    const card = header.closest('.card[data-card]')
    if (!card) return

    if (e.target.closest('.cmd-btn, .skill-copy-btn, .skills-search, .skills-toggle')) return

    card.classList.toggle('collapsed')

    const key = card.dataset.card
    const state = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')
    state[key] = card.classList.contains('collapsed')
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
  })
}

initCardCollapse()
