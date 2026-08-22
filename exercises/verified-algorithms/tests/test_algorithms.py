from __future__ import annotations
import unittest
import verified_algorithms.ranges
import verified_algorithms.trees

class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('trees')

if __name__ == '__main__':
    unittest.main()
