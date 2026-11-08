import pytest
from token_atlas.registry import TokenizerRegistry
from token_atlas.models import TokenizerSpec


def test_registry_list_and_specs():
    reg = TokenizerRegistry()
    tokenizers = reg.list_tokenizers()
    assert len(tokenizers) >= 5
    ids = [t.id for t in tokenizers]
    assert "gpt-4o" in ids
    assert "mock" in ids


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
