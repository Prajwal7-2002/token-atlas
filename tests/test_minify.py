"""Unit tests for Prompt Token Minifier."""

from typer.testing import CliRunner
from token_atlas.cli import app
from token_atlas.minify import (
    compact_json_blocks,
    minify_prompt,
    MinificationResult,
)

runner = CliRunner()


def test_compact_json_blocks():
    pretty_json = """{
      "model": "gpt-4o",
      "temperature": 0.7,
      "messages": [
        {
          "role": "user",
          "content": "Hello"
        }
      ]
    }"""
    compacted = compact_json_blocks(pretty_json)
    assert "\n" not in compacted
    assert "  " not in compacted
    assert '"model":"gpt-4o"' in compacted


def test_minify_prompt():
    raw_prompt = """
    System Prompt: You are an expert AI assistant.   
    
    
    Here is the schema:
    {
      "key": "value",
      "count": 42
    }
    
    
    Please process the request.    
    """
    res = minify_prompt(raw_prompt, tokenizer_id="mock")
    assert isinstance(res, MinificationResult)
    assert res.bytes_saved > 0
    assert res.minified_char_count < res.original_char_count
    assert "\n\n\n" not in res.minified_text


def test_cli_minify_command(tmp_path):
    sample = tmp_path / "prompt.txt"
    sample.write_text("Hello world!   \n\n\n\nSecond line.   ", encoding="utf-8")

    out_file = tmp_path / "minified.txt"
    result = runner.invoke(app, [
        "minify",
        "--file", str(sample),
        "--out", str(out_file),
        "--tokenizer", "mock",
    ])
    assert result.exit_code == 0
    assert "Prompt Token Minification Summary" in result.output
    assert out_file.exists()
    assert "\n\n\n" not in out_file.read_text(encoding="utf-8")

