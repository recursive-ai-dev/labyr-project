"""Thematic coherence verification adapter (Phase 1)."""

from __future__ import annotations

from typing import List, Optional

from ..legacy import get_legacy_module
from .measure_space import SemanticAlphabet, SemanticMeasureSpace

_legacy = get_legacy_module()


def verify_thematic_coherence(
    paths: List[str],
    expected_themes: List[SemanticAlphabet],
    measure_space: Optional[SemanticMeasureSpace] = None,
) -> float:
    """Wrapper around legacy theorematic coherence verification."""
    return _legacy.verify_theorematic_coherence(paths, expected_themes, measure_space)
