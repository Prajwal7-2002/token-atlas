"""Tokenizer-Aware Model & Architecture Router.

Analyzes input text scripts, syntax structure, and empirical token inflation
indices to recommend the most token-efficient and cost-effective model.
"""

import re
from typing import Literal, Optional
from pydantic import BaseModel, Field

from token_atlas.registry import TokenizerRegistry


# Baseline Provider Pricing (USD per 1M Input Tokens, 2025/2026 rates)
PROVIDER_PRICING: dict[str, float] = {
    "deepseek-v3": 0.27,
    "deepseek-r1": 0.55,
    "qwen2.5": 0.30,
    "qwen2.5-coder": 0.30,
    "llama-3.2": 0.15,
    "llama-3": 0.35,
    "mistral-tekken": 0.40,
    "cohere-aya": 0.50,
    "gpt-4o": 2.50,
    "gpt-4": 10.00,
    "gemma-2": 0.20,
    "smollm2": 0.10,
    "mock": 0.00,
}

# Empirical script-to-inflation multiplier lookup
SCRIPT_INFLATION_ESTIMATES: dict[str, dict[str, float]] = {
    "cjk": {
        "deepseek-v3": 0.98,
        "deepseek-r1": 0.98,
        "qwen2.5": 1.05,
        "gpt-4o": 1.35,
        "mistral-tekken": 1.45,
        "llama-3": 1.95,
        "llama-3.2": 1.95,
        "mock": 1.00,
    },
    "indic": {
        "gpt-4o": 2.65,
        "mistral-tekken": 2.70,
        "cohere-aya": 2.55,
        "deepseek-v3": 3.20,
        "deepseek-r1": 3.20,
        "qwen2.5": 3.40,
        "llama-3": 12.60,
        "llama-3.2": 12.60,
        "mock": 1.00,
    },
    "arabic": {
        "gpt-4o": 1.40,
        "mistral-tekken": 1.50,
        "qwen2.5": 1.55,
        "deepseek-v3": 1.65,
        "deepseek-r1": 1.65,
        "llama-3": 2.80,
        "llama-3.2": 2.80,
        "mock": 1.00,
    },
    "cyrillic": {
        "mistral-tekken": 1.30,
        "gpt-4o": 1.40,
        "qwen2.5": 1.45,
        "deepseek-v3": 1.45,
        "deepseek-r1": 1.45,
        "llama-3": 1.70,
        "llama-3.2": 1.70,
        "mock": 1.00,
    },
    "code": {
        "qwen2.5-coder": 0.85,
        "deepseek-v3": 0.90,
        "deepseek-r1": 0.90,
        "mistral-tekken": 0.95,
        "gpt-4o": 1.00,
        "llama-3": 1.10,
        "llama-3.2": 1.10,
        "mock": 1.00,
    },
    "latin": {
        "gpt-4o": 1.00,
        "llama-3": 1.00,
        "llama-3.2": 1.00,
        "mistral-tekken": 1.00,
        "qwen2.5": 1.02,
        "deepseek-v3": 1.05,
        "deepseek-r1": 1.05,
        "mock": 1.00,
    },
}


class CandidateScore(BaseModel):
    """Detailed score and cost breakdown for an evaluated candidate model."""
    model_id: str
    headline_price_per_1m: float
    estimated_inflation: float
    effective_cost_per_1m: float
    tokens_estimated: int
    strengths: str


class ModelRecommendation(BaseModel):
    """Routing decision for an input prompt."""
    prompt_sample: str
    detected_script: str
    is_code: bool
    recommended_model: str
    effective_cost_per_1m: float
    savings_vs_worst: str
    explanation: str
    all_candidates: list[CandidateScore] = Field(default_factory=list)


