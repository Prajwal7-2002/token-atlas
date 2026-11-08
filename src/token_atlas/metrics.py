def calculate_inflation_index(target_tokens: int, baseline_tokens: int) -> float:
    """Calculate the Token Inflation Index (tau).
    
    tau = target_tokens / baseline_tokens
    
    A value of 1.0 indicates exact parity with baseline.
    A value of 2.5 indicates 150% more tokens needed to express the same concept.
    """
    if baseline_tokens <= 0:
        return 1.0 if target_tokens == 0 else float(target_tokens)
    return round(float(target_tokens) / float(baseline_tokens), 3)


def calculate_bytes_per_token(byte_count: int, token_count: int) -> float:
    """Calculate the byte compression density (Bytes Per Token, BPT).
    
    Higher values indicate greater information density packed into each token.
    """
    if token_count <= 0:
        return 0.0
    return round(float(byte_count) / float(token_count), 3)


def calculate_effective_context(nominal_context: int, inflation_index: float) -> int:
    """Calculate the true usable context length (W_eff) in baseline semantic units.
    
    W_eff = nominal_context / inflation_index
    """
    if inflation_index <= 0.0:
        return nominal_context
    return int(round(float(nominal_context) / float(inflation_index)))


def calculate_cost_multiplier(inflation_index: float) -> float:
    """Calculate the real financial cost multiplier (kappa) relative to English.
    
    Since token-based APIs bill per token consumed, expressing the same thought in
    a language with inflation tau multiplies the invoice by tau.
    """
    return max(0.0, round(float(inflation_index), 3))
