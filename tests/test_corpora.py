from token_atlas.corpora import (
    SUPPORTED_LANGUAGES,
    PARALLEL_CORPUS,
    get_parallel_corpus,
    get_language_meta,
)


def test_supported_languages_coverage():
    expected_codes = {"en", "de", "fr", "es", "ru", "ar", "hi", "kn", "zh", "ja"}
    assert set(SUPPORTED_LANGUAGES.keys()) == expected_codes


def test_parallel_corpus_integrity():
    assert len(PARALLEL_CORPUS) >= 5
    for idx, sentence_dict in enumerate(PARALLEL_CORPUS):
        # Every sentence entry must have all supported languages
        for code in SUPPORTED_LANGUAGES:
            assert code in sentence_dict, f"Sentence #{idx} missing translation for '{code}'"
            assert len(sentence_dict[code].strip()) > 5, f"Sentence #{idx} for '{code}' is too short"


def test_get_parallel_corpus_limit():
    corpus_all = get_parallel_corpus()
    corpus_2 = get_parallel_corpus(limit=2)
    assert len(corpus_2) == 2
    assert corpus_2[0] == corpus_all[0]


def test_get_language_meta():
    meta = get_language_meta("kn")
    assert meta.code == "kn"
    assert meta.name == "Kannada"
    assert meta.family == "Dravidian"
    assert meta.script == "Kannada"

    unknown = get_language_meta("xyz")
    assert unknown.code == "xyz"
