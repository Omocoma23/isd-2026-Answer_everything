import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ocr_system.lab7b_curriculum import _normalize_pdf_thai_marks, _restore_literal_fields


class ThaiExtractionTests(unittest.TestCase):
    def test_legacy_font_marks(self):
        self.assertEqual(_normalize_pdf_thai_marks("โรงเรียนสร\uf70bางเสน\uf70aห\uf70e"),
                         "โรงเรียนสร้างเสน่ห์")

    def test_normal_text_and_unknown_characters_unchanged(self):
        text = "ภาษาไทย สระอำ น้ำ 90641001 CHARM SCHOOL \uf799"
        self.assertEqual(_normalize_pdf_thai_marks(text), text)

    def test_restore_source_title_not_model_spelling(self):
        courses = [{"code": "90641001", "name_th": "โรงเรียนสร้างเสนห์"}]
        text = _normalize_pdf_thai_marks(
            "90641001 โรงเรียนสร\uf70bางเสน\uf70aห\uf70e 2 (1-2-3)\n\nCHARM SCHOOL\n")
        _restore_literal_fields(courses, text)
        self.assertEqual(courses[0]["name_th"], "โรงเรียนสร้างเสน่ห์")
        self.assertEqual(courses[0]["credits"], "2(1-2-3)")

    def test_ambiguous_or_multiline_title_not_overwritten(self):
        for text in ["90641001 ชื่อบรรทัดแรก\nชื่อบรรทัดสอง\nCHARM SCHOOL\n",
                     "90641001 ชื่อ\uf799 2(1-2-3)\nCHARM SCHOOL\n"]:
            courses = [{"code": "90641001", "name_th": "ชื่อเดิม"}]
            _restore_literal_fields(courses, text)
            self.assertEqual(courses[0]["name_th"], "ชื่อเดิม")


if __name__ == "__main__":
    unittest.main()
