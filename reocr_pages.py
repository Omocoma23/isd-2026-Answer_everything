from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFC", str(text))
    text = text.replace("\u0e4d\u0e32", "\u0e33")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_pages(value: str) -> list[int]:
    """
    Examples:
      21-26
      21,22,23,24,25,26
      21-23,25,26
    """
    pages: set[int] = set()

    for part in value.split(","):
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            start, end = part.split("-", 1)
            a = int(start)
            b = int(end)
            if a > b:
                a, b = b, a
            pages.update(range(a, b + 1))
        else:
            pages.add(int(part))

    if not pages:
        raise ValueError("No pages selected.")

    return sorted(pages)


def rebuild_document_text(payload: dict) -> None:
    parts: list[str] = []

    for index, page in enumerate(payload.get("pages", []), start=1):
        page_no = int(page.get("page", index))
        text = str(page.get("text", "")).strip()
        parts.append(f"--- Page {page_no} ---\n{text}")

    payload["text"] = "\n\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Re-OCR only selected PDF pages and merge them into an existing "
            "*_prediction.json. Designed to avoid re-running a 300-400 page PDF."
        )
    )

    parser.add_argument("pdf", help="Original curriculum PDF")
    parser.add_argument("prediction_json", help="Existing *_prediction.json")
    parser.add_argument(
        "--pages",
        required=True,
        help='Pages to repair, e.g. "21-26"',
    )
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--psm", type=int, default=11)
    parser.add_argument("--languages", default="tha+eng")
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    prediction_path = Path(args.prediction_json)
    output_path = Path(args.output)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if not prediction_path.exists():
        raise FileNotFoundError(
            f"Prediction JSON not found: {prediction_path}"
        )

    payload = json.loads(
        prediction_path.read_text(encoding="utf-8")
    )

    pages = payload.get("pages", [])
    selected_pages = parse_pages(args.pages)

    for page_no in selected_pages:
        if page_no < 1 or page_no > len(pages):
            raise ValueError(
                f"Page {page_no} is outside prediction range "
                f"1..{len(pages)}"
            )

        print(
            f"[re-OCR] page={page_no} "
            f"dpi={args.dpi} psm={args.psm}"
        )

        images = convert_from_path(
            str(pdf_path),
            dpi=args.dpi,
            first_page=page_no,
            last_page=page_no,
            fmt="png",
            thread_count=1,
        )

        if not images:
            raise RuntimeError(
                f"Could not render PDF page {page_no}"
            )

        image = images[0]

        # image_to_string gives a better logical reading order for these
        # curriculum tables than the old PSM-4 line boxes.
        text = pytesseract.image_to_string(
            image,
            lang=args.languages,
            config=(
                f"--psm {args.psm} "
                "-c preserve_interword_spaces=1"
            ),
        )

        text = "\n".join(
            clean_text(line)
            for line in text.splitlines()
            if clean_text(line)
        )

        page = pages[page_no - 1]
        page["page"] = page_no
        page["text"] = text

        # Intentionally clear positioned lines on repaired pages.
        # curriculum_extraction.py will then use page["text"], whose
        # reading order is substantially better for the AI table layout.
        page["lines"] = []

    rebuild_document_text(payload)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Saved repaired prediction: {output_path}")


if __name__ == "__main__":
    main()
