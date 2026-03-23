import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from labyr.core.entropy import entropy_label, shannon_entropy


class TestShannonEntropy(unittest.TestCase):
    def test_empty_data(self):
        self.assertEqual(shannon_entropy(""), 0.0)

    def test_deterministic_data(self):
        self.assertAlmostEqual(shannon_entropy("aaaaaa"), 0.0, places=6)

    def test_uniform_two_symbol_data(self):
        self.assertAlmostEqual(shannon_entropy("abab"), 1.0, places=6)

    def test_entropy_label(self):
        self.assertEqual(entropy_label(0.5), "near_deterministic")
        self.assertEqual(entropy_label(2.0), "low_entropy")
        self.assertEqual(entropy_label(4.0), "medium_entropy")
        self.assertEqual(entropy_label(6.0), "high_entropy")


if __name__ == "__main__":
    unittest.main()
