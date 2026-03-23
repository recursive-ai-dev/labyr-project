# Labyr Project Plan (Codebase-Aligned)

_Last updated: 2026-03-23_

## What This Project Is

`labyr-project` is an experimental **diegetic filesystem generation project** that combines:
- a mathematically rigorous labyrinth/folder generator (`Documents/labyr-v0.6.py`)
- RPG-like gating and exploration concepts (documented in `TECHNICAL_SPEC.md`)
- desktop immersion concepts (documented in `DESKTOP_ENVIRONMENT_SPEC.md`)
- early gameplay/semantic filesystem prototypes (`additional-logic.py`, `additional-logic-002.py`)

The project is currently in **specification + prototype stage**, not yet a packaged desktop product.

## Current Reality Snapshot

### Implemented / Present
- [x] Formal mathematical generator in a monolithic Python script (`Documents/labyr-v0.6.py`)
- [x] Technical design for RPG extensions (`TECHNICAL_SPEC.md`)
- [x] Technical design for diegetic desktop layer (`DESKTOP_ENVIRONMENT_SPEC.md`)
- [x] Experimental Node-based semantic filesystem generator (`additional-logic.py`)
- [x] Experimental Node-based game filesystem with lock/key progression (`additional-logic-002.py`)

### Not Yet Implemented in Repo
- [ ] Modular package structure (`src/labyr/...`) described in `IMPLEMENTATION_GUIDE.md`
- [ ] Unified API/CLI combining mathematical core + RPG systems
- [ ] Production-ready desktop environment integration
- [ ] Test suite and CI quality gates
- [ ] Distribution packaging

## Project Concept (Unified)

The core concept is:
1. Generate coherent dark-fantasy filesystem structures using rigorous mathematical constraints.
2. Layer progression/discovery mechanics on top of that structure.
3. Optionally render/interact through a diegetic desktop/browser interface.

This is **engine-first**, with UI/desktop immersion as a later layer.

## Scope Boundaries (Now)

### In Scope
- Mathematical generation correctness and reproducibility
- RPG mechanics integrated at graph/node level
- Safe filesystem materialization in a target directory
- CLI-first interaction model

### Out of Scope (for now)
- OS-wide desktop replacement
- Store/distribution/business KPIs
- Full cross-platform desktop shell integration as a first milestone

## Roadmap

## Phase 1 - Consolidate Core Engine
Goal: turn current mathematical script into a maintainable module baseline.

- [ ] Extract `SemanticMeasureSpace`, `LabyrinthGraph`, entropy/coherence logic from `Documents/labyr-v0.6.py`
- [ ] Create minimal package skeleton (`src/labyr/core/...`)
- [ ] Preserve existing CLI behavior through compatibility wrapper
- [ ] Add deterministic test fixtures (seeded outputs)

## Phase 2 - Integrate RPG Mechanics
Goal: implement the systems described in `TECHNICAL_SPEC.md`.

- [ ] Add `character.py`, `progression.py`, `discovery.py`, `lore.py`, `difficulty.py`
- [ ] Create `enhanced_graph.py` with access checks and rewards
- [ ] Expose via single API surface (`api.py`)
- [ ] Add regression tests for access requirements and discovery behavior

## Phase 3 - Filesystem Realization + CLI
Goal: provide practical usable generator commands.

- [ ] Build filesystem manager to materialize generated paths safely
- [ ] Add metadata outputs (manifest, graph JSON)
- [ ] Unify/replace ad-hoc prototype flows from `additional-logic*.py`
- [ ] Add command set: `generate`, `explore`, `status`, `verify`

## Phase 4 - Diegetic Interface Layer (Optional Next)
Goal: implement minimal interface after engine stability.

- [ ] Start with lightweight viewer/browser mode before full desktop replacement
- [ ] Implement theme + cursor + notification proof of concept
- [ ] Integrate character/discovery state into UI feedback
- [ ] Validate performance targets before broader integration

## Phase 5 - Hardening and Release Readiness
Goal: make project reliable for repeated use.

- [ ] Unit/integration/performance tests
- [ ] Lint/type checks and reproducible dev setup
- [ ] Documentation pass (`README`, architecture, usage examples)
- [ ] Packaging and release workflow

## Immediate Next Actions

1. Establish canonical runtime choice (Python-only core; Node prototypes retained as references).
2. Create modular `src/labyr` skeleton and migrate core classes from `Documents/labyr-v0.6.py`.
3. Add first tests for deterministic generation, DAG constraints, and thematic coherence.
4. Implement minimal `LabyrinthAPI` and CLI parity with current script behavior.

## Definition of Success (Current Stage)

- The mathematical generator is modular, tested, and reproducible.
- RPG mechanics are integrated without breaking formal constraints.
- A user can generate and explore a themed filesystem via CLI reliably.
- Desktop/diegetic interface work remains optional and layered, not blocking core engine completion.
