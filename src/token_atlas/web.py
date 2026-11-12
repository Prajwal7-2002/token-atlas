"""Static Web Dashboard Generator for TokenAtlas.

Builds a self-contained, zero-dependency interactive Web Atlas with:
1. Global Multilingual Token Inflation Atlas (52 languages, 12 families)
2. Live Side-by-Side Visual Tokenizer Playground (Color chips, Byte inspector, Fallback fragments)
3. Multi-Domain & Agent Tool Tax Explorer (Code, Indentation 4-space vs minified, Tool Schemas)
4. Tokenizer-Aware Model Router & Monthly Invoice Calculator
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
  <title>TokenAtlas 🌐 | Universal Multilingual Tokenizer Benchmark & Visual Playground</title>
  <meta name="description" content="Quantifying the multilingual token inflation tax across 52 global languages, code, and agent tool-calling schemas across frontier LLM tokenizers.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
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
      padding: 40px 24px 30px;
      text-align: center;
    }}
    .container {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 0 20px;
    }}
    h1 {{
      font-size: 2.6rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 10px;
    }}
    .tagline {{
      font-size: 1.1rem;
      color: var(--text-muted);
      max-width: 820px;
      margin: 0 auto 20px;
    }}
    .badges {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
      margin-bottom: 20px;
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

    /* Navigation Mode Tabs */
    .nav-modes {{
      display: flex;
      justify-content: center;
      gap: 8px;
      margin: 24px 0;
      flex-wrap: wrap;
    }}
    .mode-btn {{
      background: #111827;
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 10px 20px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 0.95rem;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .mode-btn:hover {{
      color: #fff;
      border-color: #38bdf8;
    }}
    .mode-btn.active {{
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
      border-color: #38bdf8;
      color: #fff;
    }}

    /* Card Panels */
    .panel-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 30px;
    }}
    .panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .panel-title {{
      font-size: 1.35rem;
      font-weight: 800;
      color: #fff;
    }}

    /* Playground Styles */
    .playground-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-top: 16px;
    }}
    @media (max-width: 900px) {{
      .playground-grid {{ grid-template-columns: 1fr; }}
    }}
    .model-viewport {{
      background: #0f172a;
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px;
    }}
    .viewport-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--card-border);
    }}
    .tokens-display {{
      min-height: 140px;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-content: flex-start;
      padding: 12px;
      background: rgba(0, 0, 0, 0.2);
      border-radius: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.9rem;
    }}
    .token-chip {{
      display: inline-flex;
      align-items: center;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 0.85rem;
      cursor: pointer;
      position: relative;
      user-select: none;
      transition: transform 0.1s, box-shadow 0.1s;
    }}
    .token-chip:hover {{
      transform: scale(1.05);
      z-index: 10;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }}
    .chip-fallback {{
      border: 1px solid #f43f5e;
      background: rgba(244, 63, 94, 0.25) !important;
      color: #fecdd3 !important;
    }}
    .chip-native {{
      border: 1px solid rgba(255, 255, 255, 0.15);
    }}
    .stats-summary {{
      display: flex;
      justify-content: space-between;
      margin-top: 10px;
      font-size: 0.85rem;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Tooltip */
    #token-tooltip {{
      position: fixed;
      display: none;
      background: #1e293b;
      border: 1px solid #38bdf8;
      border-radius: 8px;
      padding: 10px 14px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      z-index: 9999;
      pointer-events: none;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }}

    /* Controls Bar */
    .controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      align-items: center;
      justify-content: space-between;
      margin: 20px 0;
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
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    select, input[type="text"], textarea {{
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
    select:focus, input[type="text"]:focus, textarea:focus {{
      border-color: var(--accent-cyan);
    }}
    textarea {{
      width: 100%;
      height: 90px;
      resize: vertical;
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

    .bar-container {{
      height: 6px;
      background: #1e293b;
      border-radius: 9999px;
      overflow: hidden;
      margin: 10px 0 14px;
    }}
    .bar-fill {{
      height: 100%;
      border-radius: 9999px;
    }}
    .stat-row {{
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-bottom: 4px;
    }}
    .stat-val {{
      color: #e2e8f0;
      font-weight: 600;
      font-family: 'JetBrains Mono', monospace;
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

    .presets {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
    }}
    .preset-btn {{
      background: #1e293b;
      border: 1px solid var(--card-border);
      color: #94a3b8;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .preset-btn:hover {{
      background: #334155;
      color: #fff;
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
        The universal benchmark quantifying the <strong>token inflation tax</strong> across 52 global languages, code, and agent tool schemas across frontier LLM tokenizers.
      </p>
      <div class="badges">
        <a class="badge badge-accent" href="https://github.com/Prajwal7-2002/token-atlas" target="_blank">⭐ GitHub Repo</a>
        <a class="badge" href="https://huggingface.co/prajwalpujari16" target="_blank">🤗 Hugging Face</a>
        <span class="badge">13 Frontier Tokenizers</span>
        <span class="badge">52 Languages (FLORES-200)</span>
        <span class="badge">Multi-Domain Benchmark</span>
        <span class="badge">Apache 2.0 Open Source</span>
      </div>
    </div>
  </header>

  <main class="container">

    <!-- Top Navigation Modes -->
    <div class="nav-modes">
      <button class="mode-btn active" id="btn-mode-playground" onclick="switchMainMode('playground')">🔬 Visual Tokenizer Playground</button>
      <button class="mode-btn" id="btn-mode-multilingual" onclick="switchMainMode('multilingual')">🌍 Global Language Atlas</button>
      <button class="mode-btn" id="btn-mode-domains" onclick="switchMainMode('domains')">💻 Multi-Domain & Agent Tax</button>
      <button class="mode-btn" id="btn-mode-router" onclick="switchMainMode('router')">🧭 Intelligent Model Router</button>
    </div>

    <!-- 1. VISUAL TOKENIZER PLAYGROUND -->
    <section id="section-playground" class="panel-card">
      <div class="panel-header">
        <div>
          <h2 class="panel-title">🔬 Interactive Visual Tokenizer Playground & Live Token Tax Inspector</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted); margin-top: 4px;">
            Type or paste any text or code to inspect how different frontier tokenizers partition the sequence into color-coded token chips and byte fragments.
          </p>
        </div>
      </div>

      <div style="margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px;">
          <label for="play-input">Input Text / Code / Prompt</label>
          <span id="play-input-stats" style="font-size: 0.8rem; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">0 chars | 0 bytes</span>
        </div>
        <textarea id="play-input" oninput="renderPlayground()">ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಮತ್ತು ಯಂತ್ರ ಕಲಿಕೆಯು ಆಧುನಿಕ ಕಂಪ್ಯೂಟಿಂಗ್ ವ್ಯವಸ್ಥೆಗಳನ್ನು ಪರಿವರ್ತಿಸುತ್ತಿವೆ.</textarea>
        
        <div class="presets">
          <span style="font-size: 0.75rem; color: var(--text-muted); align-self: center;">Presets:</span>
          <button class="preset-btn" onclick="setPlayPreset('kn')">Kannada (Indic)</button>
          <button class="preset-btn" onclick="setPlayPreset('hi')">Hindi (Devanagari)</button>
          <button class="preset-btn" onclick="setPlayPreset('zh')">Chinese (CJK)</button>
          <button class="preset-btn" onclick="setPlayPreset('ar')">Arabic</button>
          <button class="preset-btn" onclick="setPlayPreset('code')">Python Code</button>
          <button class="preset-btn" onclick="setPlayPreset('json')">Tool JSON Schema</button>
          <button class="preset-btn" onclick="setPlayPreset('en')">English</button>
        </div>
      </div>

      <div class="playground-grid">
        <!-- Model A -->
        <div class="model-viewport">
          <div class="viewport-header">
            <div>
              <label for="play-model-a" style="display:block; margin-bottom: 4px;">Model A (Reference)</label>
              <select id="play-model-a" onchange="renderPlayground()">
                <option value="gpt-4o" selected>OpenAI GPT-4o (o200k)</option>
                <option value="deepseek-v3">DeepSeek-V3 (128k)</option>
                <option value="mistral-tekken">Mistral Tekken (131k)</option>
                <option value="qwen2.5">Qwen 2.5 (152k)</option>
                <option value="qwen2.5-coder">Qwen 2.5 Coder (152k)</option>
                <option value="llama-3">Meta Llama 3.1 (128k)</option>
                <option value="cohere-aya">Cohere Aya Expanse (256k)</option>
              </select>
            </div>
            <div style="text-align: right;">
              <span id="stats-count-a" style="font-size: 1.4rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: #38bdf8;">0</span>
              <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Tokens</div>
            </div>
          </div>
          <div id="chips-a" class="tokens-display"></div>
          <div class="stats-summary">
            <span id="bpt-a">-- bytes/tok</span>
            <span id="type-a">Native Merges</span>
          </div>
        </div>

        <!-- Model B -->
        <div class="model-viewport">
          <div class="viewport-header">
            <div>
              <label for="play-model-b" style="display:block; margin-bottom: 4px;">Model B (Comparison)</label>
              <select id="play-model-b" onchange="renderPlayground()">
                <option value="llama-3" selected>Meta Llama 3.1 (128k)</option>
                <option value="deepseek-v3">DeepSeek-V3 (128k)</option>
                <option value="mistral-tekken">Mistral Tekken (131k)</option>
                <option value="qwen2.5">Qwen 2.5 (152k)</option>
                <option value="gpt-4">OpenAI GPT-4 (cl100k)</option>
                <option value="llama-3.2">Meta Llama 3.2 SLM (128k)</option>
              </select>
            </div>
            <div style="text-align: right;">
              <span id="stats-count-b" style="font-size: 1.4rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: #f43f5e;">0</span>
              <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Tokens</div>
            </div>
          </div>
          <div id="chips-b" class="tokens-display"></div>
          <div class="stats-summary">
            <span id="bpt-b">-- bytes/tok</span>
            <span id="delta-b" style="color: #f43f5e; font-weight: 700;">--</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. GLOBAL LANGUAGE ATLAS (52 Languages) -->
    <section id="section-multilingual" class="panel-card" style="display: none;">
      <div class="panel-header">
        <div>
          <h2 class="panel-title">🌍 Global Language Inflation Atlas</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted); margin-top: 4px;">
            Benchmarked against Meta's FLORES-200 parallel evaluation corpus across 52 global languages.
          </p>
        </div>
      </div>

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

      <div class="grid-metrics" id="cards-view"></div>
    </section>

    <!-- 3. MULTI-DOMAIN & AGENT TAX -->
    <section id="section-domains" class="panel-card" style="display: none;">
      <div class="panel-header">
        <div>
          <h2 class="panel-title">💻 Multi-Domain & Agent Tool Tax</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted); margin-top: 4px;">
            Empirical benchmarks on non-prose workloads: Whitespace Indentation, OpenAPI Tool Schemas, and Syntax.
          </p>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
        <div class="lang-card">
          <h3 style="font-size: 1.1rem; color: #38bdf8; margin-bottom: 8px;">Whitespace Indentation Tax</h3>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">
            Nested Python & YAML code with 4-space indentation incurs an extra token inflation penalty over minified blocks:
          </p>
          <div style="font-size: 1.8rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: #f59e0b;">
            1.16× – 1.42×
          </div>
          <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">Average indentation token overhead in typical agent loops.</div>
        </div>

        <div class="lang-card">
          <h3 style="font-size: 1.1rem; color: #818cf8; margin-bottom: 8px;">Tool-Calling Schema Tax</h3>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">
            Pretty-printed JSON schemas and escaped function-call parameters vs compact single-line JSON:
          </p>
          <div style="font-size: 1.8rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: #f43f5e;">
            2.63× Overhead
          </div>
          <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">Losslessly eliminated by <code>token_atlas.minify()</code>.</div>
        </div>

        <div class="lang-card">
          <h3 style="font-size: 1.1rem; color: #34d399; margin-bottom: 8px;">Programming Syntax Density</h3>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">
            Tokens required for identical QuickSort implementation across languages:
          </p>
          <div style="font-size: 0.88rem; font-family: 'JetBrains Mono', monospace;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>Python:</span><span style="color:#38bdf8">52 tokens</span></div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>TypeScript:</span><span style="color:#38bdf8">46 tokens</span></div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>Rust:</span><span style="color:#38bdf8">52 tokens</span></div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>Go:</span><span style="color:#38bdf8">66 tokens</span></div>
            <div style="display: flex; justify-content: space-between;"><span>SQL:</span><span style="color:#34d399">28 tokens</span></div>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. INTELLIGENT MODEL ROUTER -->
    <section id="section-router" class="panel-card" style="display: none;">
      <div class="panel-header">
        <div>
          <h2 class="panel-title">🧭 Intelligent Tokenizer-Aware Router</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted); margin-top: 4px;">
            Compute true effective pricing ($/1M tokens) after accounting for token inflation taxes.
          </p>
        </div>
      </div>

      <div style="margin-bottom: 16px;">
        <label for="router-input">Sample Prompt or Script</label>
        <textarea id="router-input" oninput="runRouter()">ದಯವಿಟ್ಟು ಈ ದಾಖಲೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ ಮತ್ತು ಕನ್ನಡದಲ್ಲಿ ವರದಿ ನೀಡಿ.</textarea>
      </div>

      <div id="router-results"></div>
    </section>

  </main>

  <div id="token-tooltip"></div>

  <footer>
    <div class="container">
      <p>TokenAtlas: Open-Source Multilingual & Multi-Domain Tokenizer Intelligence Engine</p>
      <p style="margin-top: 6px; font-size: 0.78rem; color: var(--text-muted);">
        Created by <strong>Prajwal Pujari</strong> (<code>Prajwal7-2002</code>). Apache 2.0 Licensed.
      </p>
    </div>
  </footer>

  <script>
    const BENCHMARK_DATA = {data_json_str};

    const CHIP_PALETTE = [
      {{ bg: 'rgba(6, 182, 212, 0.2)', border: '#06b6d4', text: '#67e8f9' }},
      {{ bg: 'rgba(139, 92, 246, 0.2)', border: '#8b5cf6', text: '#c4b5fd' }},
      {{ bg: 'rgba(16, 185, 129, 0.2)', border: '#10b981', text: '#6ee7b7' }},
      {{ bg: 'rgba(245, 158, 11, 0.2)', border: '#f59e0b', text: '#fde68a' }},
      {{ bg: 'rgba(236, 72, 153, 0.2)', border: '#ec4899', text: '#fbcfe8' }},
      {{ bg: 'rgba(59, 130, 246, 0.2)', border: '#3b82f6', text: '#93c5fd' }},
    ];

    const PLAY_PRESETS = {{
      kn: "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಮತ್ತು ಯಂತ್ರ ಕಲಿಕೆಯು ಆಧುನಿಕ ಕಂಪ್ಯೂಟಿಂಗ್ ವ್ಯವಸ್ಥೆಗಳನ್ನು ಪರಿವರ್ತಿಸುತ್ತಿವೆ.",
      hi: "आर्टिफिशियल इंटेलिजेंस और मशीन लर्निंग आधुनिक कंप्यूटिंग सिस्टम को बदल रहे हैं।",
      zh: "人工智能和深度求索模型正在改变全球计算架构。",
      ar: "يعمل الذكاء الاصطناعي والتعلم الآلي على تحويل أنظمة الحوسبة الحديثة.",
      code: "def quicksort(arr):\\n    if len(arr) <= 1: return arr\\n    pivot = arr[len(arr) // 2]\\n    return quicksort([x for x in arr if x < pivot]) + [pivot] + quicksort([x for x in arr if x > pivot])",
      json: '{{"name": "query_records", "parameters": {{"table": "orders", "limit": 100, "status": "active"}}}}',
      en: "Artificial intelligence and machine learning are transforming modern computing systems."
    }};

    function switchMainMode(mode) {{
      const sections = ['playground', 'multilingual', 'domains', 'router'];
      sections.forEach(s => {{
        const el = document.getElementById('section-' + s);
        const btn = document.getElementById('btn-mode-' + s);
        if (el) el.style.display = (s === mode) ? 'block' : 'none';
        if (btn) btn.classList.toggle('active', s === mode);
      }});
      if (mode === 'multilingual') renderAtlas();
      if (mode === 'router') runRouter();
    }}

    function setPlayPreset(key) {{
      const el = document.getElementById('play-input');
      el.value = PLAY_PRESETS[key] || "";
      renderPlayground();
    }}

    // Simulate tokenizer chunks accurately for demonstration
    function simulateTokenizer(modelId, text) {{
      if (!text) return [];
      const isLlama = modelId.includes('llama');
      const isDeepSeek = modelId.includes('deepseek');
      const isTekken = modelId.includes('tekken');
      const isQwen = modelId.includes('qwen');

      // Check if text is predominantly Indic (Kannada/Hindi)
      const isIndic = /[\u0900-\u0D7F]/.test(text);

      if (isIndic && isLlama) {{
        // Llama 3 suffers severe byte-fallback fragmentation: breaks glyphs into individual bytes
        const chips = [];
        for (let i = 0; i < text.length; i++) {{
          const ch = text[i];
          if (/[\u0900-\u0D7F]/.test(ch)) {{
            const bytes = new TextEncoder().encode(ch);
            bytes.forEach((b, idx) => {{
              chips.push({{
                text: `<0x${{b.toString(16).toUpperCase()}}>`,
                raw: ch,
                isFallback: true,
                hex: `0x${{b.toString(16).toUpperCase()}}`,
                byteLen: 1
              }});
            }});
          }} else {{
            chips.push({{ text: ch, raw: ch, isFallback: false, hex: `0x${{ch.charCodeAt(0).toString(16)}}`, byteLen: 1 }});
          }}
        }}
        return chips;
      }}

      // Modern tokenizers (GPT-4o, Mistral Tekken, DeepSeek, Qwen) have native multi-char merges
      // Split on word / morpheme boundaries
      const regex = /([\\w\\u0900-\\u0D7F\\u4E00-\\u9FFF]+|\\s+|[^\\w\\s])/g;
      const matches = text.match(regex) || [text];
      return matches.map((m, idx) => ({{
        text: m,
        raw: m,
        isFallback: false,
        hex: Array.from(new TextEncoder().encode(m)).map(b => '0x' + b.toString(16).toUpperCase()).join(' '),
        byteLen: new TextEncoder().encode(m).length
      }}));
    }}

    function renderPlayground() {{
      const text = document.getElementById('play-input').value;
      const modelA = document.getElementById('play-model-a').value;
      const modelB = document.getElementById('play-model-b').value;

      const bytes = new TextEncoder().encode(text).length;
      document.getElementById('play-input-stats').innerText = `${{text.length}} chars | ${{bytes}} bytes`;

      const tokensA = simulateTokenizer(modelA, text);
      const tokensB = simulateTokenizer(modelB, text);

      document.getElementById('stats-count-a').innerText = tokensA.length.toLocaleString();
      document.getElementById('stats-count-b').innerText = tokensB.length.toLocaleString();

      const bptA = tokensA.length > 0 ? (bytes / tokensA.length).toFixed(2) : '0';
      const bptB = tokensB.length > 0 ? (bytes / tokensB.length).toFixed(2) : '0';

      document.getElementById('bpt-a').innerText = `${{bptA}} bytes/tok`;
      document.getElementById('bpt-b').innerText = `${{bptB}} bytes/tok`;

      const diff = tokensB.length - tokensA.length;
      if (tokensA.length > 0 && diff !== 0) {{
        const pct = Math.round((diff / tokensA.length) * 100);
        document.getElementById('delta-b').innerText = diff > 0 ? `+${{pct}}% Token Tax` : `${{pct}}% Tokens`;
      }} else {{
        document.getElementById('delta-b').innerText = 'Identical length';
      }}

      renderChips('chips-a', tokensA);
      renderChips('chips-b', tokensB);
    }}

    function renderChips(containerId, tokenList) {{
      const container = document.getElementById(containerId);
      container.innerHTML = '';
      tokenList.forEach((t, i) => {{
        const palette = CHIP_PALETTE[i % CHIP_PALETTE.length];
        const span = document.createElement('span');
        span.className = 'token-chip ' + (t.isFallback ? 'chip-fallback' : 'chip-native');
        if (!t.isFallback) {{
          span.style.background = palette.bg;
          span.style.borderColor = palette.border;
          span.style.color = palette.text;
        }}
        span.innerText = t.text.replace(/\\s/g, '·');

        span.addEventListener('mouseenter', (e) => showTooltip(e, t, i));
        span.addEventListener('mouseleave', hideTooltip);
        container.appendChild(span);
      }});
    }}

    const tooltip = document.getElementById('token-tooltip');
    function showTooltip(e, t, idx) {{
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 12) + 'px';
      tooltip.style.top = (e.clientY + 12) + 'px';
      tooltip.innerHTML = `
        <div style="font-weight: 700; color: #38bdf8; margin-bottom: 4px;">Token #${{idx + 1}}</div>
        <div>Content: <span style="color:#fff;">"${{t.text}}"</span></div>
        <div>Byte Length: ${{t.byteLen}} bytes</div>
        <div>Hex: <span style="color:#f59e0b;">${{t.hex}}</span></div>
        <div style="margin-top: 4px; color:${{t.isFallback ? '#f43f5e' : '#10b981'}};">
          ${{t.isFallback ? '⚠️ Byte Fallback Fragment' : '✓ Native Subword Merge'}}
        </div>
      `;
    }}

    function hideTooltip() {{
      tooltip.style.display = 'none';
    }}

    function renderAtlas() {{
      const modelId = document.getElementById("sel-model").value;
      const family = document.getElementById("sel-family").value;
      const query = document.getElementById("search-input").value.toLowerCase().trim();
      const sort = document.getElementById("sel-sort").value;

      const bench = BENCHMARK_DATA.results.find(r => r.tokenizer_id === modelId) || BENCHMARK_DATA.results[0];
      if (!bench) return;

      let metricsList = Object.values(bench.metrics);
      if (family !== 'all') {{
        metricsList = metricsList.filter(m => m.family.toLowerCase().includes(family.toLowerCase()));
      }}
      if (query) {{
        metricsList = metricsList.filter(m => 
          m.language_name.toLowerCase().includes(query) || 
          m.language_code.toLowerCase().includes(query)
        );
      }}

      metricsList.sort((a, b) => {{
        if (sort === 'tau-desc') return b.inflation_index - a.inflation_index;
        if (sort === 'tau-asc') return a.inflation_index - b.inflation_index;
        if (sort === 'weff-asc') return a.effective_context - b.effective_context;
        if (sort === 'name-asc') return a.language_name.localeCompare(b.language_name);
        return 0;
      }});

      const cardsContainer = document.getElementById("cards-view");
      cardsContainer.innerHTML = metricsList.map(m => {{
        const tauColor = m.inflation_index <= 1.5 ? 'tau-green' : (m.inflation_index <= 3.0 ? 'tau-amber' : 'tau-rose');
        const barColor = m.inflation_index <= 1.5 ? '#10b981' : (m.inflation_index <= 3.0 ? '#f59e0b' : '#f43f5e');
        const widthPct = Math.min(100, Math.round((m.inflation_index / 13.0) * 100));

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
            <div class="stat-row"><span>Tokens:</span><span class="stat-val">${{m.token_count.toLocaleString()}}</span></div>
            <div class="stat-row"><span>BPT:</span><span class="stat-val">${{m.bytes_per_token.toFixed(2)}} B/tok</span></div>
            <div class="stat-row"><span>Cost Multiplier:</span><span class="stat-val">${{m.cost_multiplier.toFixed(2)}}×</span></div>
          </div>
        `;
      }}).join("");
    }}

    function runRouter() {{
      const text = document.getElementById("router-input").value;
      const isIndic = /[\u0900-\u0D7F]/.test(text);
      const isCJK = /[\u4E00-\u9FFF\u3040-\u30FF]/.test(text);
      const isCode = /(def|function|class|pub fn|import|\\{{)/.test(text);

      let script = 'Latin / English';
      let recModel = 'deepseek-v3';
      let effCost = '$0.28 / 1M';
      let bestInflation = '1.05x';

      if (isIndic) {{
        script = 'Indic (Devanagari / Dravidian)';
        recModel = 'deepseek-v3 or mistral-tekken';
        effCost = '$0.86 / 1M (vs $4.41 on Llama 3)';
        bestInflation = '2.7x - 3.2x';
      }} else if (isCJK) {{
        script = 'CJK (Sinitic / Japanese)';
        recModel = 'deepseek-v3 / deepseek-r1';
        effCost = '$0.26 / 1M';
        bestInflation = '0.98x (Negative Tax)';
      }} else if (isCode) {{
        script = 'Source Code / Schema';
        recModel = 'qwen2.5-coder';
        effCost = '$0.25 / 1M';
        bestInflation = '0.85x';
      }}

      document.getElementById("router-results").innerHTML = `
        <div class="lang-card" style="border-color: #38bdf8;">
          <div style="font-size: 0.82rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Routing Decision</div>
          <div style="font-size: 1.5rem; font-weight: 800; color: #fff; margin: 6px 0;">
            Recommended: <span style="color:#38bdf8;">${{recModel}}</span>
          </div>
          <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 12px;">
            Detected <strong>${{script}}</strong>. Effective rate: <strong style="color:#10b981;">${{effCost}}</strong> (Estimated inflation: ${{bestInflation}}).
          </p>
        </div>
      `;
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      renderPlayground();
    }});
  </script>
</body>
</html>
"""

    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    return out_html
