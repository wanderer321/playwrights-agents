/* ── WebSocket Client ── */
class LogWebSocket {
  constructor() {
    this.ws = null;
    this.taskId = null;
  }

  connect(taskId) {
    this.disconnect();
    this.taskId = taskId;
    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
    const url = `${protocol}//${location.host}/ws/logs/${taskId}`;

    this.ws = new WebSocket(url);

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this._handleMessage(data);
      } catch (e) {
        console.warn('WS parse error:', e);
      }
    };

    this.ws.onclose = () => {
      console.log('WS closed');
    };

    this.ws.onerror = (err) => {
      console.error('WS error:', err);
    };
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  _handleMessage(data) {
    switch (data.type) {
      case 'log':
        appendLog(data.message);
        break;
      case 'progress':
        updateProgress(data.progress * 100);
        if (data.status === 'running') {
          setConsoleStatus('运行中...');
        }
        break;
      case 'complete':
        setConsoleStatus(data.status === 'completed' ? '✅ 完成' : data.status === 'stopped' ? '⏹️ 已停止' : '❌ 失败');
        if (data.status === 'stopped') {
          appendLog('[system] 测试已停止\n');
        }
        if (data.result) {
          renderResults(data.result);
        }
        enableTestButton();
        break;
      case 'error':
        appendLog(`[ERROR] ${data.message}`);
        enableTestButton();
        break;
    }
  }
}

const wsClient = new LogWebSocket();
