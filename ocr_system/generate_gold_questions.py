from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Any


def credit_value(value: Any) -> int | None:
    if isinstance(value, int):
        return value
    m = re.match(r"\s*(\d+)", str(value or ""))
    return int(m.group(1)) if m else None


def from_ground_truth(path: Path, total_credits: int, years: int, limit: int) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    questions: list[dict] = [
        {"question": "หลักสูตรนี้มีทั้งหมดกี่หน่วยกิต", "expect": {"type": "value", "value": total_credits}},
        {"question": "หลักสูตรนี้ใช้เวลาเรียนกี่ปี", "expect": {"type": "value", "value": years}},
    ]

    seen: set[str] = set()
    courses = []
    for c in data.get("courses", []):
        code = str(c.get("code", "")).strip()
        if not re.fullmatch(r"\d{8}", code) or code in seen:
            continue
        seen.add(code)
        courses.append(c)

    # Use curated/ground-truth values, never the extracted database itself,
    # so the final evaluation is not circular.
    for c in courses:
        code = str(c["code"]).strip()
        credits = credit_value(c.get("credits"))
        name_th = str(c.get("name_th") or "").strip()
        name_en = str(c.get("name_en") or "").strip()
        if credits is not None:
            questions.append({
                "question": f"วิชา {code} มีกี่หน่วยกิต",
                "expect": {"type": "value", "value": credits},
            })
        if name_th:
            questions.append({
                "question": f"วิชา{name_th}มีรหัสอะไร",
                "expect": {"type": "value", "value": code},
            })
        if name_en:
            questions.append({
                "question": f"วิชา {code} ชื่อภาษาอังกฤษว่าอะไร",
                "expect": {"type": "value", "value": name_en},
            })
        if len(questions) >= limit:
            break

    if len(questions) < limit:
        raise SystemExit(f"Ground truth produced only {len(questions)} questions; need {limit}")
    return questions[:limit]


def from_database(db_path: Path, limit: int) -> list[dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    p = conn.execute("SELECT * FROM program LIMIT 1").fetchone()
    if not p:
        raise SystemExit(f"No program row in {db_path}")
    q = [
        {"question": "หลักสูตรนี้มีทั้งหมดกี่หน่วยกิต", "expect": {"type": "value", "value": p["total_credits"]}},
        {"question": "หลักสูตรนี้ใช้เวลาเรียนกี่ปี", "expect": {"type": "value", "value": p["years"]}},
    ]
    for c in conn.execute("SELECT code,name_th,name_en,credits FROM course ORDER BY code"):
        if not re.fullmatch(r"\d{8}", c["code"]):
            continue
        q.append({"question": f"วิชา {c['code']} มีกี่หน่วยกิต", "expect": {"type": "value", "value": c["credits"]}})
        if c["name_th"]:
            q.append({"question": f"วิชา{c['name_th']}มีรหัสอะไร", "expect": {"type": "value", "value": c["code"]}})
        if c["name_en"]:
            q.append({"question": f"วิชา {c['code']} ชื่อภาษาอังกฤษว่าอะไร", "expect": {"type": "value", "value": c["name_en"]}})
        if len(q) >= limit:
            break
    conn.close()
    if len(q) < limit:
        raise SystemExit(f"Database produced only {len(q)} questions; need {limit}")
    return q[:limit]


def main() -> None:
    ap = argparse.ArgumentParser(description="Build 30 grounded Lab 8B questions")
    ap.add_argument("--database")
    ap.add_argument("--ground-truth")
    ap.add_argument("--total-credits", type=int)
    ap.add_argument("--years", type=int, default=4)
    ap.add_argument("--output", required=True)
    ap.add_argument("--count", type=int, default=30)
    args = ap.parse_args()

    if args.ground_truth:
        if args.total_credits is None:
            raise SystemExit("--total-credits is required with --ground-truth")
        questions = from_ground_truth(Path(args.ground_truth), args.total_credits, args.years, args.count)
        origin = "ground_truth"
    elif args.database:
        questions = from_database(Path(args.database), args.count)
        origin = "database"
    else:
        raise SystemExit("Specify --ground-truth (recommended) or --database")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")
    (out.parent / "gold_questions.meta.json").write_text(
        json.dumps({"origin": origin, "count": len(questions)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {len(questions)} grounded questions ({origin}) -> {out}")


if __name__ == "__main__":
    main()
