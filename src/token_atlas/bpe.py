"""Educational First-Principles Byte-Pair Encoding (BPE) Implementation.

Demonstrates how BPE merge tables are constructed from raw UTF-8 bytes and
why under-represented scripts suffer from severe byte-fallback fragmentation.
"""

from typing import NamedTuple
from collections import Counter


class BPETrainResult(NamedTuple):
    vocab: dict[int, bytes]
    merges: list[tuple[bytes, bytes]]
    token_ids: list[int]


def get_stats(ids: list[int]) -> Counter[tuple[int, int]]:
    """Count frequency of consecutive token id pairs."""
    counts: Counter[tuple[int, int]] = Counter()
    for p in zip(ids[:-1], ids[1:]):
        counts[p] += 1
    return counts


def merge_ids(ids: list[int], pair: tuple[int, int], new_id: int) -> list[int]:
    """Replace all occurrences of `pair` in `ids` with `new_id`."""
    new_ids: list[int] = []
    i = 0
    n = len(ids)
    while i < n:
        if i < n - 1 and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            new_ids.append(new_id)
            i += 2
        else:
            new_ids.append(ids[i])
            i += 1
    return new_ids


def train_toy_bpe(text: str, num_merges: int = 20) -> BPETrainResult:
    """Train a first-principles BPE tokenizer from raw UTF-8 text bytes.
    
    Initializes vocabulary with 256 byte tokens (0..255).
    Iteratively merges the most frequent adjacent pair.
    """
    raw_bytes = list(text.encode("utf-8"))
    ids = list(raw_bytes)

    # Base vocabulary: 256 individual UTF-8 bytes
    vocab: dict[int, bytes] = {i: bytes([i]) for i in range(256)}
    merges: list[tuple[bytes, bytes]] = []

    for i in range(num_merges):
        stats = get_stats(ids)
        if not stats:
            break
        # Pick the most frequent pair
        pair, count = stats.most_common(1)[0]
        if count < 2:
            # No repeated pairs left to merge
            break
        
        new_id = 256 + i
        ids = merge_ids(ids, pair, new_id)
        
        piece_a = vocab[pair[0]]
        piece_b = vocab[pair[1]]
        merged_piece = piece_a + piece_b
        vocab[new_id] = merged_piece
        merges.append((piece_a, piece_b))

    return BPETrainResult(vocab=vocab, merges=merges, token_ids=ids)


def explain_fragmentation(text: str) -> dict[str, any]:
    """Diagnose UTF-8 byte fragmentation for an input string."""
    encoded_bytes = text.encode("utf-8")
    byte_len = len(encoded_bytes)
    char_len = len(text)
    
    char_breakdown = []
    for ch in text[:10]:
        ch_bytes = ch.encode("utf-8")
        char_breakdown.append({
            "char": ch,
            "unicode": f"U+{ord(ch):04X}",
            "byte_count": len(ch_bytes),
            "raw_hex": " ".join([f"0x{b:02X}" for b in ch_bytes]),
        })

    return {
        "text_sample": text[:30],
        "character_count": char_len,
        "utf8_byte_count": byte_len,
        "bytes_per_char": byte_len / max(1, char_len),
        "sample_breakdown": char_breakdown,
    }

