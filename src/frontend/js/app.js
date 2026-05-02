/* ── Main Application Logic ── */

// ── Directory management for project form ──
const pendingDirs = { frontend: [], backend: [], single: [], miniapp: [] };

async function browseDir(type) {
  // Try showDirectoryPicker first (Chrome 89+, but only returns dir name)
  try {
    const handle = await window.showDirectoryPicker();
    const input = getDirInput(type);
    if (input) {
      input.value = handle.name;
      input.placeholder = '输入完整路径，例如 D:\\githome\\' + handle.name;
      input.focus();
      input.select();
    }
    const hint = document.getElementById(`hint-${type}`);
    if (hint) hint.style.display = 'block';
    return;
  } catch (err) {
    if (err.name !== 'AbortError') {
      console.warn('showDirectoryPicker failed, trying fallback:', err);
    }
  }

  // Fallback: webkitdirectory input
  const picker = document.getElementById('dirPicker');
  picker.onchange = function () {
    if (picker.files && picker.files.length > 0) {
      const first = picker.files[0];
      const rel = first.webkitRelativePath;
      let dirPath = '';

      // file.path — Chrome extension (removed in newer versions)
      if (first.path) {
        dirPath = first.path.substring(0, first.path.length - rel.length).replace(/[/\\]$/, '');
      }

      if (dirPath) {
        pendingDirs[type].push(dirPath);
      } else {
        const input = getDirInput(type);
        if (input) {
          input.value = topDir;
          input.placeholder = '输入完整路径，例如 D:\\githome\\' + topDir;
          input.focus();
          input.select();
        }
        const hint = document.getElementById(`hint-${type}`);
        if (hint) hint.style.display = 'block';
      }
      renderDirList(type);
    }
    picker.value = '';
  };
  picker.click();
}

function getDirInput(type) {
  const map = { frontend: 'frontendDir', backend: 'backendDir', single: 'singleDir', miniapp: 'miniappDir' };
  return document.getElementById(map[type]);
}

function addDirFromInput(type) {
  const input = getDirInput(type);
  const val = input.value.trim();
  if (!val) return;
  pendingDirs[type].push(val);
  input.value = '';
  renderDirList(type);
  const hint = document.getElementById(`hint-${type}`);
  if (hint) hint.style.display = 'none';
}

function removeDir(type, index) {
  pendingDirs[type].splice(index, 1);
  renderDirList(type);
}

function renderDirList(type) {
  const map = {
    frontend: 'frontendDirs', backend: 'backendDirs',
    single: 'singleDirs', miniapp: 'miniappDirs',
  };
  const list = document.getElementById(map[type]);
  if (!list) return;
  list.innerHTML = pendingDirs[type].map((d, i) =>
    `<li><span>${d}</span><button onclick="removeDir('${type}', ${i})">✕</button></li>`
  ).join('');
}

// ── Project type switching ──
let currentProjectType = 'h5';

function selectProjectType(type) {
  currentProjectType = type;
  document.getElementById('h5Config').style.display = type === 'h5' ? 'block' : 'none';
  document.getElementById('miniprogramConfig').style.display = type === 'miniprogram' ? 'block' : 'none';
}

function toggleDirMode() {
  const single = document.getElementById('isSingleDir').checked;
  document.getElementById('dirGroupSplit').style.display = single ? 'none' : 'block';
  document.getElementById('dirGroupSingle').style.display = single ? 'block' : 'none';
}

// ── Tab switching ──
function switchTab(tab) {
  document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
  document.getElementById(`tab-${tab}`).classList.add('active');
  document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

  if (tab === 'projects') loadProjects();
  if (tab === 'test') populateProjectSelect();
  if (tab === 'settings') {
    loadAIStatus();
    loadPWVersion();
  }
}

// ── Add project form ──
document.getElementById('addProjectForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('projectName').value.trim();
  if (!name) return alert('请填写项目名称');

  const projectType = currentProjectType;

  if (projectType === 'h5') {
    const isSingle = document.getElementById('isSingleDir').checked;
    const frontend = isSingle ? [] : pendingDirs.frontend;
    const backend = isSingle ? [] : pendingDirs.backend;
    const single = isSingle ? pendingDirs.single : [];

    if (!frontend.length && !backend.length && !single.length) {
      return alert('请至少添加一个代码目录');
    }

    try {
      await API.addProject(name, projectType, frontend, backend, single, {});
      resetForm();
    } catch (err) {
      alert('添加项目失败: ' + err.message);
    }
  } else {
    const dirs = pendingDirs.miniapp;
    if (!dirs.length) return alert('请添加小程序项目目录');

    const devtoolsPath = document.getElementById('devtoolsPath').value.trim();
    const platform = document.getElementById('miniumPlatform').value;

    try {
      await API.addProject(name, projectType, [], [], dirs, {
        dev_tool_path: devtoolsPath,
        platform: platform,
      });
      resetForm();
    } catch (err) {
      alert('添加项目失败: ' + err.message);
    }
  }
});

