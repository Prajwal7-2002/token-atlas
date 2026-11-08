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
    assert "mock" in result.output


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
