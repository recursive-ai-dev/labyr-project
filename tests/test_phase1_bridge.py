import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from labyr.core import (
    CombinatorialGenerator,
    LabyrinthGraph,
    SemanticAlphabet,
    SemanticMeasureSpace,
    TopologicalConstraint,
    map_keywords_to_themes,
)


class TestPhase1Bridge(unittest.TestCase):
    def test_native_modules_are_used(self):
        self.assertEqual(SemanticMeasureSpace.__module__, "labyr.core.measure_space")
        self.assertEqual(LabyrinthGraph.__module__, "labyr.core.graph")

    def test_keyword_mapping(self):
        mapped = map_keywords_to_themes(["city", "ritual"])
        self.assertIn(SemanticAlphabet.CITY, mapped)
        self.assertIn(SemanticAlphabet.CULT, mapped)

    def test_seeded_generation_is_deterministic(self):
        random.seed(1337)
        measure = SemanticMeasureSpace()
        generator = CombinatorialGenerator(measure, [SemanticAlphabet.CITY])
        first = generator.generate_unique_paths(count=10, depth=3, breadth=2, chaos=0.2)

        random.seed(1337)
        measure2 = SemanticMeasureSpace()
        generator2 = CombinatorialGenerator(measure2, [SemanticAlphabet.CITY])
        second = generator2.generate_unique_paths(
            count=10, depth=3, breadth=2, chaos=0.2
        )

        self.assertEqual(first, second)

    def test_native_graph_smoke(self):
        random.seed(7)
        measure = SemanticMeasureSpace()
        graph = LabyrinthGraph(
            max_depth=3,
            branching_factor=min(2, TopologicalConstraint.MAX_BRANCHING_FACTOR),
            chaos=0.2,
            measure_space=measure,
        )
        paths = graph.generate(8)
        self.assertGreater(len(paths), 0)
        self.assertTrue(graph.verify_acyclicity())

    def test_secure_hash(self):
        import hashlib

        from labyr.core.graph import LabyrinthNode, generate_id

        node = LabyrinthNode(
            id=generate_id("test/path"),
            path="test/path",
            depth=0,
            theme=SemanticAlphabet.CITY,
            entropy=0.0,
        )

        expected_hash_id = hashlib.sha256(b"test/path").hexdigest()
        self.assertEqual(node.id, expected_hash_id)

        self.assertEqual(hash(node), hash(node.id))


if __name__ == "__main__":
    unittest.main()