def detect_primary_script(text: str) -> str:
    """Classify the dominant script of the text using Unicode ranges."""
    cjk_count = len(re.findall(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", text))
    indic_count = len(re.findall(r"[\u0900-\u0d7f]", text))  # Devanagari, Bengali, Gurmukhi, Gujarati, Oriya, Tamil, Telugu, Kannada, Malayalam
    arabic_count = len(re.findall(r"[\u0600-\u06ff\u0750-\u077f\u0590-\u05ff]", text))  # Arabic, Hebrew
    cyrillic_count = len(re.findall(r"[\u0400-\u04ff\u0370-\u03ff]", text))  # Cyrillic, Greek

    total_chars = max(1, len(text.strip()))
    
    if cjk_count / total_chars > 0.15:
        return "cjk"
    if indic_count / total_chars > 0.10:
        return "indic"
    if arabic_count / total_chars > 0.10:
        return "arabic"
    if cyrillic_count / total_chars > 0.15:
        return "cyrillic"
    return "latin"


def detect_is_code(text: str) -> bool:
    """Heuristic check for programming code or structured schemas."""
    code_signals = [
        r"def\s+[a-zA-Z_]\w*\s*\(",
        r"function\s+[a-zA-Z_]\w*\s*\(",
        r"pub\s+fn\s+",
        r"class\s+[a-zA-Z_]\w*[:\{]",
        r"import\s+[\w\.]+",
        r"\{\s*\"[a-zA-Z_]+\"\s*:",  # JSON
        r"SELECT\s+.*?\s+FROM",
        r"<\w+.*?>.*?</\w+>",  # HTML / XML
    ]
    for pattern in code_signals:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def recommend_model(
    prompt: str,
    task: Optional[str] = None,
    budget_tier: Literal["frugal", "balanced", "frontier"] = "balanced",
    registry: Optional[TokenizerRegistry] = None,
) -> ModelRecommendation:
    """Evaluate prompt script/structure and recommend the optimal model tokenizer."""
    is_code = detect_is_code(prompt)
    script = "code" if is_code else detect_primary_script(prompt)

    # Candidate set to evaluate
    candidates = [
        "deepseek-v3",
        "deepseek-r1",
        "qwen2.5",
        "qwen2.5-coder" if is_code else None,
        "mistral-tekken",
        "gpt-4o",
        "llama-3",
        "llama-3.2",
    ]
    candidates = [c for c in candidates if c is not None]

    reg = registry or TokenizerRegistry()
    scored_candidates: list[CandidateScore] = []

    inflation_table = SCRIPT_INFLATION_ESTIMATES.get(script, SCRIPT_INFLATION_ESTIMATES["latin"])

    # Baseline token estimation using local zero-network tiktoken
    try:
        baseline_toks = len(reg.tokenize("gpt-4o", prompt).token_ids)
    except Exception:
        baseline_toks = max(1, int(len(prompt.split()) * 1.3))

    for model_id in candidates:
        headline = PROVIDER_PRICING.get(model_id, 1.0)
        est_inf = inflation_table.get(model_id, 1.0)
        tok_count = max(1, int(baseline_toks * est_inf))
        eff_cost = round(headline * est_inf, 3)

        spec = reg.get_spec(model_id) if model_id in reg._specs else None
        strengths = spec.notes if spec and spec.notes else "Standard evaluation model"

        scored_candidates.append(
            CandidateScore(
                model_id=model_id,
                headline_price_per_1m=headline,
                estimated_inflation=est_inf,
                effective_cost_per_1m=eff_cost,
                tokens_estimated=tok_count,
                strengths=strengths,
            )
        )

    # Sort based on budget tier
    if budget_tier == "frugal":
        # Strictly lowest effective cost per 1M tokens
        scored_candidates.sort(key=lambda c: c.effective_cost_per_1m)
    elif budget_tier == "frontier":
        # Prioritize frontier models, then cost
        frontier_order = {"gpt-4o": 0, "deepseek-r1": 1, "deepseek-v3": 2}
        scored_candidates.sort(key=lambda c: (frontier_order.get(c.model_id, 99), c.effective_cost_per_1m))
    else:  # balanced
        # Balanced: weight low cost + reasonable token density
        scored_candidates.sort(key=lambda c: c.effective_cost_per_1m * (1.0 if "gpt" not in c.model_id else 0.8))

    best = scored_candidates[0]
    worst = max(scored_candidates, key=lambda c: c.effective_cost_per_1m)
    savings_ratio = round(worst.effective_cost_per_1m / max(0.001, best.effective_cost_per_1m), 1)

    explanation = (
        f"Detected {script.upper()} script. {best.model_id} achieves an estimated inflation of {best.estimated_inflation}x "
        f"with an effective cost of ${best.effective_cost_per_1m}/1M tokens "
        f"({savings_ratio}x cheaper effective cost than {worst.model_id} at ${worst.effective_cost_per_1m}/1M)."
    )

    return ModelRecommendation(
        prompt_sample=prompt[:80] + ("..." if len(prompt) > 80 else ""),
        detected_script=script,
        is_code=is_code,
        recommended_model=best.model_id,
        effective_cost_per_1m=best.effective_cost_per_1m,
        savings_vs_worst=f"{savings_ratio}x",
        explanation=explanation,
        all_candidates=scored_candidates,
    )
