from __future__ import annotations

import argparse
import json
from pathlib import Path


SUSPICIOUS_CODE = "06016401"
EXPECTED_NAME_EN = "MATHEMATICS FOR INFORMATION TECHNOLOGY"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit/fix the suspicious IT-prefix row in an AI Ground Truth file. "
            "By default this only audits. Use --apply to write a corrected copy."
        )
    )
    parser.add_argument("input_gt", help="AI Ground Truth JSON")
    parser.add_argument(
        "--output",
        default="data/ground_truth/AI_academic_plan_corrected.json",
        help="Output corrected GT JSON",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually remove the suspicious row and write a new GT copy.",
    )
    args = parser.parse_args()

    src = Path(args.input_gt)
    payload = json.loads(src.read_text(encoding="utf-8"))

    courses = payload.get("courses", [])
    matches = [
        (i, row)
        for i, row in enumerate(courses)
        if str(row.get("code", "")).strip() == SUSPICIOUS_CODE
    ]

    if not matches:
        print(f"{SUSPICIOUS_CODE}: not found. Nothing to fix.")
        return

    print(f"Found {len(matches)} suspicious row(s):")
    for index, row in matches:
        print(f"\nGT index = {index}")
        print(json.dumps(row, ensure_ascii=False, indent=2))

    # Safety: do not silently delete an arbitrary 06016401 row.
    safe_matches = [
        (i, row)
        for i, row in matches
        if str(row.get("name_en", "")).strip().upper() == EXPECTED_NAME_EN
        and str(row.get("year", "")).strip() == "1"
        and str(row.get("semester", "")).strip() == "1"
    ]

    if len(safe_matches) != 1:
        raise SystemExit(
            "\nRefusing to modify the GT automatically because the suspicious "
            "row did not match the expected signature exactly."
        )

    if not args.apply:
        print(
            "\nAUDIT ONLY: no file was changed.\n"
            "If this GT is your own/team-created GT and you have verified that "
            "06016401 does not belong to the AI curriculum, rerun with --apply."
        )
        return

    remove_index = safe_matches[0][0]
    corrected = dict(payload)
    corrected["courses"] = [
        row for i, row in enumerate(courses)
        if i != remove_index
    ]

    dst = Path(args.output)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(
        json.dumps(corrected, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\nRemoved GT index {remove_index}: {SUSPICIOUS_CODE}")
    print(f"Saved corrected GT: {dst}")
    print(f"Courses: {len(corrected['courses'])}")


if __name__ == "__main__":
    main()
