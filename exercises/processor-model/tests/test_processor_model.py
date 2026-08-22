from __future__ import annotations
import unittest
import processor_model.bits
import processor_model.isa

class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('isa')

if __name__ == '__main__':
    unittest.main()
