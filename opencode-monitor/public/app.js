const statusDot = document.getElementById('statusDot')
const statusText = document.getElementById('statusText')
const contextModel = document.getElementById('contextModel')
const contextFill = document.getElementById('contextFill')
const contextText = document.getElementById('contextText')
const btnCompact = document.getElementById('btnCompact')
const btnClear = document.getElementById('btnClear')
const btnSummarize = document.getElementById('btnSummarize')
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

let eventCount = 0
let startTime = null
let eventSource = null
let currentInput = null

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

function updateFlowDiagram(event) {
  document.querySelectorAll('.flow-node').forEach(n => n.classList.remove('active', 'done'))
  document.querySelectorAll('.flow-arrow').forEach(a => a.classList.remove('active'))

  const t = event.type

  if (t === 'chat.message' || t === 'session:prompt') {
    document.getElementById('node-user').classList.add('active')
    const agent = event.properties?.agent || event.agent
    if (agent) document.getElementById('agentLabel').textContent = agent
  } else if (t === 'tool.execute.before' || t === 'tool:call') {
    document.getElementById('node-tools').classList.add('active')
    document.getElementById('arrow-3').classList.add('active')
    const tool = event.properties?.tool || event.tool
    if (tool) document.getElementById('toolLabel').textContent = tool
  } else if (t === 'tool.execute.after' || t === 'tool:result') {
    document.getElementById('node-tools').classList.add('done')
  } else if (t === 'message.updated' || t === 'session:response') {
    const msg = event.properties?.info || event.properties
    if (msg?.role === 'assistant') {
      document.getElementById('node-harness').classList.add('done')
      document.getElementById('node-llm').classList.add('done')
      document.getElementById('node-response').classList.add('active')
      const model = msg.modelID || msg.model || ''
      if (model) document.getElementById('modelLabel').textContent = model.split('/').pop()
    }
  } else if (t === 'message.part.updated') {
    const part = event.properties?.part
    if (part?.type === 'tool') {
      document.getElementById('node-tools').classList.add('active')
    } else if (part?.type === 'text') {
      document.getElementById('node-llm').classList.add('active')
    }
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
    timeline.appendChild(group)
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
    timeline.appendChild(group)
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

  currentInput.appendChild(item)
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

  eventsLog.appendChild(row)
  eventsLog.scrollTop = eventsLog.scrollHeight
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

async function fetchSessionStatus() {
  try {
    const res = await fetch('/api/session-status')
    const state = await res.json()

    if (state.totalTokens > 0) statTokens.textContent = formatNumber(state.totalTokens)
    if (state.totalCost > 0) statCost.textContent = '$' + state.totalCost.toFixed(4)
    if (state.tokensPerSecond > 0) statTps.textContent = state.tokensPerSecond
    if (state.sessionStatus) statStatus.textContent = state.sessionStatus
    if (state.sessionId) statSession.textContent = state.sessionId.slice(0, 8)
    if (state.lastModel) contextModel.textContent = state.lastModel

    if (state.contextLimit.input > 0) {
      const used = state.contextUsed
      const limit = state.contextLimit.input
      const pct = Math.min(100, (used / limit) * 100)
      contextFill.style.width = pct + '%'
      contextText.textContent = formatNumber(used) + ' / ' + formatNumber(limit) + ' tokens'
    }

    statTools.textContent = state.toolCount
  } catch {
    // Server might be down
  }
}

function formatNumber(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'K'
  return n.toString()
}

async function loadTools() {
  try {
    const [agentsRes, mcpRes] = await Promise.all([
      fetch('/api/tools').catch(() => null),
      fetch('/api/mcp').catch(() => null),
    ])

    const items = []

    if (agentsRes && agentsRes.ok) {
      const agents = await agentsRes.json()
      const list = Array.isArray(agents) ? agents : []
      for (const agent of list) {
        items.push({
          name: agent.name,
          type: 'agent',
          icon: agent.mode === 'subagent' ? '\uD83E\uDD16' : '\uD83D\uDC64',
          description: agent.description || agent.mode,
        })
      }
    }

    if (mcpRes && mcpRes.ok) {
      const mcps = await mcpRes.json()
      for (const [name, status] of Object.entries(mcps)) {
        items.push({
          name: name,
          type: 'mcp',
          icon: status.status === 'connected' ? '\uD83D\uDD0C' : '\u26A0\uFE0F',
          description: status.status,
        })
      }
    }

    if (items.length === 0) {
      toolsGrid.innerHTML = '<div class="no-events">Nenhuma ferramenta detectada</div>'
      return
    }

    toolsGrid.innerHTML = items.map(item =>
      '<div class="tool-chip" data-type="' + item.type + '" data-name="' + item.name + '" title="' + escapeHtml(item.description) + '">' +
      '<span class="tool-icon">' + item.icon + '</span> ' +
      '<span class="tool-name">' + escapeHtml(item.name) + '</span> ' +
      '<span class="tool-type">' + item.type + '</span>' +
      '</div>'
    ).join('')
  } catch {
    toolsGrid.innerHTML = '<div class="no-events">Erro ao carregar ferramentas</div>'
  }
}

btnCompact.addEventListener('click', async () => {
  btnCompact.disabled = true
  try {
    await fetch('/api/compact', { method: 'POST' })
  } catch { /* ignore */ }
  btnCompact.disabled = false
})

btnClear.addEventListener('click', async () => {
  if (!confirm('Criar nova sess\u00E3o? A sess\u00E3o atual ser\u00E1 finalizada.')) return
  btnClear.disabled = true
  try {
    await fetch('/api/clear', { method: 'POST' })
  } catch { /* ignore */ }
  btnClear.disabled = false
})

btnSummarize.addEventListener('click', async () => {
  btnSummarize.disabled = true
  try {
    await fetch('/api/summarize', { method: 'POST' })
  } catch { /* ignore */ }
  btnSummarize.disabled = false
})

setInterval(fetchSessionStatus, 2000)

connect()
loadTools()
fetchSessionStatus()
