"""Semantic measure-space implementation for Phase 1 migration."""

from __future__ import annotations

import copy
import random
from typing import Dict, List, Optional

from ..legacy import get_legacy_module

_legacy = get_legacy_module()

SemanticAlphabet = _legacy.SemanticAlphabet
SemanticElement = _legacy.SemanticElement
map_keywords_to_themes = _legacy.map_keywords_to_themes
_DEFAULT_OMEGA = None
_DEFAULT_TRANSITION_KERNEL = None


def _load_default_ontology():
    """Load and cache the canonical default ontology from legacy data."""
    global _DEFAULT_OMEGA, _DEFAULT_TRANSITION_KERNEL
    if _DEFAULT_OMEGA is not None and _DEFAULT_TRANSITION_KERNEL is not None:
        return

    # Reuse the mature ontology content without duplicating thousands of lines
    # during this early migration phase.
    bootstrap = _legacy.SemanticMeasureSpace()
    _DEFAULT_OMEGA = copy.deepcopy(bootstrap.Ω)
    _DEFAULT_TRANSITION_KERNEL = copy.deepcopy(bootstrap.transition_kernel)


class SemanticMeasureSpace:
    """Construct (Ω, F, P) as the semantic probability space.

    This class is now natively defined in `src/labyr/core` and keeps behavior
    compatible with the legacy model.
    """

    def __init__(self):
        self.Ω: Dict[SemanticAlphabet, Dict[str, List[SemanticElement]]] = {}
        self.transition_kernel: Dict[SemanticAlphabet, Dict[SemanticAlphabet, float]] = {}
        self._initialize_sample_space()
        self._construct_transition_kernel()
        self._validate_measure()

    def _initialize_sample_space(self):
        _load_default_ontology()
        self.Ω = copy.deepcopy(_DEFAULT_OMEGA)

    def _construct_transition_kernel(self):
        _load_default_ontology()
        self.transition_kernel = copy.deepcopy(_DEFAULT_TRANSITION_KERNEL)

    def _validate_measure(self):
        for theme, categories in self.Ω.items():
            for category, elements in categories.items():
                total_prob = sum(e.weight for e in elements)
                assert abs(total_prob - 1.0) < 1e-6 or total_prob == 0, (
                    f"Measure violation in {theme}.{category}: {total_prob}"
                )

    def sample_element(
        self, theme: SemanticAlphabet, category: Optional[str] = None
    ) -> SemanticElement:
        """Sample an element from a theme/category using weighted selection."""
        if theme not in self.Ω:
            raise ValueError(f"Invalid theme: {theme}")

        categories = self.Ω[theme]
        if category and category in categories:
            elements = categories[category]
        else:
            elements = [e for cat_elements in categories.values() for e in cat_elements]

        weights = [e.weight for e in elements]
        total = sum(weights)
        if total == 0:
            return random.choice(elements)

        r = random.uniform(0, total)
        cumulative = 0.0
        for element in elements:
            cumulative += element.weight
            if r <= cumulative:
                return element

        return elements[-1]

    def transition(self, current_theme: SemanticAlphabet) -> SemanticAlphabet:
        """Markov transition to next theme based on transition kernel."""
        row = self.transition_kernel[current_theme]
        themes = list(row.keys())
        weights = list(row.values())
        return random.choices(themes, weights=weights, k=1)[0]
