import re
import unicodedata
from collections import defaultdict

import numpy as np
import pytesseract

from .base import BaseOCREngine
from ocr_system.schemas import OCRLine


THAI_DIGIT_TRANS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")


def clean_thai_text(text: str) -> str:
    text = unicodedata.normalize("NFC", str(text)).strip()
    text = text.replace("\u0e4d\u0e32", "\u0e33")
    # PSM 4 can separate Thai syllables/characters with spaces; Thai course names
    # normally do not need those spaces, so merge Thai-to-Thai gaps.
    text = re.sub(r"(?<=[ก-๙])\s+(?=[ก-๙])", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


class TesseractOCREngine(BaseOCREngine):
    name = "tesseract"

    def __init__(self, languages: str = "tha+eng"):
        self.languages = languages
        self.pytesseract = pytesseract

    def recognize(
        self,
        image: np.ndarray,
        page: int | None = None,
    ) -> list[OCRLine]:
        # PSM 4 handles curriculum/table-like pages much better than PSM 6.
        data = self.pytesseract.image_to_data(
            image,
            lang=self.languages,
            config="--psm 4 -c preserve_interword_spaces=1",
            output_type=self.pytesseract.Output.DICT,
        )

        groups: dict[tuple[int, int, int], list[dict]] = defaultdict(list)

        n = len(data.get("text", []))
        for i in range(n):
            text = clean_thai_text(data["text"][i])
            if not text:
                continue

            try:
                confidence = float(data["conf"][i])
            except (TypeError, ValueError):
                confidence = -1.0

            if confidence < 0:
                continue

            x = int(data["left"][i])
            y = int(data["top"][i])
            w = int(data["width"][i])
            h = int(data["height"][i])

            key = (
                int(data.get("block_num", [0] * n)[i]),
                int(data.get("par_num", [0] * n)[i]),
                int(data.get("line_num", [i] * n)[i]),
            )

            groups[key].append({
                "text": text,
                "confidence": confidence,
                "x": x,
                "y": y,
                "x2": x + w,
                "y2": y + h,
            })

        lines: list[OCRLine] = []

        for tokens in groups.values():
            tokens.sort(key=lambda t: (t["x"], t["y"]))

            text = clean_thai_text(" ".join(t["text"] for t in tokens))
            if not text:
                continue

            x1 = min(t["x"] for t in tokens)
            y1 = min(t["y"] for t in tokens)
            x2 = max(t["x2"] for t in tokens)
            y2 = max(t["y2"] for t in tokens)
            confidence = sum(t["confidence"] for t in tokens) / len(tokens)

            lines.append(
                OCRLine(
                    text=text,
                    confidence=confidence / 100.0,
                    box=[
                        [x1, y1],
                        [x2, y1],
                        [x2, y2],
                        [x1, y2],
                    ],
                    engine=self.name,
                    page=page,
                )
            )

        # Reading order
        lines.sort(key=lambda line: (line.box[0][1], line.box[0][0]))
        return lines
