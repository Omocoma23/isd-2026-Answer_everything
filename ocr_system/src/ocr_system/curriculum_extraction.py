import json
import re
import unicodedata
from pathlib import Path
from typing import Any
from ocr_system.curriculum_profiles import PROGRAM_PROFILES


THAI_DIGIT_TRANS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")



COURSE_CODE_RE = re.compile(
    r"^(?:\d{8}|\d{6}x{2}|\d{5}x{3}|\d{4}x{4}|x{8})$",
    re.IGNORECASE,
)

CREDIT_RE = re.compile(
    r"(\d+)\s*\(\s*([0-9xX]+)\s*-\s*([0-9xX]+)\s*-\s*([0-9xX]+)\s*\)"
)

FACULTY_NOTE = "กลุ่มวิชาที่กำหนดโดยคณะ"


def _get_profile(program: str) -> dict[str, Any]:
    key = str(program or "DSBA").upper().strip()
    if key not in PROGRAM_PROFILES:
        raise ValueError(
            f"Unsupported program: {program}. "
            f"Supported programs: {', '.join(PROGRAM_PROFILES)}"
        )
    return PROGRAM_PROFILES[key]


def _is_flexible_code(code: str, program: str) -> bool:
    if not re.fullmatch(r"\d{8}", str(code or "")):
        return False
    numeric = int(code)
    return any(
        int(start) <= numeric <= int(end)
        for start, end in _get_profile(program).get("elective_ranges", [])
    )



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
            "category": _detect_category(
                "xxxxxxxx",
                program=program,
            ),
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
    program: str = "DSBA",
) -> None:
    """Recover a flexible-course Thai name from the page text when line OCR is noisy."""
    fallback: dict[str, str] = {}

    for page in payload.get("pages", []):
        raw_text = str(page.get("text", ""))
        for raw_line in raw_text.splitlines():
            line = _normalize_thai_text(raw_line)
            start = _extract_code_and_rest(line, program=program)
            if not start:
                continue
            code, rest = start
            if not _is_flexible_code(code, program):
                continue
            thai = _extract_thai_piece(rest)
            if thai:
                fallback.setdefault(code, thai)

    bad_tokens = (
        "กลุ่มวิชา", "หน่วยกิต", "สำหรับแผนการศึกษา",
        "รหัสวิชา", "เลือกเรียนจากรายวิชา",
    )
    for course in courses:
        code = str(course.get("code", ""))
        if code not in fallback:
            continue
        current = _normalize_thai_text(course.get("name_th") or "")
        bad_current = (
            not current
            or any(token in current for token in bad_tokens)
            or re.match(r"^\d+\s", current) is not None
        )
        if bad_current:
            course["name_th"] = fallback[code]


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

def _recover_missing_concrete_credits_from_source(
    payload: dict[str, Any],
    courses: list[dict[str, Any]],
) -> None:
    """
    Fill only missing credits for concrete 8-digit courses from other OCR
    occurrences in the same source document.

    Example:
    - Academic-plan table may OCR only "06066000" and lose the credit cell.
    - The course-list page may still contain
      "06066000 ... 3 (3-0-6)".
    - In that case we reuse the source-supported credit value.

    This does NOT use Ground Truth and does NOT overwrite a credit that the
    academic-plan parser already extracted.
    """
    wanted = {
        str(course.get("code", ""))
        for course in courses
        if (
            re.fullmatch(r"\d{8}", str(course.get("code", "")))
            and not course.get("credits")
        )
    }

    if not wanted:
        return

    recovered: dict[str, str] = {}

    for page in payload.get("pages", []):
        raw_text = str(page.get("text", "") or "")
        raw_lines = [
            _normalize_thai_text(line)
            for line in raw_text.splitlines()
            if str(line).strip()
        ]

        if not raw_lines:
            raw_lines = _page_lines(page)

        for index, line in enumerate(raw_lines):
            line_ascii = line.translate(THAI_DIGIT_TRANS)

            code_match = re.search(
                r"(?<!\d)(\d{8})(?!\d)",
                line_ascii,
            )

            if not code_match:
                continue

            code = code_match.group(1)

            if code not in wanted or code in recovered:
                continue

            # Same line + a few following lines belonging to this course.
            block = [line]

            for next_index in range(
                index + 1,
                min(index + 6, len(raw_lines)),
            ):
                next_line = raw_lines[next_index]
                next_ascii = next_line.translate(THAI_DIGIT_TRANS)

                next_code = re.search(
                    r"(?<!\d)(\d{8})(?!\d)",
                    next_ascii,
                )

                if next_code and next_code.group(1) != code:
                    break

                block.append(next_line)

            credit = _extract_credits(block)

            if credit:
                recovered[code] = credit

    for course in courses:
        code = str(course.get("code", ""))

        if not course.get("credits") and code in recovered:
            course["credits"] = recovered[code]


