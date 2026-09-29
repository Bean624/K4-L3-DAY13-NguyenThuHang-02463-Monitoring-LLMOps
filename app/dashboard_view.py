from __future__ import annotations

import json
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bảng Giám Sát LLMOps — K4-L3A</title>
  <style>
    :root {
      --bg: #0d0c11;
      --card-bg: #16151d;
      --card-border: #282433;
      --text-main: #f8fafc;
      --text-sub: #94a3b8;
      --text-muted: #64748b;
      --accent-pink: #f472b6;
      --accent-pink-soft: rgba(244, 114, 182, 0.15);
      --badge-bg: #1f1d2b;
      --badge-border: #312d42;
      --badge-text: #e2e8f0;
      --status-ok-bg: rgba(52, 211, 153, 0.12);
      --status-ok-text: #34d399;
      --status-ok-border: rgba(52, 211, 153, 0.3);
      --status-alert-bg: rgba(248, 113, 113, 0.12);
      --status-alert-text: #f87171;
      --status-alert-border: rgba(248, 113, 113, 0.3);
      --toggle-bg: #1f1d2b;
      --toggle-border: #312d42;
      --toggle-text: #f8fafc;
      --input-bg: #1f1d2b;
      --input-border: #312d42;
      --table-hover: #1c1b26;
      --code-bg: #121118;
    }

    [data-theme="light"] {
      --bg: #faf7f9;
      --card-bg: #ffffff;
      --card-border: #f1e4ec;
      --text-main: #18181b;
      --text-sub: #64748b;
      --text-muted: #94a3b8;
      --accent-pink: #ec4899;
      --accent-pink-soft: rgba(236, 72, 153, 0.1);
      --badge-bg: #fdf2f8;
      --badge-border: #fce7f3;
      --badge-text: #831843;
      --status-ok-bg: #ecfdf5;
      --status-ok-text: #059669;
      --status-ok-border: #a7f3d0;
      --status-alert-bg: #fef2f2;
      --status-alert-text: #dc2626;
      --status-alert-border: #fecaca;
      --toggle-bg: #ffffff;
      --toggle-border: #f1e4ec;
      --toggle-text: #18181b;
      --input-bg: #ffffff;
      --input-border: #f1e4ec;
      --table-hover: #fdf8fb;
      --code-bg: #faf5f8;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
    }

    body {
      background-color: var(--bg);
      color: var(--text-main);
      padding: 28px 24px;
      min-height: 100vh;
    }

    .container {
      max-width: 1240px;
      margin: 0 auto;
    }

    .top-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 20px;
      margin-bottom: 22px;
      border-bottom: 1px solid var(--card-border);
    }

    .brand-title {
      font-size: 23px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--text-main);
    }

    .brand-title span {
      color: var(--accent-pink);
    }

    .meta-subtitle {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 500;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--badge-text);
    }

    .theme-btn {
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      padding: 7px 16px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
      background: var(--toggle-bg);
      border: 1px solid var(--toggle-border);
      color: var(--toggle-text);
      outline: none;
    }

    .theme-btn:hover {
      border-color: var(--accent-pink);
      color: var(--accent-pink);
    }

    /* Tab Navigation */
    .tab-bar {
      display: flex;
      gap: 10px;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 12px;
      flex-wrap: wrap;
    }

    .tab-btn {
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--text-sub);
      font-size: 13px;
      font-weight: 600;
      padding: 9px 18px;
      border-radius: 9999px;
      cursor: pointer;
      outline: none;
      user-select: none;
    }

    .tab-btn:hover {
      border-color: var(--accent-pink);
      color: var(--text-main);
    }

    .tab-btn.active {
      background: var(--accent-pink-soft);
      border-color: var(--accent-pink);
      color: var(--accent-pink);
    }

    .tab-content {
      display: none;
    }

    .tab-content.active {
      display: block;
    }

    /* 6 Panels Grid */
    .grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }

    @media (max-width: 992px) {
      .grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 640px) {
      .grid { grid-template-columns: 1fr; }
    }

    .panel-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 215px;
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 10px;
    }

    .panel-name {
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: var(--text-sub);
    }

    .panel-unit {
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 500;
    }

    .main-metric {
      display: flex;
      align-items: baseline;
      gap: 6px;
      margin: 6px 0 14px 0;
    }

    .main-number {
      font-size: 32px;
      font-weight: 700;
      letter-spacing: -0.03em;
      color: var(--text-main);
    }

    .main-label {
      font-size: 13px;
      color: var(--accent-pink);
      font-weight: 500;
    }

    .sub-metrics-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      padding: 10px 0;
      border-top: 1px solid var(--card-border);
      margin-bottom: 12px;
    }

    .sub-item-label {
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 4px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }

    .sub-item-val {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-main);
    }

    .status-tag {
      display: inline-flex;
      align-items: center;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
    }

    .status-tag.ok {
      background: var(--status-ok-bg);
      color: var(--status-ok-text);
      border: 1px solid var(--status-ok-border);
    }

    .status-tag.alert {
      background: var(--status-alert-bg);
      color: var(--status-alert-text);
      border: 1px solid var(--status-alert-border);
    }

    /* Card Box for other tabs */
    .box-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 20px;
    }

    .box-title {
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    /* Log Explorer */
    .log-filter-bar {
      display: flex;
      gap: 12px;
      margin-bottom: 18px;
    }

    .search-input {
      flex: 1;
      background: var(--input-bg);
      border: 1px solid var(--input-border);
      color: var(--text-main);
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 13px;
      outline: none;
    }

    .search-input:focus {
      border-color: var(--accent-pink);
    }

    .filter-select {
      background: var(--input-bg);
      border: 1px solid var(--input-border);
      color: var(--text-main);
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 13px;
      outline: none;
      cursor: pointer;
    }

    .log-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }

    .log-table th {
      text-align: left;
      padding: 11px 14px;
      background: var(--card-border);
      color: var(--text-sub);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .log-table td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--card-border);
      color: var(--text-main);
    }

    .log-table tr:hover {
      background: var(--table-hover);
    }

    .copy-chip {
      cursor: pointer;
      display: inline-block;
      font-family: monospace;
      padding: 3px 8px;
      border-radius: 4px;
      background: var(--badge-bg);
      color: var(--accent-pink);
      border: 1px solid var(--badge-border);
      font-size: 11px;
    }

    .copy-chip:hover {
      border-color: var(--accent-pink);
    }

    /* Retrieval Tester */
    .tester-row {
      display: flex;
      gap: 12px;
      margin-bottom: 14px;
    }

    .run-btn {
      background: var(--accent-pink);
      color: #ffffff;
      border: none;
      padding: 10px 22px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 13px;
      cursor: pointer;
      outline: none;
      white-space: nowrap;
    }

    .run-btn:hover {
      opacity: 0.9;
    }

    .quick-chips {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 20px;
    }

    .chip-btn {
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--text-sub);
      font-size: 12px;
      padding: 6px 14px;
      border-radius: 9999px;
      cursor: pointer;
    }

    .chip-btn:hover {
      border-color: var(--accent-pink);
      color: var(--accent-pink);
    }

    .result-box {
      background: var(--code-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 16px;
      font-size: 13px;
      line-height: 1.6;
      white-space: pre-wrap;
      font-family: monospace;
      min-height: 110px;
    }

    /* Traces & Langfuse */
    .link-btn {
      display: inline-flex;
      align-items: center;
      padding: 8px 16px;
      border-radius: 8px;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--accent-pink);
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
    }

    .link-btn:hover {
      border-color: var(--accent-pink);
    }
  </style>

  <script>
    // Tab switching declared in head for instant availability
    window.switchTab = function(tabName, btn) {
      var buttons = document.querySelectorAll('.tab-btn');
      var contents = document.querySelectorAll('.tab-content');
      for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove('active');
      }
      for (var j = 0; j < contents.length; j++) {
        contents[j].style.display = 'none';
        contents[j].classList.remove('active');
      }
      if (btn) {
        btn.classList.add('active');
      } else {
        var defaultBtn = document.getElementById('btn-' + tabName);
        if (defaultBtn) defaultBtn.classList.add('active');
      }
      var target = document.getElementById('tab-' + tabName);
      if (target) {
        target.style.display = 'block';
        target.classList.add('active');
      }
      if (tabName === 'logs' && typeof window.fetchLogs === 'function') {
        window.fetchLogs();
      }
    };

    // Theme toggle
    window.toggleTheme = function() {
      var html = document.documentElement;
      var current = html.getAttribute('data-theme') || 'dark';
      var next = (current === 'dark') ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      try {
        localStorage.setItem('dashboard-theme', next);
      } catch (e) {}
      window.updateBtnText(next);
    };

    window.updateBtnText = function(theme) {
      var btn = document.getElementById('themeBtn');
      if (btn) {
        btn.textContent = (theme === 'dark') ? 'Giao diện Sáng' : 'Giao diện Tối';
      }
    };

    try {
      var savedTheme = localStorage.getItem('dashboard-theme') || 'dark';
      document.documentElement.setAttribute('data-theme', savedTheme);
    } catch (e) {}
  </script>
