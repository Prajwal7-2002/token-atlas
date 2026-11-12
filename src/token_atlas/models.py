from typing import Literal, Optional
from pydantic import BaseModel, Field


class TokenizerSpec(BaseModel):
    """Specification of an evaluated tokenizer model."""
    id: str = Field(..., description="Short unique identifier, e.g. 'qwen2.5'")
    name: str = Field(..., description="Full display name")
    vocab_size: int = Field(..., description="Reported vocabulary size")
    context_window: int = Field(..., description="Maximum context window in tokens")
    backend: Literal["tiktoken", "transformers", "mock"] = Field(..., description="Loader backend")
    hf_path: Optional[str] = Field(None, description="Hugging Face hub repo ID")
    tiktoken_encoding: Optional[str] = Field(None, description="Tiktoken encoding name if applicable")
    category: str = Field("general", description="Category: general, multilingual, code, reasoning, slm")
    notes: Optional[str] = Field(None, description="Architectural characteristics, compression profile, and strengths")


class TokenizationResult(BaseModel):
    """Result of tokenizing a single text segment."""
    tokenizer_id: str
    language: str
    text: str
    token_count: int
    char_count: int
    byte_count: int
    bytes_per_token: float
    token_pieces: list[str] = Field(default_factory=list)
    token_ids: list[int] = Field(default_factory=list)


class LanguageMetric(BaseModel):
    """Aggregated efficiency metric for a language under a specific tokenizer."""
    language_code: str
    language_name: str
    family: str
    token_count: int
    char_count: int
    byte_count: int
    bytes_per_token: float
    inflation_index: float = Field(..., description="Ratio of target tokens vs English tokens (tau)")
    effective_context: int = Field(..., description="Nominal context window / inflation index")
    cost_multiplier: float = Field(..., description="Effective financial cost ratio vs English")


class BenchmarkResult(BaseModel):
    """Full benchmark evaluation for a single tokenizer across languages."""
    tokenizer_id: str
    tokenizer_name: str
    vocab_size: int
    context_window: int
    sample_count: int
    metrics: dict[str, LanguageMetric]


class LanguageComparison(BaseModel):
    """Direct cross-tokenizer comparison for a specific language."""
    language_code: str
    language_name: str
    sample_text: str
    results: list[TokenizationResult]


class BenchmarkReport(BaseModel):
    """Comprehensive benchmark report across multiple tokenizers and languages."""
    timestamp: str
    corpora_source: str
    tokenizers: list[str]
    languages: list[str]
    results: list[BenchmarkResult]
