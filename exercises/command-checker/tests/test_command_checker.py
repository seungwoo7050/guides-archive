from __future__ import annotations
import unittest
import command_checker.process
import command_checker.runner

class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('process')

if __name__ == '__main__':
    unittest.main()
