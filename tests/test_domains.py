"""Unit tests for Multi-Domain Tokenization Benchmark (Code, Indentation, Tools, Math)."""

import pytest
from typer.testing import CliRunner
from token_atlas.cli import app
from token_atlas.domains import (
    DOMAIN_SAMPLES,
    evaluate_domain,
    DomainBenchmarkReport,
)

runner = CliRunner()


def test_domain_samples_coverage():
    """Verify that all target domains and expected variants exist."""
    domains = {s.domain for s in DOMAIN_SAMPLES}
    assert "code" in domains
    assert "indentation" in domains
    assert "tools" in domains
    assert "math" in domains

    variants = {s.variant for s in DOMAIN_SAMPLES}
    assert "python" in variants
    assert "rust" in variants
    assert "spaces_4" in variants
    assert "minified" in variants
    assert "verbose_schema" in variants
    assert "compact_schema" in variants


def test_evaluate_domain_code_mock():
    """Verify evaluating code domain across mock tokenizer."""
    report = evaluate_domain(domain="code", tokenizer_ids=["mock"])
    assert isinstance(report, DomainBenchmarkReport)
    assert report.domain == "code"
    assert len(report.rows) >= 5
    for r in report.rows:
        assert r.domain == "code"
        assert r.token_count > 0
        assert r.char_count > 0
        assert r.bytes_per_token > 0.0


def test_evaluate_domain_indentation_metrics():
    """Verify indentation tax calculation in summary metrics."""
    report = evaluate_domain(domain="indentation", tokenizer_ids=["mock"])
    assert "indentation_tax_ratio" in report.summary_metrics
    tax_mock = report.summary_metrics["indentation_tax_ratio"]["mock"]
    assert tax_mock >= 1.0  # 4-space should never be fewer tokens than minified


def test_evaluate_domain_tool_schema_metrics():
    """Verify tool schema whitespace tax calculation."""
    report = evaluate_domain(domain="tools", tokenizer_ids=["mock"])
    assert "tool_schema_whitespace_tax" in report.summary_metrics
    tool_tax = report.summary_metrics["tool_schema_whitespace_tax"]["mock"]
    assert tool_tax >= 1.0


def test_evaluate_domain_invalid():
    """Verify raising ValueError on unknown domain."""
    with pytest.raises(ValueError, match="Unknown domain"):
        evaluate_domain(domain="invalid_domain_xyz", tokenizer_ids=["mock"])


def test_cli_bench_domain():
    """Verify CLI execution of bench-domain."""
    result = runner.invoke(app, [
        "bench-domain",
        "--domain", "code",
        "--tokenizers", "mock",
    ])
    assert result.exit_code == 0
    assert "Multi-Domain Tokenization Benchmark" in result.output
    assert "QuickSort (Python)" in result.output
    assert "mock" in result.output


def test_cli_bench_domain_json_export(tmp_path):
    """Verify CLI json output for bench-domain."""
    json_path = tmp_path / "domain_bench.json"
    result = runner.invoke(app, [
        "bench-domain",
        "--domain", "indentation",
        "--tokenizers", "mock",
        "--json-out", str(json_path),
    ])
    assert result.exit_code == 0
    assert json_path.exists()
    assert "indentation_tax_ratio" in json_path.read_text(encoding="utf-8")
