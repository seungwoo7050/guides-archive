from __future__ import annotations
import unittest
import kernel_model.filesystem
import kernel_model.journal

class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('storage')

if __name__ == '__main__':
    unittest.main()
