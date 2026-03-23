import random
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from labyr.core import (
    CombinatorialGenerator,
    SemanticAlphabet,
    SemanticMeasureSpace,
    map_keywords_to_themes,
)


class TestPhase1Bridge(unittest.TestCase):
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
        second = generator2.generate_unique_paths(count=10, depth=3, breadth=2, chaos=0.2)

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
