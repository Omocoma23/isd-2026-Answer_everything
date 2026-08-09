import argparse
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any


FIELDS = [
    "code",
    "name_th",
    "name_en",
    "credits",
    "year",
    "semester",
    "category",
    "type",
    "prerequisite",
    "flexible_year_semester",
    "note",
]

THAI_DIGIT_TRANS = str.maketrans(
    "๐๑๒๓๔๕๖๗๘๙",
    "0123456789",
)

VALID_SIMPLE_CODES = {
    "06026xxx",
    "90644xxx",
    "9064xxxx",
    "xxxxxxxx",
}


def _normalize_text(value: Any) -> str:
    """Normalize representational differences only; do not repair semantic content."""
    if value is None:
        return ""

    text = unicodedata.normalize("NFC", str(value))
    text = text.translate(THAI_DIGIT_TRANS)
    text = text.replace("\u0e4d\u0e32", "\u0e33")
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()


def _normalize_code(value: Any) -> str:
    text = _normalize_text(value)
    if not text:
        return ""

    text = text.replace("×", "x")

    numbers = re.findall(r"\d{8}", text)
    if len(numbers) == 2 and (
        "หรือ" in text
        or re.search(r"\bor\b", text, re.IGNORECASE)
    ):
        return f"{numbers[0]}|{numbers[1]}"

    return re.sub(r"[\s|:;,_\-./\\]+", "", text)


def _normalize_credits(
    value: Any,
) -> str:

    text = _normalize_text(value)

    if not text:
        return ""

    matches = re.findall(
        r"(\d+)\s*"
        r"\(\s*"
        r"(\d+)\s*-\s*"
        r"(\d+)\s*-\s*"
        r"(\d+)\s*"
        r"\)",
        text,
    )

    if not matches:
        return re.sub(
            r"\s+",
            "",
            text,
        )

    credits = []

    for a, b, c, d in matches:

        credit = (
            f"{a}({b}-{c}-{d})"
        )

        if credit not in credits:
            credits.append(credit)

    # alternative credits ไม่มีลำดับ
    credits = sorted(credits)

    return "หรือ".join(credits)


def _normalize_flexible(value: Any) -> str:
    text = _normalize_text(value)
    if not text:
        return ""

    parts = [
        re.sub(r"\s+", "", part)
        for part in text.split(",")
        if part.strip()
    ]
    return ",".join(parts)


def normalize_value(
    field: str,
    value: Any,
) -> str:

    if field == "code":
        return _normalize_code(value)

    if field == "credits":
        return _normalize_credits(value)

    if field == "flexible_year_semester":
        return _normalize_flexible(value)

    if field == "name_th":

        text = _normalize_text(
            value
        )

        # ภาษาไทย whitespace มักเกิดจาก
        # line break / OCR segmentation
        return re.sub(
            r"\s+",
            "",
            text,
        )

    if field in {
        "year",
        "semester",
    }:

        text = _normalize_text(
            value
        )

        if not text:
            return ""

        try:
            return str(
                int(float(text))
            )

        except ValueError:
            return text

    return _normalize_text(value)


def _is_valid_course_code(value: Any) -> bool:
    code = _normalize_code(value)

    if re.fullmatch(r"\d{8}", code):
        return True
    if code in VALID_SIMPLE_CODES:
        return True
    if re.fullmatch(r"\d{8}\|\d{8}", code):
        return True
    return False


