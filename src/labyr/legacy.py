"""Helpers for loading the legacy monolithic implementation.

Phase 1 keeps behavior stable by adapting from `Documents/labyr-v0.6.py`
while we progressively migrate implementation details into modular files.
"""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType


_LEGACY_MODULE: ModuleType | None = None


def get_legacy_module() -> ModuleType:
    """Load and cache the legacy monolithic module."""
    global _LEGACY_MODULE
    if _LEGACY_MODULE is not None:
        return _LEGACY_MODULE

    legacy_path = Path(__file__).resolve().parents[2] / "Documents" / "labyr-v0.6.py"
    spec = spec_from_file_location("labyr_v0_6", legacy_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load legacy module from {legacy_path}")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    _apply_runtime_patches(module)
    _LEGACY_MODULE = module
    return module


def _apply_runtime_patches(module: ModuleType) -> None:
    """Patch known legacy issues without editing the source file in place."""
    base_cls = module.SemanticMeasureSpace

    class PatchedSemanticMeasureSpace(base_cls):
        def __init__(self):
            self.Ω = {}
            self.transition_kernel = {}
            super().__init__()

    module.SemanticMeasureSpace = PatchedSemanticMeasureSpace
