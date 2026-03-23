"""Entropy utilities for Phase 1.

Includes Shannon entropy helper based on the project `shannon.txt` example.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Union


def shannon_entropy(data: Union[str, bytes]) -> float:
    """Calculate Shannon entropy in bits per symbol.

    Formula: H(X) = -sum(p(x) * log2(p(x))).
    For `str` input we analyze UTF-8 encoded bytes.
    """
    if not data:
        return 0.0

    if isinstance(data, str):
        data = data.encode("utf-8")

    freq = Counter(data)
    total = len(data)

    entropy = 0.0
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy


def entropy_label(entropy: float) -> str:
    """Map entropy value (bits/symbol) into coarse bins."""
    if entropy < 1.0:
        return "near_deterministic"
    if entropy < 3.0:
        return "low_entropy"
    if entropy < 5.0:
        return "medium_entropy"
    if entropy < 7.0:
        return "high_entropy"
    return "near_random"