function resetForm() {
  document.getElementById('projectName').value = '';
  for (const key of Object.keys(pendingDirs)) {
    pendingDirs[key] = [];
    renderDirList(key);
  }
  loadProjects();
}

// ── Load projects (expandable) ──
async function loadProjects() {
  try {
    const projects = await API.listProjects();
    const list = document.getElementById('projectList');
    if (projects.length === 0) {
      list.innerHTML = '<p class="text-muted">暂无项目，请添加</p>';
      return;
    }
    list.innerHTML = projects.map(p => {
      const ptype = p.project_type || 'h5';
      const isMini = ptype === 'miniprogram';
      const typeTag = isMini
        ? '<span class="type-tag mp">小程序</span>'
        : '<span class="type-tag h5">H5</span>';

      const dirs = isMini
        ? (p.single_dirs || [])
        : [...(p.frontend_dirs || []), ...(p.backend_dirs || [])];
      const allDirs = dirs.length ? dirs : (p.single_dirs || []);
      const modeTag = isMini ? '' : (!(p.frontend_dirs || []).length && (p.single_dirs || []).length > 0 ? ' 总目录' : '');

      return `<div class="project-item" onclick="toggleProjectExpand('${p.id}')">
        <div>
          <div class="name">${typeTag} ${p.name}</div>
          <div class="info">${allDirs.length} 个目录${modeTag}</div>
        </div>
        <button class="delete-btn" onclick="event.stopPropagation();deleteProject('${p.id}')">删除</button>
      </div>
      <div class="project-detail" id="detail-${p.id}" style="display:none">
        ${allDirs.map(d => `<div class="detail-dir">📁 ${d}</div>`).join('')}
        ${isMini && p.miniprogram_config ? `
          <div class="detail-dir">⚙️ 平台: ${p.miniprogram_config.platform || 'ide'}</div>
          ${p.miniprogram_config.dev_tool_path ? `<div class="detail-dir">🔧 开发者工具: ${p.miniprogram_config.dev_tool_path}</div>` : ''}
        ` : ''}
      </div>`;
    }).join('');
  } catch (err) {
    console.error('loadProjects error:', err);
  }
}

function toggleProjectExpand(id) {
  const el = document.getElementById('detail-' + id);
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
}

async function deleteProject(id) {
  if (!confirm('确定删除此项目？')) return;
  try {
    await API.deleteProject(id);
    loadProjects();
  } catch (err) {
    alert('删除失败: ' + err.message);
  }
}

// ── Populate project select ──
async function populateProjectSelect() {
  try {
    const projects = await API.listProjects();
    const sel = document.getElementById('testProjectSelect');
    sel.innerHTML = '<option value="">-- 选择项目 --</option>' +
      projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
  } catch (err) {
    console.error(err);
  }
}

// ── Start test ──
async function startTest() {
  const projectId = document.getElementById('testProjectSelect').value;
  if (!projectId) return alert('请先选择项目');

  // Show project type in console
  const projects = await API.listProjects();
  const project = projects.find(p => p.id === projectId);
  const ptype = project?.project_type || 'h5';
  const label = ptype === 'miniprogram' ? '微信小程序' : 'H5 网页';

  const btn = document.getElementById('startTestBtn');
  btn.disabled = true;
  btn.textContent = '⏳ 测试中...';

  document.getElementById('progressContainer').style.display = 'flex';
  updateProgress(0);
  clearConsole();
  setConsoleStatus('启动中...');
  appendLog(`[system] 项目类型: ${label}\n`);

  try {
    const result = await API.startTest(projectId);
    wsClient.connect(result.task_id);
    appendLog(`[system] 任务已创建: ${result.task_id}\n`);
  } catch (err) {
    appendLog(`[ERROR] ${err.message}\n`);
    enableTestButton();
  }
}

