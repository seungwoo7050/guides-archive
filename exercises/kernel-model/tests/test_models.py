from __future__ import annotations
import unittest
import kernel_model.synchronization

class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('sync')

if __name__ == '__main__':
    unittest.main()
