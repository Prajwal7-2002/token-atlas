# Development Log: TokenAtlas

## 2026-11-08: v0.2.0 Interactive Web Atlas & 52-Language Expansion
- **52 Global Languages:** Expanded evaluation corpus to 52 languages across 12 families (Germanic, Romance, Slavic, Hellenic, Finno-Ugric, Semitic, Iranian, Turkic, Indo-Aryan, Dravidian, Sinitic/CJK, Austroasiatic, Austronesian, Niger-Congo, Bantu).
- **Interactive Web Atlas (`docs/index.html`):**
  - Built zero-dependency responsive dark-themed dashboard.
  - Interactive filtering by linguistic family and token inflation index ($\tau$).
  - Client-side Live Token Tax & Context Shrinkage Calculator with real-time heuristic token estimation and progress bar context reduction visualization.
  - Added CLI command: `token-atlas export-web --out-dir docs/`.
- **First-Principles Educational Engine:**
  - Implemented `token_atlas.bpe`: Pure-Python 30-line BPE learner from raw UTF-8 bytes to demonstrate merge table dynamics.
  - Added CLI command `token-atlas explain-bytes --text "..."` to diagnose UTF-8 byte fragmentation.
  - Authored comprehensive systems guide: `docs/learn-tokenizers.md` detailing the UTF-8 byte fallback mechanism and the $V \times d_{\text{model}}$ embedding VRAM scaling trade-off.
- **Test Suite:** 24/24 unit tests passing in 0.73s.

## 2026-11-08: v0.1.5 Multilingual Corpus Expansion & Frontier Tokenizers
- **Expanded Corpus Coverage:** Expanded from 10 to **28 global languages** across 12 language families and scripts (Germanic, Romance, Slavic Cyrillic/Latin, Semitic RTL, Iranian, Turkic, Indo-Aryan, Dravidian, CJK, Austroasiatic, Austronesian, Kra-Dai, Bantu).
- **Frontier Tokenizers Added:**
  - `deepseek-v3`: DeepSeek-V3 byte-level BPE (128,815 vocab).
  - `mistral-tekken`: Mistral Tekken BPE (131,072 vocab) via `mistralai/Mistral-Nemo-Instruct-2407`.
- **CLI Enhancements:**
  - Added `--file` / `-f` to `compare` command for benchmarking arbitrary local text files.
  - Added `--custom-corpus` to `bench` command for custom domain parallel corpora.
  - Added `languages="all"` support in `bench` to benchmark all 28 languages in one shot.
- **Empirical Breakthrough Findings:**
  - **Chinese Compression:** DeepSeek-V3 encodes Chinese at $\tau = 0.98\times$ (83 tokens vs 85 English tokens), making Chinese more compact than English!
  - **Arabic Parity:** Mistral Tekken achieves $\tau = 1.41\times$ on Arabic (123 tokens), outperforming GPT-4o ($\tau = 1.67\times$) and GPT-4 ($\tau = 3.98\times$).
  - **Dravidian Inflation Relief:** On Kannada (`kn`), Mistral Tekken ($\tau = 2.94\times$) and GPT-4o ($\tau = 2.71\times$) compress text by ~77–79% compared to GPT-4 ($\tau = 12.63\times$).
- **Test Suite:** Expanded to 20 unit tests, passing in 0.79s.

## 2026-11-08: v0.1.0 Initial Scaffolding & Core Architecture
- Initialized repository with Apache 2.0 license and CITATION.cff attribution.
- Elevated from `token-tax` study to universal `token-atlas` flagship per Portfolio Roadmap v3.
- Designed 4 core measurement axes:
  1. Token Inflation Index ($\tau$) relative to English semantic ground truth.
  2. Bytes Per Token (BPT) density.
  3. Effective Context Window ($W_{\text{eff}}$) shrinkage.
  4. Financial Cost Multipliers ($\kappa$) across global language families.
- Adopted Meta FLORES-200 parallel corpus for balanced, cherry-pick-free evaluation.
