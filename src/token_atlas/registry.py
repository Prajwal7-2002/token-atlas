"""Tokenizer Registry: Loads and manages frontier tokenizers with zero weight downloads."""

from typing import Any, Optional, Protocol
import tiktoken
from token_atlas.models import TokenizerSpec, TokenizationResult
from token_atlas.metrics import calculate_bytes_per_token


class TokenizerProtocol(Protocol):
    """Common interface for any tokenizer backend."""
    def encode(self, text: str) -> list[int]:
        ...
    
    def decode_tokens(self, ids: list[int]) -> list[str]:
        ...


class TiktokenAdapter:
    """Adapter for OpenAI tiktoken encodings."""
    def __init__(self, encoding_name: str):
        self.encoding = tiktoken.get_encoding(encoding_name)

    def encode(self, text: str) -> list[int]:
        return self.encoding.encode(text, disallowed_special=())

    def decode_tokens(self, ids: list[int]) -> list[str]:
        # Return string representation of each single token id
        pieces = []
        for tid in ids:
            try:
                pieces.append(self.encoding.decode([tid]))
            except Exception:
                pieces.append(f"<byte_{tid}>")
        return pieces


class MockTokenizerAdapter:
    """Deterministic, lightweight tokenizer for unit testing and offline environments."""
    def __init__(self, name: str, vocab_size: int = 50000):
        self.name = name
        self.vocab_size = vocab_size

    def encode(self, text: str) -> list[int]:
        # For non-Latin or complex text without spaces, tokenize per character
        # For Latin text with spaces, split on space and punctuation
        words = text.strip().split()
        if not words:
            return []
        tokens = []
        for w in words:
            # Deterministic hash to token id
            tokens.append(abs(hash(w)) % self.vocab_size)
        return tokens

    def decode_tokens(self, ids: list[int]) -> list[str]:
        return [f"[tok_{i}]" for i in ids]


class TransformersAdapter:
    """Adapter for Hugging Face AutoTokenizer (fetches only metadata files ~2MB, zero weights)."""
    def __init__(self, model_id: str):
        from transformers import AutoTokenizer
        kwargs: dict[str, Any] = {"trust_remote_code": True}
        if "Mistral-Nemo" in model_id:
            kwargs["fix_mistral_regex"] = True
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, **kwargs)

    def encode(self, text: str) -> list[int]:
        return self.tokenizer.encode(text, add_special_tokens=False)

    def decode_tokens(self, ids: list[int]) -> list[str]:
        return [self.tokenizer.decode([i]) for i in ids]


DEFAULT_SPECS: dict[str, TokenizerSpec] = {
    "gpt-4o": TokenizerSpec(
        id="gpt-4o",
        name="OpenAI GPT-4o (o200k_base)",
        vocab_size=200000,
        context_window=128000,
        backend="tiktoken",
        tiktoken_encoding="o200k_base",
        category="multilingual",
        notes="Frontier 200k multilingual Tiktoken with native Indic/CJK tokens",
    ),
    "gpt-4": TokenizerSpec(
        id="gpt-4",
        name="OpenAI GPT-4 (cl100k_base)",
        vocab_size=100277,
        context_window=128000,
        backend="tiktoken",
        tiktoken_encoding="cl100k_base",
        category="general",
        notes="Legacy English-biased baseline; severe byte fallback on non-Latin scripts",
    ),
    "qwen2.5": TokenizerSpec(
        id="qwen2.5",
        name="Qwen2.5 (152k Vocab)",
        vocab_size=152064,
        context_window=131072,
        backend="transformers",
        hf_path="Qwen/Qwen2.5-7B",
        category="multilingual",
        notes="High-capacity multilingual Byte BPE with strong Asian & CJK compression",
    ),
    "qwen2.5-coder": TokenizerSpec(
        id="qwen2.5-coder",
        name="Qwen2.5-Coder (152k Vocab)",
        vocab_size=152064,
        context_window=131072,
        backend="transformers",
        hf_path="Qwen/Qwen2.5-Coder-7B",
        category="code",
        notes="Code-specialized merges for syntax, multi-space indentation, and repo paths",
    ),
    "deepseek-v3": TokenizerSpec(
        id="deepseek-v3",
        name="DeepSeek-V3 (128k Vocab)",
        vocab_size=128815,
        context_window=128000,
        backend="transformers",
        hf_path="deepseek-ai/DeepSeek-V3",
        category="reasoning",
        notes="Sinitic-first Byte BPE with extreme Chinese compression (tau ≈ 0.98x)",
    ),
    "deepseek-r1": TokenizerSpec(
        id="deepseek-r1",
        name="DeepSeek-R1 (128k Vocab)",
        vocab_size=128815,
        context_window=128000,
        backend="transformers",
        hf_path="deepseek-ai/DeepSeek-R1",
        category="reasoning",
        notes="Frontier open reasoning tokenizer for dense long-form thinking traces",
    ),
    "mistral-tekken": TokenizerSpec(
        id="mistral-tekken",
        name="Mistral Tekken (131k Vocab)",
        vocab_size=131072,
        context_window=128000,
        backend="transformers",
        hf_path="mistralai/Mistral-Nemo-Instruct-2407",
        category="multilingual",
        notes="Balanced multilingual BPE with superior European and Indic byte packing",
    ),
    "cohere-aya": TokenizerSpec(
        id="cohere-aya",
        name="Cohere Aya Expanse (256k Vocab)",
        vocab_size=256000,
        context_window=128000,
        backend="transformers",
        hf_path="CohereForAI/aya-expanse-8b",
        category="multilingual",
        notes="Engineered specifically for 101 global languages with massive Dravidian & African subwords",
    ),
    "gemma-2": TokenizerSpec(
        id="gemma-2",
        name="Google Gemma 2 (256k Vocab)",
        vocab_size=256000,
        context_window=8192,
        backend="transformers",
        hf_path="unsloth/gemma-2-2b",
        category="general",
        notes="Massive 256k SentencePiece vocabulary with high memory embedding footprint",
    ),
    "llama-3": TokenizerSpec(
        id="llama-3",
        name="Meta Llama 3.1 (128k Vocab)",
        vocab_size=128256,
        context_window=128000,
        backend="transformers",
        hf_path="unsloth/Meta-Llama-3.1-8B",
        category="general",
        notes="Latin-first Tiktoken BPE; high inflation penalty on Indic and African scripts",
    ),
    "llama-3.2": TokenizerSpec(
        id="llama-3.2",
        name="Meta Llama 3.2 (128k Vocab, SLM)",
        vocab_size=128256,
        context_window=128000,
        backend="transformers",
        hf_path="unsloth/Llama-3.2-1B",
        category="slm",
        notes="Edge-optimized compact SLM tokenizer sharing Llama-3.1 vocabulary layout",
    ),
    "smollm2": TokenizerSpec(
        id="smollm2",
        name="HuggingFace SmolLM2 (49k Vocab, SLM)",
        vocab_size=49152,
        context_window=8192,
        backend="transformers",
        hf_path="HuggingFaceTB/SmolLM2-1.7B",
        category="slm",
        notes="Ultra-compact 49k vocabulary minimizing embedding memory for on-device deployment",
    ),
    "mock": TokenizerSpec(
        id="mock",
        name="Mock Deterministic Baseline",
        vocab_size=50000,
        context_window=32768,
        backend="mock",
        category="general",
        notes="Offline test baseline generating deterministic token IDs with zero dependencies",
    ),
}


