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


def _ground_truth_plan_slots(data: dict) -> list[dict[str, Any]]:
    """Normalize Ground Truth rows into plan slots and their course codes."""
    slots: list[dict[str, Any]] = []
    for source in data.get("courses", []):
        try:
            year = int(source.get("year") or 0)
            semester = int(source.get("semester") or 0)
        except (TypeError, ValueError):
            continue

        credits = credit_value(source.get("credits"))
        raw_code = str(source.get("code") or "").strip()
        codes = [code.lower() for code in re.findall(
            r"(?<![0-9xX])[0-9xX]{8}(?![0-9xX])", raw_code,
        )]
        if year < 1 or semester < 1 or credits is None or not codes:
            continue

        name_th = re.sub(r"\s+", " ", str(source.get("name_th") or "")).strip()
        slots.append({
            "year": year,
            "semester": semester,
            "codes": codes,
            "name_th": name_th,
            "credits": credits,
            "source": source,
        })
    return slots


def _slot_rows(slots: list[dict[str, Any]], *, include_term: bool = False) -> list[dict[str, Any]]:
    """Expand alternative codes into the rows returned by v_plan."""
    result = []
    for slot in slots:
        for code in slot["codes"]:
            row = {
                "code": code,
                "name_th": slot["name_th"] or code,
                "credits": slot["credits"],
            }
            if include_term:
                row = {
                    "year": slot["year"],
                    "semester": slot["semester"],
                    **row,
                }
            result.append(row)
    return result


def intermediate_questions(data: dict) -> list[dict]:
    slots = _ground_truth_plan_slots(data)
    questions: list[dict] = []

    def slots_in(year: int, semester: int) -> list[dict[str, Any]]:
        return [s for s in slots if s["year"] == year and s["semester"] == semester]

    def add_rows(question: str, rows: list[dict[str, Any]]) -> None:
        if rows:
            questions.append({"question": question, "expect": {"type": "rows", "value": rows}})

    # 1) รายชื่อวิชาในเทอมเดียว
    term_1_1 = slots_in(1, 1)
    add_rows(
        "ตามแผนการศึกษา ปี 1 เทอม 1 มีวิชาอะไรบ้าง ขอรหัส ชื่อวิชา และหน่วยกิตของแต่ละวิชา",
        _slot_rows(term_1_1),
    )

    # 2) รายชื่อวิชาสองเทอม โดยเก็บปีและเทอมไว้ตรวจการแยกกลุ่ม
    year_1_terms = [s for s in slots if s["year"] == 1 and s["semester"] in (1, 2)]
    add_rows(
        "ปี 1 มีวิชาอะไรบ้างในเทอม 1 และเทอม 2 ช่วยแยกรายชื่อ รหัส และหน่วยกิตตามเทอม",
        _slot_rows(year_1_terms, include_term=True),
    )

    # 3) นับจำนวนช่องเรียนและรวมหน่วยกิตจากเทอมเดียว
    if term_1_1:
        questions.append({
            "question": "ปี 1 เทอม 1 มีทั้งหมดกี่วิชา และมีหน่วยกิตรวมเท่าไร",
            "expect": {
                "type": "rows",
                "value": [{
                    "course_count": len(term_1_1),
                    "total_credits": sum(s["credits"] for s in term_1_1),
                }],
            },
        })

    # 4) เปรียบเทียบจำนวนวิชาในสองเทอมของปี 1
    term_1_2 = slots_in(1, 2)
    if term_1_1 and term_1_2:
        count_1, count_2 = len(term_1_1), len(term_1_2)
        questions.append({
            "question": "ปี 1 เทอม 1 กับเทอม 2 เทอมไหนมีวิชามากกว่า และต่างกันกี่วิชา",
            "expect": {
                "type": "rows",
                "value": [{
                    "term1_course_count": count_1,
                    "term2_course_count": count_2,
                    "semester_with_more": 1 if count_1 > count_2 else 2 if count_2 > count_1 else 0,
                    "difference": abs(count_1 - count_2),
                }],
            },
        })

    # 5) ค้นตำแหน่งของวิชาจากรหัส
    placed_course = next((
        (slot, code)
        for slot in slots
        for code in slot["codes"]
        if re.fullmatch(r"\d{8}", code)
    ), None)
    if placed_course:
        slot, code = placed_course
        matching_slots = [s for s in slots if code in s["codes"]]
        add_rows(
            f"วิชา {code} อยู่ในแผนการเรียนปีไหน เทอมไหน และมีชื่อกับหน่วยกิตเท่าไร",
            _slot_rows(matching_slots, include_term=True),
        )

    # 6) ตรวจคำถามวิชาเลือกในเทอม 1/1 ตามตัวอย่างที่เลือกไว้.
    # Ground Truth บางหลักสูตรอาจไม่มีรายการในเทอมนี้; เก็บ expected ว่างไว้
    # เพื่อให้การประเมินแยก "ไม่มีรายการ" ออกจาก SQL ที่คืนผลเกินจริงได้.
    elective_slots = [s for s in slots if (
        "เลือก" in " ".join(str(s["source"].get(k) or "") for k in ("type", "category", "name_th"))
        or any("x" in code for code in s["codes"])
        or len(s["codes"]) > 1
    )]
    first_term_electives = [
        s for s in elective_slots
        if (s["year"], s["semester"]) == (1, 1)
    ]
    questions.append({
        "question": "ปี 1 เทอม 1 มีวิชาเลือกอะไรบ้าง และมีตัวเลือกใดให้เลือกแทนกันได้",
        "expect": {
            "type": "rows",
            "value": _slot_rows(first_term_electives, include_term=True),
        },
    })

    # เพิ่มเคสผลลัพธ์ที่มีข้อมูลจริงด้วย หากเทอมแรกไม่มีวิชาเลือกให้แสดง
    if elective_slots:
        elective_term = min((s["year"], s["semester"]) for s in elective_slots)
        year, semester = elective_term
        same_term_electives = [
            s for s in elective_slots
            if (s["year"], s["semester"]) == elective_term
        ]
        if elective_term != (1, 1):
            add_rows(
                f"ปี {year} เทอม {semester} มีวิชาเลือกอะไรบ้าง และมีตัวเลือกใดให้เลือกแทนกันได้",
                _slot_rows(same_term_electives, include_term=True),
            )

    return questions

def from_ground_truth(path: Path, total_credits: int, years: int, limit: int) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    questions: list[dict] = [
        {"question": "หลักสูตรนี้มีทั้งหมดกี่หน่วยกิต", "expect": {"type": "value", "value": total_credits}},
        {"question": "หลักสูตรนี้ใช้เวลาเรียนกี่ปี", "expect": {"type": "value", "value": years}},
    ]
    questions.extend(intermediate_questions(data))
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