// ── Start expanded test ──
async function startExpandedTest() {
  const projectId = document.getElementById('testProjectSelect').value;
  if (!projectId) return alert('请先选择项目');

  const projects = await API.listProjects();
  const project = projects.find(p => p.id === projectId);
  const ptype = project?.project_type || 'h5';
  const label = ptype === 'miniprogram' ? '微信小程序' : 'H5 网页';

  const btn = document.getElementById('startExpandedBtn');
  btn.disabled = true;
  btn.textContent = '⏳ 扩充测试中...';

  document.getElementById('progressContainer').style.display = 'flex';
  updateProgress(0);
  clearConsole();
  setConsoleStatus('启动扩充测试...');
  appendLog('[system] 项目类型: ' + label + ' | 模式: 扩充测试\n');
  appendLog('[system] 将生成边界、异常、并发等更多场景的测试用例\n');

  try {
    const result = await API.startExpandedTest(projectId);
    wsClient.connect(result.task_id);
    appendLog('[system] 扩充测试任务已创建: ' + result.task_id + '\n');
  } catch (err) {
    appendLog('[ERROR] ' + err.message + '\n');
    enableExpandedTestButton();
  }
}

function enableExpandedTestButton() {
  const btn = document.getElementById('startExpandedBtn');
  btn.disabled = false;
  btn.textContent = '🔬 扩充测试场景开始测试';
}

function enableTestButton() {
  const btn = document.getElementById('startTestBtn');
  btn.disabled = false;
  btn.textContent = '🚀 开始测试';
  const btn2 = document.getElementById('startExpandedBtn');
  if (btn2) {
    btn2.disabled = false;
    btn2.textContent = '🔬 扩充测试场景开始测试';
  }
}

// ── Console ──
function clearConsole() {
  document.getElementById('consoleBody').innerHTML = '';
}

function clearLogs() {
  clearConsole();
  setConsoleStatus('就绪');
}

function appendLog(message) {
  const body = document.getElementById('consoleBody');
  const empty = body.querySelector('.log-empty');
  if (empty) empty.remove();

  const line = document.createElement('div');
  line.className = 'log-line';
  if (message.includes('[ERROR]')) line.classList.add('error');
  else if (message.includes('[system]')) line.classList.add('info');
  else if (message.includes('passed')) line.classList.add('success');
  else if (message.includes('Step') || message.includes('步骤')) line.classList.add('warn');
  line.textContent = message;
  body.appendChild(line);
  body.scrollTop = body.scrollHeight;
}

function setConsoleStatus(text) {
  document.getElementById('consoleStatus').textContent = text;
}

function updateProgress(percent) {
  const fill = document.getElementById('progressFill');
  const text = document.getElementById('progressText');
  const p = Math.min(100, Math.max(0, percent));
  fill.style.width = p + '%';
  text.textContent = Math.round(p) + '%';
}

