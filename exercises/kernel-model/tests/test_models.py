from __future__ import annotations
import unittest
import kernel_model.deadlock

class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('deadlock')

if __name__ == '__main__':
    unittest.main()
