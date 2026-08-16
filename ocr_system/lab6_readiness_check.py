from __future__ import annotations

import argparse
import json
from pathlib import Path


PROGRAMS = ("AI", "IT", "BIT")


def pct(value):
    if value is None:
        return "-"
    return f"{float(value) * 100:.2f}%"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check whether Lab 4 evaluation outputs are structurally ready for Lab 6."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()

    eval_candidates = {
        "AI": [
            root / "outputs/AI/AI_evaluation.json",
        ],
        "IT": [
            root / "outputs/IT/IT_evaluation.json",
        ],
        "BIT": [
            root / "outputs/BIT/BIT_evaluation.json",
        ],
    }

    print("=" * 90)
    print("LAB 6 READINESS")
    print("=" * 90)

    all_structurally_ready = True

    for program in PROGRAMS:
        path = next((p for p in eval_candidates[program] if p.exists()), None)

        if path is None:
            print(f"{program}: NOT READY — evaluation JSON not found")
            all_structurally_ready = False
            continue

        d = json.loads(path.read_text(encoding="utf-8"))

        gt = d.get("total_ground_truth_courses", 0)
        pred = d.get("total_prediction_courses", 0)
        missing = d.get("missing_courses", 0)
        extra = d.get("extra_prediction_courses", 0)

        structural = gt == pred and missing == 0 and extra == 0

        print(
            f"{program}: "
            f"GT={gt} PRED={pred} "
            f"missing={missing} extra={extra} | "
            f"course={pct(d.get('course_match_rate'))} "
            f"field={pct(d.get('overall_field_accuracy'))}"
        )

        if program == "AI" and not structural:
            print(
                "     AI requires review of the suspicious 06016401 GT row "
                "before treating the dataset as clean."
            )

        if not structural:
            all_structurally_ready = False

    print()
    if all_structurally_ready:
        print("STRUCTURAL RESULT: READY for Lab 6.")
    else:
        print(
            "STRUCTURAL RESULT: NOT ALL READY. "
            "Fix/review the items above before final Lab 6."
        )

    print("\nLab 6 also needs a page-map CSV for each program:")
    for program in PROGRAMS:
        page_map = root / f"data/ground_truth/{program}_page_map.csv"
        print(
            f"  {program}: "
            + ("FOUND" if page_map.exists() else f"MISSING -> {page_map}")
        )


if __name__ == "__main__":
    main()