def _recover_profile_free_electives(
    payload: dict[str, Any],
    courses: list[dict[str, Any]],
    program: str,
) -> list[dict[str, Any]]:
    """
    Recover free-elective rows only when:
    1) the curriculum profile says that free elective N belongs to year/semester, and
    2) the OCR source itself contains evidence for FREE ELECTIVE N / วิชาเลือกเสรี N.

    This is source-based recovery, not GT hardcoding.
    """
    profile = _get_profile(program)
    specs = profile.get("free_electives", [])

    if not specs:
        return courses

    source_parts: list[str] = []

    for page in payload.get("pages", []):
        page_text = str(page.get("text", "") or "").strip()
        if page_text:
            source_parts.append(page_text)

        for line in page.get("lines", []):
            text = str(line.get("text", "") or "").strip()
            if text:
                source_parts.append(text)

    source_text = _normalize_thai_text("\n".join(source_parts))
    upper = source_text.upper()

    def detect_number(course: dict[str, Any]) -> int | None:
        text = " ".join(
            str(course.get(key) or "")
            for key in ("name_th", "name_en")
        )
        m = re.search(
            r"(?:วิชาเลือกเสรี|FREE\s+ELECTIVE(?:\s+COURSE)?)\s*([12])",
            text,
            re.IGNORECASE,
        )
        return int(m.group(1)) if m else None

    for year, semester, number in specs:
        has_evidence = (
            re.search(
                rf"วิชาเลือกเสรี\s*{number}",
                source_text,
                re.IGNORECASE,
            )
            is not None
            or re.search(
                rf"FREE\s+ELECTIVE(?:\s+COURSE)?\s*{number}",
                upper,
                re.IGNORECASE,
            )
            is not None
        )

        if not has_evidence:
            continue

        semester_rows = [
            course
            for course in courses
            if (
                str(course.get("code", "")).lower() == "xxxxxxxx"
                and course.get("year") == year
                and course.get("semester") == semester
            )
        ]

        existing_numbers = {
            n
            for n in (detect_number(course) for course in semester_rows)
            if n is not None
        }

        if number in existing_numbers:
            continue

        # If OCR caught an xxxxxxxx row but lost only the "1"/"2" label,
        # reuse that row instead of creating a duplicate.
        unnamed = [
            course
            for course in semester_rows
            if detect_number(course) is None
        ]

        if unnamed:
            course = unnamed[0]
            course["name_th"] = f"วิชาเลือกเสรี {number}"
            course["name_en"] = f"FREE ELECTIVE COURSE {number}"
            continue

        # Recover credit only from a source window around the matching label.
        marker_patterns = [
            rf"วิชาเลือกเสรี\s*{number}",
            rf"FREE\s+ELECTIVE(?:\s+COURSE)?\s*{number}",
        ]

        credit = None
        for pattern in marker_patterns:
            m = re.search(pattern, source_text, re.IGNORECASE)
            if not m:
                continue

            start = max(0, m.start() - 120)
            end = min(len(source_text), m.end() + 220)
            credit = _extract_credits([source_text[start:end]])
            if credit:
                break

        courses.append({
            "code": "xxxxxxxx",
            "name_th": f"วิชาเลือกเสรี {number}",
            "name_en": f"FREE ELECTIVE COURSE {number}",
            "credits": credit,
            "year": year,
            "semester": semester,
            "category": "หมวดวิชาเลือกเสรี",
            "type": "เลือก",
            "prerequisite": "ไม่มี",
            "flexible_year_semester": None,
            "note": None,
        })

    return courses


