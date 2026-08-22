from __future__ import annotations
import unittest
import kernel_model.lifecycle

class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('lifecycle')

if __name__ == '__main__':
    unittest.main()
