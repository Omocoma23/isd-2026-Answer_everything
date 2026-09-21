#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from ocr_system.evaluation import (
    FIELDS,
    evaluate_from_files,
    _filter_course_rows,
)


def load_page_map(path: Path | None) -> dict[int, dict[str, str]]:
    if path is None:
        return {}
    result: dict[int, dict[str, str]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            result[int(row["gt_index"])] = row
    return result


def aggregate(indices: list[int], details: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(indices)
    matched = sum(1 for i in indices if details[i].get("matched"))
    exact = sum(1 for i in indices if details[i].get("exact_match", False))
    field_correct = {
        field: sum(1 for i in indices if details[i]["fields"].get(field, False))
        for field in FIELDS
    }
    row: dict[str, Any] = {
        "gt_courses": n,
        "matched_courses": matched,
        "missing_courses": n - matched,
        "course_match_rate": matched / n if n else 0.0,
        "exact_course_matches": exact,
        "exact_course_accuracy": exact / n if n else 0.0,
        "overall_field_accuracy": (
            sum(field_correct.values()) / (n * len(FIELDS)) if n else 0.0
        ),
    }
    for field in FIELDS:
        row[f"{field}_accuracy"] = field_correct[field] / n if n else 0.0
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def print_report(
    overall: dict[str, Any],
    field_rows: list[dict[str, Any]],
    page_rows: list[dict[str, Any]],
    category_rows: list[dict[str, Any]],
) -> None:
    pct = lambda x: f"{100 * float(x or 0):.2f}%"
    print("=" * 78)
    print("LAB 6 — FIELD / PAGE / CATEGORY EVALUATION")
    print("=" * 78)
    print(f"GT courses            : {overall['total_ground_truth_courses']}")
    print(f"Prediction courses    : {overall['total_prediction_courses']}")
    print(f"Matched courses       : {overall['matched_courses']}")
    print(f"Missing courses       : {overall['missing_courses']}")
    print(f"Extra predictions     : {overall['extra_prediction_courses']}")
    print(f"Course match rate     : {pct(overall['course_match_rate'])}")
    print(f"Exact course accuracy : {pct(overall['exact_course_accuracy'])}")
    print(f"Overall field accuracy: {pct(overall['overall_field_accuracy'])}")

    print("\n[FIELD LEVEL]")
    for row in field_rows:
        print(
            f"{row['field']:24s} "
            f"{row['correct']:>3}/{row['total']:<3} {pct(row['accuracy'])}"
        )

    print("\n[PAGE LEVEL]")
    for row in page_rows:
        print(
            f"PDF {str(row['pdf_page']):>8} | GT={row['gt_courses']:>2} "
            f"| matched={row['matched_courses']:>2} "
            f"| course={pct(row['course_match_rate'])} "
            f"| field={pct(row['overall_field_accuracy'])}"
        )

    print("\n[CATEGORY LEVEL]")
    for row in category_rows:
        print(
            f"{row['category']} | GT={row['gt_courses']} "
            f"| matched={row['matched_courses']} "
            f"| course={pct(row['course_match_rate'])} "
            f"| field={pct(row['overall_field_accuracy'])}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lab 6 evaluator: Field Level, Page Level and Category Level"
    )
    parser.add_argument("--ground-truth", required=True)
    parser.add_argument("--prediction", required=True)
    parser.add_argument("--page-map")
    parser.add_argument("--output-dir", default="outputs/lab6")
    args = parser.parse_args()

    gt_path = Path(args.ground_truth)
    gt = json.loads(gt_path.read_text(encoding="utf-8"))
    gt_courses, _ = _filter_course_rows(gt.get("courses", []))

    result = evaluate_from_files(args.ground_truth, args.prediction)
    details = result["details"]
    if len(details) != len(gt_courses):
        raise ValueError(
            f"Evaluation details ({len(details)}) do not align with valid GT rows "
            f"({len(gt_courses)})."
        )

    field_rows = [
        {
            "field": field,
            "correct": result["field_correct"][field],
            "total": result["field_total"][field],
            "accuracy": result["field_accuracy"][field],
            "accuracy_percent": round(result["field_accuracy"][field] * 100, 2),
        }
        for field in FIELDS
    ]

    page_map = load_page_map(Path(args.page_map) if args.page_map else None)
    page_groups: dict[tuple[str, str], list[int]] = defaultdict(list)
    for i in range(len(gt_courses)):
        meta = page_map.get(i, {})
        key = (
            meta.get("pdf_page", "UNMAPPED"),
            meta.get("curriculum_page", "UNMAPPED"),
        )
        page_groups[key].append(i)

    def page_key(item: tuple[tuple[str, str], list[int]]):
        p = str(item[0][0])
        return (999999 if not p.isdigit() else int(p), p)

    page_rows = [
        {
            "pdf_page": pdf_page,
            "curriculum_page": curriculum_page,
            **aggregate(indices, details),
        }
        for (pdf_page, curriculum_page), indices
        in sorted(page_groups.items(), key=page_key)
    ]

    category_groups: dict[str, list[int]] = defaultdict(list)
    for i, course in enumerate(gt_courses):
        category_groups[course.get("category") or "(ว่าง)"].append(i)

    category_rows = [
        {"category": category, **aggregate(indices, details)}
        for category, indices in sorted(category_groups.items())
    ]

    overall_keys = [
        "total_ground_truth_courses", "total_prediction_courses",
        "matched_courses", "missing_courses", "extra_prediction_courses",
        "course_match_rate", "exact_course_matches", "exact_course_accuracy",
        "overall_field_accuracy", "program_match", "plan_match",
    ]
    overall = {key: result.get(key) for key in overall_keys}

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "field_level.csv", field_rows)
    write_csv(out / "page_level.csv", page_rows)
    write_csv(out / "category_level.csv", category_rows)

    report = {
        "overall": overall,
        "field_level": field_rows,
        "page_level": page_rows,
        "category_level": category_rows,
    }
    (out / "lab6_evaluation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print_report(overall, field_rows, page_rows, category_rows)


if __name__ == "__main__":
    main()