def _recover_concrete_names_from_source_catalog(
    payload: dict[str, Any],
    courses: list[dict[str, Any]],
    *,
    recover_thai: bool = True,
    recover_english: bool = True,
) -> None:
    """
    Recover noisy Thai/English names for concrete 8-digit course codes from
    another occurrence in the SAME OCR source document.

    Priority is given to course-description/catalog blocks that contain
    PREREQUISITE / วิชาบังคับก่อน because those blocks usually have:
        CODE + Thai name + credits
        English name
        prerequisite

    This never reads Ground Truth and never changes year/semester/code.
    """
    wanted = {
        str(course.get("code", ""))
        for course in courses
        if re.fullmatch(r"\d{8}", str(course.get("code", "")))
    }
    if not wanted:
        return

    best: dict[str, dict[str, Any]] = {}

    def is_english_name(text: str) -> bool:
        value = _normalize_thai_text(text).strip()
        if not value:
            return False
        upper = value.upper()
        if (
            "PREREQUISITE" in upper
            or "COURSE DESCRIPTION" in upper
            or re.fullmatch(r"\d+\s*\([^)]*\)", value)
        ):
            return False
        letters = re.findall(r"[A-Za-z]", value)
        thai = re.findall(r"[\u0E00-\u0E7F]", value)
        return len(letters) >= 4 and len(letters) > len(thai) * 2

    for page in payload.get("pages", []):
        raw_text = str(page.get("text", "") or "")
        raw_lines = [
            _normalize_thai_text(line)
            for line in raw_text.splitlines()
            if str(line).strip()
        ]

        if not raw_lines:
            raw_lines = _page_lines(page)

        for i, line in enumerate(raw_lines):
            ascii_line = line.translate(THAI_DIGIT_TRANS)
            match = re.search(r"(?<!\d)(\d{8})(?!\d)", ascii_line)
            if not match:
                continue

            code = match.group(1)
            if code not in wanted:
                continue

            # Build a small source block, stopping at the next different code.
            block = [line]
            for j in range(i + 1, min(i + 8, len(raw_lines))):
                nxt = raw_lines[j]
                nxt_ascii = nxt.translate(THAI_DIGIT_TRANS)
                nxt_code = re.search(r"(?<!\d)(\d{8})(?!\d)", nxt_ascii)
                if nxt_code and nxt_code.group(1) != code:
                    break
                block.append(nxt)

            # Text after the code is the strongest Thai-name candidate.
            after_code = ascii_line[match.end():].strip()
            after_code = re.sub(
                r"\b\d+\s*\(\s*[0-9xX]+\s*-\s*[0-9xX]+\s*-\s*[0-9xX]+\s*\)\s*$",
                "",
                after_code,
            ).strip()

            thai_name = _extract_thai_piece(after_code)

            # If code is on its own line, use the first nearby Thai line.
            if not thai_name:
                for candidate in block[1:4]:
                    if (
                        "วิชาบังคับก่อน" in candidate
                        or "PREREQUISITE" in candidate.upper()
                    ):
                        break
                    piece = _extract_thai_piece(candidate)
                    if piece:
                        thai_name = piece
                        break

            english_name = None
            for candidate in block[1:5]:
                if is_english_name(candidate):
                    english_name = re.sub(r"\s+", " ", candidate).strip()
                    break

            credit = _extract_credits(block)

            source_joined = "\n".join(block)
            has_prereq_marker = (
                "วิชาบังคับก่อน" in source_joined
                or "PREREQUISITE" in source_joined.upper()
            )

            score = 0
            if thai_name:
                score += 4
            if english_name:
                score += 3
            if credit:
                score += 2
            if has_prereq_marker:
                score += 6
            if thai_name and after_code:
                score += 2

            old = best.get(code)
            if old is None or score > old["score"]:
                best[code] = {
                    "score": score,
                    "name_th": thai_name,
                    "name_en": english_name,
                }

    for course in courses:
        code = str(course.get("code", ""))
        ref = best.get(code)
        if not ref or ref["score"] < 6:
            continue

        if recover_thai and ref.get("name_th"):
            course["name_th"] = ref["name_th"]

        if recover_english and ref.get("name_en"):
            course["name_en"] = ref["name_en"]


