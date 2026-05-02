/* ── API Client ── */
const API = {
  async get(path) {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`GET ${path} ${res.status}`);
    return res.json();
  },
  async post(path, body) {
    const res = await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`POST ${path} ${res.status}`);
    return res.json();
  },
  async del(path) {
    const res = await fetch(path, { method: 'DELETE' });
    if (!res.ok) throw new Error(`DELETE ${path} ${res.status}`);
    return res.json();
  },

  // ── Projects ──
  listProjects() { return this.get('/api/projects'); },
  addProject(name, projectType, frontendDirs, backendDirs, singleDirs, miniprogramConfig) {
    return this.post('/api/projects', {
      name,
      project_type: projectType,
      frontend_dirs: frontendDirs,
      backend_dirs: backendDirs,
      single_dirs: singleDirs,
      miniprogram_config: miniprogramConfig,
    });
  },
  deleteProject(id) { return this.del(`/api/projects/${id}`); },
  validatePath(path) { return this.post('/api/validate-path', { path }); },

  // ── Test ──
  startTest(projectId, forceRegeneratePlan = false) { return this.post('/api/test/start', { project_id: projectId, force_regenerate_plan: forceRegeneratePlan }); },
  startExpandedTest(projectId, forceRegeneratePlan = false) { return this.post('/api/test/start-expanded', { project_id: projectId, force_regenerate_plan: forceRegeneratePlan }); },
  stopTest(taskId) { return this.post('/api/test/stop', { task_id: taskId }); },
  testStatus(taskId) { return this.get(`/api/test/status/${taskId}`); },
  testReport(taskId) { return this.get(`/api/test/report/${taskId}`); },
  testLogs(taskId) { return this.get(`/api/test/logs/${taskId}`); },
  listTasks() { return this.get('/api/tasks'); },

  // ── Playwright ──
  pwVersion() { return this.get('/api/playwright/version'); },
  updatePlaywright(version, workDir) { return this.post('/api/playwright/update', { version, work_dir: workDir }); },
};
