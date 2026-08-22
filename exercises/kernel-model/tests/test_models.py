from __future__ import annotations
import unittest
import kernel_model.device_io

class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('device')

if __name__ == '__main__':
    unittest.main()