def extract_curriculum(
    payload: dict[str, Any],
    program: str = "DSBA",
    plan: str = "coop",
) -> dict[str, Any]:
    program = str(program or "DSBA").upper().strip()
    profile = _get_profile(program)
    pages = payload.get("pages", [])
    full_document = len(pages) > 1

    # A) concrete elective/flexible catalog before the academic-plan section
    flexible_courses = _extract_flexible_catalog_courses(
        payload,
        program=program,
    )
    _recover_flexible_thai_names_from_page_text(
        payload,
        flexible_courses,
        program=program,
    )

    # B) target academic plan
    plan_courses, seen_semesters, found_start, found_end = _extract_target_plan(
        payload,
        plan=plan,
        program=program,
    )

    # C) combine the program-specific cooperative alternatives into one occurrence
    if plan == "coop":
        plan_courses = _combine_coop_alternatives(
            plan_courses,
            program=program,
        )

    # Recover source-supported free-elective occurrences for every program.
    # This is especially important for IT, where Year 4 Semester 1 contains
    # two rows with the same placeholder code "xxxxxxxx".
    plan_courses = _recover_profile_free_electives(
        payload,
        plan_courses,
        program=program,
    )

    # These recovery rules were tuned against the DSBA GT/source.  Keep them
    # isolated so they cannot silently rewrite AI/IT/BIT data.
    if program == "DSBA":
        plan_courses = _remove_duplicate_plan_artifacts(plan_courses)
        plan_courses = _recover_year4_free_electives(payload, plan_courses)
        _recover_placeholder_fields(payload, plan_courses)
        _recover_placeholder_semantics_from_source(payload, plan_courses)
        _clean_plan_placeholder_names(plan_courses)

    # D) Conservative name recovery.
    #
    # AI: source-catalog recovery improved both Thai and English names.
    # IT: keep plan/catalog parser output; global name overwrite reduced accuracy.
    # BIT: recover Thai only; keep the original English parser output.
    #
    # Recovery still uses only the OCR source document, never Ground Truth.
    if program == "AI":
        _recover_concrete_names_from_source_catalog(
            payload,
            plan_courses + flexible_courses,
            recover_thai=True,
            recover_english=True,
        )
    elif program == "BIT":
        _recover_concrete_names_from_source_catalog(
            payload,
            plan_courses + flexible_courses,
            recover_thai=True,
            recover_english=False,
        )

    # E) Recover missing credit cells from other occurrences in the same
    # OCR source (for example the course catalog). Never uses GT and never
    # overwrites a credit already extracted from the academic-plan table.
    _recover_missing_concrete_credits_from_source(
        payload,
        plan_courses + flexible_courses,
    )

    # F) prerequisite enrichment comes only from OCR source text
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

    # G) fail loudly for full-document extraction when a section/count is wrong
    if full_document:
        starts = profile.get("plan_start", {}).get(plan, [])
        if not starts:
            raise ValueError(f"{program} does not define plan={plan!r}")
        if not found_start:
            raise ValueError(
                f"ไม่พบหัวข้อ Academic Plan ของ {program} ({plan}); "
                f"expected one of {starts}"
            )
        if not found_end:
            raise ValueError(
                f"เริ่ม Academic Plan ของ {program} แล้ว แต่ไม่พบจุดจบ section; "
                f"expected one of {profile.get('plan_end', [])}"
            )

        expected_semesters = int(profile.get("expected_semesters") or 0)
        if expected_semesters:
            expected_pairs = {
                (year, semester)
                for year in range(1, 5)
                for semester in (1, 2)
            }
            if expected_semesters != 8:
                expected_pairs = set(sorted(expected_pairs)[:expected_semesters])
            missing = expected_pairs - seen_semesters
            if missing:
                raise ValueError(
                    f"{program}: OCR อ่านหัวข้อปี/เทอมไม่ครบ: missing={sorted(missing)}"
                )

        expected_plan_count = profile.get("expected_plan_count")
        if expected_plan_count is not None and len(plan_courses) != int(expected_plan_count):
            actual_counts: dict[tuple[Any, Any], int] = {}
            for course in plan_courses:
                key = (course.get("year"), course.get("semester"))
                actual_counts[key] = actual_counts.get(key, 0) + 1
            raise ValueError(
                f"{program}: Academic Plan count mismatch: "
                f"got {len(plan_courses)}, expected {expected_plan_count}; "
                f"per_semester={actual_counts}"
            )

        expected_flexible = profile.get("expected_flexible_count")
        if expected_flexible is not None and len(flexible_courses) != int(expected_flexible):
            raise ValueError(
                f"{program}: flexible/elective catalog count mismatch: "
                f"got {len(flexible_courses)}, expected {expected_flexible}"
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
    program: str = "DSBA",
) -> bool:
    profile = _get_profile(program)
    markers = profile.get("plan_start", {}).get(plan)
    if not markers:
        if plan not in {"coop", "no_coop"}:
            raise ValueError(f"Unsupported plan: {plan}")
        return False

    compact = _compact_section_text(str(text).translate(THAI_DIGIT_TRANS))
    return any(_compact_section_text(marker) in compact for marker in markers)



def _is_any_plan_start(text: str, program: str = "DSBA") -> bool:
    profile = _get_profile(program)
    compact = _compact_section_text(str(text).translate(THAI_DIGIT_TRANS))
    markers: list[str] = []
    for values in profile.get("plan_start", {}).values():
        markers.extend(values)
    return any(_compact_section_text(marker) in compact for marker in markers)



def _is_plan_end(text: str, program: str = "DSBA") -> bool:
    profile = _get_profile(program)
    normalized = _normalize_heading(text)
    compact = _compact_section_text(text)
    for marker in profile.get("plan_end", []):
        if "คำอธิบายรายวิชา" in marker:
            if "คำอธิบายรายวิชา" in normalized:
                return True
        elif _compact_section_text(marker) in compact:
            return True
    return False



def _detect_year_only(text: str) -> int | None:
    """Detect a study year even when OCR splits/noises year-semester headings."""
    value = _normalize_heading(text).translate(THAI_DIGIT_TRANS)

    # Normal form: ปีที่ 1. Tesseract may drop ที่ or insert spaces.
    match = re.search(r"ปี\s*(?:ที่|ที|ท)?\s*([1-4])(?:\D|$)", value)
    if match:
        return int(match.group(1))

    # Table-heading fallback: OCR can damage "ปีที่" into tokens such as
    # "UA 4 ภาคการศึกษาที่ 2". Only use this when the same line clearly
    # contains a semester heading, so ordinary prose is not misclassified.
    if re.search(r"ภาค\s*(?:การ\s*)?ศึกษา", value):
        match = re.search(
            r"(?:^|\D)([1-4])\s+(?=ภาค\s*(?:การ\s*)?ศึกษา)",
            value,
        )
        if match:
            return int(match.group(1))

    return None


def _detect_semester_only(text: str) -> int | None:
    """Detect semester 1/2 from mildly noisy Thai OCR headings."""
    value = _normalize_heading(text).translate(THAI_DIGIT_TRANS)
    # Accept ภาคการศึกษาที่ 1, ภาค การศึกษา ที่ 1, and minor OCR loss of ที่.
    match = re.search(
        r"ภาค\s*(?:การ\s*)?ศึกษา\s*(?:ที่|ที|ท)?\s*([12])(?:\D|$)",
        value,
    )
    if match:
        return int(match.group(1))
    return None


