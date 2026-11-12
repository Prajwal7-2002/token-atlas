"""Unit tests for Tokenizer-Aware Model Router."""

from typer.testing import CliRunner
from token_atlas.cli import app
from token_atlas.router import (
    detect_primary_script,
    detect_is_code,
    recommend_model,
    ModelRecommendation,
)

runner = CliRunner()


def test_detect_primary_script():
    assert detect_primary_script("Hello world, this is English text.") == "latin"
    assert detect_primary_script("ಕನ್ನಡದಲ್ಲಿ ತಂತ್ರಜ್ಞಾನ ಮತ್ತು ಕಂಪ್ಯೂಟರ್") == "indic"
    assert detect_primary_script("यह एक हिंदी वाक्य है और मशीन लर्निंग") == "indic"
    assert detect_primary_script("这是一个用于评估深度求索模型的中文句子") == "cjk"
    assert detect_primary_script("هذا نص باللغة العربية لاختبار التجزئة") == "arabic"
    assert detect_primary_script("Это русский текст для тестирования токенизатора") == "cyrillic"


def test_detect_is_code():
    code_python = "def calculate_loss(pred, target):\n    return ((pred - target) ** 2).mean()"
    assert detect_is_code(code_python) is True

    json_snippet = '{\n  "status": "success",\n  "code": 200\n}'
    assert detect_is_code(json_snippet) is True

    prose = "The transformer architecture relies on scaled dot-product attention."
    assert detect_is_code(prose) is False


def test_recommend_model_indic():
    prompt = "ದಯವಿಟ್ಟು ಈ ತಾಂತ್ರಿಕ ವಿವರಣೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ ಮತ್ತು ಸಾರಾಂಶವನ್ನು ನೀಡಿ."
    rec = recommend_model(prompt, budget_tier="frugal")
    assert isinstance(rec, ModelRecommendation)
    assert rec.detected_script == "indic"
    assert rec.recommended_model in ("deepseek-v3", "qwen2.5", "mistral-tekken", "gpt-4o", "llama-3.2")
    assert len(rec.all_candidates) > 0


def test_recommend_model_cjk():
    prompt = "请使用深度求索模型进行数学推理和推理链生成。"
    rec = recommend_model(prompt, budget_tier="frugal")
    assert rec.detected_script == "cjk"
    assert rec.recommended_model in ("deepseek-v3", "deepseek-r1", "qwen2.5", "llama-3.2")


def test_recommend_model_code():
    prompt = "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1"
    rec = recommend_model(prompt, budget_tier="balanced")
    assert rec.is_code is True
    assert "code" in rec.detected_script or rec.is_code


def test_cli_route_command():
    result = runner.invoke(app, [
        "route",
        "--text", "Machine learning inference on edge hardware",
        "--budget", "frugal",
    ])
    assert result.exit_code == 0
    assert "Tokenizer-Aware Model Routing Decision" in result.output
    assert "LATIN" in result.output
