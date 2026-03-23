"""Graph core adapter (Phase 1)."""

from __future__ import annotations

from ..legacy import get_legacy_module

_legacy = get_legacy_module()

TopologicalConstraint = _legacy.TopologicalConstraint
LabyrinthNode = _legacy.LabyrinthNode
LabyrinthGraph = _legacy.LabyrinthGraph
CombinatorialGenerator = _legacy.CombinatorialGenerator
