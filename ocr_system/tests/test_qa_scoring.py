import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "lab8b", ROOT / "src/ocr_system/lab8b_curriculum_db.py")
lab8b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab8b)


class ScoringTests(unittest.TestCase):
    def test_real_ground_truth_multiline_names(self):
        data = json.loads((ROOT / "data/ground_truth/DSBA_academic_plan_coop.json")
                          .read_text(encoding="utf-8"))
        names = [c["name_en"] for c in data["courses"]
                 if "\n" in (c.get("name_en") or "")]
        self.assertTrue(names)
        for name in names:
            with self.subTest(name=name):
                got = {"rows": [{"name_en": name.replace("\n", " ").strip()}]}
                self.assertTrue(lab8b.score_one({"type": "value", "value": name}, got)[0])

    def test_different_values_remain_wrong(self):
        for expected, actual in [("06026101", "6026101"), (3, 6),
                                 ("CALCULUS 1", "CALCULUS 2")]:
            self.assertFalse(lab8b.score_one(
                {"type": "value", "value": expected},
                {"rows": [{"value": actual}]} )[0])

    def test_failed_query_is_not_a_correct_empty_result(self):
        for expect in ({"type": "none"}, {"type": "count", "value": 0},
                       {"type": "set", "value": []}):
            self.assertFalse(lab8b.score_one(
                expect, {"rows": [], "error": "invalid SQL"})[0])

    def test_set_rejects_extra_courses(self):
        expect = {"type": "set", "value": ["06026101"]}
        self.assertFalse(lab8b.score_one(expect, {
            "rows": [{"code": "06026101"}, {"code": "06026102"}]} )[0])
        self.assertTrue(lab8b.score_one(expect, {
            "rows": [{"code": "06026101"}]} )[0])


if __name__ == "__main__":
    unittest.main()
