from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path
from difflib import SequenceMatcher


THAI_DIGIT_TRANS = str.maketrans(
    "๐๑๒๓๔๕๖๗๘๙",
    "0123456789",
)

COURSE_CODE_RE = re.compile(
    r"^(?:"
    r"\d{8}"
    r"|\d{6}x{2}"
    r"|\d{5}x{3}"
    r"|\d{4}x{4}"
    r"|x{8}"
    r"|\d{8}\|\d{8}"
    r")$",
    re.IGNORECASE,
)

PROFILES = {
    "AI": {
        "plan_pages": range(23, 27),       # PDF 23-26
        "catalog_pages": range(21, 23),    # PDF 21-22
        "curriculum_offset": -4,           # PDF 23 = printed page 19
        "semester_fallback": {
            (1, 1): 23,
            (1, 2): 23,
            (2, 1): 24,
            (2, 2): 24,
            (3, 1): 25,
            (3, 2): 25,
            (4, 1): 26,
            (4, 2): 26,
        },
    },
    "IT": {
        "plan_pages": range(38, 45),       # PDF 38-44
        "catalog_pages": range(26, 30),    # PDF 26-29
        "curriculum_offset": -5,           # PDF 38 = printed page 33
        "semester_fallback": {
            (1, 1): 38,
            (1, 2): 39,
            (2, 1): 40,
            (2, 2): 41,
            (3, 1): 42,
            (3, 2): 42,
            (4, 1): 43,
            (4, 2): 44,
        },
    },
    "BIT": {
        "plan_pages": range(31, 36),       # PDF 31-35
        "catalog_pages": range(22, 26),    # PDF 22-25
        "curriculum_offset": -5,           # PDF 31 = printed page 26
        "semester_fallback": {
            (1, 1): 31,
            (1, 2): 32,
            (2, 1): 32,
            (2, 2): 33,
            (3, 1): 33,
            (3, 2): 34,
            (4, 1): 35,
            (4, 2): 35,
        },
    },
}


def normalize(value: object) -> str:
    if value is None:
        return ""

    text = unicodedata.normalize("NFC", str(value))
    text = text.translate(THAI_DIGIT_TRANS)
    text = text.replace("\u0e4d\u0e32", "\u0e33")
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compact(value: object) -> str:
    text = normalize(value)
    return re.sub(r"[^0-9a-z\u0e00-\u0e7f]+", "", text)


def normalize_code(value: object) -> str:
    text = normalize(value).replace("×", "x")
    nums = re.findall(r"\d{8}", text)

    if len(nums) == 2 and (
        "หรือ" in text
        or re.search(r"\bor\b", text)
        or "|" in text
    ):
        return f"{nums[0]}|{nums[1]}"

    return re.sub(r"[\s,:;_\-./\\]+", "", text)


def is_course_row(row: dict) -> bool:
    return bool(
        COURSE_CODE_RE.fullmatch(
            normalize_code(row.get("code"))
        )
    )


def page_text(page: dict) -> str:
    parts: list[str] = []

    text = str(page.get("text", "") or "")
    if text:
        parts.append(text)

    for line in page.get("lines", []) or []:
        if isinstance(line, dict):
            value = str(line.get("text", "") or "")
        else:
            value = str(line)
        if value:
            parts.append(value)

    return "\n".join(parts)


def load_pages(prediction_path: Path) -> dict[int, str]:
    payload = json.loads(
        prediction_path.read_text(encoding="utf-8")
    )

    result: dict[int, str] = {}

    for index, page in enumerate(
        payload.get("pages", []),
        start=1,
    ):
        page_no = int(page.get("page", index))
        result[page_no] = page_text(page)

    if not result:
        raise ValueError(
            f"No pages found in {prediction_path}"
        )

    return result


def exact_code_score(
    code: str,
    text: str,
) -> tuple[int, list[str]]:
    norm_text = normalize(text)
    evidence: list[str] = []
    score = 0

    numbers = re.findall(r"\d{8}", code)

    if numbers:
        found = [
            number
            for number in numbers
            if re.search(
                rf"(?<!\d){re.escape(number)}(?!\d)",
                norm_text,
            )
        ]

        if found:
            score += 100 * len(found)
            evidence.extend(found)

        if len(numbers) == 2 and len(found) == 2:
            score += 100

        return score, evidence

    # Placeholder codes such as 060464xx / 9064xxxx / xxxxxxxx.
    needle = compact(code)
    haystack = compact(text)

    if needle and needle in haystack:
        score += 100
        evidence.append(code)

    return score, evidence


