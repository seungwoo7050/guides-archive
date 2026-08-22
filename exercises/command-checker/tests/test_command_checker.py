from __future__ import annotations
import unittest
import command_checker.model
import command_checker.specification

class HistoricalStageTests(unittest.TestCase):
    def test_stage_is_importable(self) -> None:
        self.assertTrue('command checker foundation')

if __name__ == '__main__':
    unittest.main()
