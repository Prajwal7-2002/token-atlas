"""Static Web Dashboard Generator for TokenAtlas.

Builds a self-contained, zero-dependency interactive Web Atlas suitable for
instant deployment to GitHub Pages or Hugging Face Spaces.
"""

import json
from pathlib import Path


def generate_web_dashboard(benchmark_data: dict, out_dir: Path) -> Path:
    """Generate standalone interactive HTML dashboard."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_html = out_dir / "index.html"
    out_json = out_dir / "benchmark_data.json"

    # Save raw json alongside
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2)

    data_json_str = json.dumps(benchmark_data)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TokenAtlas 🌐 | Universal Multilingual Tokenizer Benchmark</title>
  <meta name="description" content="Quantifying the multilingual token inflation tax across 52 global languages and frontier LLM tokenizers using Meta FLORES-200.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0b0f19;
      --card-bg: #111827;
      --card-border: #1f293d;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --accent-cyan: #06b6d4;
      --accent-violet: #8b5cf6;
      --accent-green: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background: var(--bg);
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.5;
      padding-bottom: 60px;
    }}
    header {{
      background: linear-gradient(180deg, #161e31 0%, var(--bg) 100%);
      border-bottom: 1px solid var(--card-border);
      padding: 48px 24px 36px;
      text-align: center;
    }}
    .container {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 0 20px;
    }}
    h1 {{
      font-size: 2.75rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 12px;
    }}
    .tagline {{
      font-size: 1.15rem;
      color: var(--text-muted);
      max-width: 760px;
      margin: 0 auto 24px;
    }}
    .badges {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
      margin-bottom: 24px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      padding: 5px 12px;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      color: #e2e8f0;
      text-decoration: none;
    }}
    .badge:hover {{
      background: rgba(255, 255, 255, 0.1);
      border-color: var(--accent-cyan);
    }}
    .badge-accent {{
      border-color: rgba(6, 182, 212, 0.4);
      background: rgba(6, 182, 212, 0.1);
      color: #38bdf8;
    }}

    /* Controls Bar */
    .controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      align-items: center;
      justify-content: space-between;
      margin: 36px 0 24px;
      padding: 16px 20px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
    }}
    .filter-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
    }}
    label {{
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    select, input[type="text"] {{
      background: #0f172a;
      border: 1px solid var(--card-border);
      color: #fff;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-family: inherit;
      outline: none;
      transition: border-color 0.15s;
    }}
    select:focus, input[type="text"]:focus {{
      border-color: var(--accent-cyan);
    }}

    /* Tabs */
    .tabs {{
      display: flex;
      gap: 8px;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 12px;
    }}
    .tab-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 8px 16px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      border-radius: 8px;
      transition: all 0.15s;
    }}
    .tab-btn.active {{
      background: rgba(6, 182, 212, 0.15);
      color: #38bdf8;
    }}

    /* Grid & Cards */
    .grid-metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
      margin-bottom: 40px;
    }}
    .lang-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px;
      transition: transform 0.15s, border-color 0.15s;
    }}
    .lang-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(56, 189, 248, 0.4);
    }}
    .lang-header {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 10px;
    }}
    .lang-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #fff;
    }}
    .lang-meta {{
      font-size: 0.75rem;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }}
    .tau-badge {{
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.25rem;
      font-weight: 700;
      padding: 2px 0;
    }}
    .tau-green {{ color: var(--accent-green); }}
    .tau-amber {{ color: var(--accent-amber); }}
    .tau-rose {{ color: var(--accent-rose); }}

    .stat-row {{
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      margin-top: 6px;
      color: var(--text-muted);
    }}
    .stat-val {{
      font-weight: 600;
      color: #e2e8f0;
      font-family: 'JetBrains Mono', monospace;
    }}
    .bar-container {{
      width: 100%;
      height: 6px;
      background: #1e293b;
      border-radius: 999px;
      margin-top: 12px;
      overflow: hidden;
    }}
    .bar-fill {{
      height: 100%;
      border-radius: 999px;
      transition: width 0.3s ease;
    }}

    /* Calculator Section */
    .calculator-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 28px;
      margin-bottom: 40px;
    }}
    .calc-grid {{
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 28px;
    }}
    @media (max-width: 860px) {{
      .calc-grid {{
        grid-template-columns: 1fr;
      }}
    }}
    textarea {{
      width: 100%;
      height: 130px;
      background: #0f172a;
      border: 1px solid var(--card-border);
      color: #fff;
      padding: 12px;
      border-radius: 8px;
      font-size: 0.95rem;
      font-family: inherit;
      resize: vertical;
      outline: none;
    }}
    textarea:focus {{
      border-color: var(--accent-cyan);
    }}
    .presets {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }}
    .preset-btn {{
      background: #1e293b;
      border: 1px solid var(--card-border);
      color: #94a3b8;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .preset-btn:hover {{
      background: #334155;
      color: #fff;
    }}
    .calc-results {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}
    .result-tile {{
      background: #0f172a;
      border: 1px solid var(--card-border);
      padding: 14px;
      border-radius: 10px;
    }}
    .result-title {{
      font-size: 0.75rem;
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 4px;
    }}
    .result-number {{
      font-size: 1.5rem;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: #38bdf8;
    }}
    .result-sub {{
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    /* Table View */
    .table-container {{
      overflow-x: auto;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      margin-bottom: 40px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
      text-align: left;
    }}
    th, td {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--card-border);
    }}
    th {{
      background: #0f172a;
      font-weight: 700;
      color: #94a3b8;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.05em;
    }}
    tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
    }}
    .font-mono {{
      font-family: 'JetBrains Mono', monospace;
    }}

    footer {{
      border-top: 1px solid var(--card-border);
      padding: 32px 24px;
      text-align: center;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>

  <header>
    <div class="container">
      <h1>TokenAtlas 🌐</h1>
      <p class="tagline">
        The universal multilingual benchmark quantifying the <strong>token inflation tax</strong> across 52 global languages and frontier LLM tokenizers using Meta's FLORES-200.
      </p>
      <div class="badges">
        <a class="badge badge-accent" href="https://github.com/Prajwal7-2002/token-atlas" target="_blank">⭐ GitHub Repo</a>
        <a class="badge" href="https://huggingface.co/prajwalpujari16" target="_blank">🤗 Hugging Face</a>
        <span class="badge">52 Languages Evaluated</span>
        <span class="badge">6 Frontier Tokenizers</span>
        <span class="badge">Apache 2.0 Open Source</span>
      </div>
    </div>
  </header>

  <main class="container">

    <!-- Interactive Calculator -->
    <div class="calculator-card">
      <h2 style="font-size: 1.3rem; margin-bottom: 14px; font-weight: 800;">⚡ Live Token Tax & Context Shrinkage Calculator</h2>
      <div class="calc-grid">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px;">
            <label for="calc-text">Input Text</label>
            <span id="char-count" style="font-size: 0.78rem; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">0 chars | 0 bytes</span>
          </div>
          <textarea id="calc-text" placeholder="Type or paste text in any language...">ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಮತ್ತು ಯಂತ್ರ ಕಲಿಕೆಯು ಆಧುನಿಕ ಕಂಪ್ಯೂಟಿಂಗ್ ವ್ಯವಸ್ಥೆಗಳನ್ನು ಪರಿವರ್ತಿಸುತ್ತಿವೆ.</textarea>
          
          <div class="presets">
            <span style="font-size: 0.75rem; color: var(--text-muted); align-self: center;">Samples:</span>
            <button class="preset-btn" onclick="setPreset('kn')">Kannada</button>
            <button class="preset-btn" onclick="setPreset('hi')">Hindi</button>
            <button class="preset-btn" onclick="setPreset('ar')">Arabic</button>
            <button class="preset-btn" onclick="setPreset('zh')">Chinese</button>
            <button class="preset-btn" onclick="setPreset('ja')">Japanese</button>
            <button class="preset-btn" onclick="setPreset('ru')">Russian</button>
            <button class="preset-btn" onclick="setPreset('de')">German</button>
            <button class="preset-btn" onclick="setPreset('en')">English</button>
          </div>
        </div>

        <div>
          <div style="display: flex; gap: 12px; margin-bottom: 16px;">
            <div style="flex: 1;">
              <label for="calc-model" style="display: block; margin-bottom: 6px;">Select Model</label>
              <select id="calc-model" style="width: 100%;" onchange="runCalculator()">
                <option value="gpt-4o">OpenAI GPT-4o (o200k)</option>
                <option value="mistral-tekken">Mistral Tekken (131k)</option>
                <option value="gemma-2">Google Gemma 2 (256k)</option>
                <option value="deepseek-v3">DeepSeek-V3 (128k)</option>
                <option value="qwen2.5">Qwen 2.5 (152k)</option>
                <option value="llama-3">Meta Llama 3.1 (128k)</option>
                <option value="gpt-4">OpenAI GPT-4 (cl100k)</option>
              </select>
            </div>
            <div style="flex: 1;">
              <label for="calc-context-limit" style="display: block; margin-bottom: 6px;">Nominal Context</label>
              <select id="calc-context-limit" style="width: 100%;" onchange="runCalculator()">
                <option value="128000">128k Tokens</option>
                <option value="64000">64k Tokens</option>
                <option value="32000">32k Tokens</option>
                <option value="8192">8k Tokens</option>
              </select>
            </div>
          </div>

          <div class="calc-results">
            <div class="result-tile">
              <div class="result-title">Estimated Tokens</div>
              <div class="result-number" id="res-tokens">--</div>
              <div class="result-sub" id="res-bpt">-- bytes/tok</div>
            </div>
            <div class="result-tile">
              <div class="result-title">Inflation Index (τ)</div>
              <div class="result-number" id="res-tau">--</div>
              <div class="result-sub" id="res-tau-sub">vs English</div>
            </div>
            <div class="result-tile">
              <div class="result-title">Effective Context</div>
              <div class="result-number" id="res-weff">--</div>
              <div class="result-sub" id="res-weff-loss">-- usable words</div>
            </div>
            <div class="result-tile">
              <div class="result-title">Financial Multiplier</div>
              <div class="result-number" id="res-cost">--</div>
              <div class="result-sub">invoice tax factor</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Controls -->
    <div class="controls">
      <div class="filter-group">
        <div>
          <label for="sel-model" style="margin-right: 8px;">Model:</label>
          <select id="sel-model" onchange="renderAtlas()">
            <option value="gpt-4o">OpenAI GPT-4o (o200k)</option>
            <option value="mistral-tekken">Mistral Tekken (131k)</option>
            <option value="gemma-2">Google Gemma 2 (256k)</option>
            <option value="deepseek-v3">DeepSeek-V3 (128k)</option>
            <option value="qwen2.5">Qwen 2.5 (152k)</option>
            <option value="llama-3">Meta Llama 3.1 (128k)</option>
            <option value="gpt-4">OpenAI GPT-4 (cl100k)</option>
          </select>
        </div>

        <div>
          <label for="sel-family" style="margin-right: 8px;">Family:</label>
          <select id="sel-family" onchange="renderAtlas()">
            <option value="all">All Language Families (52)</option>
            <option value="Dravidian">Dravidian (Kannada, Tamil, Telugu, Malayalam)</option>
            <option value="Indo-Aryan">Indo-Aryan (Hindi, Bengali, Marathi, Urdu, etc.)</option>
            <option value="Semitic">Semitic (Arabic, Hebrew, Amharic)</option>
            <option value="Slavic">Slavic (Russian, Ukrainian, Polish, etc.)</option>
            <option value="Germanic">Germanic (English, German, Dutch, Nordic)</option>
            <option value="Romance">Romance (French, Spanish, Portuguese, Italian)</option>
            <option value="Sinitic">Sinitic / CJK (Chinese, Japanese, Korean)</option>
            <option value="Turkic">Turkic (Turkish, Azerbaijani, Kazakh, Uzbek)</option>
            <option value="Austronesian">Austronesian (Indonesian, Malay, Filipino)</option>
          </select>
        </div>
      </div>

      <div class="filter-group">
        <input type="text" id="search-input" placeholder="Search language or code..." oninput="renderAtlas()">
        <div>
          <label for="sel-sort" style="margin-right: 8px;">Sort:</label>
          <select id="sel-sort" onchange="renderAtlas()">
            <option value="tau-desc">Inflation (τ) High → Low</option>
            <option value="tau-asc">Inflation (τ) Low → High</option>
            <option value="weff-asc">Usable Context Low → High</option>
            <option value="name-asc">Language Name A → Z</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Tabs View Selector -->
    <div class="tabs">
      <button class="tab-btn active" id="tab-cards-btn" onclick="switchTab('cards')">Grid Cards View</button>
      <button class="tab-btn" id="tab-table-btn" onclick="switchTab('table')">Full Comparison Table</button>
    </div>

    <!-- Grid View -->
    <div id="cards-view" class="grid-metrics"></div>

    <!-- Table View -->
    <div id="table-view" class="table-container" style="display: none;">
      <table>
        <thead>
          <tr>
            <th>Language</th>
            <th>Code</th>
            <th>Family</th>
            <th>Tokens</th>
            <th>Inflation (τ)</th>
            <th>Effective Context (Weff)</th>
            <th>Cost Multiplier (κ)</th>
            <th>Bytes / Token</th>
          </tr>
        </thead>
        <tbody id="table-body"></tbody>
      </table>
    </div>

  </main>

  <footer>
    <div class="container">
      <p>TokenAtlas: Open-Source Multilingual Inference Benchmark by <strong>Prajwal Pujari</strong> (<code>Prajwal7-2002</code>)</p>
      <p style="margin-top: 6px; font-size: 0.78rem;">Evaluated on identical parallel sentences from Meta FLORES-200. Licensed under Apache 2.0.</p>
    </div>
  </footer>

  <script>
    const BENCHMARK_DATA = {data_json_str};

    const PRESETS = {{
      kn: "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಮತ್ತು ಯಂತ್ರ ಕಲಿಕೆಯು ಆಧುನಿಕ ಕಂಪ್ಯೂಟಿಂಗ್ ವ್ಯವಸ್ಥೆಗಳನ್ನು ಪರಿವರ್ತಿಸುತ್ತಿವೆ.",
      hi: "आर्टिफिशियल इंटेलिजेंस और मशीन लर्निंग आधुनिक कंप्यूटिंग सिस्टम और हार्डवेयर आर्किटेक्चर को बदल रहे हैं।",
      ar: "يعمل الذكاء الاصطناعي والتعلم الآلي على تحويل أنظمة الحوسبة الحديثة وبنية الأجهزة.",
      zh: "人工智能和机器学习正在改变现代计算系统和硬件架构。",
      ja: "人工知能と機械学習は、現代の計算システムとハードウェアアーキテクチャを変革しています。",
      ru: "Искусственный интеллект и машинное обучение трансформируют современные вычислительные системы.",
      de: "Künstliche Intelligenz und maschinelles Lernen verändern moderne Rechensysteme.",
      en: "Artificial intelligence and machine learning are transforming modern computing systems and hardware architecture."
    }};

    function setPreset(lang) {{
      const el = document.getElementById("calc-text");
      el.value = PRESETS[lang] || "";
      runCalculator();
    }}

    function getSelectedBenchmark(modelId) {{
      if (!BENCHMARK_DATA || !BENCHMARK_DATA.results) return null;
      return BENCHMARK_DATA.results.find(r => r.tokenizer_id === modelId) || BENCHMARK_DATA.results[0];
    }}

    function switchTab(view) {{
      const cardsView = document.getElementById("cards-view");
      const tableView = document.getElementById("table-view");
      const cardsBtn = document.getElementById("tab-cards-btn");
      const tableBtn = document.getElementById("tab-table-btn");

      if (view === 'cards') {{
        cardsView.style.display = 'grid';
        tableView.style.display = 'none';
        cardsBtn.classList.add('active');
        tableBtn.classList.remove('active');
      }} else {{
        cardsView.style.display = 'none';
        tableView.style.display = 'block';
        tableBtn.classList.add('active');
        cardsBtn.classList.remove('active');
      }}
    }}

    function renderAtlas() {{
      const modelId = document.getElementById("sel-model").value;
      const family = document.getElementById("sel-family").value;
      const query = document.getElementById("search-input").value.toLowerCase().trim();
      const sort = document.getElementById("sel-sort").value;

      const bench = getSelectedBenchmark(modelId);
      if (!bench) return;

      let metricsList = Object.values(bench.metrics);

      // Filtering
      if (family !== 'all') {{
        metricsList = metricsList.filter(m => m.family.toLowerCase().includes(family.toLowerCase()));
      }}
      if (query) {{
        metricsList = metricsList.filter(m => 
          m.language_name.toLowerCase().includes(query) || 
          m.language_code.toLowerCase().includes(query)
        );
      }}

      // Sorting
      metricsList.sort((a, b) => {{
        if (sort === 'tau-desc') return b.inflation_index - a.inflation_index;
        if (sort === 'tau-asc') return a.inflation_index - b.inflation_index;
        if (sort === 'weff-asc') return a.effective_context - b.effective_context;
        if (sort === 'name-asc') return a.language_name.localeCompare(b.language_name);
        return 0;
      }});

      // Render Cards
      const cardsContainer = document.getElementById("cards-view");
      cardsContainer.innerHTML = metricsList.map(m => {{
        const tauColor = m.inflation_index <= 1.5 ? 'tau-green' : (m.inflation_index <= 3.0 ? 'tau-amber' : 'tau-rose');
        const barColor = m.inflation_index <= 1.5 ? '#10b981' : (m.inflation_index <= 3.0 ? '#f59e0b' : '#f43f5e');
        const maxTau = 13.0;
        const widthPct = Math.min(100, Math.round((m.inflation_index / maxTau) * 100));

        return `
          <div class="lang-card">
            <div class="lang-header">
              <span class="lang-title">${{m.language_name}}</span>
              <span class="lang-meta">[${{m.language_code}}] ${{m.family}}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <span class="tau-badge ${{tauColor}}">${{m.inflation_index.toFixed(2)}}×</span>
              <span style="font-size: 0.78rem; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">
                ${{m.effective_context.toLocaleString()}} usable tok
              </span>
            </div>
            <div class="bar-container">
              <div class="bar-fill" style="width: ${{widthPct}}%; background: ${{barColor}};"></div>
            </div>
            <div class="stat-row">
              <span>Sample Tokens:</span>
              <span class="stat-val">${{m.token_count.toLocaleString()}}</span>
            </div>
            <div class="stat-row">
              <span>Compression (BPT):</span>
              <span class="stat-val">${{m.bytes_per_token.toFixed(2)}} B/tok</span>
            </div>
            <div class="stat-row">
              <span>Cost Multiplier:</span>
              <span class="stat-val">${{m.cost_multiplier.toFixed(2)}}×</span>
            </div>
          </div>
        `;
      }}).join("");

      // Render Table
      const tableBody = document.getElementById("table-body");
      tableBody.innerHTML = metricsList.map(m => {{
        const tauColor = m.inflation_index <= 1.5 ? 'tau-green' : (m.inflation_index <= 3.0 ? 'tau-amber' : 'tau-rose');
        return `
          <tr>
            <td style="font-weight: 700;">${{m.language_name}}</td>
            <td><code class="font-mono">${{m.language_code}}</code></td>
            <td style="color: var(--text-muted);">${{m.family}}</td>
            <td class="font-mono">${{m.token_count.toLocaleString()}}</td>
            <td class="font-mono ${{tauColor}}" style="font-weight: 700;">${{m.inflation_index.toFixed(2)}}×</td>
            <td class="font-mono" style="color: #38bdf8;">${{m.effective_context.toLocaleString()}}</td>
            <td class="font-mono" style="color: #c084fc;">${{m.cost_multiplier.toFixed(2)}}×</td>
            <td class="font-mono" style="color: var(--text-muted);">${{m.bytes_per_token.toFixed(2)}}</td>
          </tr>
        `;
      }}).join("");
    }}

    function runCalculator() {{
      const text = document.getElementById("calc-text").value;
      const modelId = document.getElementById("calc-model").value;
      const contextLimit = parseInt(document.getElementById("calc-context-limit").value, 10);

      const byteCount = new TextEncoder().encode(text).length;
      const charCount = text.length;
      document.getElementById("char-count").innerText = `${{charCount}} chars | ${{byteCount}} bytes`;

      if (byteCount === 0) {{
        document.getElementById("res-tokens").innerText = "0";
        document.getElementById("res-tau").innerText = "1.00×";
        document.getElementById("res-weff").innerText = contextLimit.toLocaleString();
        document.getElementById("res-cost").innerText = "1.00×";
        return;
      }}

      // Detect language heuristic from benchmark dataset or script
      const bench = getSelectedBenchmark(modelId);
      if (!bench) return;

      // Estimate BPT based on character script
      let matchedLangCode = 'en';
      if (/[\u0C80-\u0CFF]/.test(text)) matchedLangCode = 'kn';
      else if (/[\u0900-\u097F]/.test(text)) matchedLangCode = 'hi';
      else if (/[\u0600-\u06FF]/.test(text)) matchedLangCode = 'ar';
      else if (/[\u4E00-\u9FFF]/.test(text)) matchedLangCode = 'zh';
      else if (/[\u3040-\u30FF]/.test(text)) matchedLangCode = 'ja';
      else if (/[\u0400-\u04FF]/.test(text)) matchedLangCode = 'ru';
      else if (/[äöüßÄÖÜ]/.test(text)) matchedLangCode = 'de';

      const metric = bench.metrics[matchedLangCode] || bench.metrics['en'];
      const bpt = metric.bytes_per_token || 4.0;
      const tau = metric.inflation_index || 1.0;

      const estimatedTokens = Math.max(1, Math.round(byteCount / bpt));
      const effectiveContext = Math.max(1, Math.round(contextLimit / tau));
      const contextLossPct = Math.round((1 - (effectiveContext / contextLimit)) * 100);

      document.getElementById("res-tokens").innerText = estimatedTokens.toLocaleString();
      document.getElementById("res-bpt").innerText = `${{bpt.toFixed(2)}} bytes/tok`;
      document.getElementById("res-tau").innerText = `${{tau.toFixed(2)}}×`;
      document.getElementById("res-tau-sub").innerText = `vs English baseline`;
      document.getElementById("res-weff").innerText = effectiveContext.toLocaleString();
      document.getElementById("res-weff-loss").innerText = `-${{contextLossPct}}% usable window`;
      document.getElementById("res-cost").innerText = `${{tau.toFixed(2)}}×`;
    }}

    // Initial load
    window.addEventListener("DOMContentLoaded", () => {{
      renderAtlas();
      runCalculator();
    }});
  </script>
</body>
</html>
"""

    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    return out_html