def name_similarity_score(
    row: dict,
    text: str,
) -> tuple[float, str]:
    hay = compact(text)

    if not hay:
        return 0.0, ""

    best = 0.0
    best_label = ""

    for field in ("name_en", "name_th"):
        value = compact(row.get(field))

        if len(value) < 5:
            continue

        # Exact compact occurrence is strong evidence.
        if value in hay:
            return 80.0, f"{field}:exact"

        # Compare the course name with windows around its approximate length.
        window_len = max(len(value), 8)
        step = max(window_len // 5, 1)

        if len(hay) <= window_len:
            ratio = SequenceMatcher(
                None,
                value,
                hay,
            ).ratio()
        else:
            ratio = 0.0
            for start in range(
                0,
                max(len(hay) - window_len + 1, 1),
                step,
            ):
                window = hay[
                    start:start + window_len + 20
                ]
                ratio = max(
                    ratio,
                    SequenceMatcher(
                        None,
                        value,
                        window,
                    ).ratio(),
                )

        candidate = ratio * 40.0

        if candidate > best:
            best = candidate
            best_label = (
                f"{field}:similarity={ratio:.2f}"
            )

    return best, best_label


def map_row(
    row: dict,
    pages: dict[int, str],
    profile: dict,
) -> dict:
    code = normalize_code(row.get("code"))

    try:
        year = int(row.get("year") or 0)
    except (TypeError, ValueError):
        year = 0

    try:
        semester = int(row.get("semester") or 0)
    except (TypeError, ValueError):
        semester = 0

    is_flexible = year == 0 and semester == 0

    if is_flexible:
        candidates = list(
            profile["catalog_pages"]
        )
        section = "catalog"
    else:
        candidates = list(
            profile["plan_pages"]
        )
        section = "academic_plan"

    scored: list[
        tuple[float, int, str]
    ] = []

    for page_no in candidates:
        text = pages.get(page_no, "")

        if not text:
            continue

        code_score, code_evidence = (
            exact_code_score(code, text)
        )
        name_score, name_evidence = (
            name_similarity_score(row, text)
        )

        score = float(code_score) + name_score

        evidence = ",".join(
            code_evidence
            + (
                [name_evidence]
                if name_evidence
                else []
            )
        )

        scored.append(
            (score, page_no, evidence)
        )

    scored.sort(
        key=lambda item: (-item[0], item[1])
    )

    selected_page: int | None = None
    method = ""
    score = 0.0
    evidence = ""

    if scored and scored[0][0] >= 70:
        score, selected_page, evidence = scored[0]
        method = "source_match"

    elif not is_flexible:
        fallback = profile[
            "semester_fallback"
        ].get((year, semester))

        if fallback is not None:
            selected_page = fallback
            method = "semester_fallback"
            score = (
                scored[0][0]
                if scored
                else 0.0
            )
            evidence = (
                scored[0][2]
                if scored
                else ""
            )

    if selected_page is None:
        return {
            "pdf_page": "UNMAPPED",
            "curriculum_page": "UNMAPPED",
            "source_section": section,
            "mapping_method": "UNMAPPED",
            "mapping_score": round(score, 2),
            "evidence": evidence,
        }

    curriculum_page = (
        selected_page
        + int(
            profile["curriculum_offset"]
        )
    )

    return {
        "pdf_page": selected_page,
        "curriculum_page": curriculum_page,
        "source_section": section,
        "mapping_method": method,
        "mapping_score": round(score, 2),
        "evidence": evidence,
    }


def build_page_map(
    program: str,
    gt_path: Path,
    prediction_path: Path,
    output_path: Path,
) -> None:
    program = program.upper()

    if program not in PROFILES:
        raise ValueError(
            f"Unsupported program: {program}"
        )

    profile = PROFILES[program]

    gt = json.loads(
        gt_path.read_text(encoding="utf-8")
    )

    gt_courses = [
        row
        for row in gt.get("courses", [])
        if is_course_row(row)
    ]

    pages = load_pages(prediction_path)

    rows: list[dict] = []

    for gt_index, row in enumerate(gt_courses):
        mapped = map_row(
            row,
            pages,
            profile,
        )

        rows.append({
            "gt_index": gt_index,
            "code": normalize_code(
                row.get("code")
            ),
            "year": row.get("year"),
            "semester": row.get("semester"),
            **mapped,
        })

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "gt_index",
        "code",
        "year",
        "semester",
        "pdf_page",
        "curriculum_page",
        "source_section",
        "mapping_method",
        "mapping_score",
        "evidence",
    ]

    with output_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)

    unmapped = [
        row
        for row in rows
        if row["pdf_page"] == "UNMAPPED"
    ]

    fallback = [
        row
        for row in rows
        if row["mapping_method"]
        == "semester_fallback"
    ]

    print(
        f"\n[{program}] "
        f"GT={len(gt_courses)} "
        f"mapped={len(rows) - len(unmapped)} "
        f"unmapped={len(unmapped)} "
        f"fallback={len(fallback)}"
    )
    print(f"Saved: {output_path}")

    if fallback:
        print(
            "  REVIEW semester_fallback rows:"
        )
        for row in fallback:
            print(
                f"    gt_index={row['gt_index']} "
                f"code={row['code']} "
                f"-> PDF {row['pdf_page']}"
            )

    if unmapped:
        print("  UNMAPPED rows:")
        for row in unmapped:
            print(
                f"    gt_index={row['gt_index']} "
                f"code={row['code']}"
            )


