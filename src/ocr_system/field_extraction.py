import re

def extract_common_fields(text: str) -> dict:
    """
    Format OCR output to Ground Truth format
    """

    result = {}

    # เก็บข้อความทั้งหมด
    result["text"] = text.strip()

    # แยกบรรทัด
    result["lines"] = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # จำนวนบรรทัด
    result["line_count"] = len(result["lines"])

    # จำนวนคำ
    result["word_count"] = len(text.split())

    return result