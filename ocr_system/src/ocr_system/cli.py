import argparse
import json
from pathlib import Path
from rich import print
from dataclasses import asdict
from .config import OCRConfig
from .pipeline import run_ocr
from .evaluation import evaluate_from_files
from .curriculum_extraction import extract_curriculum_from_file
from .utils.io import save_json


def parse_args():
    parser = argparse.ArgumentParser(
        description="Thai-English OCR system"
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True
    )

    # -------------------------
    # OCR
    # -------------------------
    ocr = sub.add_parser(
        "ocr",
        help="Run OCR on image or PDF"
    )

    ocr.add_argument("input_path")

    ocr.add_argument(
        "--output-dir",
        default="outputs"
    )

    ocr.add_argument(
        "--engine",
        choices=[
            "paddle",
            "tesseract",
            "trocr",
            "ensemble"
        ],
        default="ensemble"
    )

    ocr.add_argument(
        "--languages",
        default="tha+eng"
    )

    ocr.add_argument(
        "--paddle-lang",
        default="ta",
        help="PaddleOCR language"
    )

    ocr.add_argument(
        "--dpi",
        type=int,
        default=300
    )

    ocr.add_argument(
        "--no-preprocess",
        action="store_true"
    )

    ocr.add_argument(
        "--no-deskew",
        action="store_true"
    )

    ocr.add_argument(
        "--save-debug-images",
        action="store_true"
    )

    ocr.add_argument(
        "--min-confidence",
        type=float,
        default=0.0
    )

    ocr.add_argument(
        "--device",
        default="cpu"
    )

    # -------------------------
    # EVALUATE
    # -------------------------
    ev = sub.add_parser(
        "evaluate",
        help="Evaluate OCR extraction against ground truth"
    )

    ev.add_argument(
        "ground_truth_json"
    )

    ev.add_argument(
        "prediction_json"
    )

    ev.add_argument(
        "--output",
        default="outputs/evaluation_result.json"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # =====================================================
    # OCR
    # =====================================================
    if args.command == "ocr":

        output_dir = Path(args.output_dir)

        config = OCRConfig(
            input_path=Path(args.input_path),
            output_dir=output_dir,
            page_image_dir=output_dir / "pages",
            engine=args.engine,
            languages=args.languages,
            paddle_lang=args.paddle_lang,
            dpi=args.dpi,
            preprocess=not args.no_preprocess,
            deskew=not args.no_deskew,
            save_debug_images=args.save_debug_images,
            min_confidence=args.min_confidence,
            device=args.device,
        )

        # Run OCR
        result = run_ocr(config)

        # -------------------------------------------------
        # Curriculum extraction
        # -------------------------------------------------
        ocr_prediction_path = (
            output_dir /
            f"{Path(args.input_path).stem}_prediction.json"
        )

        # Save raw OCR result first
        save_json(
            asdict(result),
            ocr_prediction_path
        )

        # -------------------------------------------------
        # Extract curriculum fields
        # -------------------------------------------------
        curriculum = extract_curriculum_from_file(
            ocr_prediction_path,
            program="DSBA",
            plan="coop",
        )

        curriculum_path = (
            output_dir /
            f"{Path(args.input_path).stem}_extracted.json"
        )

        save_json(
            curriculum,
            curriculum_path
        )

        print(
            "[green]OCR done[/green]"
        )

        print(
            f"Raw OCR: {ocr_prediction_path}"
        )

        print(
            f"Extracted curriculum: {curriculum_path}"
        )

        print(
            json.dumps(
                curriculum,
                ensure_ascii=False,
                indent=2
            )
        )

    # =====================================================
    # EVALUATE
    # =====================================================
    elif args.command == "evaluate":

        result = evaluate_from_files(
            args.ground_truth_json,
            args.prediction_json
        )

        save_json(
            result,
            args.output
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2
            )
        )


if __name__ == "__main__":
    main()