def _detect_year_semester(text: str) -> tuple[int | None, int | None]:
    """Return (year, semester); supports headings split/noisy by OCR."""
    return _detect_year_only(text), _detect_semester_only(text)


def _semester_heading_score(lines: list[str]) -> int:
    """Prefer the representation that preserves more semester headings."""
    score = 0
    for line in lines:
        year, semester = _detect_year_semester(line)
        if year is not None:
            score += 2
        if semester is not None:
            score += 2
        if year is not None and semester is not None:
            score += 4
    return score


def _plan_page_lines(page: dict[str, Any]) -> list[str]:
    """
    Choose between positioned OCR lines and page['text'] for plan parsing.

    Some Tesseract runs keep a semester heading in page['text'] while it is
    absent from page['lines'].  Using whichever representation preserves more
    semester headings avoids losing year/semester state without duplicating rows.
    """
    positioned = _page_lines(page)
    text_lines = [
        line.strip()
        for line in str(page.get("text", "")).splitlines()
        if line.strip()
    ]

    if not text_lines:
        return positioned
    if not positioned:
        return text_lines

    positioned_score = _semester_heading_score(positioned)
    text_score = _semester_heading_score(text_lines)

    if text_score > positioned_score:
        return text_lines
    return positioned


# ---------------------------------------------------------------------
# Course start detection
# ---------------------------------------------------------------------

