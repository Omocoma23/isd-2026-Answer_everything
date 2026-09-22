from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Standardize only the top-level AI Ground Truth metadata "
            "for evaluation. Course rows are not modified."
        )
    )
    parser.add_argument(
        "input_gt",
        help="AI corrected Ground Truth JSON",
    )
    parser.add_argument(
        "--output",
        default="data/ground_truth/AI_academic_plan_corrected_v2.json",
    )
    parser.add_argument(
        "--program",
        default="AI",
    )
    parser.add_argument(
        "--plan",
        default="coop",
    )
    args = parser.parse_args()

    src = Path(args.input_gt)
    data = json.loads(src.read_text(encoding="utf-8"))

    print("Before:")
    print("  program =", repr(data.get("program")))
    print("  plan    =", repr(data.get("plan")))
    print("  courses =", len(data.get("courses", [])))

    # Only standardize metadata used by evaluation.py.
    # Never change course rows here.
    data["program"] = args.program
    data["plan"] = args.plan

    dst = Path(args.output)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\nAfter:")
    print("  program =", repr(data.get("program")))
    print("  plan    =", repr(data.get("plan")))
    print("  courses =", len(data.get("courses", [])))
    print("\nSaved:", dst)


if __name__ == "__main__":
    main()
