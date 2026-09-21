import argparse
import json
from pathlib import Path

from ocr_system.curriculum_extraction import extract_curriculum_from_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run curriculum extraction from an existing OCR prediction JSON without OCRing the PDF again."
    )
    parser.add_argument("prediction_json", help="Path to *_prediction.json")
    parser.add_argument("--program", default="DSBA")
    parser.add_argument("--plan", default="coop", choices=["coop", "no_coop"])
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    prediction_path = Path(args.prediction_json)

    result = extract_curriculum_from_file(
        prediction_path,
        program=args.program,
        plan=args.plan,
    )

    output_path = (
        Path(args.output)
        if args.output
        else prediction_path.with_name(
            prediction_path.name.replace("_prediction.json", "_extracted.json")
        )
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Saved: {output_path}")
    print(f"Courses: {len(result.get('courses', []))}")


if __name__ == "__main__":
    main()
