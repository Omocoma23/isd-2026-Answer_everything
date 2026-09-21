from __future__ import annotations

import json
from pathlib import Path


PROGRAMS = ("AI", "IT", "BIT")


def main() -> None:
    root = Path(".").resolve()

    print("=" * 80)
    print("LAB 6 FINAL READINESS")
    print("=" * 80)

    ready_all = True

    for program in PROGRAMS:
        path = root / "outputs" / program / f"{program}_evaluation.json"

        if not path.exists():
            print(f"{program}: NOT READY - missing {path}")
            ready_all = False
            continue

        d = json.loads(path.read_text(encoding="utf-8"))

        gt = d.get("total_ground_truth_courses", 0)
        pred = d.get("total_prediction_courses", 0)
        missing = d.get("missing_courses", 0)
        extra = d.get("extra_prediction_courses", 0)
        program_match = d.get("program_match")
        plan_match = d.get("plan_match")

        structural = (
            gt == pred
            and missing == 0
            and extra == 0
            and program_match is True
            and plan_match is True
        )

        print(
            f"{program}: "
            f"GT={gt} PRED={pred} "
            f"missing={missing} extra={extra} "
            f"program_match={program_match} "
            f"plan_match={plan_match}"
        )

        if not structural:
            ready_all = False

    print("\nPage maps:")
    for program in PROGRAMS:
        page_map = root / "data" / "ground_truth" / f"{program}_page_map.csv"
        ok = page_map.exists()
        print(f"{program}: {'FOUND' if ok else 'MISSING'} -> {page_map}")
        if not ok:
            ready_all = False

    print()
    if ready_all:
        print("READY: AI / IT / BIT are ready for Lab 6.")
    else:
        print("NOT READY: fix the items shown above before final Lab 6.")


if __name__ == "__main__":
    main()