// ── Results ──
function renderResults(result) {
  const summary = result.summary || {};
  const suites = result.suites || [];
  const diagSummary = result.diagnostic_summary || {};

  document.getElementById('resultSummary').style.display = 'block';

  const modeLabel = result.test_mode === 'expanded' ? '🔬 扩充测试' : '🚀 标准测试';

  let statsHtml = `
    <div class="stat-card total"><div class="stat-value">${summary.total || 0}</div><div class="stat-label">总计 <span class="text-muted" style="font-weight:400">${modeLabel}</span></div></div>
    <div class="stat-card passed"><div class="stat-value">${summary.passed || 0}</div><div class="stat-label">通过</div></div>
    <div class="stat-card failed"><div class="stat-value">${summary.failed || 0}</div><div class="stat-label">失败</div></div>`;

  // Diagnostic summary
  const cats = diagSummary.categories;
  if (cats && Object.keys(cats).length > 0) {
    statsHtml += `<div class="diag-summary">
      <div class="diag-summary-title">失败分类诊断:</div>`;
    for (const [label, count] of Object.entries(cats)) {
      const cls = label.includes('被测对象') ? 'app-bug'
                : label.includes('工具') ? 'tool-issue'
                : label.includes('用例') ? 'test-issue' : 'unknown';
      statsHtml += `<span class="diag-tag ${cls}">${label}: ${count}</span>`;
    }
    statsHtml += `</div>`;
  }

  document.getElementById('statsGrid').innerHTML = statsHtml;

  const detail = document.getElementById('resultDetail');
  detail.innerHTML = suites.map(s => `
    <div class="suite-card">
      <div class="suite-header">
        <span>${s.title || 'Unknown Suite'}</span>
        <span>${s.tests ? s.tests.filter(t => t.status === 'expected' || t.status === 'passed').length + '/' + s.tests.length : 0}</span>
      </div>
      <div class="suite-body">
        ${(s.tests || []).map(t => {
          const isPass = t.status === 'expected' || t.status === 'passed';
          const isFail = t.status === 'unexpected' || t.status === 'failed';
          const diag = t.diagnosis || {};
          const catLabel = diag.category_label || '';
          const catClass = diag.category === 'app_bug' ? 'diag-app-bug'
                         : diag.category === 'tool_issue' ? 'diag-tool-issue'
                         : diag.category === 'test_issue' ? 'diag-test-issue'
                         : '';
          return `
          <div class="test-row">
            <span>${t.title || 'Unknown Test'}</span>
            <span class="test-status ${isPass ? 'passed' : isFail ? 'failed' : 'skipped'}">
              ${isPass ? '通过' : isFail ? '失败' : '跳过'}
            </span>
          </div>
          ${isFail && diag.root_cause ? `<div class="test-row" style="font-size:11px;color:var(--warning);flex-direction:column;align-items:start">
            ${catLabel ? `<span class="diag-badge ${catClass}">${catLabel}</span>` : ''}
            <strong>AI 诊断:</strong> ${diag.root_cause || ''}
            ${diag.fix_suggestion ? `<br/><strong>建议:</strong> ${diag.fix_suggestion}` : ''}
          </div>` : ''}`;
        }).join('')}
      </div>
    </div>
  `).join('');

  document.getElementById('noResults').style.display = 'none';
  switchTab('results');
}

// ── History ──
async function loadHistory() {
  const list = document.getElementById('historyList');
  const detail = document.getElementById('historyDetail');
  detail.style.display = 'none';
  list.innerHTML = '<p class="text-muted">加载中...</p>';

  try {
    const reports = await API.get('/api/reports');
    if (reports.length === 0) {
      list.innerHTML = '<p class="text-muted">暂无历史报告</p>';
      return;
    }

    list.innerHTML = reports.map(r => {
      const ptype = r.project_type || 'h5';
      const isMini = ptype === 'miniprogram';
      const tag = isMini ? '<span class="type-tag mp">小程序</span>' : '<span class="type-tag h5">H5</span>';
      const s = r.summary || {};
      const time = r.completed_at || r.created_at || '';
      const dateStr = time ? new Date(time).toLocaleString('zh-CN') : '--';
      return `<div class="history-item" onclick="viewHistoryReport('${r.task_id}')">
        <div class="history-item-header">
          <span>${tag} ${r.project_name || '未知项目'}</span>
          <span class="text-muted">${dateStr}</span>
        </div>
        <div class="history-item-stats">
          <span>总计: ${s.total || 0}</span>
          <span class="text-pass">通过: ${s.passed || 0}</span>
          <span class="text-fail">失败: ${s.failed || 0}</span>
        </div>
      </div>`;
    }).join('');
  } catch (err) {
    list.innerHTML = `<p class="text-muted">加载失败: ${err.message}</p>`;
  }
}

