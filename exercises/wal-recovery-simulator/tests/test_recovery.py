from __future__ import annotations
import unittest


class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('wal')

if __name__ == '__main__':
    unittest.main()
