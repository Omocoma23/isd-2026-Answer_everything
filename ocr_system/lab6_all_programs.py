from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


PROGRAMS = ("DSBA", "AI", "IT", "BIT")


GT_CANDIDATES = {
    "DSBA": [
        "data/ground_truth/DSBA_academic_plan_coop.json",
        "data/ground_truth/DSBA_academic_plan.json",
    ],
    "AI": [
        "data/ground_truth/AI_academic_plan_corrected_v2.json",
        "data/ground_truth/AI_academic_plan_corrected.json",
        "data/ground_truth/AI_academic_plan_coop.json",
        "data/ground_truth/AI_academic_plan.json",
    ],
    "IT": [
        "data/ground_truth/IT_academic_plan_coop.json",
        "data/ground_truth/IT_academic_plan.json",
    ],
    "BIT": [
        "data/ground_truth/BIT_academic_plan_coop.json",
        "data/ground_truth/BIT_academic_plan.json",
    ],
}


PREDICTION_CANDIDATES = {
    "DSBA": [
        "outputs/DSBA/DSBA_extracted.json",
        "outputs/DSBA_extracted.json",
    ],
    "AI": [
        "outputs/AI/AI_extracted.json",
    ],
    "IT": [
        "outputs/IT/IT_extracted.json",
    ],
    "BIT": [
        "outputs/BIT/BIT_extracted.json",
    ],
}


def first_existing(
    root: Path,
    candidates: list[str],
) -> Path | None:
    for relative in candidates:
        path = root / relative
        if path.exists():
            return path
    return None


def paths_for(
    root: Path,
    program: str,
) -> dict[str, Path | None]:
    return {
        "gt": first_existing(
            root,
            GT_CANDIDATES[program],
        ),
        "prediction": first_existing(
            root,
            PREDICTION_CANDIDATES[program],
        ),
        "page_map": (
            root
            / "data"
            / "ground_truth"
            / f"{program}_page_map.csv"
        ),
        "output_dir": (
            root
            / "outputs"
            / "lab6"
            / program
        ),
    }


def run_program(
    root: Path,
    program: str,
) -> dict:
    paths = paths_for(
        root,
        program,
    )

    missing: list[str] = []

    if paths["gt"] is None:
        missing.append(
            "Ground Truth: "
            + " | ".join(
                GT_CANDIDATES[program]
            )
        )

    if paths["prediction"] is None:
        missing.append(
            "Prediction: "
            + " | ".join(
                PREDICTION_CANDIDATES[
                    program
                ]
            )
        )

    page_map = paths["page_map"]
    assert isinstance(page_map, Path)

    if not page_map.exists():
        missing.append(
            f"Page map: {page_map}"
        )

    if missing:
        print(
            f"\n[{program}] MISSING INPUT"
        )
        for item in missing:
            print(f"  - {item}")

        return {
            "program": program,
            "status": "MISSING_INPUT",
            "missing": missing,
        }

    gt = paths["gt"]
    prediction = paths["prediction"]
    output_dir = paths["output_dir"]

    assert isinstance(gt, Path)
    assert isinstance(prediction, Path)
    assert isinstance(output_dir, Path)

    cmd = [
        sys.executable,
        "-m",
        "ocr_system.lab6_evaluation",
        "--ground-truth",
        str(gt),
        "--prediction",
        str(prediction),
        "--page-map",
        str(page_map),
        "--output-dir",
        str(output_dir),
    ]

    print("\n" + "=" * 90)
    print(f"LAB 6 — {program}")
    print("=" * 90)

    completed = subprocess.run(cmd)

    if completed.returncode != 0:
        return {
            "program": program,
            "status": "FAILED",
            "returncode": (
                completed.returncode
            ),
        }

    report_path = (
        output_dir
        / "lab6_evaluation_report.json"
    )

    report = json.loads(
        report_path.read_text(
            encoding="utf-8"
        )
    )

    overall = report["overall"]

    return {
        "program": program,
        "status": "DONE",
        "gt_courses": overall.get(
            "total_ground_truth_courses"
        ),
        "prediction_courses": overall.get(
            "total_prediction_courses"
        ),
        "matched_courses": overall.get(
            "matched_courses"
        ),
        "missing_courses": overall.get(
            "missing_courses"
        ),
        "extra_predictions": overall.get(
            "extra_prediction_courses"
        ),
        "course_match_rate": overall.get(
            "course_match_rate"
        ),
        "exact_course_accuracy": overall.get(
            "exact_course_accuracy"
        ),
        "overall_field_accuracy": overall.get(
            "overall_field_accuracy"
        ),
        "program_match": overall.get(
            "program_match"
        ),
        "plan_match": overall.get(
            "plan_match"
        ),
        "report": str(report_path),
    }


def write_summary(
    root: Path,
    rows: list[dict],
) -> None:
    output_dir = (
        root
        / "outputs"
        / "lab6"
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    json_path = (
        output_dir
        / "all_programs_summary.json"
    )

    json_path.write_text(
        json.dumps(
            rows,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    columns = [
        "program",
        "status",
        "gt_courses",
        "prediction_courses",
        "matched_courses",
        "missing_courses",
        "extra_predictions",
        "course_match_rate",
        "exact_course_accuracy",
        "overall_field_accuracy",
        "program_match",
        "plan_match",
        "report",
        "missing",
    ]

    csv_path = (
        output_dir
        / "all_programs_summary.csv"
    )

    with csv_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=columns,
        )
        writer.writeheader()

        for row in rows:
            item = {
                key: row.get(key)
                for key in columns
            }

            if isinstance(
                item.get("missing"),
                list,
            ):
                item["missing"] = " | ".join(
                    item["missing"]
                )

            writer.writerow(item)

    print("\n" + "=" * 90)
    print("LAB 6 — ALL PROGRAMS SUMMARY")
    print("=" * 90)

    for row in rows:
        if row["status"] == "DONE":
            course = (
                float(
                    row.get(
                        "course_match_rate"
                    )
                    or 0
                )
                * 100
            )
            exact = (
                float(
                    row.get(
                        "exact_course_accuracy"
                    )
                    or 0
                )
                * 100
            )
            field = (
                float(
                    row.get(
                        "overall_field_accuracy"
                    )
                    or 0
                )
                * 100
            )

            print(
                f"{row['program']:5s} "
                f"| DONE "
                f"| GT={row.get('gt_courses')} "
                f"PRED={row.get('prediction_courses')} "
                f"MATCH={row.get('matched_courses')} "
                f"| course={course:.2f}% "
                f"exact={exact:.2f}% "
                f"field={field:.2f}%"
            )
        else:
            print(
                f"{row['program']:5s} "
                f"| {row['status']}"
            )

    print(f"\nSummary JSON: {json_path}")
    print(f"Summary CSV : {csv_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run Lab 6 for DSBA, AI, IT, "
            "and BIT."
        )
    )

    parser.add_argument(
        "--root",
        default=".",
        help="Project root.",
    )

    parser.add_argument(
        "--programs",
        nargs="+",
        choices=PROGRAMS,
        default=list(PROGRAMS),
    )

    args = parser.parse_args()

    root = Path(args.root).resolve()

    rows = [
        run_program(root, program)
        for program in args.programs
    ]

    write_summary(root, rows)

    failed = [
        row
        for row in rows
        if row["status"] != "DONE"
    ]

    if failed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
