from pathlib import Path
import unittest


class HistoricalStageTest(unittest.TestCase):
    def test_model_and_engine_sources_are_present(self) -> None:
        root = Path(__file__).resolve().parents[1]
        model = root / "src" / "session_room_lifecycle" / "model.py"
        engine = root / "src" / "session_room_lifecycle" / "engine.py"
        self.assertIn("Implementation 1", model.read_text(encoding="utf-8"))
        self.assertIn("Implementation 7", engine.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