class TokenizerRegistry:
    """Manages lazy-loading and tokenization across frontier model families."""
    def __init__(self):
        self._instances: dict[str, Any] = {}
        self._specs = dict(DEFAULT_SPECS)

    def register(self, spec: TokenizerSpec, instance: Any = None):
        """Register a custom tokenizer spec or active instance."""
        self._specs[spec.id] = spec
        if instance is not None:
            self._instances[spec.id] = instance

    def get_spec(self, tokenizer_id: str) -> TokenizerSpec:
        if tokenizer_id not in self._specs:
            raise KeyError(
                f"Unknown tokenizer '{tokenizer_id}'. Available: {list(self._specs.keys())}"
            )
        return self._specs[tokenizer_id]

    def list_tokenizers(self, category: Optional[str] = None) -> list[TokenizerSpec]:
        specs = list(self._specs.values())
        if category:
            cat = category.strip().lower()
            specs = [s for s in specs if s.category.lower() == cat]
        return specs

    def get_tokenizer(self, tokenizer_id: str) -> TokenizerProtocol:
        if tokenizer_id in self._instances:
            return self._instances[tokenizer_id]

        spec = self.get_spec(tokenizer_id)
        if spec.backend == "tiktoken":
            instance = TiktokenAdapter(spec.tiktoken_encoding or "o200k_base")
        elif spec.backend == "mock":
            instance = MockTokenizerAdapter(spec.name, spec.vocab_size)
        elif spec.backend == "transformers":
            instance = TransformersAdapter(spec.hf_path or "Qwen/Qwen2.5-0.5B")
        else:
            raise ValueError(f"Unsupported backend '{spec.backend}'")

        self._instances[tokenizer_id] = instance
        return instance

    def tokenize(self, tokenizer_id: str, text: str, language: str = "en") -> TokenizationResult:
        """Tokenize a text string and return complete statistical metadata."""
        tokenizer = self.get_tokenizer(tokenizer_id)
        token_ids = tokenizer.encode(text)
        token_count = len(token_ids)
        char_count = len(text)
        byte_count = len(text.encode("utf-8"))
        bytes_per_token = calculate_bytes_per_token(byte_count, token_count)
        
        # Decode token pieces only if reasonably sized to keep memory low
        pieces = tokenizer.decode_tokens(token_ids[:30]) if token_count <= 100 else []

        return TokenizationResult(
            tokenizer_id=tokenizer_id,
            language=language,
            text=text,
            token_count=token_count,
            char_count=char_count,
            byte_count=byte_count,
            bytes_per_token=bytes_per_token,
            token_pieces=pieces,
            token_ids=token_ids[:30],
        )
