# TokenAtlas 🌐

> **Universal Multilingual Tokenizer Benchmark & Global Inflation Atlas**

[![PyPI](https://img.shields.io/pypi/v/token-atlas.svg?color=blue)](https://pypi.org/project/token-atlas/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/Prajwal7-2002/token-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/Prajwal7-2002/token-atlas/actions)

TokenAtlas is an open-source benchmarking engine and diagnostic suite that measures the **token inflation tax** across global languages and frontier LLM tokenizers using Meta's FLORES-200 parallel evaluation corpus.

---

## ⚡ The Problem: The Hidden Token Tax

Large Language Model tokenizers (like BPE, Tiktoken, and WordPiece) are trained predominantly on English datasets. Expressing the **exact same thought** in other languages requires significantly more tokens.

This creates 4 compounding penalties for international users:
1. **Financial Tax:** APIs bill strictly per token. Multilingual conversations cost up to $4\times$ more per 1k words.
2. **Context Shrinkage:** A 128k context window is effectively cut to ~30k words for high-inflation languages.
3. **TTFT Latency Penalty:** Attention prefill latency scales with sequence token length.
4. **VRAM Footprint:** Paged KV-cache memory allocators must reserve more physical blocks per user session.

---

## 🚀 Quickstart

### Installation
```bash
pip install token-atlas
```

### 1. Compare Tokenizers on Single String
```bash
token-atlas compare --text "ここでテキストを分かち書きします" --tokenizers gpt-4o,gpt-4 --language ja
```

### 2. Run Multilingual Parallel Benchmark
```bash
# Benchmark all 28 languages across models
token-atlas bench --tokenizers gpt-4o,gpt-4 --languages all --samples 5

# Benchmark with custom parallel corpus JSON
token-atlas bench --tokenizers deepseek-v3,mistral-tekken --custom-corpus my_corpus.json
```

### 3. Compare Text from File or String
```bash
token-atlas compare --file document.txt --tokenizers gpt-4o,mistral-tekken --language kn
```

### 4. Diagnose UTF-8 Byte Fragmentation
```bash
token-atlas explain-bytes --text "ಕನ್ನಡ"
```

### 5. Export Standalone Interactive Web Atlas
```bash
token-atlas export-web --out-dir docs/
```

### 6. List Supported Tokenizers & Language Families
```bash
token-atlas list-tokenizers
token-atlas list-languages
```

---

## 🌐 Interactive Web Atlas & Live Demo

TokenAtlas exports a zero-dependency, self-contained interactive web application with:
* Real-time sorting and filtering by language family and token inflation index.
* Cross-model head-to-head comparison table.
* **Live Token Tax & Context Shrinkage Calculator** with interactive preset prompts.

Live GitHub Pages Deployment: [prajwal7-2002.github.io/token-atlas](https://prajwal7-2002.github.io/token-atlas/)

---

## 📚 Educational Guide: How Tokenizers Work

For a first-principles breakdown of Byte-Pair Encoding (BPE), UTF-8 byte fallback mechanics, and the vocabulary VRAM scaling equation ($V \times d_{\text{model}}$), see:
👉 [**docs/learn-tokenizers.md**](docs/learn-tokenizers.md)

---

## 📊 Core Metrics

TokenAtlas rigorously evaluates 4 dimensions on identical parallel sentences:

* **Token Inflation Index ($\tau$):**  
  $$\tau(L, M) = \frac{\text{Tokens in Language } L}{\text{Tokens in English}}$$
* **Bytes Per Token (BPT):** Compression density of information per token ($BPT = \text{Bytes} / \text{Tokens}$).
* **Effective Context Window ($W_{\text{eff}}$):** Real usable context in equivalent English tokens ($W_{\text{eff}} = \text{ContextLimit} / \tau$).
* **Cost Multiplier ($\kappa$):** Financial invoice scaling factor per 1k semantic words.

---

## 🔬 Evaluated Frontier Tokenizers

| Tokenizer | Vocab Size | Context Limit | Category | Target Architecture & Focus |
| :--- | :---: | :---: | :---: | :--- |
| **OpenAI GPT-4o** (`o200k_base`) | 200,000 | 128,000 | Multilingual | Frontier Multilingual Tiktoken |
| **Mistral Tekken** | 131,072 | 128,000 | Multilingual | Balanced Multilingual BPE (`Mistral-Nemo-Instruct-2407`) |
| **Cohere Aya Expanse** | 256,000 | 128,000 | Multilingual | 101-Language Global Tokenizer with massive Dravidian/African merges |
| **DeepSeek-R1 & V3** | 128,815 | 128,000 | Reasoning | Sinitic-first Byte BPE ($\tau = 0.98\times$ on Chinese) & Reasoning |
| **Qwen 2.5** | 152,064 | 131,072 | Multilingual | High-capacity Asian & Multilingual Byte BPE |
| **Qwen 2.5 Coder** | 152,064 | 131,072 | Code | Specialized syntax, indentation, and repo path compression |
| **Google Gemma 2** | 256,000 | 8,192 | General | Ultra-large Vocab SentencePiece |
| **Meta Llama 3.1** | 128,256 | 128,000 | General | Latin-first Tiktoken BPE |
| **Meta Llama 3.2** | 128,256 | 128,000 | SLM | Edge-optimized Latin-first BPE |
| **HuggingFace SmolLM2** | 49,152 | 8,192 | SLM | Ultra-compact 49k vocabulary minimizing embedding memory |
| **OpenAI GPT-4** (`cl100k_base`) | 100,277 | 128,000 | General | English-biased Baseline Tiktoken |

---

## 🌍 Supported Language Coverage (52 Languages)

TokenAtlas evaluates 52 global languages across 12 linguistic families aligned to FLORES-200:
* **Germanic & Romance:** English (`en`), German (`de`), Dutch (`nl`), Swedish (`sv`), Danish (`da`), Norwegian (`no`), French (`fr`), Spanish (`es`), Italian (`it`), Portuguese (`pt`), Romanian (`ro`)
* **Slavic:** Russian (`ru`), Ukrainian (`uk`), Polish (`pl`), Czech (`cs`), Bulgarian (`bg`), Serbian (`sr`), Croatian (`hr`)
* **Hellenic & Finno-Ugric:** Greek (`el`), Finnish (`fi`), Hungarian (`hu`)
* **Semitic & Middle Eastern:** Arabic (`ar`), Hebrew (`he`), Amharic (`am`), Persian (`fa`)
* **Turkic:** Turkish (`tr`), Azerbaijani (`az`), Uzbek (`uz`), Kazakh (`kk`)
* **Indic (Indo-Aryan):** Hindi (`hi`), Bengali (`bn`), Marathi (`mr`), Urdu (`ur`), Gujarati (`gu`), Punjabi (`pa`), Nepali (`ne`), Sinhala (`si`)
* **Indic (Dravidian):** Kannada (`kn`), Tamil (`ta`), Telugu (`te`), Malayalam (`ml`)
* **CJK:** Simplified Chinese (`zh`), Traditional Chinese (`zh-tw`), Japanese (`ja`), Korean (`ko`)
* **Southeast Asian & Austronesian:** Vietnamese (`vi`), Thai (`th`), Indonesian (`id`), Malay (`ms`), Filipino (`tl`)
* **African:** Swahili (`sw`), Yoruba (`yo`)

---

## 🛠️ Developer Setup & Testing

```bash
# Clone repository
git clone https://github.com/Prajwal7-2002/token-atlas.git
cd token-atlas

# Run test suite
uv run pytest
```

---

## 📜 Citation

If you use TokenAtlas in your research or benchmarks, please cite:

```bibtex
@software{Pujari_TokenAtlas_2026,
  author = {Pujari, Prajwal},
  title = {{TokenAtlas: Universal Multilingual Tokenizer Benchmark & Global Inflation Atlas}},
  year = {2026},
  url = {https://github.com/Prajwal7-2002/token-atlas},
  license = {Apache-2.0}
}
```

## License

Apache 2.0 © 2026 Prajwal Pujari. See [LICENSE](LICENSE) for details.
