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
token-atlas bench --tokenizers gpt-4o,gpt-4 --languages en,de,fr,es,ru,ar,hi,kn,zh,ja --samples 5
```

### 3. List Supported Tokenizers & Language Families
```bash
token-atlas list-tokenizers
token-atlas list-languages
```

---

## 📊 Core Metrics

TokenAtlas rigorously evaluates 4 dimensions on identical parallel sentences:

* **Token Inflation Index ($\tau$):**  
  $$\tau(L, M) = \frac{\text{Tokens in Language } L}{\text{Tokens in English}}$$
* **Bytes Per Token (BPT):** Compression density of information per token ($BPT = \text{Bytes} / \text{Tokens}$).
* **Effective Context Window ($W_{\text{eff}}$):** Real usable context in equivalent English tokens ($W_{\text{eff}} = \text{ContextLimit} / \tau$).
* **Cost Multiplier ($\kappa$):** Financial invoice scaling factor per 1k semantic words.

---

## 🔬 Evaluated Tokenizers

* **Qwen2.5** (152k vocab, multilingual-first byte BPE)
* **Google Gemma 2** (256k vocab, SentencePiece)
* **Meta Llama 3.1** (128k vocab, Tiktoken BPE)
* **Mistral Tekken** (131k vocab, multilingual BPE)
* **OpenAI GPT-4o** (`o200k_base`, Tiktoken BPE)

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