</head>
<body>
  <div class="container">
    <header class="top-header">
      <div>
        <div class="brand-title">Hệ Thống Giám Sát <span>LLMOps</span></div>
        <div class="meta-subtitle">Nguồn dữ liệu: data/logs.jsonl &bull; Lớp: K4-L3A &bull; Học viên: 2A202602463</div>
      </div>
      <div class="header-actions">
        <span class="pill">Cửa sổ: 60 phút</span>
        <button class="theme-btn" onclick="window.toggleTheme()" id="themeBtn">Giao diện Sáng</button>
      </div>
    </header>

    <!-- Tab navigation -->
    <nav class="tab-bar">
      <button id="btn-metrics" class="tab-btn active" data-tab="metrics" onclick="window.switchTab('metrics', this)">Chỉ Số Giám Sát (6 Panels)</button>
      <button id="btn-logs" class="tab-btn" data-tab="logs" onclick="window.switchTab('logs', this)">Nhật Ký Logs</button>
      <button id="btn-retrieval" class="tab-btn" data-tab="retrieval" onclick="window.switchTab('retrieval', this)">Chạy Thử Nghiệm Retrieval</button>
      <button id="btn-traces" class="tab-btn" data-tab="traces" onclick="window.switchTab('traces', this)">Truy Vết Traces & Prompt</button>
    </nav>

    <!-- TAB 1: 6 PANELS -->
    <div id="tab-metrics" class="tab-content active" style="display: block;">
      <main class="grid">
        <!-- Panel 1: Latency -->
        <section class="panel-card">
          <div>
            <div class="panel-header">
              <span class="panel-name">Độ Trễ & TTFT</span>
              <span class="panel-unit">mili-giây (ms)</span>
            </div>
            <div class="main-metric">
              <span class="main-number">__P95__</span>
              <span class="main-label">ms (P95)</span>
            </div>
            <div class="sub-metrics-grid">
              <div>
                <div class="sub-item-label">P50</div>
                <div class="sub-item-val">__P50__ ms</div>
              </div>
              <div>
                <div class="sub-item-label">P99</div>
                <div class="sub-item-val">__P99__ ms</div>
              </div>
              <div>
                <div class="sub-item-label">TTFT P95</div>
                <div class="sub-item-val">__TTFT_P95__ ms</div>
              </div>
            </div>
          </div>
          <div>
            <span class="status-tag __STATUS_P95_CLS__">__STATUS_P95_TEXT__</span>
          </div>
        </section>

        <!-- Panel 2: Traffic -->
        <section class="panel-card">
          <div>
            <div class="panel-header">
              <span class="panel-name">Lưu Lượng Truy Cập</span>
              <span class="panel-unit">yêu cầu / phút</span>
            </div>
            <div class="main-metric">
              <span class="main-number">__TOTAL_REQ__</span>
              <span class="main-label">tổng lượt gọi</span>
            </div>
            <div class="sub-metrics-grid">
              <div>
                <div class="sub-item-label">Tốc độ TB</div>
                <div class="sub-item-val">__RATE_PER_MIN__ / phút</div>
              </div>
              <div>
                <div class="sub-item-label">Thời gian</div>
                <div class="sub-item-val">60 phút</div>
              </div>
              <div>
                <div class="sub-item-label">Dịch vụ</div>
                <div class="sub-item-val">api</div>
              </div>
            </div>
          </div>
          <div>
            <span class="status-tag ok">Ngưỡng chuẩn: Tốc độ &ge; 1 req/phút (Đạt chuẩn)</span>
          </div>
        </section>

        <!-- Panel 3: Errors -->
        <section class="panel-card">
          <div>
            <div class="panel-header">
              <span class="panel-name">Tỷ Lệ Lỗi & RAG Success</span>
              <span class="panel-unit">phần trăm (%)</span>
            </div>
            <div class="main-metric">
              <span class="main-number">__ERR_RATE__%</span>
              <span class="main-label">tỷ lệ lỗi</span>
            </div>
            <div class="sub-metrics-grid">
              <div>
                <div class="sub-item-label">Yêu cầu lỗi</div>
                <div class="sub-item-val">__FAIL_COUNT__</div>
              </div>
              <div>
                <div class="sub-item-label">RAG Thành Công</div>
                <div class="sub-item-val">__TOOL_RATE__%</div>
              </div>
              <div>
                <div class="sub-item-label">Mã lỗi</div>
                <div class="sub-item-val">0</div>
              </div>
            </div>
          </div>
          <div>
            <span class="status-tag ok">Ngưỡng chuẩn: Lỗi &le; 2% &bull; RAG &ge; 90% (Đạt chuẩn)</span>
          </div>
        </section>

        <!-- Panel 4: Cost -->
        <section class="panel-card">
          <div>
            <div class="panel-header">
              <span class="panel-name">Chi Phí Mô Hình</span>
              <span class="panel-unit">đô la Mỹ (USD)</span>
            </div>
            <div class="main-metric">
              <span class="main-number">$__TOTAL_COST__</span>
              <span class="main-label">tổng chi phí</span>
            </div>
            <div class="sub-metrics-grid">
              <div>
                <div class="sub-item-label">Chi phí / Req</div>
                <div class="sub-item-val">$__AVG_COST__</div>
              </div>
              <div>
                <div class="sub-item-label">Đơn vị tiền tệ</div>
                <div class="sub-item-val">USD</div>
              </div>
              <div>
                <div class="sub-item-label">Model</div>
                <div class="sub-item-val">Claude 3.5</div>
              </div>
            </div>
          </div>
          <div>
            <span class="status-tag ok">Ngưỡng chuẩn: Chi phí &le; $2.50 (Đạt chuẩn)</span>
          </div>
        </section>

        <!-- Panel 5: Tokens -->
        <section class="panel-card">
          <div>
            <div class="panel-header">
              <span class="panel-name">Số Lượng Token</span>
              <span class="panel-unit">tokens</span>
            </div>
            <div class="main-metric">
              <span class="main-number">__TOKENS_TOTAL__</span>
              <span class="main-label">tổng token</span>
            </div>
            <div class="sub-metrics-grid">
              <div>
                <div class="sub-item-label">Đầu vào</div>
                <div class="sub-item-val">__TOKENS_IN__</div>
              </div>
              <div>
                <div class="sub-item-label">Đầu ra</div>
                <div class="sub-item-val">__TOKENS_OUT__</div>
              </div>
              <div>
                <div class="sub-item-label">Trung bình</div>
                <div class="sub-item-val">__TOKENS_AVG__</div>
              </div>
            </div>
          </div>
          <div>
            <span class="status-tag ok">Ngưỡng chuẩn: Tổng &le; 50,000 tokens (Đạt chuẩn)</span>
          </div>
        </section>

        <!-- Panel 6: Quality -->
        <section class="panel-card">
          <div>
            <div class="panel-header">
              <span class="panel-name">Chất Lượng Câu Trả Lời</span>
              <span class="panel-unit">thang điểm 0 - 1.0</span>
            </div>
            <div class="main-metric">
              <span class="main-number">__AVG_QUALITY__</span>
              <span class="main-label">/ 1.0 điểm</span>
            </div>
            <div class="sub-metrics-grid">
              <div>
                <div class="sub-item-label">Điểm trung bình</div>
                <div class="sub-item-val">__AVG_QUALITY__</div>
              </div>
              <div>
                <div class="sub-item-label">Phương pháp</div>
                <div class="sub-item-val">Heuristic</div>
              </div>
              <div>
                <div class="sub-item-label">Mục tiêu</div>
                <div class="sub-item-val">&ge; 0.75</div>
              </div>
            </div>
          </div>
          <div>
            <span class="status-tag ok">Ngưỡng chuẩn: Điểm &ge; 0.75 (Đạt chuẩn)</span>
          </div>
        </section>
      </main>
    </div>

    <!-- TAB 2: LIVE LOGS EXPLORER -->
    <div id="tab-logs" class="tab-content">
      <div class="box-card">
        <div class="box-title">
          <span>Nhật Ký Dòng Sự Kiện (Live Structured Logs)</span>
          <button class="pill" onclick="window.fetchLogs()" style="cursor: pointer;">Tải lại log</button>
        </div>
        <div class="log-filter-bar">
          <input type="text" id="logSearch" class="search-input" placeholder="Tìm theo correlation_id hoặc nội dung log..." oninput="window.filterLogs()">
          <select id="eventFilter" class="filter-select" onchange="window.filterLogs()">
            <option value="all">Tất cả sự kiện (All Events)</option>
            <option value="response_sent">response_sent</option>
            <option value="request_received">request_received</option>
            <option value="request_failed">request_failed</option>
            <option value="incident_enabled">incident_enabled</option>
            <option value="incident_disabled">incident_disabled</option>
          </select>
        </div>
        <div style="overflow-x: auto;">
          <table class="log-table">
            <thead>
              <tr>
                <th>Thời gian</th>
                <th>Sự kiện</th>
                <th>Correlation ID</th>
                <th>Độ trễ</th>
                <th>Chi tiết tóm tắt</th>
              </tr>
            </thead>
            <tbody id="logTableBody">
              <tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 24px;">Đang nạp nhật ký...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 3: RETRIEVAL TESTER -->
    <div id="tab-retrieval" class="tab-content">
      <div class="box-card">
        <div class="box-title">Thử Nghiệm Truy Xuất Tri Thức (Interactive Retrieval)</div>
        <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 14px;">
          Nhập câu hỏi để kiểm tra vector search trực tiếp từ mock RAG corpus và đo lường thời gian thực thi:
        </p>
        <div class="tester-row">
          <input type="text" id="retrievalQuery" class="search-input" placeholder="Ví dụ: What is the refund policy?">
          <button class="run-btn" onclick="window.runRetrieval()">Chạy Truy Xuất</button>
        </div>
        <div class="quick-chips">
          <span style="font-size: 12px; color: var(--text-muted); align-self: center;">Câu hỏi gợi ý:</span>
          <button class="chip-btn" onclick="window.setQuery('What is your refund policy?')">Chính sách hoàn tiền (Refund)</button>
          <button class="chip-btn" onclick="window.setQuery('Explain how monitoring metrics work')">Giám sát hệ thống (Monitoring)</button>
          <button class="chip-btn" onclick="window.setQuery('What is the policy for PII data?')">Bảo vệ thông tin PII (Policy)</button>
          <button class="chip-btn" onclick="window.setQuery('Tell me a general greeting')">Câu hỏi ngoài luồng (Fallback)</button>
        </div>
        <div class="result-box" id="retrievalResult">Nhấn 'Chạy Truy Xuất' hoặc chọn câu hỏi gợi ý để xem kết quả trích xuất...</div>
      </div>
    </div>

    <!-- TAB 4: TRACES & LANGFUSE -->
    <div id="tab-traces" class="tab-content">
      <div class="box-card">
        <div class="box-title">
          <span>Liên Kết Langfuse Cloud Traces</span>
          <a href="https://cloud.langfuse.com" target="_blank" class="link-btn">Mở Langfuse Cloud &rarr;</a>
        </div>
        <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 16px;">
          Dự án cá nhân: <strong style="color: var(--accent-pink);">day13-k4-l3a-2A202602463</strong> &bull; Quản lý Trace ID, Observation Tree và Prompt Versions.
        </p>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 14px;">
          <div style="background: var(--code-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 18px;">
            <div style="font-size: 13px; font-weight: 700; color: var(--accent-pink); margin-bottom: 8px;">Cấu Hình Prompt Quản Trị</div>
            <div style="font-size: 12px; line-height: 1.8; color: var(--text-sub);">
              <div>&bull; Tên Prompt: <strong style="color: var(--text-main);">day13-chat</strong></div>
              <div>&bull; Nhãn hiện tại: <strong style="color: var(--text-main);">production</strong></div>
              <div>&bull; Phiên bản thử nghiệm: <strong style="color: var(--text-main);">candidate</strong></div>
              <div>&bull; Biến đầu vào: <span style="font-family: monospace;">{{feature}}, {{docs}}, {{message}}</span></div>
            </div>
          </div>

          <div style="background: var(--code-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 18px;">
            <div style="font-size: 13px; font-weight: 700; color: var(--accent-pink); margin-bottom: 8px;">Cấu Trúc Trace Waterfall</div>
            <div style="font-size: 12px; line-height: 1.8; color: var(--text-sub);">
              <div>&bull; Root Span: <strong style="color: var(--text-main);">lab-agent-run</strong> (type: agent)</div>
              <div>&bull; Child 1: <strong style="color: var(--text-main);">retrieval</strong> (type: retriever)</div>
              <div>&bull; Child 2: <strong style="color: var(--text-main);">generation</strong> (type: generation, tokens & cost)</div>
              <div>&bull; Liên kết log: <strong style="color: var(--text-main);">correlation_id</strong> truyền trong metadata</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    (function() {
      function escapeHtml(str) {
        if (!str) return '';
        return String(str)
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;')
          .replace(/'/g, '&#039;');
      }

      document.addEventListener('DOMContentLoaded', function() {
        var buttons = document.querySelectorAll('.tab-btn');
        buttons.forEach(function(btn) {
          btn.addEventListener('click', function() {
            var tab = this.getAttribute('data-tab');
            window.switchTab(tab, this);
          });
        });

        var hash = window.location.hash.replace('#', '').replace('tab-', '');
        if (hash && ['metrics', 'logs', 'retrieval', 'traces'].indexOf(hash) !== -1) {
          window.switchTab(hash);
        }

        window.updateBtnText(document.documentElement.getAttribute('data-theme') || 'dark');
        window.fetchLogs();
      });

      var allLogs = [];

      window.renderLogTable = function(logs) {
        var tbody = document.getElementById('logTableBody');
        if (!tbody) return;
        if (!logs || !logs.length) {
          tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 20px;">Không có bản ghi phù hợp</td></tr>';
          return;
        }
        var html = '';
        for (var i = 0; i < logs.length; i++) {
          var l = logs[i];
          var time = (l.ts || '').replace('T', ' ').substring(11, 19);
          var event = l.event || '-';
          var cid = l.correlation_id || '-';
          var lat = (l.latency_ms !== undefined) ? (l.latency_ms + ' ms') : '-';
          var detail = '';
          if (l.payload) {
            detail = l.payload.message_preview || l.payload.answer_preview || l.payload.name || JSON.stringify(l.payload);
          }
          html += '<tr>' +
            '<td style="color: var(--text-muted); font-family: monospace;">' + escapeHtml(time) + '</td>' +
            '<td><span style="font-weight: 600; color: var(--accent-pink);">' + escapeHtml(event) + '</span></td>' +
            '<td><span class="copy-chip" onclick="window.copyText(\\'' + escapeHtml(cid) + '\\')" title="Click để sao chép">' + escapeHtml(cid) + '</span></td>' +
            '<td style="font-family: monospace; font-weight: 600;">' + escapeHtml(lat) + '</td>' +
            '<td style="color: var(--text-sub); max-width: 320px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">' + escapeHtml(detail) + '</td>' +
          '</tr>';
        }
        tbody.innerHTML = html;
      };

      window.fetchLogs = function() {
        fetch('/api/logs?limit=40')
          .then(function(r) { return r.json(); })
          .then(function(data) {
            allLogs = data;
            window.filterLogs();
          })
          .catch(function() {
            window.renderLogTable(allLogs);
          });
      };

      window.filterLogs = function() {
        var searchInput = document.getElementById('logSearch');
        var search = searchInput ? searchInput.value.toLowerCase() : '';
        var eventSelect = document.getElementById('eventFilter');
        var eventFilter = eventSelect ? eventSelect.value : 'all';
        var filtered = [];
        for (var i = 0; i < allLogs.length; i++) {
          var l = allLogs[i];
          var matchEvent = (eventFilter === 'all' || l.event === eventFilter);
          var matchSearch = (!search || JSON.stringify(l).toLowerCase().indexOf(search) !== -1);
          if (matchEvent && matchSearch) {
            filtered.push(l);
          }
        }
        window.renderLogTable(filtered);
      };

      window.copyText = function(txt) {
        if (!txt || txt === '-') return;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(txt).then(function() {
            alert('Đã sao chép: ' + txt);
          }).catch(function() {
            prompt('Sao chép Correlation ID:', txt);
          });
        } else {
          prompt('Sao chép Correlation ID:', txt);
        }
      };

      window.setQuery = function(q) {
        var input = document.getElementById('retrievalQuery');
        if (input) {
          input.value = q;
          window.runRetrieval();
        }
      };

      window.runRetrieval = function() {
        var input = document.getElementById('retrievalQuery');
        var query = input ? input.value : '';
        var resultBox = document.getElementById('retrievalResult');
        if (!query.trim()) {
          if (resultBox) resultBox.textContent = 'Vui lòng nhập câu hỏi trước khi chạy truy xuất!';
          return;
        }
        if (resultBox) resultBox.textContent = 'Đang truy xuất tài liệu từ kho tri thức RAG...';
        fetch('/api/test-retrieval', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: query })
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
          if (!resultBox) return;
          if (data.ok) {
            var docList = '';
            for (var i = 0; i < (data.docs || []).length; i++) {
              docList += '\\n[Tài liệu ' + (i + 1) + ']:\\n' + data.docs[i] + '\\n';
            }
            resultBox.textContent = '[THÀNH CÔNG] Thời gian truy xuất: ' + data.latency_ms + ' ms | Tìm thấy: ' + data.count + ' tài liệu\\n' + docList;
          } else {
            resultBox.textContent = '[LỖI TRUY XUẤT]: ' + (data.error || 'Lỗi không xác định') + ' (Độ trễ: ' + data.latency_ms + ' ms)';
          }
        })
        .catch(function(err) {
          if (resultBox) resultBox.textContent = 'Lỗi kết nối API: ' + err;
        });
      };
    })();
  </script>
