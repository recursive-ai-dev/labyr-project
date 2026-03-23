"""Graph core implementation for Phase 1 migration."""

from __future__ import annotations

import random
import warnings
from collections import deque
from dataclasses import dataclass, field
from math import exp, floor, log2
from typing import Dict, Optional, Set, Tuple

from ..legacy import get_legacy_module
from .measure_space import SemanticAlphabet, SemanticMeasureSpace

_legacy = get_legacy_module()


class TopologicalConstraint:
    """Formal constraints on labyrinth graph generation."""

    MAX_DEPTH: int = 20
    MAX_IN_DEGREE: int = 5
    MAX_BRANCHING_FACTOR: int = 15
    MIN_THEMATIC_ENTROPY: float = 2.0


@dataclass
class LabyrinthNode:
    """Vertex v ∈ V in labyrinth graph G = (V, E)."""

    id: str
    path: str
    depth: int
    theme: SemanticAlphabet
    children: Set[str] = field(default_factory=set)
    entropy: float = 0.0

    def __hash__(self):
        return hash(self.id)


class LabyrinthGraph:
    """Directed acyclic graph representation of the generated labyrinth."""

    def __init__(
        self, max_depth: int, branching_factor: int, chaos: float, measure_space: SemanticMeasureSpace
    ):
        self.max_depth = max_depth
        self.branching_factor = branching_factor
        self.chaos = chaos
        self.measure = measure_space
        self.vertices: Dict[str, LabyrinthNode] = {}
        self.path_space: Set[str] = set()
        self.root: Optional[LabyrinthNode] = None

    def _generate_vertex_label(self, current_node: LabyrinthNode) -> Tuple[str, SemanticAlphabet]:
        if random.random() < self.chaos:
            next_theme = random.choice(list(SemanticAlphabet))
        else:
            next_theme = self.measure.transition(current_node.theme)

        element = self.measure.sample_element(next_theme)
        return element.symbol, next_theme

    def generate(self, target_vertices: int) -> Set[str]:
        if target_vertices <= 0:
            return set()

        theoretical_max = sum(
            min(
                self.branching_factor**d,
                len(SemanticAlphabet) * (max(len(cat) for cat in self.measure.Ω.values()) ** d),
            )
            for d in range(1, self.max_depth + 1)
        )

        if target_vertices > theoretical_max:
            warnings.warn(
                f"Target {target_vertices} exceeds theoretical capacity {theoretical_max}. "
                "Truncating generation."
            )
            target_vertices = floor(theoretical_max)

        root_theme = random.choice(list(SemanticAlphabet))
        root_element = self.measure.sample_element(root_theme)
        root_path = root_element.symbol

        if root_path in self.path_space:
            root_path = f"{root_path}_{random.randint(0, 65535):04x}"

        self.root = LabyrinthNode(
            id=hash(root_path),
            path=root_path,
            depth=0,
            theme=root_theme,
            entropy=root_element.entropy if hasattr(root_element, "entropy") else 0.0,
        )
        self.vertices[root_path] = self.root
        self.path_space.add(root_path)

        frontier = deque([self.root])
        paths = {root_path}

        while len(paths) < target_vertices and frontier:
            current = frontier.popleft()

            depth_ratio = current.depth / self.max_depth if self.max_depth > 0 else 1.0
            survival_prob = exp(-3.0 * depth_ratio)
            residual_quota = target_vertices - len(paths)

            max_children = min(self.branching_factor, residual_quota)
            if max_children <= 0:
                break

            actual_branching = sum(1 for _ in range(max_children) if random.random() < survival_prob)
            actual_branching = max(1, actual_branching) if max_children > 0 else 0

            attempts = 0
            max_attempts = actual_branching * 5

            while (
                len(current.children) < actual_branching
                and len(paths) < target_vertices
                and attempts < max_attempts
                and current.depth < self.max_depth
            ):
                attempts += 1
                segment, theme = self._generate_vertex_label(current)
                new_path = f"{current.path}/{segment}"

                if new_path in self.path_space:
                    continue

                child_id = hash(new_path) & 0xFFFFFFFFFFFFFFFF
                child = LabyrinthNode(
                    id=child_id,
                    path=new_path,
                    depth=current.depth + 1,
                    theme=theme,
                    entropy=0.0,
                )

                current.children.add(new_path)
                self.vertices[new_path] = child
                self.path_space.add(new_path)
                paths.add(new_path)
                frontier.append(child)

        return paths

    def verify_acyclicity(self) -> bool:
        if not self.vertices:
            return True

        WHITE, GRAY, BLACK = 0, 1, 2
        color = {v: WHITE for v in self.vertices}

        for start_vertex in self.vertices:
            if color[start_vertex] != WHITE:
                continue

            stack = [(start_vertex, iter(self.vertices[start_vertex].children), False)]
            color[start_vertex] = GRAY

            while stack:
                node_path, children_iter, processed = stack[-1]

                if not processed:
                    stack[-1] = (node_path, children_iter, True)

                    for child_path in children_iter:
                        if child_path not in self.vertices:
                            continue

                        child_color = color.get(child_path, WHITE)
                        if child_color == GRAY:
                            return False

                        if child_color == WHITE:
                            color[child_path] = GRAY
                            child_node = self.vertices[child_path]
                            stack.append((child_path, iter(child_node.children), False))
                            break
                else:
                    color[node_path] = BLACK
                    stack.pop()

        return True

    def calculate_shannon_entropy(self) -> float:
        total = len(self.vertices)
        if total <= 1:
            return 0.0

        depth_counts = {}
        for node in self.vertices.values():
            d = node.depth
            depth_counts[d] = depth_counts.get(d, 0) + 1

        entropy = 0.0
        for count in depth_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * log2(p)

        path_entropy = 0.0
        for node in self.vertices.values():
            if node.depth == 0:
                continue
            parent_path = node.path.rsplit("/", 1)[0] if "/" in node.path else None
            if parent_path and parent_path in self.vertices:
                parent = self.vertices[parent_path]
                if parent.children:
                    path_entropy += log2(len(parent.children)) / total

        return (entropy + path_entropy) / 2.0


CombinatorialGenerator = _legacy.CombinatorialGenerator
