import json
import re
import unicodedata
from pathlib import Path
from typing import Any


THAI_DIGIT_TRANS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")

COURSE_CODE_RE = re.compile(
    r"^(?:\d{8}|\d{5}x{3}|\d{4}x{4}|x{8})$",
    re.IGNORECASE,
)

CREDIT_RE = re.compile(
    r"(\d+)\s*\(\s*(\d+)\s*-\s*(\d+)\s*-\s*(\d+)\s*\)"
)

FACULTY_NOTE = "กลุ่มวิชาที่กำหนดโดยคณะ"

# ในเอกสาร DSBA ส่วนรายวิชา flexible/elective concrete อยู่ช่วง 06026216..06026260
FLEX_CODE_MIN = 6026216
FLEX_CODE_MAX = 6026260


def extract_curriculum_from_file(
    ocr_path: str | Path,
    template_path: str | Path | None = None,
    program: str = "DSBA",
    plan: str = "coop",
) -> dict[str, Any]:
    """Extract curriculum from OCR prediction JSON.

    template_path intentionally is not used while evaluating OCR/extraction quality.
    """
    payload = _load_ocr_payload(ocr_path)
    return extract_curriculum(payload, program=program, plan=plan)

def _recover_placeholder_semantics_from_source(
    payload: dict[str, Any],
    courses: list[dict[str, Any]],
) -> None:
    """
    Recover placeholder English names and alternative credits
    only when OCR source itself contains supporting evidence.
    """

    source_parts: list[str] = []

    top_text = str(
        payload.get("text", "")
    ).strip()

    if top_text:
        source_parts.append(top_text)

    for page in payload.get("pages", []):

        page_text = str(
            page.get("text", "")
        ).strip()

        if page_text:
            source_parts.append(page_text)

        line_text = "\n".join(
            _page_lines(page)
        ).strip()

        if line_text:
            source_parts.append(line_text)

    source_text = re.sub(
        r"\s+",
        " ",
        "\n".join(source_parts),
    ).strip()

    upper = source_text.upper()

    specs = {
        "90644xxx": (
            "ELECTIVE IN LANGUAGE "
            "AND COMMUNICATION"
        ),
        "9064xxxx": (
            "ELECTIVE IN GENERAL EDUCATION"
        ),
    }

    for course in courses:

        code = str(
            course.get("code", "")
        )

        marker = specs.get(code)

        if not marker:
            continue

        position = upper.find(marker)

        # ไม่มีหลักฐานใน OCR source -> ไม่เติม
        if position < 0:
            continue

        # English name มีหลักฐานตรงจาก source
        course["name_en"] = marker

        # ดูบริเวณรอบข้อความ placeholder
        start = max(
            0,
            position - 300,
        )

        end = min(
            len(source_text),
            position + 600,
        )

        window = source_text[
            start:end
        ]

        found: list[str] = []

        for match in CREDIT_RE.finditer(
            window
        ):

            credit = (
                f"{match.group(1)}"
                f"({match.group(2)}"
                f"-{match.group(3)}"
                f"-{match.group(4)})"
            )

            if credit not in found:
                found.append(credit)

        # ต้องมีหลักฐานของทั้ง 2 แบบจริง
        required = {
            "3(3-0-6)",
            "3(2-2-5)",
        }

        if required.issubset(
            set(found)
        ):
            course["credits"] = (
                "3(3-0-6) หรือ "
                "3(2-2-5)"
            )