def _filter_course_rows(
    courses: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Ignore rows whose code cell is explanatory prose instead of a course code."""
    valid: list[dict[str, Any]] = []
    ignored: list[dict[str, Any]] = []

    for index, course in enumerate(courses):
        if not isinstance(course, dict):
            ignored.append({
                "index": index,
                "reason": "row is not an object",
                "row": course,
            })
            continue

        if not _is_valid_course_code(course.get("code")):
            ignored.append({
                "index": index,
                "reason": "invalid/non-course code",
                "row": course,
            })
            continue

        valid.append(course)

    return valid, ignored


def course_match(
    ground_truth: dict[str, Any],
    prediction: dict[str, Any],
) -> dict[str, bool]:
    result: dict[str, bool] = {}

    for field in FIELDS:
        result[field] = (
            normalize_value(field, ground_truth.get(field))
            == normalize_value(field, prediction.get(field))
        )

    return result


def _candidate_score(
    ground_truth: dict[str, Any],
    prediction: dict[str, Any],
) -> int:
    """Pick the best unmatched occurrence when a code appears more than once."""
    weights = {
        "year": 30,
        "semester": 30,
        "name_th": 12,
        "name_en": 10,
        "credits": 6,
        "flexible_year_semester": 6,
        "category": 3,
        "type": 3,
        "prerequisite": 2,
        "note": 1,
    }

    score = 0
    for field, weight in weights.items():
        if normalize_value(field, ground_truth.get(field)) == normalize_value(
            field,
            prediction.get(field),
        ):
            score += weight

    return score


def _occurrence_number(
    rows: list[dict[str, Any]],
    row_index: int,
) -> int:
    code = _normalize_code(rows[row_index].get("code"))
    year = normalize_value("year", rows[row_index].get("year"))
    semester = normalize_value("semester", rows[row_index].get("semester"))

    count = 0
    for i in range(row_index + 1):
        row = rows[i]
        if (
            _normalize_code(row.get("code")) == code
            and normalize_value("year", row.get("year")) == year
            and normalize_value("semester", row.get("semester")) == semester
        ):
            count += 1

    return count


def evaluate_courses(
    ground_truth_courses: list[dict[str, Any]],
    prediction_courses: list[dict[str, Any]],
) -> dict[str, Any]:

    gt_courses, ignored_gt = _filter_course_rows(ground_truth_courses)
    pred_courses, ignored_pred = _filter_course_rows(prediction_courses)

    prediction_by_code: dict[str, list[int]] = defaultdict(list)
    for pred_index, course in enumerate(pred_courses):
        prediction_by_code[_normalize_code(course.get("code"))].append(pred_index)

    used_prediction_indices: set[int] = set()
    total_gt = len(gt_courses)

    field_total = {field: total_gt for field in FIELDS}
    field_correct = {field: 0 for field in FIELDS}

    matched_courses = 0
    exact_course_matches = 0
    details: list[dict[str, Any]] = []

    for gt_index, gt_course in enumerate(gt_courses):
        code = _normalize_code(gt_course.get("code"))

        candidate_indices = [
            idx
            for idx in prediction_by_code.get(code, [])
            if idx not in used_prediction_indices
        ]

        occurrence = _occurrence_number(gt_courses, gt_index)

        if not candidate_indices:
            details.append({
                "gt_index": gt_index,
                "occurrence": occurrence,
                "code": code,
                "year": gt_course.get("year"),
                "semester": gt_course.get("semester"),
                "matched": False,
                "prediction_index": None,
                "fields": {field: False for field in FIELDS},
                "differences": {
                    field: {
                        "ground_truth": gt_course.get(field),
                        "prediction": None,
                    }
                    for field in FIELDS
                },
            })
            continue

        best_pred_index = max(
            candidate_indices,
            key=lambda idx: (
                _candidate_score(gt_course, pred_courses[idx]),
                -idx,
            ),
        )

        pred_course = pred_courses[best_pred_index]
        used_prediction_indices.add(best_pred_index)
        matched_courses += 1

        matches = course_match(gt_course, pred_course)

        for field in FIELDS:
            if matches[field]:
                field_correct[field] += 1

        exact_match = all(matches.values())
        if exact_match:
            exact_course_matches += 1

        differences = {
            field: {
                "ground_truth": gt_course.get(field),
                "prediction": pred_course.get(field),
            }
            for field in FIELDS
            if not matches[field]
        }

        details.append({
            "gt_index": gt_index,
            "occurrence": occurrence,
            "code": code,
            "year": gt_course.get("year"),
            "semester": gt_course.get("semester"),
            "matched": True,
            "prediction_index": best_pred_index,
            "exact_match": exact_match,
            "fields": matches,
            "differences": differences,
        })

    extra_predictions = []
    for pred_index, pred_course in enumerate(pred_courses):
        if pred_index in used_prediction_indices:
            continue

        extra_predictions.append({
            "prediction_index": pred_index,
            "code": pred_course.get("code"),
            "year": pred_course.get("year"),
            "semester": pred_course.get("semester"),
            "course": pred_course,
        })

    missing_courses = total_gt - matched_courses

    field_accuracy = {
        field: (
            field_correct[field] / field_total[field]
            if field_total[field]
            else 0.0
        )
        for field in FIELDS
    }

    total_field_checks = sum(field_total.values())
    total_field_correct = sum(field_correct.values())

    overall_accuracy = (
        total_field_correct / total_field_checks
        if total_field_checks
        else 0.0
    )

    course_match_rate = matched_courses / total_gt if total_gt else 0.0
    exact_course_accuracy = exact_course_matches / total_gt if total_gt else 0.0

    return {
        "total_ground_truth_courses": total_gt,
        "total_prediction_courses": len(pred_courses),
        "ignored_ground_truth_rows": ignored_gt,
        "ignored_prediction_rows": ignored_pred,
        "matched_courses": matched_courses,
        "missing_courses": missing_courses,
        "extra_prediction_courses": len(extra_predictions),
        "course_match_rate": course_match_rate,
        "exact_course_matches": exact_course_matches,
        "exact_course_accuracy": exact_course_accuracy,
        "field_correct": field_correct,
        "field_total": field_total,
        "field_accuracy": field_accuracy,
        "overall_field_accuracy": overall_accuracy,
        "details": details,
        "extra_predictions": extra_predictions,
    }


def evaluate_from_files(
    ground_truth_json: str | Path,
    prediction_json: str | Path,
) -> dict[str, Any]:

    ground_truth_json = Path(ground_truth_json)
    prediction_json = Path(prediction_json)

    with ground_truth_json.open("r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    with prediction_json.open("r", encoding="utf-8") as f:
        prediction = json.load(f)

    result = evaluate_courses(
        ground_truth.get("courses", []),
        prediction.get("courses", []),
    )

    result["ground_truth_file"] = str(ground_truth_json)
    result["prediction_file"] = str(prediction_json)
    result["program_match"] = (
        _normalize_text(ground_truth.get("program"))
        == _normalize_text(prediction.get("program"))
    )
    result["plan_match"] = (
        _normalize_text(ground_truth.get("plan"))
        == _normalize_text(prediction.get("plan"))
    )

    return result


def _percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def print_summary(result: dict[str, Any]) -> None:
    print("=" * 64)
    print("STRUCTURED CURRICULUM EVALUATION")
    print("=" * 64)
    print("Ground Truth courses :", result["total_ground_truth_courses"])
    print("Prediction courses   :", result["total_prediction_courses"])
    print("Matched occurrences  :", result["matched_courses"])
    print("Missing courses      :", result["missing_courses"])
    print("Extra predictions    :", result["extra_prediction_courses"])
    print("Course match rate    :", _percent(result["course_match_rate"]))
    print("Exact course accuracy:", _percent(result["exact_course_accuracy"]))
    print("Overall field accuracy:", _percent(result["overall_field_accuracy"]))
    print("Program match        :", result["program_match"])
    print("Plan match           :", result["plan_match"])

    ignored_gt = result.get("ignored_ground_truth_rows", [])
    if ignored_gt:
        print("Ignored GT non-course rows:", len(ignored_gt))

    ignored_pred = result.get("ignored_prediction_rows", [])
    if ignored_pred:
        print("Ignored prediction non-course rows:", len(ignored_pred))

    print("\nFIELD ACCURACY")
    for field in FIELDS:
        correct = result["field_correct"][field]
        total = result["field_total"][field]
        accuracy = result["field_accuracy"][field]
        print(f"  {field:24s} {correct:>3}/{total:<3} {_percent(accuracy)}")

    missing = [item for item in result["details"] if not item["matched"]]
    if missing:
        print("\nMISSING FROM PREDICTION")
        for item in missing:
            print(
                " ",
                item["code"],
                f"year={item['year']}",
                f"semester={item['semester']}",
                f"occurrence={item['occurrence']}",
            )

    wrong = [
        item
        for item in result["details"]
        if item["matched"] and not item.get("exact_match", False)
    ]
    if wrong:
        print("\nMATCHED COURSES WITH FIELD ERRORS")
        for item in wrong:
            fields = ", ".join(item["differences"].keys())
            print(
                " ",
                item["code"],
                f"year={item['year']}",
                f"semester={item['semester']}",
                f"occurrence={item['occurrence']}",
                f"wrong=[{fields}]",
            )

    extras = result.get("extra_predictions", [])
    if extras:
        print("\nEXTRA PREDICTIONS")
        for item in extras:
            print(
                " ",
                item["code"],
                f"year={item['year']}",
                f"semester={item['semester']}",
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate structured curriculum extraction JSON against Ground Truth."
    )
    parser.add_argument("ground_truth_json", help="Path to Ground Truth JSON")
    parser.add_argument("prediction_json", help="Path to extracted/prediction JSON")
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to save detailed evaluation JSON",
    )
    args = parser.parse_args()

    result = evaluate_from_files(
        args.ground_truth_json,
        args.prediction_json,
    )
    print_summary(result)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("\nSaved detailed evaluation:", output_path)


if __name__ == "__main__":
    main()