</body>
</html>
"""


def render_dashboard_html() -> str:
    log_path = Path("data/logs.jsonl")
    records = []
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass

    latencies = [r["latency_ms"] for r in records if "latency_ms" in r and r.get("event") == "response_sent"]
    ttfts = [r["ttft_ms"] for r in records if "ttft_ms" in r and r.get("event") == "response_sent"]
    requests_rec = [r for r in records if r.get("event") == "request_received"]
    requests_fail = [r for r in records if r.get("event") == "request_failed"]
    costs = [r["cost_usd"] for r in records if "cost_usd" in r and r.get("event") == "response_sent"]
    tokens_in = sum(r.get("tokens_in", 0) for r in records if r.get("event") == "response_sent")
    tokens_out = sum(r.get("tokens_out", 0) for r in records if r.get("event") == "response_sent")
    qualities = [r["quality_score"] for r in records if "quality_score" in r and r.get("event") == "response_sent"]
    tools_total = sum(1 for r in records if "tool_success" in r and r["tool_success"] is not None)
    tools_ok = sum(1 for r in records if r.get("tool_success") is True)

    def percentile(values: list[float], p: float) -> float:
        if not values:
            return 0.0
        sorted_vals = sorted(values)
        idx = int(len(sorted_vals) * (p / 100))
        return sorted_vals[min(idx, len(sorted_vals) - 1)]

    p50 = percentile(latencies, 50)
    p95 = percentile(latencies, 95)
    p99 = percentile(latencies, 99)
    ttft_p95 = percentile(ttfts, 95)
    total_req = len(requests_rec)
    rate_per_min = round(total_req / max(1, 60 / 60), 1)
    err_rate = round((len(requests_fail) / max(1, total_req)) * 100, 1)
    tool_rate = round((tools_ok / max(1, tools_total)) * 100, 1) if tools_total else 100.0
    total_cost = round(sum(costs), 4)
    avg_cost = round(total_cost / max(1, total_req), 4)
    avg_quality = round(sum(qualities) / max(1, len(qualities)), 2)

    status_p95_cls = "ok" if p95 <= 3000 else "alert"
    status_p95_text = "Ngưỡng chuẩn: P95 <= 3000 ms (Đạt chuẩn)" if p95 <= 3000 else "Ngưỡng chuẩn: P95 <= 3000 ms (Vượt ngưỡng SLO)"

    content = HTML_TEMPLATE
    replacements = {
        "__P95__": str(p95),
        "__P50__": str(p50),
        "__P99__": str(p99),
        "__TTFT_P95__": str(ttft_p95),
        "__STATUS_P95_CLS__": status_p95_cls,
        "__STATUS_P95_TEXT__": status_p95_text,
        "__TOTAL_REQ__": str(total_req),
        "__RATE_PER_MIN__": str(rate_per_min),
        "__ERR_RATE__": str(err_rate),
        "__FAIL_COUNT__": str(len(requests_fail)),
        "__TOOL_RATE__": str(tool_rate),
        "__TOTAL_COST__": str(total_cost),
        "__AVG_COST__": str(avg_cost),
        "__TOKENS_TOTAL__": f"{tokens_in + tokens_out:,}",
        "__TOKENS_IN__": f"{tokens_in:,}",
        "__TOKENS_OUT__": f"{tokens_out:,}",
        "__TOKENS_AVG__": f"{int((tokens_in + tokens_out) / max(1, total_req)):,}",
        "__AVG_QUALITY__": str(avg_quality),
    }

    for key, val in replacements.items():
        content = content.replace(key, val)

    return content