def first_existing(
    root: Path,
    candidates: list[str],
) -> Path | None:
    for value in candidates:
        path = root / value
        if path.exists():
            return path
    return None


def run_all(root: Path) -> None:
    configs = {
        "AI": {
            "gt": [
                "data/ground_truth/AI_academic_plan_corrected_v2.json",
                "data/ground_truth/AI_academic_plan_corrected.json",
                "data/ground_truth/AI_academic_plan_coop.json",
                "data/ground_truth/AI_academic_plan.json",
            ],
            "prediction": [
                "outputs/AI/AI_prediction_repaired.json",
                "outputs/AI/AI_prediction.json",
            ],
        },
        "IT": {
            "gt": [
                "data/ground_truth/IT_academic_plan_coop.json",
                "data/ground_truth/IT_academic_plan.json",
            ],
            "prediction": [
                "outputs/IT/IT_prediction_repaired.json",
                "outputs/IT/IT_prediction.json",
            ],
        },
        "BIT": {
            "gt": [
                "data/ground_truth/BIT_academic_plan_coop.json",
                "data/ground_truth/BIT_academic_plan.json",
            ],
            "prediction": [
                "outputs/BIT/BIT_prediction_repaired.json",
                "outputs/BIT/BIT_prediction.json",
            ],
        },
    }

    failed = False

    for program, config in configs.items():
        gt = first_existing(
            root,
            config["gt"],
        )
        pred = first_existing(
            root,
            config["prediction"],
        )

        if gt is None or pred is None:
            failed = True
            print(
                f"\n[{program}] MISSING INPUT"
            )
            print(
                "  GT:",
                gt
                if gt
                else "not found",
            )
            print(
                "  Prediction:",
                pred
                if pred
                else "not found",
            )
            continue

        output = (
            root
            / "data"
            / "ground_truth"
            / f"{program}_page_map.csv"
        )

        build_page_map(
            program,
            gt,
            pred,
            output,
        )

    if failed:
        raise SystemExit(2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build Lab 6 page-map CSV files from "
            "GT + existing OCR prediction JSON. "
            "No OCR rerun is required."
        )
    )

    parser.add_argument(
        "--root",
        default=".",
        help="Project root",
    )
    parser.add_argument(
        "--program",
        choices=["AI", "IT", "BIT"],
    )
    parser.add_argument("--gt")
    parser.add_argument("--prediction")
    parser.add_argument("--output")

    args = parser.parse_args()
    root = Path(args.root).resolve()

    if args.program:
        if not (
            args.gt
            and args.prediction
            and args.output
        ):
            parser.error(
                "--program requires "
                "--gt --prediction --output"
            )

        build_page_map(
            args.program,
            Path(args.gt),
            Path(args.prediction),
            Path(args.output),
        )
        return

    run_all(root)


if __name__ == "__main__":
    main()