def _remove_duplicate_plan_artifacts(
    courses: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    ลบ duplicate ที่เกิดจาก OCR/parser สำหรับ placeholder
    ที่ใน academic plan มีได้เพียงหนึ่ง occurrence ต่อ semester

    สำคัญ:
    - ไม่ dedupe 06026xxx เพราะในเทอมเดียวกันมีหลายตัวจริง
    - ไม่ dedupe xxxxxxxx เพราะ Year 4/1 มี FREE ELECTIVE 1 และ 2 จริง
    """

    singleton_placeholder_codes = {
        "90644xxx",
        "9064xxxx",
    }

    seen: set[tuple[str, Any, Any]] = set()
    result: list[dict[str, Any]] = []

    for course in courses:

        code = str(
            course.get("code", "")
        ).lower()

        year = course.get("year")
        semester = course.get("semester")

        if code in singleton_placeholder_codes:

            key = (
                code,
                year,
                semester,
            )

            if key in seen:
                continue

            seen.add(key)

        result.append(course)

    return result

def _recover_year4_free_electives(
    payload: dict[str, Any],
    courses: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Recover Year 4 Semester 1 free-elective rows when OCR text contains
    FREE ELECTIVE 1/2 but the course-code token was lost.

    จะเพิ่มเฉพาะเมื่อ source OCR มีหลักฐานของวิชาเลือกเสรี 1/2 จริง
    """

    # --------------------------------------------------
    # รวม source text จากทุก field เพื่อไม่พลาดกรณี
    # ข้อความอยู่ใน page["text"] แต่หายจาก page["lines"]
    # --------------------------------------------------
    source_parts: list[str] = []

    for page in payload.get("pages", []):

        page_text = str(
            page.get("text", "")
        ).strip()

        if page_text:
            source_parts.append(page_text)

        for line in page.get("lines", []):
            text = str(
                line.get("text", "")
            ).strip()

            if text:
                source_parts.append(text)

    source_text = _normalize_thai_text(
        "\n".join(source_parts)
    )

    upper = source_text.upper()

    # --------------------------------------------------
    # ต้องมีหลักฐานจาก OCR source
    # --------------------------------------------------
    has_free_1 = (
        re.search(
            r"วิชาเลือกเสรี\s*1",
            source_text,
        )
        is not None
        or re.search(
            r"FREE\s+ELECTIVE\s+COURSE\s*1",
            upper,
        )
        is not None
    )

    has_free_2 = (
        re.search(
            r"วิชาเลือกเสรี\s*2",
            source_text,
        )
        is not None
        or re.search(
            r"FREE\s+ELECTIVE\s+COURSE\s*2",
            upper,
        )
        is not None
    )

    # ถ้า source เองไม่มีข้อความ ก็ไม่เดา
    if not has_free_1 and not has_free_2:
        return courses

    # --------------------------------------------------
    # ดู free elective ที่ parser จับได้แล้ว
    # --------------------------------------------------
    existing = [
        course
        for course in courses
        if (
            course.get("code") == "xxxxxxxx"
            and course.get("year") == 4
            and course.get("semester") == 1
        )
    ]

    # ถ้ามีครบ 2 แล้ว ไม่ต้องทำอะไร
    if len(existing) >= 2:
        return courses

    def get_number(course: dict[str, Any]) -> int | None:

        text = " ".join(
            str(value or "")
            for value in [
                course.get("name_th"),
                course.get("name_en"),
            ]
        )

        if re.search(
            r"(?:วิชาเลือกเสรี|FREE\s+ELECTIVE\s+COURSE)\s*1",
            text,
            re.IGNORECASE,
        ):
            return 1

        if re.search(
            r"(?:วิชาเลือกเสรี|FREE\s+ELECTIVE\s+COURSE)\s*2",
            text,
            re.IGNORECASE,
        ):
            return 2

        return None

    existing_numbers = {
        number
        for number in (
            get_number(course)
            for course in existing
        )
        if number is not None
    }

    # --------------------------------------------------
    # ถ้ามีอยู่หนึ่งตัวแต่ OCR ชื่อไม่ชัดจนไม่รู้ว่า 1/2
    # ให้ใช้ source เป็นตัวตัดสิน
    # --------------------------------------------------
    if len(existing) == 1 and not existing_numbers:

        existing_course = existing[0]

        joined_name = " ".join(
            str(existing_course.get(key) or "")
            for key in ["name_th", "name_en"]
        ).upper()

        if "1" in joined_name:
            existing_numbers.add(1)
        elif "2" in joined_name:
            existing_numbers.add(2)

    # --------------------------------------------------
    # เพิ่มเฉพาะ occurrence ที่ source ยืนยันว่ามี
    # --------------------------------------------------
    missing_numbers: list[int] = []

    if has_free_1 and 1 not in existing_numbers:
        missing_numbers.append(1)

    if has_free_2 and 2 not in existing_numbers:
        missing_numbers.append(2)

    # เราต้องการรวมแล้วสูงสุด 2 occurrence เท่านั้น
    slots_left = 2 - len(existing)

    missing_numbers = missing_numbers[
        :slots_left
    ]

    for number in missing_numbers:

        courses.append({
            "code": "xxxxxxxx",
            "name_th": f"วิชาเลือกเสรี {number}",
            "name_en": f"FREE ELECTIVE COURSE {number}",
            "credits": "3(3-0-6) หรือ 3(2-2-5)",
            "year": 4,
            "semester": 1,
            "category": "หมวดวิชาเลือกเสรี",
            "type": "เลือก",
            "prerequisite": "ไม่มี",
            "flexible_year_semester": None,
            "note": None,
        })

    return courses

def _clean_plan_placeholder_names(
    courses: list[dict[str, Any]],
) -> None:

    for course in courses:

        code = str(
            course.get("code", "")
        )

        name_th = _normalize_thai_text(
            course.get("name_th")
            or ""
        )

        # ----------------------------------
        # 06026xxx
        # เก็บเฉพาะชื่อ elective ทั้ง 3 กลุ่ม
        # ----------------------------------
        if code == "06026xxx":

            patterns = [
                r"วิชาเลือกกลุ่มวิทยาการข้อมูล\s*[1-4]?",
                r"วิชาเลือกกลุ่มการวิเคราะห์เชิงสถิติ\s*[1-4]?",
                r"วิชาเลือกกลุ่มวิศวกรรมข้อมูล\s*[1-4]?",
            ]

            parts: list[str] = []

            for pattern in patterns:

                match = re.search(
                    pattern,
                    name_th,
                )

                if match:
                    value = re.sub(
                        r"\s+",
                        " ",
                        match.group(0),
                    ).strip()

                    parts.append(value)

            if parts:
                course["name_th"] = "\n".join(
                    parts
                )

        # ----------------------------------
        # Free elective
        # ลบเศษ "2 หรือ"
        # ----------------------------------
        elif code == "xxxxxxxx":

            match = re.search(
                r"วิชาเลือกเสรี\s*([12])",
                name_th,
            )

            if match:
                number = match.group(1)

                course["name_th"] = (
                    f"วิชาเลือกเสรี {number}"
                )

def _recover_flexible_thai_names_from_page_text(
    payload: dict[str, Any],
    courses: list[dict[str, Any]],
) -> None:

    fallback: dict[str, str] = {}

    for page in payload.get("pages", []):

        raw_text = str(
            page.get("text", "")
        )

        for raw_line in raw_text.splitlines():

            line = _normalize_thai_text(
                raw_line
            )

            start = _extract_code_and_rest(
                line
            )

            if not start:
                continue

            code, rest = start

            if not re.fullmatch(
                r"\d{8}",
                code,
            ):
                continue

            numeric = int(code)

            if not (
                FLEX_CODE_MIN
                <= numeric
                <= FLEX_CODE_MAX
            ):
                continue

            # เอาเฉพาะชื่อไทยจากบรรทัดที่มี code
            thai = _extract_thai_piece(
                rest
            )

            if thai:
                fallback.setdefault(
                    code,
                    thai,
                )

    bad_tokens = (
        "กลุ่มวิชา",
        "หน่วยกิต",
        "สำหรับแผนการศึกษา",
        "รหัสวิชา",
        "เลือกเรียนจากรายวิชา",
    )

    for course in courses:

        code = str(
            course.get("code", "")
        )

        if code not in fallback:
            continue

        current = _normalize_thai_text(
            course.get("name_th") or ""
        )

        bad_current = (
            not current
            or any(
                token in current
                for token in bad_tokens
            )
            or re.match(
                r"^\d+\s",
                current,
            )
            is not None
        )

        if bad_current:
            course["name_th"] = (
                fallback[code]
            )

def _recover_placeholder_fields(
    payload: dict[str, Any],
    courses: list[dict[str, Any]],
) -> None:

    wanted = {
        "90644xxx",
        "9064xxxx",
    }

    references: dict[
        str,
        dict[str, Any],
    ] = {}

    source_documents: list[str] = []

    # 1) top-level OCR text
    top_text = str(
        payload.get("text", "")
    ).strip()

    if top_text:
        source_documents.append(
            top_text
        )

    # 2) page text + page lines
    for page in payload.get(
        "pages",
        [],
    ):

        page_text = str(
            page.get("text", "")
        ).strip()

        if page_text:
            source_documents.append(
                page_text
            )

        line_text = "\n".join(
            _page_lines(page)
        ).strip()

        if line_text:
            source_documents.append(
                line_text
            )


    for source_document in source_documents:

        raw_lines = [
            _normalize_thai_text(line)
            for line in source_document.splitlines()
            if line.strip()
        ]

        for index, line in enumerate(
            raw_lines
        ):

            start = _extract_code_and_rest(
                line
            )

            if not start:
                continue

            code, rest = start

            if code not in wanted:
                continue

            texts: list[str] = []

            if rest:
                texts.append(rest)

            # อ่านเฉพาะ block ของ placeholder นี้
            for next_line in raw_lines[
                index + 1:
            ]:

                # เจอ course ใหม่ = จบ
                next_start = (
                    _extract_code_and_rest(
                        next_line
                    )
                )

                if next_start:
                    break

                upper = next_line.upper()

                # สำคัญ:
                # ป้องกัน 9064xxxx กลืน
                # FREE ELECTIVE COURSE 1
                if (
                    "วิชาเลือกเสรี"
                    in next_line
                    or
                    "FREE ELECTIVE COURSE"
                    in upper
                ):
                    break

                if next_line.startswith(
                    "รวม"
                ):
                    break

                if (
                    _detect_year_semester(
                        next_line
                    )
                    != (None, None)
                ):
                    break

                texts.append(
                    next_line
                )

                # block นี้ต้องการไม่เกิน
                # 2 credit alternatives
                credits_found = []

                for item in texts:
                    for match in (
                        CREDIT_RE.finditer(
                            item
                        )
                    ):
                        credit = (
                            f"{match.group(1)}"
                            f"({match.group(2)}"
                            f"-{match.group(3)}"
                            f"-{match.group(4)})"
                        )

                        if (
                            credit
                            not in credits_found
                        ):
                            credits_found.append(
                                credit
                            )

                # ถ้ามี English + credit 2 แบบ
                # ถือว่า block สมบูรณ์แล้ว
                has_english = any(
                    re.search(
                        r"[A-Za-z]",
                        item,
                    )
                    for item in texts
                )

                if (
                    has_english
                    and len(
                        credits_found
                    ) >= 2
                ):
                    break

            candidate = (
                _parse_course_block(
                    code,
                    texts,
                    year=None,
                    semester=None,
                    flexible=False,
                )
            )

            # -----------------------------
            # Clean English placeholder
            # -----------------------------
            if code == "9064xxxx":

                for item in texts:

                    english = (
                        _extract_english_piece(
                            item
                        )
                    )

                    marker = (
                        "ELECTIVE IN "
                        "GENERAL EDUCATION"
                    )

                    if marker in english:
                        candidate[
                            "name_en"
                        ] = marker
                        break

            elif code == "90644xxx":

                for item in texts:

                    english = (
                        _extract_english_piece(
                            item
                        )
                    )

                    marker = (
                        "ELECTIVE IN LANGUAGE "
                        "AND COMMUNICATION"
                    )

                    if marker in english:
                        candidate[
                            "name_en"
                        ] = marker
                        break

            # -----------------------------
            # Credits
            # -----------------------------
            credits_found: list[str] = []

            for item in texts:

                for match in (
                    CREDIT_RE.finditer(
                        item
                    )
                ):

                    credit = (
                        f"{match.group(1)}"
                        f"({match.group(2)}"
                        f"-{match.group(3)}"
                        f"-{match.group(4)})"
                    )

                    if (
                        credit
                        not in credits_found
                    ):
                        credits_found.append(
                            credit
                        )

            if len(credits_found) >= 2:
                candidate["credits"] = (
                    " หรือ ".join(
                        credits_found[:2]
                    )
                )

            # เลือก occurrence ที่ข้อมูลครบกว่า
            old = references.get(code)

            def score(
                value: dict[str, Any],
            ) -> int:

                result = 0

                if value.get("name_en"):
                    result += 10

                if value.get("name_th"):
                    result += 5

                credits = str(
                    value.get("credits")
                    or ""
                )

                if credits:
                    result += 5

                if "หรือ" in credits:
                    result += 20

                return result

            if (
                old is None
                or score(candidate)
                > score(old)
            ):
                references[
                    code
                ] = candidate

    # ------------------------------------
    # เอาข้อมูลที่ recover ได้มาเติม
    # ------------------------------------
    for course in courses:

        code = str(
            course.get("code", "")
        )

        ref = references.get(code)

        if not ref:
            continue

        if ref.get("name_en"):
            course["name_en"] = (
                ref["name_en"]
            )

        old_credit = str(
            course.get("credits")
            or ""
        )

        new_credit = str(
            ref.get("credits")
            or ""
        )

        if (
            "หรือ" in new_credit
            and "หรือ" not in old_credit
        ):
            course["credits"] = (
                new_credit
            )

def extract_curriculum(
    payload: dict[str, Any],
    program: str = "DSBA",
    plan: str = "coop",
) -> dict[str, Any]:
    pages = payload.get("pages", [])
    full_document = len(pages) > 1

    # A) concrete flexible/elective courses from course-list pages before 3.1.4
    flexible_courses = _extract_flexible_catalog_courses(payload)
    
    _recover_flexible_thai_names_from_page_text(
    payload,
    flexible_courses,)

    # B) exact academic plan section 3.1.4.2 (coop) / 3.1.4.1 (no_coop)
    plan_courses, seen_semesters, found_start, found_end = _extract_target_plan(
        payload,
        plan=plan,
    )

    # C) Coop year 4 semester 2 is one alternative occurrence: 06026259 OR 06026260
    if plan == "coop":
        plan_courses = _combine_coop_alternatives(plan_courses)
        
    plan_courses = _remove_duplicate_plan_artifacts(
    plan_courses)
    
    plan_courses = _recover_year4_free_electives(
    payload,
    plan_courses,)
    
    _recover_placeholder_fields(
    payload,
    plan_courses,)
    
    _recover_placeholder_semantics_from_source(
    payload,
    plan_courses,)
    
    _clean_plan_placeholder_names(
    plan_courses,)
    # D) Enrich prerequisite only from source OCR, never from GT/template
    concrete_codes = {
        str(course.get("code"))
        for course in (plan_courses + flexible_courses)
        if re.fullmatch(r"\d{8}", str(course.get("code", "")))
    }
    prereq_map = _extract_prerequisite_map(payload, concrete_codes)

    for course in plan_courses + flexible_courses:
        code = str(course.get("code", ""))
        if code in prereq_map:
            course["prerequisite"] = prereq_map[code]

    # E) Fail loudly on full-document extraction instead of silently outputting wrong data
    if full_document:
        section = "3.1.4.2" if plan == "coop" else "3.1.4.1"

        if not found_start:
            raise ValueError(
                f"ไม่พบหัวข้อ {section} ใน OCR prediction; "
                "หยุด extraction เพื่อป้องกันการอ่านผิด section"
            )

        if not found_end:
            raise ValueError(
                "เริ่ม Academic Plan แล้ว แต่ไม่พบ 3.1.5; "
                "หยุดเพื่อป้องกันการอ่านเกิน section"
            )

        if plan == "coop":
            expected_semesters = {
                (1, 1), (1, 2),
                (2, 1), (2, 2),
                (3, 1), (3, 2),
                (4, 1), (4, 2),
            }

            missing = expected_semesters - seen_semesters
            if missing:
                raise ValueError(
                    "OCR อ่านหัวข้อปี/เทอมไม่ครบ: "
                    f"missing={sorted(missing)}. "
                    "ไม่สร้าง output ที่อาจใส่ year/semester ผิด"
                )

            # DSBA coop fixed plan = 44 occurrences after combining 59/60
            if len(plan_courses) != 44:

                expected_counts = {
                    (1, 1): 7,
                    (1, 2): 7,
                    (2, 1): 6,
                    (2, 2): 7,
                    (3, 1): 6,
                    (3, 2): 6,
                    (4, 1): 4,
                    (4, 2): 1,
                }

                actual_counts = {}

                for course in plan_courses:

                    key = (
                        course.get("year"),
                        course.get("semester"),
                    )

                    actual_counts[key] = (
                        actual_counts.get(
                            key,
                            0
                        )
                        + 1
                    )

                details = []

                for key, expected in (
                    expected_counts.items()
                ):

                    actual = actual_counts.get(
                        key,
                        0
                    )

                    if actual != expected:

                        codes = [
                            course.get("code")
                            for course in plan_courses
                            if (
                                course.get("year"),
                                course.get("semester"),
                            ) == key
                        ]

                        details.append(
                            f"{key[0]}/{key[1]} "
                            f"ได้ {actual}/{expected} "
                            f"codes={codes}"
                        )

                raise ValueError(
                    "จำนวนรายวิชาใน Academic Plan ไม่ครบ: "
                    f"ได้ {len(plan_courses)} แต่คาด 44; "
                    + " | ".join(details)
                )

            # 06026216..06026260 = 45 flexible concrete courses
            if len(flexible_courses) != 45:
                raise ValueError(
                    "จำนวน flexible/elective concrete courses ไม่ครบ: "
                    f"ได้ {len(flexible_courses)} แต่คาด 45. "
                    "ตรวจ prediction แถวหน้ารายวิชา 19-22"
                )

    courses = plan_courses + flexible_courses

    return {
        "source": "OCR curriculum extraction",
        "description": f"Extracted academic plan from OCR for {program} ({plan})",
        "program": program,
        "plan": plan,
        "courses": courses,
    }


def _load_ocr_payload(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------
# Page / line helpers
# ---------------------------------------------------------------------

def _page_items(page: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    for line in page.get("lines", []):
        text = str(line.get("text", "")).strip()
        if not text:
            continue

        box = line.get("box") or [[0, 0]]
        xs = [p[0] for p in box if isinstance(p, (list, tuple)) and len(p) >= 2]
        ys = [p[1] for p in box if isinstance(p, (list, tuple)) and len(p) >= 2]

        items.append({
            "text": text,
            "x": min(xs) if xs else 0,
            "y": min(ys) if ys else 0,
        })

    items.sort(key=lambda item: (item["y"], item["x"]))
    return items


def _page_lines(page: dict[str, Any]) -> list[str]:
    items = _page_items(page)
    if items:
        return [item["text"] for item in items]

    return [
        line.strip()
        for line in str(page.get("text", "")).splitlines()
        if line.strip()
    ]


def _page_text(page: dict[str, Any]) -> str:
    lines = _page_lines(page)
    return "\n".join(lines) if lines else str(page.get("text", ""))

def _section_search_text(
    page: dict[str, Any],
) -> str:
    """
    ใช้สำหรับหา section heading เท่านั้น

    รวมทั้ง page["text"] และ page["lines"]
    เพราะบาง OCR prediction มี heading ใน text
    แต่ heading หายจาก lines
    """

    parts: list[str] = []

    page_text = str(
        page.get("text", "")
    ).strip()

    if page_text:
        parts.append(page_text)

    line_text = "\n".join(
        _page_lines(page)
    ).strip()

    if line_text:
        parts.append(line_text)

    return "\n".join(parts)

# ---------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------

def _normalize_thai_text(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFC", str(text))
    text = text.translate(THAI_DIGIT_TRANS)

    # Sara Am: Tesseract sometimes returns ํ + า
    text = text.replace("\u0e4d\u0e32", "\u0e33")

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return text.strip()


def _normalize_heading(text: str) -> str:
    text = _normalize_thai_text(text)
    text = text.replace("ป", "ปี")
    text = text.replace("หนวยกิต", "หน่วยกิต")
    return re.sub(r"\s+", " ", text).strip()


def _compact_section_text(text: str) -> str:
    return re.sub(r"\s+", "", _normalize_heading(text))


def _normalize_code_text(text: str) -> str:
    text = str(text).translate(THAI_DIGIT_TRANS)
    text = text.replace("×", "x").replace("X", "x")
    text = re.sub(r"[\s|:;,_\-./\\]+", "", text)
    return text.lower()


# ---------------------------------------------------------------------
# Section / semester detection
# ---------------------------------------------------------------------

def _is_target_plan_start(
    text: str,
    plan: str,
) -> bool:

    raw = str(text).translate(THAI_DIGIT_TRANS)

    # ---------------------------------------------
    # 1) วิธีหลัก: section number
    # รองรับ
    # 3.1.4.2
    # 3 . 1 . 4 . 2
    # 3 1 4 2
    # 3-1-4-2
    # ---------------------------------------------
    if plan == "coop":

        if re.search(
            r"3\s*[\.\-,:]?\s*1\s*[\.\-,:]?\s*4\s*[\.\-,:]?\s*2",
            raw,
        ):
            return True

    elif plan == "no_coop":

        if re.search(
            r"3\s*[\.\-,:]?\s*1\s*[\.\-,:]?\s*4\s*[\.\-,:]?\s*1",
            raw,
        ):
            return True

    else:
        raise ValueError(
            f"Unsupported plan: {plan}"
        )

    # ---------------------------------------------
    # 2) fallback แบบปลอดภัย
    #
    # ไม่ใช้แค่คำว่า "สหกิจศึกษา"
    # เพราะหน้า 22 ก็มีคำนี้
    #
    # ต้องมีพร้อมกัน:
    # - แผนการศึกษา
    # - สหกิจศึกษา
    # - ปี 1 เทอม 1
    # - 06026200
    # ---------------------------------------------

    normalized = _normalize_heading(raw)

    has_plan_word = (
        "แผนการศึกษา" in normalized
    )

    has_coop_word = (
        "สหกิจศึกษา" in normalized
    )

    has_year1_sem1 = (
        re.search(
            r"ปี\s*ที่?\s*1.*?"
            r"ภาคการศึกษา\s*ที่?\s*1",
            normalized,
        )
        is not None
    )

    has_first_course = (
        "06026200" in normalized
    )

    # ตรวจคำปฏิเสธของ non-coop
    is_non_coop_text = (
        "ไม่เข้า" in normalized
        or "ไม่เข้าร่วม" in normalized
    )

    if plan == "coop":
        return (
            has_plan_word
            and has_coop_word
            and has_year1_sem1
            and has_first_course
            and not is_non_coop_text
        )

    if plan == "no_coop":
        return (
            has_plan_word
            and has_coop_word
            and has_year1_sem1
            and has_first_course
            and is_non_coop_text
        )

    return False


def _is_any_plan_start(text: str) -> bool:
    compact = _compact_section_text(text)
    return "3.1.4.1" in compact or "3.1.4.2" in compact


def _is_plan_end(text: str) -> bool:
    normalized = _normalize_heading(text)
    compact = _compact_section_text(text)
    return "3.1.5" in compact or "คำอธิบายรายวิชา" in normalized


def _detect_year_semester(text: str) -> tuple[int | None, int | None]:
    text = _normalize_heading(text).translate(THAI_DIGIT_TRANS)

    match = re.search(
        r"ปี\s*ที่?\s*(\d+).*?ภาคการศึกษา\s*ที่?\s*(\d+)",
        text,
    )

    if not match:
        return None, None

    return int(match.group(1)), int(match.group(2))


# ---------------------------------------------------------------------
# Course start detection
# ---------------------------------------------------------------------

def _extract_code_and_rest(line: str) -> tuple[str, str] | None:
    original = _normalize_thai_text(line)
    normalized = original.translate(THAI_DIGIT_TRANS)
    upper = original.upper()

    # 1) normal 8-char code / placeholder
    m = re.match(
        r"^\s*([0-9xX×]{8})\s*[|:]?\s*(.*)$",
        normalized,
        re.IGNORECASE,
    )
    if m:
        raw_code = _normalize_code_text(m.group(1))
        rest = m.group(2).strip()

        if "วิชาเลือกเสรี" in original or "FREE ELECTIVE" in upper:
            return "xxxxxxxx", rest

        if COURSE_CODE_RE.fullmatch(raw_code):
            return raw_code, rest

    # 2) code split by OCR, e.g. "06026 xxx" / "9064 xxxx"
    m = re.match(
        r"^\s*([0-9xX×]{4,5})\s+([0-9xX×]{3,4})\s*[|:]?\s*(.*)$",
        normalized,
        re.IGNORECASE,
    )
    if m:
        raw_code = _normalize_code_text(m.group(1) + m.group(2))
        rest = m.group(3).strip()

        if "วิชาเลือกเสรี" in original or "FREE ELECTIVE" in upper:
            return "xxxxxxxx", rest

        if COURSE_CODE_RE.fullmatch(raw_code):
            return raw_code, rest

    # 3) placeholder code OCR is noisy but prefix + row meaning survives
    if original.lstrip().startswith("06026") and "วิชาเลือก" in original:
        rest = re.sub(r"^\s*06026\S*\s*", "", original).strip(" |:")
        return "06026xxx", rest

    # language elective
    if (
        "วิชาเลือกด้านภาษาและการสื่อสาร"
        in original
        or
        "ELECTIVE IN LANGUAGE AND COMMUNICATION"
        in upper
    ):
        rest = re.sub(
            r"^\s*9064\S*\s*",
            "",
            original
        ).strip(" |:")

        return "90644xxx", rest


    # general education elective
    if (
        "วิชาเลือกหมวดวิชาศึกษาทั่วไป"
        in original
        or
        "ELECTIVE IN GENERAL EDUCATION"
        in upper
    ):
        rest = re.sub(
            r"^\s*9064\S*\s*",
            "",
            original
        ).strip(" |:")

        return "9064xxxx", rest

    # xxxxxxxx may be read as zeros/Thai digits/etc.
    if "วิชาเลือกเสรี" in original or "FREE ELECTIVE COURSE" in upper:
        parts = original.split(maxsplit=1)
        prefix = parts[0] if parts else ""
        if len(_normalize_code_text(prefix)) >= 6 or re.search(r"\d", prefix):
            rest = parts[1] if len(parts) > 1 else ""
            return "xxxxxxxx", rest.strip(" |:")

    return None


# ---------------------------------------------------------------------
# Noise / fields
# ---------------------------------------------------------------------

def _is_footer(text: str) -> bool:
    text = _normalize_thai_text(text)

    if re.match(r"^ม\s*ค\s*อ\s*\.?\s*\d*", text):
        return True
    if re.match(r"^วท\s*\.\s*บ", text):
        return True
    if text.startswith("คณะเทคโนโลยีสารสนเทศ") and "สจล" in text:
        return True

    return False


def _is_noise_line(text: str) -> bool:
    text = _normalize_thai_text(text)

    if not text or _is_footer(text):
        return True

    if re.fullmatch(r"\d{1,3}", text):
        return True

    if _detect_year_semester(text) != (None, None):
        return True

    if _is_any_plan_start(text) or _is_plan_end(text):
        return True

    noise_tokens = (
        "รหัสวิชา",
        "ชื่อวิชา",
        "บรรยาย",
        "ปฏิบัติ",
        "ศึกษาด้วยตนเอง",
        "รวมตลอดหลักสูตร",
        "นักศึกษาเลือกลงทะเบียน",
        "กำหนดระยะเวลา",
        "หมวดวิชาเลือกเสรี",
    )
    if any(token in text for token in noise_tokens):
        return True

    if text.startswith("รวม"):
        return True

    return False


def _detect_category(code: str) -> str | None:
    code = str(code).lower()

    if code == "xxxxxxxx":
        return "หมวดวิชาเลือกเสรี"
    if code.startswith("906"):
        return "หมวดวิชาศึกษาทั่วไป"
    if code.startswith("060"):
        return "หมวดวิชาเฉพาะ"

    return None


def _detect_note_from_text(texts: list[str]) -> str | None:
    joined = " ".join(_normalize_thai_text(t) for t in texts)
    return FACULTY_NOTE if FACULTY_NOTE in joined else None


def _clean_faculty_note(text: str) -> str:
    text = re.sub(
        r"กลุ่มวิชา\s*ที่?\s*กำหนดโดยคณะ\s*\*?",
        " ",
        text,
    )
    return re.sub(r"\s+", " ", text).strip()


def _extract_thai_piece(text: str) -> str:
    text = _normalize_thai_text(text)
    text = CREDIT_RE.sub(" ", text)
    text = re.sub(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", " ", text)
    text = text.replace("|", " ")
    text = re.sub(r"[^\u0E00-\u0E7F0-9\s\-*]", " ", text)
    text = _clean_faculty_note(text)
    return _normalize_thai_text(text)


def _extract_english_piece(text: str) -> str:
    text = CREDIT_RE.sub(" ", str(text))
    words = re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+", text)
    if not words:
        return ""

    value = " ".join(words)
    value = re.sub(
        r"^(?:\d{4,8}|[A-Z]XXX|XXXX|DXXX)\s+",
        "",
        value,
        flags=re.IGNORECASE,
    )
    return re.sub(r"\s+", " ", value).strip().upper()


def _extract_credits(texts: list[str]) -> str | None:
    found: list[str] = []

    for text in texts:
        for m in CREDIT_RE.finditer(str(text)):
            value = f"{m.group(1)}({m.group(2)}-{m.group(3)}-{m.group(4)})"
            if value not in found:
                found.append(value)

    if not found:
        return None
    if len(found) == 1:
        return found[0]

    return " หรือ ".join(found[:2])


def _parse_course_block(
    code: str,
    texts: list[str],
    year: int | None,
    semester: int | None,
    *,
    flexible: bool = False,
) -> dict[str, Any]:
    note = _detect_note_from_text(texts)
    credits = _extract_credits(texts)

    thai_parts: list[str] = []
    english_parts: list[str] = []

    for raw in texts:
        text = _normalize_thai_text(raw)

        if _is_noise_line(text) or text.strip() == "หรือ":
            continue

        credit_removed = CREDIT_RE.sub(" ", text)
        if not credit_removed.strip():
            continue

        if re.search(r"[\u0E00-\u0E7F]", credit_removed):
            thai = _extract_thai_piece(credit_removed)
            if thai and thai != "หรือ":
                thai_parts.append(thai)

        if re.search(r"[A-Za-z]", credit_removed):
            english = _extract_english_piece(credit_removed)
            if english:
                english_parts.append(english)

    name_th = _normalize_thai_text(" ".join(thai_parts)) or None
    name_en = re.sub(r"\s+", " ", " ".join(english_parts)).strip().upper() or None

    return {
        "code": code,
        "name_th": name_th,
        "name_en": name_en,
        "credits": credits,
        "year": 0 if flexible else year,
        "semester": 0 if flexible else semester,
        "category": _detect_category(code),
        "type": "เลือก" if flexible or "x" in code.lower() else "บังคับ",
        "prerequisite": "ไม่มี",
        "flexible_year_semester": "3/1, 3/2, 4/1" if flexible else None,
        "note": note,
    }


# ---------------------------------------------------------------------
# Flexible catalog: concrete 06026216..06026260 before 3.1.4
# ---------------------------------------------------------------------

def _extract_flexible_catalog_courses(payload: dict[str, Any]) -> list[dict[str, Any]]:
    courses_by_code: dict[str, dict[str, Any]] = {}

    current_code: str | None = None
    current_texts: list[str] = []

    def flush() -> None:
        nonlocal current_code, current_texts

        if current_code and re.fullmatch(r"\d{8}", current_code):
            numeric = int(current_code)
            if FLEX_CODE_MIN <= numeric <= FLEX_CODE_MAX:
                if current_code not in courses_by_code:
                    courses_by_code[current_code] = _parse_course_block(
                        current_code,
                        current_texts,
                        year=0,
                        semester=0,
                        flexible=True,
                    )

        current_code = None
        current_texts = []

    stop_catalog = False

    for page in payload.get("pages", []):

        section_text = _section_search_text(
            page
        )

        # ถึง Academic Plan แล้ว
        # หยุด catalog extraction
        if _is_any_plan_start(section_text):
            flush()
            stop_catalog = True
            break

        for line in _page_lines(page):

            start = _extract_code_and_rest(
                line
            )

            if start:
                new_code, rest = start

                if re.fullmatch(
                    r"\d{8}",
                    new_code
                ):
                    numeric = int(new_code)

                    if (
                        FLEX_CODE_MIN
                        <= numeric
                        <= FLEX_CODE_MAX
                    ):
                        flush()
                        current_code = new_code
                        current_texts = (
                            [rest]
                            if rest
                            else []
                        )
                        continue

                flush()
                continue

            if current_code is not None:

                normalized_line = _normalize_thai_text(
                    line
                )

                # --------------------------------------------------
                # ตรวจว่าเป็นข้อความจบ section / หัวข้อ
                # ไม่ใช่ชื่อวิชาต่อเนื่อง
                # --------------------------------------------------
                is_boundary = (
                    _is_noise_line(normalized_line)
                    or normalized_line.startswith("-")
                    or normalized_line.startswith("*")
                    or "เลือกเรียนจากรายวิชา" in normalized_line
                    or "ดังต่อไปนี้" in normalized_line
                    or "สำหรับแผนการศึกษา" in normalized_line
                    or "นักศึกษาเลือกลงทะเบียน" in normalized_line
                    or "กำหนดระยะเวลา" in normalized_line
                )

                if is_boundary:

                    # ถ้ามี course ค้างอยู่ให้บันทึกก่อน
                    if current_texts:
                        flush()

                    continue

                # --------------------------------------------------
                # สำคัญ:
                # ถึงแม้จะเจอ credits แล้วก็ยัง append ต่อ
                #
                # เพราะ OCR อาจได้:
                #
                # 06026216 ปัญญาประดิษฐ์ 3(3-0-6)
                # ARTIFICIAL INTELLIGENCE
                #
                # ถ้า flush ทันทีจะทำ English name หาย
                # --------------------------------------------------
                current_texts.append(
                    line
                )

        if stop_catalog:
            break

        flush()

    flush()

    return [
        courses_by_code[code]
        for code in sorted(courses_by_code, key=lambda x: int(x))
    ]


# ---------------------------------------------------------------------
# Academic plan
# ---------------------------------------------------------------------

def _split_compound_plan_line(
    line: str,
) -> list[str]:
    """
    แยกเฉพาะกรณีที่ Tesseract เอา FREE ELECTIVE
    ไปติดท้าย course ก่อนหน้า

    สำคัญ:
    - 90644xxx เป็น row ปกติ ห้ามสร้างใหม่จากชื่อ
    - 9064xxxx เป็น row ปกติ ห้ามสร้างใหม่จากชื่อ
    - 06026xxx เป็น row ปกติ ห้ามสร้างใหม่จากชื่อ
    - split เฉพาะ xxxxxxxx / วิชาเลือกเสรี
      เพราะเคยพบ OCR กลืนเข้ากับ row ก่อนหน้า
    """

    text = _normalize_thai_text(line)

    if not text:
        return []

    # ดูก่อนว่าบรรทัดนี้เองเป็น course อะไร
    start = _extract_code_and_rest(text)

    first_code = (
        start[0]
        if start
        else None
    )

    # -------------------------------------------------
    # ถ้าบรรทัดนี้เป็น free elective อยู่แล้ว
    # ไม่ต้อง split ซ้ำ
    #
    # เช่น:
    # xxxxxxxx วิชาเลือกเสรี 1
    # 00000000 วิชาเลือกเสรี 1
    # -------------------------------------------------
    if first_code == "xxxxxxxx":
        return [text]

    # -------------------------------------------------
    # split เฉพาะ free elective ที่ถูกฝังอยู่
    # ใน course ก่อนหน้า
    # -------------------------------------------------
    free_pattern = re.compile(
        r"วิชาเลือกเสรี\s*[12]"
        r"|FREE\s+ELECTIVE\s+COURSE\s*[12]",
        re.IGNORECASE,
    )

    matches = list(
        free_pattern.finditer(text)
    )

    if not matches:
        # IMPORTANT:
        # 90644xxx / 9064xxxx / 06026xxx
        # กลับไปเป็นบรรทัดเดิมตรง ๆ
        return [text]

    result: list[str] = []

    # -------------------------------------------------
    # ส่วนก่อน free elective ตัวแรก
    # -------------------------------------------------
    first_position = matches[0].start()

    before = text[
        :first_position
    ].strip()

    # บางครั้ง OCR จะได้ประมาณ:
    #
    # 9064xxxx วิชาเลือก... 00000000 วิชาเลือกเสรี 1
    #
    # 00000000 เป็น code ของ free elective
    # จึงต้องเอาออกจากท้าย course ก่อนหน้า
    before = re.sub(
        r"(?:[0-9๐-๙xX×]\s*){6,10}$",
        "",
        before,
    ).strip()

    if before:
        result.append(before)

    # -------------------------------------------------
    # สร้าง free elective แต่ละตัว
    # -------------------------------------------------
    for index, match in enumerate(matches):

        start_pos = match.start()

        end_pos = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(text)
        )

        part = text[
            start_pos:end_pos
        ].strip()

        # ถ้ามี code ของ free elective ตัวถัดไป
        # หลงอยู่ท้าย part ให้ลบทิ้ง
        part = re.sub(
            r"(?:[0-9๐-๙xX×]\s*){6,10}$",
            "",
            part,
        ).strip()

        if not part:
            continue

        result.append(
            f"xxxxxxxx {part}"
        )

    return result

def _extract_target_plan(
    payload: dict[str, Any],
    plan: str,
) -> tuple[list[dict[str, Any]], set[tuple[int, int]], bool, bool]:
    courses: list[dict[str, Any]] = []
    seen_semesters: set[tuple[int, int]] = set()

    current_year: int | None = None
    current_semester: int | None = None

    in_target_plan = False
    found_start = False
    found_end = False

    current_code: str | None = None
    current_texts: list[str] = []

    def flush() -> None:
        nonlocal current_code, current_texts

        if current_code is None:
            return

        course = _parse_course_block(
            current_code,
            current_texts,
            year=current_year,
            semester=current_semester,
            flexible=False,
        )
        course["year"] = current_year
        course["semester"] = current_semester
        courses.append(course)

        current_code = None
        current_texts = []

    for page in payload.get("pages", []):

        lines = _page_lines(page)

        # ใช้ทั้ง page["text"] และ lines
        # เฉพาะตอนตรวจ section
        section_text = _section_search_text(
            page
        )

        if not in_target_plan:

            if _is_target_plan_start(
                section_text,
                plan
            ):
                in_target_plan = True
                found_start = True

            else:
                continue

        for line in lines:
            if _is_plan_end(line):
                flush()
                found_end = True
                in_target_plan = False
                break

            detected_year, detected_semester = _detect_year_semester(line)
            if detected_year is not None and detected_semester is not None:
                flush()
                current_year = detected_year
                current_semester = detected_semester
                seen_semesters.add((current_year, current_semester))
                continue

            if _is_target_plan_start(line, plan):
                continue

            if line.strip().startswith("รวม"):
                flush()
                continue

            if _is_footer(line):
                continue

            start = _extract_code_and_rest(line)
            if start:
                flush()
                current_code, rest = start
                current_texts = [rest] if rest else []
                continue

            if current_code is not None:
                current_texts.append(line)

        if found_end:
            break

        flush()
        if _is_plan_end(section_text):
            found_end = True
            in_target_plan = False
            break

    flush()
    return courses, seen_semesters, found_start, found_end


def _combine_coop_alternatives(courses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Combine 06026259 and 06026260 into one Year 4 Semester 2 alternative row."""
    output: list[dict[str, Any]] = []
    i = 0

    while i < len(courses):
        current = courses[i]

        if (
            i + 1 < len(courses)
            and current.get("code") == "06026259"
            and courses[i + 1].get("code") == "06026260"
            and current.get("year") == 4
            and current.get("semester") == 2
            and courses[i + 1].get("year") == 4
            and courses[i + 1].get("semester") == 2
        ):
            nxt = courses[i + 1]

            output.append({
                "code": "06026259 หรือ 06026260",
                "name_th": "\n".join(
                    value for value in [current.get("name_th"), nxt.get("name_th")] if value
                ) or None,
                "name_en": "\n".join(
                    value for value in [current.get("name_en"), nxt.get("name_en")] if value
                ) or None,
                "credits": current.get("credits") or nxt.get("credits"),
                "year": 4,
                "semester": 2,
                "category": "หมวดวิชาเฉพาะ",
                "type": "บังคับ",
                "prerequisite": "ไม่มี",
                "flexible_year_semester": None,
                "note": None,
            })

            i += 2
            continue

        output.append(current)
        i += 1

    return output


# ---------------------------------------------------------------------
# Prerequisite from course-description blocks
# ---------------------------------------------------------------------

def _extract_prerequisite_map(
    payload: dict[str, Any],
    wanted_codes: set[str],
) -> dict[str, str]:
    result: dict[str, str] = {}

    current_code: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_code, current_lines

        if current_code is None or current_code not in wanted_codes:
            current_code = None
            current_lines = []
            return

        joined = " ".join(_normalize_thai_text(x) for x in current_lines)

        m = re.search(
            r"วิชาบังคับ\s*ก่อน\s*[:：]?\s*([0-9๐-๙]{8}|ไม่มี)",
            joined,
        )
        if m:
            result[current_code] = m.group(1).translate(THAI_DIGIT_TRANS)
        else:
            m = re.search(
                r"PREREQUISITE\s*[:：]?\s*(\d{8}|NONE)",
                joined,
                re.IGNORECASE,
            )
            if m:
                value = m.group(1)
                result[current_code] = "ไม่มี" if value.upper() == "NONE" else value

        current_code = None
        current_lines = []

    for page in payload.get("pages", []):
        for line in _page_lines(page):
            start = _extract_code_and_rest(line)

            if start:
                code, rest = start
                if re.fullmatch(r"\d{8}", code):
                    flush()
                    current_code = code
                    current_lines = [rest] if rest else []
                    continue

            if current_code is not None:
                current_lines.append(line)

                # prerequisite is near the top of a description block
                if len(current_lines) >= 12:
                    flush()

        flush()

    flush()
    return result
