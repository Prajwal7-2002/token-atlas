"""Benchmarking Engine: Runs cross-lingual evaluations and computes inflation indices."""

import datetime
from token_atlas.models import (
    TokenizationResult,
    LanguageMetric,
    BenchmarkResult,
    BenchmarkReport,
    LanguageComparison,
)
from token_atlas.metrics import (
    calculate_inflation_index,
    calculate_bytes_per_token,
    calculate_effective_context,
    calculate_cost_multiplier,
)
from token_atlas.corpora import get_parallel_corpus, get_language_meta, SUPPORTED_LANGUAGES
from token_atlas.registry import TokenizerRegistry


def compare_single_text(
    text: str,
    tokenizer_ids: list[str],
    language: str = "en",
    registry: TokenizerRegistry | None = None,
) -> LanguageComparison:
    """Compare how multiple tokenizers encode a single text string."""
    reg = registry or TokenizerRegistry()
    meta = get_language_meta(language)
    results: list[TokenizationResult] = []

    for tid in tokenizer_ids:
        res = reg.tokenize(tid, text, language=language)
        results.append(res)

    return LanguageComparison(
        language_code=language,
        language_name=meta.name,
        sample_text=text,
        results=results,
    )


def run_benchmark(
    tokenizer_ids: list[str],
    language_codes: list[str] | None = None,
    sample_limit: int | None = None,
    custom_corpus: list[dict[str, str]] | None = None,
    corpora_source: str | None = None,
    registry: TokenizerRegistry | None = None,
) -> BenchmarkReport:
    """Execute full cross-lingual benchmark across parallel sentences."""
    reg = registry or TokenizerRegistry()
    langs = language_codes or list(SUPPORTED_LANGUAGES.keys())
    
    # Ensure English is always present as baseline
    if "en" not in langs:
        langs.insert(0, "en")

    if custom_corpus is not None:
        corpus = custom_corpus[:sample_limit] if sample_limit is not None else custom_corpus
        source_name = corpora_source or "Custom User-Provided Corpus"
    else:
        corpus = get_parallel_corpus(limit=sample_limit)
        source_name = corpora_source or "Meta FLORES-200 Parallel Corpus (Curated Subset)"

    benchmark_results: list[BenchmarkResult] = []

    for tid in tokenizer_ids:
        spec = reg.get_spec(tid)
        lang_totals: dict[str, dict[str, int]] = {
            code: {"tokens": 0, "chars": 0, "bytes": 0} for code in langs
        }

        # Accumulate metrics across all parallel sentences
        for sentence_pair in corpus:
            for code in langs:
                if code in sentence_pair:
                    text = sentence_pair[code]
                    res = reg.tokenize(tid, text, language=code)
                    lang_totals[code]["tokens"] += res.token_count
                    lang_totals[code]["chars"] += res.char_count
                    lang_totals[code]["bytes"] += res.byte_count

        en_tokens = lang_totals.get("en", {}).get("tokens", 1)
        metrics: dict[str, LanguageMetric] = {}

        for code in langs:
            meta = get_language_meta(code)
            tokens = lang_totals[code]["tokens"]
            chars = lang_totals[code]["chars"]
            bytes_cnt = lang_totals[code]["bytes"]

            bpt = calculate_bytes_per_token(bytes_cnt, tokens)
            tau = calculate_inflation_index(tokens, en_tokens)
            w_eff = calculate_effective_context(spec.context_window, tau)
            kappa = calculate_cost_multiplier(tau)

            metrics[code] = LanguageMetric(
                language_code=code,
                language_name=meta.name,
                family=meta.family,
                token_count=tokens,
                char_count=chars,
                byte_count=bytes_cnt,
                bytes_per_token=bpt,
                inflation_index=tau,
                effective_context=w_eff,
                cost_multiplier=kappa,
            )

        benchmark_results.append(
            BenchmarkResult(
                tokenizer_id=tid,
                tokenizer_name=spec.name,
                vocab_size=spec.vocab_size,
                context_window=spec.context_window,
                sample_count=len(corpus),
                metrics=metrics,
            )
        )

    return BenchmarkReport(
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        corpora_source=source_name,
        tokenizers=tokenizer_ids,
        languages=langs,
        results=benchmark_results,
    )
