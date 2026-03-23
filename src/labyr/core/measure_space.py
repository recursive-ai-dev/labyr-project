"""Semantic measure-space adapter (Phase 1).

This currently re-exports the mature implementation from the legacy module.
Future phases should replace these aliases with native module implementations.
"""

from __future__ import annotations

from ..legacy import get_legacy_module

_legacy = get_legacy_module()

SemanticAlphabet = _legacy.SemanticAlphabet
SemanticElement = _legacy.SemanticElement
map_keywords_to_themes = _legacy.map_keywords_to_themes


class SemanticMeasureSpace(_legacy.SemanticMeasureSpace):
    """Compatibility wrapper for the legacy semantic measure space.

    The legacy implementation declares mutable attributes with
    `dataclasses.field(...)` inside a non-dataclass class. Initializing the
    dicts here avoids runtime failures and preserves legacy behavior.
    """

    def __init__(self):
        self.Ω = {}
        self.transition_kernel = {}
        super().__init__()