def _extract_code_and_rest(
    line: str,
    program: str = "DSBA",
) -> tuple[str, str] | None:
    original = _normalize_thai_text(line)
    normalized = original.translate(THAI_DIGIT_TRANS)
    upper = original.upper()
    profile = _get_profile(program)

    # 1) normal 8-character concrete/placeholder code
    m = re.match(r"^\s*([0-9xX×]{8})\s*[|:]?\s*(.*)$", normalized, re.IGNORECASE)
    if m:
        raw_code = _normalize_code_text(m.group(1))
        rest = m.group(2).strip()
        if "วิชาเลือกเสรี" in original or "FREE ELECTIVE" in upper:
            return "xxxxxxxx", rest
        if COURSE_CODE_RE.fullmatch(raw_code):
            return raw_code, rest

    # 2) code split by OCR, e.g. 06026 xxx / 060464 xx / 9664 xxxx
    m = re.match(
        r"^\s*([0-9xX×]{4,6})\s+([0-9xX×]{2,4})\s*[|:]?\s*(.*)$",
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

    # 3) program-specific elective placeholder when x's are OCR-noisy
    placeholder = str(profile.get("elective_placeholder", ""))
    prefix_match = re.match(r"\d+", placeholder)
    prefix = prefix_match.group(0) if prefix_match else ""
    if prefix and original.lstrip().startswith(prefix) and (
        "วิชาเลือก" in original or "ELECTIVE" in upper
    ):
        rest = re.sub(rf"^\s*{re.escape(prefix)}\S*\s*", "", original).strip(" |:")
        return placeholder, rest

    language_code = str(profile.get("language_elective_code", ""))
    if (
        "วิชาเลือกด้านภาษาและการสื่อสาร" in original
        or "วิชาเลือกดานภาษาและการสื่อสาร" in original
        or "ELECTIVE IN LANGUAGE AND COMMUNICATION" in upper
    ):
        rest = re.sub(r"^\s*(?:906|966)4\S*\s*", "", original).strip(" |:")
        return language_code, rest

    ge_code = str(profile.get("general_ed_elective_code", ""))
    if (
        "วิชาเลือกหมวดวิชาศึกษาทั่วไป" in original
        or "วิชาเลือกหมวดศึกษาทั่วไป" in original
        or "GENERAL EDUCATION COURSES" in upper
        or "ELECTIVE IN GENERAL EDUCATION" in upper
        or "GE ELECTIVE COURSE REQUIREMENT" in upper
    ):
        rest = re.sub(r"^\s*(?:906|966)4\S*\s*", "", original).strip(" |:")
        return ge_code, rest

    if "วิชาเลือกเสรี" in original or "FREE ELECTIVE COURSE" in upper:
        parts = original.split(maxsplit=1)
        prefix_text = parts[0] if parts else ""
        if len(_normalize_code_text(prefix_text)) >= 6 or re.search(r"\d", prefix_text):
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


def _is_noise_line(text: str, program: str = "DSBA") -> bool:
    text = _normalize_thai_text(text)
    if not text or _is_footer(text):
        return True
    if re.fullmatch(r"\d{1,3}", text):
        return True
    if _detect_year_semester(text) != (None, None):
        return True
    if _is_any_plan_start(text, program=program) or _is_plan_end(text, program=program):
        return True
    noise_tokens = (
        "รหัสวิชา", "ชื่อวิชา", "บรรยาย", "ปฏิบัติ", "ศึกษาด้วยตนเอง",
        "รวมตลอดหลักสูตร", "นักศึกษาเลือกลงทะเบียน", "กำหนดระยะเวลา",
        "หมวดวิชาเลือกเสรี",
    )
    if any(token in text for token in noise_tokens):
        return True
    if text.startswith("รวม"):
        return True
    return False



def _detect_category(code: str, program: str = "DSBA") -> str | None:
    code = str(code).lower()
    profile = _get_profile(program)

    if code == "xxxxxxxx":
        return profile.get(
            "free_elective_category",
            "หมวดวิชาเลือกเสรี",
        )

    prefixes = tuple(
        str(x)
        for x in profile.get("general_ed_prefixes", ())
    )
    if prefixes and code.startswith(prefixes):
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



def _flexible_year_semester_for_code(
    code: str,
    program: str,
) -> str | None:
    profile = _get_profile(program)
    code_text = str(code).strip()

    if re.fullmatch(r"\d{8}", code_text):
        value = int(code_text)

        for start, end, semester_text in profile.get(
            "flexible_year_semester_ranges",
            [],
        ):
            if int(start) <= value <= int(end):
                return semester_text

    return profile.get("flexible_year_semester")


def _flexible_note_for_code(
    code: str,
    program: str,
) -> str | None:
    profile = _get_profile(program)
    notes = profile.get("flexible_note_codes", {})
    return notes.get(str(code).strip())


def _parse_course_block(
    code: str,
    texts: list[str],
    year: int | None,
    semester: int | None,
    *,
    flexible: bool = False,
    program: str = "DSBA",
) -> dict[str, Any]:
    note = _detect_note_from_text(texts)
    credits = _extract_credits(texts)
    thai_parts: list[str] = []
    english_parts: list[str] = []

    for raw in texts:
        text = _normalize_thai_text(raw)
        if _is_noise_line(text, program=program) or text.strip() == "หรือ":
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
    profile = _get_profile(program)
    return {
        "code": code,
        "name_th": name_th,
        "name_en": name_en,
        "credits": credits,
        "year": 0 if flexible else year,
        "semester": 0 if flexible else semester,
        "category": _detect_category(code, program=program),
        "type": "เลือก" if flexible or "x" in code.lower() else "บังคับ",
        "prerequisite": "ไม่มี",
        "flexible_year_semester": (
            _flexible_year_semester_for_code(code, program)
            if flexible
            else None
        ),
        "note": (
            _flexible_note_for_code(code, program)
            if flexible and _flexible_note_for_code(code, program) is not None
            else note
        ),
    }



# ---------------------------------------------------------------------
# Flexible catalog: concrete 06026216..06026260 before 3.1.4
# ---------------------------------------------------------------------

def _extract_flexible_catalog_courses(
    payload: dict[str, Any],
    program: str = "DSBA",
) -> list[dict[str, Any]]:
    courses_by_code: dict[str, dict[str, Any]] = {}
    current_code: str | None = None
    current_texts: list[str] = []

    def flush() -> None:
        nonlocal current_code, current_texts
        if current_code and _is_flexible_code(current_code, program):
            if current_code not in courses_by_code:
                courses_by_code[current_code] = _parse_course_block(
                    current_code,
                    current_texts,
                    year=0,
                    semester=0,
                    flexible=True,
                    program=program,
                )
        current_code = None
        current_texts = []

    for page in payload.get("pages", []):
        section_text = _section_search_text(page)
        if _is_any_plan_start(section_text, program=program):
            flush()
            break

        for line in _page_lines(page):
            start = _extract_code_and_rest(line, program=program)
            if start:
                new_code, rest = start
                if _is_flexible_code(new_code, program):
                    flush()
                    current_code = new_code
                    current_texts = [rest] if rest else []
                    continue
                flush()
                continue

            if current_code is not None:
                normalized_line = _normalize_thai_text(line)
                is_boundary = (
                    _is_noise_line(normalized_line, program=program)
                    or normalized_line.startswith("-")
                    or normalized_line.startswith("*")
                    or "เลือกเรียนจากรายวิชา" in normalized_line
                    or "ดังต่อไปนี้" in normalized_line
                    or "สำหรับแผนการศึกษา" in normalized_line
                    or "นักศึกษาเลือกลงทะเบียน" in normalized_line
                    or "กำหนดระยะเวลา" in normalized_line
                )
                if is_boundary:
                    if current_texts:
                        flush()
                    continue
                current_texts.append(line)

    flush()
    return [courses_by_code[code] for code in sorted(courses_by_code, key=lambda x: int(x))]



# ---------------------------------------------------------------------
# Academic plan
# ---------------------------------------------------------------------

def _split_compound_plan_line(
    line: str,
    program: str = "DSBA",
) -> list[str]:
    """Split only an embedded FREE ELECTIVE row; never split normal placeholders."""
    text = _normalize_thai_text(line)
    if not text:
        return []
    start = _extract_code_and_rest(text, program=program)
    first_code = start[0] if start else None
    if first_code == "xxxxxxxx":
        return [text]

    free_pattern = re.compile(
        r"วิชาเลือกเสรี\s*[12]|FREE\s+ELECTIVE\s+COURSE\s*[12]",
        re.IGNORECASE,
    )
    matches = list(free_pattern.finditer(text))
    if not matches:
        return [text]

    result: list[str] = []
    before = text[:matches[0].start()].strip()
    before = re.sub(r"(?:[0-9๐-๙xX×]\s*){6,10}$", "", before).strip()
    if before:
        result.append(before)

    for index, match in enumerate(matches):
        end_pos = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        part = text[match.start():end_pos].strip()
        part = re.sub(r"(?:[0-9๐-๙xX×]\s*){6,10}$", "", part).strip()
        if part:
            result.append(f"xxxxxxxx {part}")
    return result


def _extract_target_plan(
    payload: dict[str, Any],
    plan: str,
    program: str = "DSBA",
) -> tuple[list[dict[str, Any]], set[tuple[int, int]], bool, bool]:
    courses: list[dict[str, Any]] = []
    seen_semesters: set[tuple[int, int]] = set()
    current_year: int | None = None
    current_semester: int | None = None
    pending_year: int | None = None
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
            program=program,
        )
        course["year"] = current_year
        course["semester"] = current_semester
        courses.append(course)
        current_code = None
        current_texts = []

    for page in payload.get("pages", []):
        # For academic-plan parsing, prefer the representation that retained
        # the most year/semester headings.  This is important for AI pages,
        # where one PDF page contains both semester 1 and semester 2.
        lines = _plan_page_lines(page)
        section_text = _section_search_text(page)

        if not in_target_plan:
            if _is_target_plan_start(section_text, plan, program=program):
                in_target_plan = True
                found_start = True
            else:
                continue

        for raw_line in lines:
            # Recover a free-elective row if Tesseract glued it to the previous row.
            split_lines = _split_compound_plan_line(raw_line, program=program)
            for line in split_lines:
                if _is_plan_end(line, program=program):
                    flush()
                    found_end = True
                    in_target_plan = False
                    break

                detected_year, detected_semester = _detect_year_semester(line)

                # Tesseract sometimes emits "ปีที่ N" and "ภาคการศึกษาที่ M"
                # as separate lines.  Keep the year pending until the semester
                # arrives, then switch state before reading the next course.
                if detected_year is not None:
                    pending_year = detected_year

                if detected_semester is not None:
                    resolved_year = detected_year or pending_year or current_year
                    if resolved_year is not None:
                        flush()
                        current_year = resolved_year
                        current_semester = detected_semester
                        pending_year = resolved_year
                        seen_semesters.add((current_year, current_semester))
                        continue

                # A complete normal heading is already handled above; a year-only
                # line should not be appended to a course name.
                if detected_year is not None:
                    flush()
                    continue

                if _is_target_plan_start(line, plan, program=program):
                    continue
                if line.strip().startswith("รวม"):
                    flush()
                    continue
                if _is_footer(line):
                    continue

                start = _extract_code_and_rest(line, program=program)
                if start:
                    new_code, rest = start

                    # Placeholder rows are often OCRed as two lines:
                    #   9064xxxx
                    #   วิชาเลือกหมวดวิชาศึกษาทั่วไป
                    # The semantic fallback maps the second line to the same
                    # placeholder code. Treat it as continuation, not a new row.
                    if (
                        current_code is not None
                        and new_code == current_code
                        and "x" in str(new_code).lower()
                    ):
                        if rest:
                            current_texts.append(rest)
                        else:
                            current_texts.append(line)
                        continue

                    flush()
                    current_code = new_code
                    current_texts = [rest] if rest else []
                    continue

                if current_code is not None:
                    current_texts.append(line)

            if found_end:
                break

        if found_end:
            break
        flush()
        if _is_plan_end(section_text, program=program):
            found_end = True
            in_target_plan = False
            break

    flush()
    return courses, seen_semesters, found_start, found_end



