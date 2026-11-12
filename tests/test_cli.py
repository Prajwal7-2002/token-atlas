from typer.testing import CliRunner
from token_atlas.cli import app

runner = CliRunner()


def test_cli_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "TokenAtlas version" in result.output


def test_cli_list_tokenizers():
    result = runner.invoke(app, ["list-tokenizers"])
    assert result.exit_code == 0
    assert "gpt-4o" in result.output
    assert "qwen2.5-coder" in result.output
    assert "deepseek-r1" in result.output
    assert "mock" in result.output

    # Test filtering by category
    code_res = runner.invoke(app, ["list-tokenizers", "--category", "code"])
    assert code_res.exit_code == 0
    assert "qwen2.5-coder" in code_res.output
    assert "gpt-4o" not in code_res.output


def test_cli_list_languages():
    result = runner.invoke(app, ["list-languages"])
    assert result.exit_code == 0
    assert "English" in result.output
    assert "Kannada" in result.output
    assert "Japanese" in result.output


def test_cli_compare():
    result = runner.invoke(app, [
        "compare",
        "--text", "Artificial intelligence in modern computing",
        "--tokenizers", "mock",
        "--language", "en",
    ])
    assert result.exit_code == 0
    assert "mock" in result.output
    assert "Tokens" in result.output


def test_cli_compare_file(tmp_path):
    text_file = tmp_path / "sample.txt"
    text_file.write_text("Testing tokenization directly from a local file.", encoding="utf-8")

    result = runner.invoke(app, [
        "compare",
        "--file", str(text_file),
        "--tokenizers", "mock",
        "--language", "en",
    ])
    assert result.exit_code == 0
    assert "mock" in result.output
    assert "Testing tokenization directly" in result.output


def test_cli_bench_mock(tmp_path):
    json_file = tmp_path / "report.json"
    md_file = tmp_path / "report.md"

    result = runner.invoke(app, [
        "bench",
        "--tokenizers", "mock",
        "--languages", "en,de,ja",
        "--samples", "2",
        "--json-out", str(json_file),
        "--md-out", str(md_file),
    ])
    assert result.exit_code == 0
    assert json_file.exists()
    assert md_file.exists()
    assert "Mock Deterministic Baseline" in result.output


def test_cli_bench_custom_corpus(tmp_path):
    custom_file = tmp_path / "custom_corpus.json"
    import json
    data = [
        {"en": "Hello world", "de": "Hallo Welt", "es": "Hola mundo"},
        {"en": "Open source inference", "de": "Open-Source-Inferenz", "es": "Inferencia de código abierto"},
    ]
    custom_file.write_text(json.dumps(data), encoding="utf-8")

    result = runner.invoke(app, [
        "bench",
        "--tokenizers", "mock",
        "--languages", "en,de,es",
        "--custom-corpus", str(custom_file),
    ])
    assert result.exit_code == 0
    assert "Mock Deterministic Baseline" in result.output


def test_cli_export_web(tmp_path):
    json_file = tmp_path / "bench.json"
    bench_res = runner.invoke(app, [
        "bench",
        "--tokenizers", "mock",
        "--languages", "en,de",
        "--samples", "1",
        "--json-out", str(json_file),
    ])
    assert bench_res.exit_code == 0
    assert json_file.exists()

    web_dir = tmp_path / "web_out"
    result = runner.invoke(app, [
        "export-web",
        "--benchmark-json", str(json_file),
        "--out-dir", str(web_dir),
    ])
    assert result.exit_code == 0
    assert (web_dir / "index.html").exists()
    assert (web_dir / "benchmark_data.json").exists()
    content = (web_dir / "index.html").read_text(encoding="utf-8")
    assert "TokenAtlas" in content
    assert "Live Token Tax" in content
