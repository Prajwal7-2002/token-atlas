import pytest
from token_atlas.bpe import train_toy_bpe, explain_fragmentation


def test_train_toy_bpe_english():
    text = "low low low lower lowest"
    res = train_toy_bpe(text, num_merges=10)
    assert len(res.vocab) > 256
    assert len(res.merges) > 0
    # Merged token count must be strictly less than raw UTF-8 bytes
    assert len(res.token_ids) < len(text.encode("utf-8"))


def test_explain_fragmentation_indic():
    # Kannada word
    text = "ಕನ್ನಡ"
    diag = explain_fragmentation(text)
    assert diag["character_count"] == 5
    # Each Kannada char in UTF-8 takes 3 bytes
    assert diag["utf8_byte_count"] == 15
    assert diag["bytes_per_char"] == 3.0
    assert len(diag["sample_breakdown"]) == 5
    assert diag["sample_breakdown"][0]["byte_count"] == 3


def test_explain_fragmentation_ascii():
    text = "Hello"
    diag = explain_fragmentation(text)
    assert diag["character_count"] == 5
    assert diag["utf8_byte_count"] == 5
    assert diag["bytes_per_char"] == 1.0

