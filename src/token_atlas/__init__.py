"""TokenAtlas: Universal Multilingual Tokenizer Benchmark & Global Inflation Atlas."""

__version__ = "0.2.0"
__author__ = "Prajwal Pujari"

from token_atlas.models import (
    TokenizationResult,
    LanguageComparison,
    BenchmarkReport,
    TokenizerSpec,
)
from token_atlas.metrics import (
    calculate_inflation_index,
    calculate_bytes_per_token,
    calculate_effective_context,
    calculate_cost_multiplier,
)
from token_atlas.router import recommend_model, ModelRecommendation
from token_atlas.minify import minify_prompt, MinificationResult
from token_atlas.domains import evaluate_domain, DomainBenchmarkReport

__all__ = [
    "__version__",
    "TokenizationResult",
    "LanguageComparison",
    "BenchmarkReport",
    "TokenizerSpec",
    "calculate_inflation_index",
    "calculate_bytes_per_token",
    "calculate_effective_context",
    "calculate_cost_multiplier",
    "recommend_model",
    "ModelRecommendation",
    "minify_prompt",
    "MinificationResult",
    "evaluate_domain",
    "DomainBenchmarkReport",
]
