from __future__ import annotations
import unittest
import processor_model.vm

class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('vm')

if __name__ == '__main__':
    unittest.main()
