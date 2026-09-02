"""Compatibility CLI for Phase 1 migration.

This preserves the legacy command surface while routing execution through
patched core adapters so known legacy runtime issues do not block progress.
"""

from __future__ import annotations

import argparse
import os
import random
from collections.abc import Sequence
from math import log2

from .core.graph import (
    CombinatorialGenerator,
    LabyrinthGraph,
    LabyrinthNode,
    TopologicalConstraint,
    generate_id,
)
from .core.measure_space import SemanticMeasureSpace, map_keywords_to_themes


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Mathematically rigorous labyrinth generator using graph theory "
        "and measure-theoretic probability.",
    )
    parser.add_argument(
        "keywords", nargs="+", help="Semantic keywords to seed the measure space"
    )
    parser.add_argument(
        "--base", "-b", default="./labyrinth", help="Base directory (root of graph)"
    )
    parser.add_argument(
        "--count", "-c", type=int, default=25, help="Target number of vertices |V|"
    )
    parser.add_argument(
        "--depth",
        "-d",
        type=int,
        default=5,
        help="Maximum depth D (graph diameter bound)",
    )
    parser.add_argument(
        "--breadth",
        "-w",
        type=int,
        default=4,
        help="Maximum out-degree (branching factor)",
    )
    parser.add_argument(
        "--chaos",
        "-x",
        type=float,
        default=0.3,
        help="Entropy injection factor α ∈ [0,1]",
    )
    parser.add_argument(
        "--seed", "-s", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Simulate without file system mutation",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify graph properties (acyclicity, entropy estimate)",
    )
    parser.add_argument(
        "--export", "-e", default=None, help="Export graph to shell script"
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.seed is not None:
        random.seed(args.seed)

    count = max(1, args.count)
    depth = max(1, min(args.depth, TopologicalConstraint.MAX_DEPTH))
    breadth = max(1, min(args.breadth, TopologicalConstraint.MAX_BRANCHING_FACTOR))
    chaos = max(0.0, min(1.0, args.chaos))

    print("\n[MATHEMATICAL SPECIFICATION]")
    print(f"  Target vertices |V| = {count}")
    print(f"  Maximum depth D = {depth}")
    print(f"  Branching factor b = {breadth}")
    print(f"  Entropy factor α = {chaos}")
    if args.seed is not None:
        print(f"  Random seed = {args.seed}")

    print("\n[CONSTRUCTING MEASURE SPACE]")
    measure = SemanticMeasureSpace()
    themes = map_keywords_to_themes(args.keywords)
    print(f"  Active themes: {[t.name for t in themes]}")

    combinatorial = CombinatorialGenerator(measure, themes)
    capacity = combinatorial.calculate_capacity(depth, breadth)
    print(f"  Theoretical capacity C(D,B) = {capacity}")
    print(f"  Requested |V| = {count} (utilization: {count / max(capacity, 1):.2%})")

    feasible, max_p, collision_prob = combinatorial.verify_feasibility(
        count, depth, breadth
    )
    if not feasible:
        if count > max_p:
            print(f"  WARNING: Exceeds capacity. Truncating to {max_p}.")
            count = max_p
        if collision_prob >= 0.5:
            print(f"  WARNING: Collision probability is high ({collision_prob:.2%}).")

    print("\n[GRAPH CONSTRUCTION]")
    print("  Generating DAG G = (V, E)...")
    paths = combinatorial.generate_unique_paths(count, depth, breadth, chaos)
    print(f"  Generated |V| = {len(paths)} vertices")
    if len(paths) > 0:
        print(f"  Path space entropy H ≈ {log2(len(paths)):.2f} bits")

    if args.verify:
        print("\n[FORMAL VERIFICATION]")
        graph = LabyrinthGraph(depth, breadth, chaos, measure)
        for path in paths:
            parts = path.split("/")
            for i in range(len(parts)):
                subpath = "/".join(parts[: i + 1])
                if subpath not in graph.vertices:
                    node = LabyrinthNode(
                        id=generate_id(subpath),
                        path=subpath,
                        depth=i,
                        theme=random.choice(themes),
                    )
                    graph.vertices[subpath] = node

        is_dag = graph.verify_acyclicity()
        print(f"  DAG property: {'VERIFIED' if is_dag else 'FAILED'}")
        print(f"  Shannon entropy H(X) = {graph.calculate_shannon_entropy():.4f} bits")

    if args.dry_run:
        print(f"\n[DRY RUN] Would create {len(paths)} directories:")
        for i, p in enumerate(paths[:10], 1):
            print(f"  {i}. {p}")
        if len(paths) > 10:
            print(f"  ... and {len(paths) - 10} more")
    else:
        print("\n[FILE SYSTEM MUTATION]")
        base_path = os.path.abspath(args.base)
        os.makedirs(base_path, exist_ok=True)
        created = 0
        failed = 0
        for path in paths:
            full_path = os.path.join(base_path, path)
            try:
                os.makedirs(full_path, exist_ok=False)
                created += 1
            except FileExistsError:
                failed += 1
            except Exception:
                failed += 1
        print(f"  Created: {created}")
        print(f"  Failed:  {failed}")

    if args.export:
        with open(args.export, "w", encoding="utf-8") as f:
            f.write("#!/bin/bash\n")
            f.write(f"# Rigorous Labyrinth: |V|={len(paths)}, D={depth}, b={breadth}\n")
            f.write(f'BASE="{os.path.abspath(args.base)}"\n')
            for path in paths:
                f.write(f'mkdir -p "$BASE/{path}"\n')
        os.chmod(args.export, 0o755)
        print(f"\n[EXPORT] Shell script: {args.export}")

    print("\n[DONE]")


if __name__ == "__main__":
    main()
