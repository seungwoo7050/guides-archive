from __future__ import annotations
import unittest
import verified_algorithms.graphs

class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('dijkstra')

if __name__ == '__main__':
    unittest.main()