async function viewHistoryReport(taskId) {
  const detail = document.getElementById('historyDetail');
  const title = document.getElementById('historyDetailTitle');
  const body = document.getElementById('historyDetailBody');
  detail.style.display = 'block';
  title.textContent = `报告详情 (${taskId})`;

  try {
    const data = await API.get(`/api/reports/${taskId}`);
    const summary = data.summary || {};
    const diagSummary = data.diagnostic_summary || {};

    let html = `
    <div class="stats-grid">
      <div class="stat-card total"><div class="stat-value">${summary.total || 0}</div><div class="stat-label">总计</div></div>
      <div class="stat-card passed"><div class="stat-value">${summary.passed || 0}</div><div class="stat-label">通过</div></div>
      <div class="stat-card failed"><div class="stat-value">${summary.failed || 0}</div><div class="stat-label">失败</div></div>`;

    // Diagnostic summary
    const cats = diagSummary.categories;
    if (cats && Object.keys(cats).length > 0) {
      html += `<div class="diag-summary">
        <div class="diag-summary-title">失败分类诊断:</div>`;
      for (const [label, count] of Object.entries(cats)) {
        const cls = label.includes('被测对象') ? 'app-bug'
                  : label.includes('工具') ? 'tool-issue'
                  : label.includes('用例') ? 'test-issue' : 'unknown';
        html += `<span class="diag-tag ${cls}">${label}: ${count}</span>`;
      }
      html += `</div>`;
    }
    html += `</div>`;

    const suites = data.suites || [];
    suites.forEach(s => {
      html += `<div class="suite-card">
        <div class="suite-header">
          <span>${s.title || 'Unknown Suite'}</span>
          <span>${(s.tests || []).filter(t => t.status === 'expected' || t.status === 'passed').length}/${(s.tests || []).length}</span>
        </div>
        <div class="suite-body">`;
      (s.tests || []).forEach(t => {
        const isPass = t.status === 'expected' || t.status === 'passed';
        const isFail = t.status === 'unexpected' || t.status === 'failed';
        const diag = t.diagnosis || {};
        const catLabel = diag.category_label || '';
        const catClass = diag.category === 'app_bug' ? 'diag-app-bug'
                       : diag.category === 'tool_issue' ? 'diag-tool-issue'
                       : diag.category === 'test_issue' ? 'diag-test-issue'
                       : '';
        html += `<div class="test-row">
          <span>${t.title || 'Unknown Test'}</span>
          <span class="test-status ${isPass ? 'passed' : isFail ? 'failed' : 'skipped'}">
            ${isPass ? '通过' : isFail ? '失败' : '跳过'}
          </span>
        </div>`;
        if (isFail && diag.root_cause) {
          html += `<div class="test-row" style="font-size:11px;color:var(--warning);flex-direction:column;align-items:start">
            ${catLabel ? `<span class="diag-badge ${catClass}">${catLabel}</span>` : ''}
            <strong>AI 诊断:</strong> ${diag.root_cause || ''}
            ${diag.fix_suggestion ? `<br/><strong>建议:</strong> ${diag.fix_suggestion}` : ''}
          </div>`;
        }
      });
      html += `</div></div>`;
    });

    if (data.plan) {
      html += `<div class="card" style="margin-top:12px">
        <h4>测试计划</h4>
        <pre style="white-space:pre-wrap;font-size:12px;max-height:400px;overflow:auto">${data.plan}</pre>
      </div>`;
    }

    body.innerHTML = html;
  } catch (err) {
    body.innerHTML = `<p class="text-muted">加载失败: ${err.message}</p>`;
  }
}

function switchToHistory() {
  switchTab('history');
  loadHistory();
}

// ── Settings ──
async function loadAIStatus() {
  try {
    const status = await API.get('/api/ai/status');
    document.getElementById('aiProviderLabel').textContent = `${status.provider} (${status.model})`;
    document.getElementById('aiModelLabel').textContent = status.model;
    document.getElementById('aiLabel').textContent = `AI: ${status.provider} / ${status.model}`;
  } catch (err) {
    document.getElementById('aiProviderLabel').textContent = '查询失败';
    document.getElementById('aiLabel').textContent = 'AI: 未连接';
  }
}

async function loadPWVersion() {
  try {
    const data = await API.pwVersion();
    document.getElementById('pwVersion').textContent = data.version || '未安装';
  } catch (err) {
    document.getElementById('pwVersion').textContent = '查询失败';
  }
}

async function updatePlaywright() {
  const version = document.getElementById('pwVersion').textContent;
  const workDir = document.getElementById('pwWorkDir').value || '.';
  if (!confirm(`更新 Playwright${version !== '查询中...' ? ' (当前: ' + version + ')' : ''}？`)) return;

  try {
    const result = await API.updatePlaywright(null, workDir);
    showSaveResult('pwUpdateResult', `已更新到 ${result.version}`);
    loadPWVersion();
  } catch (err) {
    showSaveResult('pwUpdateResult', '更新失败: ' + err.message, true);
  }
}

function showSaveResult(elId, msg, isError = false) {
  const el = document.getElementById(elId);
  el.textContent = msg;
  el.className = 'save-hint ' + (isError ? 'err' : 'ok');
  setTimeout(() => { el.textContent = ''; }, 3000);
}

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
  loadProjects();
  loadAIStatus();
  loadPWVersion();

  // Default init: show H5 config, hide miniprogram config
  selectProjectType('h5');

  const pwWorkDir = document.getElementById('pwWorkDir');
  if (!pwWorkDir.value) {
    pwWorkDir.value = 'D:\\githome\\playwright-agents';
  }
});
