"""Prepare Hugging Face upload artifacts for TokenAtlas."""

import json
import csv
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent.parent

    # 1. Prepare Space
    space_dir = root / "hf_space"
    space_dir.mkdir(parents=True, exist_ok=True)

    docs_html = (root / "docs" / "index.html").read_text(encoding="utf-8")
    docs_json = (root / "docs" / "benchmark_data.json").read_text(encoding="utf-8")

    (space_dir / "index.html").write_text(docs_html, encoding="utf-8")
    (space_dir / "benchmark_data.json").write_text(docs_json, encoding="utf-8")

    space_readme = """---
title: TokenAtlas
emoji: 🌐
colorFrom: blue
colorTo: indigo
sdk: static
pinned: false
license: apache-2.0
---

# TokenAtlas 🌐

The universal multilingual benchmark quantifying the **token inflation tax** across 52 global languages and frontier LLM tokenizers using Meta FLORES-200.

* **GitHub Repository:** [Prajwal7-2002/token-atlas](https://github.com/Prajwal7-2002/token-atlas)
* **Dataset:** [prajwalpujari16/token-atlas-benchmark](https://huggingface.co/datasets/prajwalpujari16/token-atlas-benchmark)
* **Author:** Prajwal Pujari ([@Prajwal7-2002](https://github.com/Prajwal7-2002))
"""
    (space_dir / "README.md").write_text(space_readme, encoding="utf-8")

    # 2. Prepare Dataset
    dataset_dir = root / "hf_dataset"
    dataset_dir.mkdir(parents=True, exist_ok=True)

    with open(root / "benchmarks" / "flores200_benchmark.json", "r", encoding="utf-8") as f:
        bench_data = json.load(f)

    (dataset_dir / "flores200_benchmark.json").write_text(json.dumps(bench_data, indent=2), encoding="utf-8")

    # Flatten to CSV
    rows = []
    for bench in bench_data.get("results", []):
        tid = bench["tokenizer_id"]
        tname = bench["tokenizer_name"]
        vsize = bench["vocab_size"]
        ctx = bench["context_window"]
        for code, m in bench["metrics"].items():
            rows.append({
                "tokenizer_id": tid,
                "tokenizer_name": tname,
                "vocab_size": vsize,
                "context_window": ctx,
                "language_code": m["language_code"],
                "language_name": m["language_name"],
                "family": m["family"],
                "token_count": m["token_count"],
                "char_count": m["char_count"],
                "byte_count": m["byte_count"],
                "bytes_per_token": m["bytes_per_token"],
                "inflation_index_tau": m["inflation_index"],
                "effective_context_weff": m["effective_context"],
                "cost_multiplier_kappa": m["cost_multiplier"],
            })

    if rows:
        fieldnames = list(rows[0].keys())
        with open(dataset_dir / "flores200_benchmark.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    dataset_readme = """---
license: apache-2.0
task_categories:
  - tabular-classification
  - translation
tags:
  - tokenization
  - bpe
  - llm-inference
  - flores-200
  - cost-analysis
  - serving
pretty_name: TokenAtlas Multilingual Tokenizer Benchmark
size_categories:
  - n<1K
language:
  - en
  - de
  - nl
  - sv
  - da
  - no
  - fr
  - es
  - it
  - pt
  - ro
  - ru
  - uk
  - pl
  - cs
  - bg
  - sr
  - hr
  - el
  - fi
  - hu
  - ar
  - he
  - am
  - fa
  - tr
  - az
  - uz
  - kk
  - hi
  - bn
  - mr
  - ur
  - gu
  - pa
  - ne
  - si
  - kn
  - ta
  - te
  - ml
  - zh
  - ja
  - ko
  - vi
  - th
  - id
  - ms
  - tl
  - sw
  - yo
---

# TokenAtlas: Multilingual Tokenizer Benchmark & Inflation Dataset

## Overview
TokenAtlas provides empirical measurements of token inflation, bytes-per-token density, effective context window shrinkage ($W_{\\text{eff}}$), and cost multipliers ($\\kappa$) across **52 global languages** and **6 frontier LLM tokenizers** (`gpt-4o`, `mistral-tekken`, `gemma-2`, `deepseek-v3`, `qwen2.5`, `llama-3.1`, `gpt-4`).

Evaluations are performed against identical parallel sentences extracted and aligned from the **Meta FLORES-200** multilingual evaluation benchmark.

## Quickstart
```python
from datasets import load_dataset
import pandas as pd

dataset = load_dataset("prajwalpujari16/token-atlas-benchmark", data_files="flores200_benchmark.csv")
df = pd.DataFrame(dataset["train"])
print(df.head())
```

## Evaluated Frontier Tokenizers
* **OpenAI GPT-4o** (`o200k_base`, 200k vocab)
* **Mistral Tekken** (131k vocab, `mistralai/Mistral-Nemo-Instruct-2407`)
* **Google Gemma 2** (256k vocab, `google/gemma-2-2b`)
* **DeepSeek-V3** (128k vocab, `deepseek-ai/DeepSeek-V3`)
* **Alibaba Qwen 2.5** (152k vocab, `Qwen/Qwen2.5-7B`)
* **Meta Llama 3.1** (128k vocab, `meta-llama/Llama-3.1-8B`)
* **OpenAI GPT-4** (`cl100k_base`, 100k vocab baseline)

## Key Findings
* **Chinese Super-Compression:** DeepSeek-V3 encodes Chinese at $\\tau = 0.98\\times$ (more compact than English).
* **Arabic Optimization:** Mistral Tekken leads the industry on Arabic at $\\tau = 1.41\\times$.
* **Dravidian Inflation Relief:** GPT-4o ($\\tau = 2.71\\times$) and Mistral Tekken ($\\tau = 2.94\\times$) reduce Kannada sequence lengths by ~78% compared to Llama 3.1 ($\\tau = 12.63\\times$).

## Interactive Web Space
The live interactive atlas and Token Tax & Context Shrinkage Calculator is hosted on Hugging Face Spaces at:
👉 **[prajwalpujari16/token-atlas](https://huggingface.co/spaces/prajwalpujari16/token-atlas)**

## Citation
```bibtex
@software{Pujari_TokenAtlas_2026,
  author = {Pujari, Prajwal},
  title = {{TokenAtlas: Universal Multilingual Tokenizer Benchmark & Global Inflation Atlas}},
  year = {2026},
  url = {https://github.com/Prajwal7-2002/token-atlas},
  license = {Apache-2.0}
}
```
"""
    (dataset_dir / "README.md").write_text(dataset_readme, encoding="utf-8")
    print(f"Artifacts prepared successfully: {space_dir} and {dataset_dir}")


if __name__ == "__main__":
    main()
