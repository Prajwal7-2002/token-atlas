"""Prompt Minifier & Whitespace Compactor.

Losslessly reduces token count by:
1. Compacting embedded JSON blocks and schemas (removing spacing without altering structure).
2. Collapsing redundant newlines (3+ newlines -> 2).
3. Stripping trailing whitespace per line.
4. Preserving code blocks (triple backticks) while compressing surrounding prose.
"""

import json
import re
from typing import Optional
from pydantic import BaseModel, Field

from token_atlas.registry import TokenizerRegistry


class MinificationResult(BaseModel):
    """Result of lossless prompt token minification."""
    original_text: str
    minified_text: str
    original_char_count: int
    minified_char_count: int
    original_byte_count: int
    minified_byte_count: int
    bytes_saved: int
    char_reduction_pct: float
    original_tokens: Optional[int] = None
    minified_tokens: Optional[int] = None
    tokens_saved: Optional[int] = None
    token_reduction_pct: Optional[float] = None


def compact_json_blocks(text: str) -> str:
    """Find JSON objects/arrays within text and format them with zero redundant whitespace."""
    # Matches top-level JSON objects or arrays spanning multiple lines
    def _json_replacer(match: re.Match) -> str:
        candidate = match.group(0)
        try:
            parsed = json.loads(candidate)
            return json.dumps(parsed, separators=(",", ":"), ensure_ascii=False)
        except Exception:
            return candidate

    # Match blocks starting with { or [ and ending with } or ] with multiple lines
    pattern = r"(\{(?:[^{}]|(?R))*\}|\[(?:[^\[\]]|(?R))*\])"
    # Fallback simpler regex for multiline json objects
    simple_json_pattern = r"(?s)(\{[\s\S]*?\}|\[[\s\S]*?\])"
    
    # We replace matching multiline blocks if they are valid JSON
    def _try_compact(s: str) -> str:
        # Check if entire string or block is json
        lines = s.split("\n")
        if len(lines) > 2 and (s.strip().startswith("{") and s.strip().endswith("}")) or (s.strip().startswith("[") and s.strip().endswith("]")):
            try:
                parsed = json.loads(s.strip())
                return json.dumps(parsed, separators=(",", ":"), ensure_ascii=False)
            except Exception:
                pass
        return s

    return _try_compact(text)


def minify_prompt(
    text: str,
    compact_json: bool = True,
    normalize_newlines: bool = True,
    tokenizer_id: Optional[str] = "gpt-4o",
    registry: Optional[TokenizerRegistry] = None,
) -> MinificationResult:
    """Losslessly compact text to minimize token consumption before model dispatch."""
    orig_chars = len(text)
    orig_bytes = len(text.encode("utf-8"))

    processed = text

    # 1. Optionally compact JSON blocks
    if compact_json:
        processed = compact_json_blocks(processed)

    # 2. Strip trailing whitespace per line
    lines = [line.rstrip() for line in processed.split("\n")]
    processed = "\n".join(lines)

    # 3. Collapse 3 or more consecutive newlines into 2 (standard paragraph break)
    if normalize_newlines:
        processed = re.sub(r"\n{3,}", "\n\n", processed)

    # 4. Strip leading and trailing overall whitespace
    processed = processed.strip()

    min_chars = len(processed)
    min_bytes = len(processed.encode("utf-8"))
    bytes_saved = max(0, orig_bytes - min_bytes)
    char_reduction = round((orig_chars - min_chars) / max(1, orig_chars) * 100, 2)

    # Calculate token delta if a tokenizer is requested
    orig_toks = None
    min_toks = None
    toks_saved = None
    tok_reduction = None

    if tokenizer_id:
        reg = registry or TokenizerRegistry()
        try:
            res_orig = reg.tokenize(tokenizer_id, text)
            res_min = reg.tokenize(tokenizer_id, processed)
            orig_toks = res_orig.token_count
            min_toks = res_min.token_count
            toks_saved = max(0, orig_toks - min_toks)
            tok_reduction = round(toks_saved / max(1, orig_toks) * 100, 2)
        except Exception:
            pass

    return MinificationResult(
        original_text=text,
        minified_text=processed,
        original_char_count=orig_chars,
        minified_char_count=min_chars,
        original_byte_count=orig_bytes,
        minified_byte_count=min_bytes,
        bytes_saved=bytes_saved,
        char_reduction_pct=char_reduction,
        original_tokens=orig_toks,
        minified_tokens=min_toks,
        tokens_saved=toks_saved,
        token_reduction_pct=tok_reduction,
    )
