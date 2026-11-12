import pytest
from token_atlas.registry import TokenizerRegistry
from token_atlas.models import TokenizerSpec


def test_registry_list_and_specs():
    reg = TokenizerRegistry()
    tokenizers = reg.list_tokenizers()
    assert len(tokenizers) >= 12
    ids = [t.id for t in tokenizers]
    assert "gpt-4o" in ids
    assert "gpt-4" in ids
    assert "deepseek-v3" in ids
    assert "deepseek-r1" in ids
    assert "cohere-aya" in ids
    assert "qwen2.5-coder" in ids
    assert "llama-3.2" in ids
    assert "smollm2" in ids
    assert "mistral-tekken" in ids
    assert "mock" in ids


def test_registry_category_filtering():
    reg = TokenizerRegistry()
    code_specs = reg.list_tokenizers(category="code")
    assert any(s.id == "qwen2.5-coder" for s in code_specs)
    assert all(s.category == "code" for s in code_specs)

    reasoning_specs = reg.list_tokenizers(category="reasoning")
    assert any(s.id == "deepseek-r1" for s in reasoning_specs)
    assert all(s.category == "reasoning" for s in reasoning_specs)

    slm_specs = reg.list_tokenizers(category="slm")
    assert any(s.id in ("llama-3.2", "smollm2") for s in slm_specs)
    assert all(s.category == "slm" for s in slm_specs)


def test_registry_mock_tokenization():
    reg = TokenizerRegistry()
    text = "Artificial intelligence and machine learning"
    res = reg.tokenize("mock", text, language="en")
    
    assert res.tokenizer_id == "mock"
    assert res.token_count == 5
    assert res.char_count == len(text)
    assert res.byte_count == len(text.encode("utf-8"))
    assert res.bytes_per_token > 0.0


def test_registry_tiktoken_gpt4o():
    reg = TokenizerRegistry()
    text = "Hello world! Testing TokenAtlas tokenization."
    res = reg.tokenize("gpt-4o", text, language="en")

    assert res.tokenizer_id == "gpt-4o"
    assert res.token_count > 0
    assert len(res.token_pieces) > 0
    assert len(res.token_ids) > 0


def test_registry_custom_spec_registration():
    reg = TokenizerRegistry()
    custom_spec = TokenizerSpec(
        id="custom-fast",
        name="Custom Fast Spec",
        vocab_size=32000,
        context_window=8192,
        backend="mock",
    )
    reg.register(custom_spec)
    spec = reg.get_spec("custom-fast")
    assert spec.id == "custom-fast"
    assert spec.vocab_size == 32000


def test_registry_unknown_tokenizer():
    reg = TokenizerRegistry()
    with pytest.raises(KeyError):
        reg.get_spec("nonexistent-tokenizer-999")