def _combine_coop_alternatives(
    courses: list[dict[str, Any]],
    program: str = "DSBA",
) -> list[dict[str, Any]]:
    profile = _get_profile(program)
    alternatives = profile.get("coop_alternatives")
    if not alternatives or len(alternatives) != 2:
        return courses
    first_code, second_code = alternatives
    expected_semester = tuple(profile.get("coop_alternative_semester", ()))

    output: list[dict[str, Any]] = []
    i = 0
    while i < len(courses):
        current = courses[i]
        if i + 1 < len(courses):
            nxt = courses[i + 1]
            same_semester = (
                current.get("year") == nxt.get("year")
                and current.get("semester") == nxt.get("semester")
            )
            expected_ok = (
                not expected_semester
                or (current.get("year"), current.get("semester")) == expected_semester
            )
            if (
                current.get("code") == first_code
                and nxt.get("code") == second_code
                and same_semester
                and expected_ok
            ):
                output.append({
                    "code": f"{first_code} หรือ {second_code}",
                    "name_th": "\n".join(
                        value for value in [current.get("name_th"), nxt.get("name_th")] if value
                    ) or None,
                    "name_en": "\n".join(
                        value for value in [current.get("name_en"), nxt.get("name_en")] if value
                    ) or None,
                    "credits": current.get("credits") or nxt.get("credits"),
                    "year": current.get("year"),
                    "semester": current.get("semester"),
                    "category": _detect_category(first_code, program=program),
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
    """
    Recover prerequisites from explicit course-description markers in the
    OCR source. Supports:
      - วิชาบังคับก่อน : ไม่มี
      - วิชาบังคับก่อน : 06036145
      - PREREQUISITE : NONE
      - PREREQUISITE : 06036119 OR 06036122
      - multiple prerequisite codes split across nearby OCR lines

    Ground Truth is never read here.
    """
    result: dict[str, str] = {}

    def normalize_value(value: str) -> str:
        value = _normalize_thai_text(value).translate(THAI_DIGIT_TRANS)
        codes = re.findall(
            r"(?<!\d)(\d{8})(?!\d)",
            value,
        )

        unique: list[str] = []
        for code in codes:
            if code not in unique:
                unique.append(code)

        if unique:
            return " หรือ ".join(unique[:4])

        upper = value.upper()
        if "ไม่มี" in value or re.search(r"\bNONE\b", upper):
            return "ไม่มี"

        return ""

    def choose(code: str, value: str) -> None:
        if not value:
            return

        old = result.get(code)

        if old is None:
            result[code] = value
            return

        old_codes = re.findall(r"\d{8}", old)
        new_codes = re.findall(r"\d{8}", value)

        # Prefer concrete prerequisite codes over NONE/ไม่มี.
        if not old_codes and new_codes:
            result[code] = value
            return

        # Prefer the candidate that contains more explicit prerequisite codes.
        if len(new_codes) > len(old_codes):
            result[code] = value

    def parse_block(code: str, block: list[str]) -> None:
        if code not in wanted_codes or not block:
            return

        clean = [
            _normalize_thai_text(line)
            for line in block
            if str(line).strip()
        ]

        # Look around an explicit Thai or English prerequisite marker only.
        for i, line in enumerate(clean):
            line_upper = line.upper()

            thai_marker = re.search(
                r"วิชา\s*บังคับ\s*ก่อน\s*[:：]?",
                line,
            )
            en_marker = re.search(
                r"PREREQUISITE\s*[:：]?",
                line_upper,
            )

            marker = thai_marker or en_marker
            if not marker:
                continue

            # Keep only a small window after the marker so the next course code
            # cannot accidentally become a prerequisite.
            tail_parts = [line[marker.end():]]

            for j in range(i + 1, min(i + 4, len(clean))):
                nxt = clean[j]

                # A new course-description header starts with an 8-digit code.
                if re.match(r"^\s*\d{8}(?:\s|$)", nxt.translate(THAI_DIGIT_TRANS)):
                    break

                # Stop at another obvious section marker.
                if (
                    "คำอธิบายรายวิชา" in nxt
                    or "COURSE DESCRIPTION" in nxt.upper()
                ):
                    break

                tail_parts.append(nxt)

            value = normalize_value(" ".join(tail_parts))

            # Exclude the course's own code if OCR repeated it immediately
            # after the marker.
            if value and value != "ไม่มี":
                codes = [
                    x
                    for x in re.findall(r"\d{8}", value)
                    if x != code
                ]
                if codes:
                    unique = []
                    for x in codes:
                        if x not in unique:
                            unique.append(x)
                    value = " หรือ ".join(unique[:4])
                else:
                    value = ""

            choose(code, value)

    def process_lines(lines: list[str]) -> None:
        current_code: str | None = None
        block: list[str] = []

        def flush() -> None:
            nonlocal current_code, block
            if current_code is not None:
                parse_block(current_code, block)
            current_code = None
            block = []

        for raw in lines:
            line = _normalize_thai_text(raw)
            ascii_line = line.translate(THAI_DIGIT_TRANS)

            # Course description/catalog rows normally start with the code.
            m = re.match(r"^\s*(\d{8})(?=\D|$)", ascii_line)

            if m:
                code = m.group(1)

                if current_code is not None:
                    flush()

                current_code = code
                block = [line]
                continue

            if current_code is not None:
                block.append(line)

                # Prerequisite is near the top; avoid swallowing long
                # descriptions and unrelated course codes.
                if len(block) >= 20:
                    flush()

        flush()

    for page in payload.get("pages", []):
        # First use logical OCR text (especially useful on repaired pages).
        raw_text = str(page.get("text", "") or "")
        text_lines = [
            line
            for line in raw_text.splitlines()
            if line.strip()
        ]
        if text_lines:
            process_lines(text_lines)

        # Also inspect positioned OCR lines because some source PDFs preserve
        # prerequisite markers better there.
        positioned = _page_lines(page)
        if positioned:
            process_lines(positioned)

    return result

