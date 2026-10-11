"""Qwen text-to-SQL adapter that reuses Lab 8B's Ollama helper."""

import json
import re
from types import ModuleType
from typing import Any

import requests

from .config import Settings
from .database import CurriculumDatabase, SQL_SCHEMA_CONTEXT


SQL_SCHEMA = {
    "type": "object",
    "properties": {"sql": {"type": "string"}},
    "required": ["sql"],
    "additionalProperties": False,
}
ANSWER_SCHEMA = {
    "type": "object",
    "properties": {"answer": {"type": "string"}},
    "required": ["answer"],
    "additionalProperties": False,
}


class QwenTextToSQL:
    def __init__(self, config: Settings, lab8b: ModuleType):
        self.config = config
        self.lab8b = lab8b

    def available(self) -> bool:
        try:
            return requests.get(
                f"{self.config.ollama_url}/api/tags", timeout=3
            ).ok
        except requests.RequestException:
            return False

    def _chat(self, prompt: str, schema: dict) -> dict:
        # MODEL INTEGRATION POINT: เปลี่ยนฟังก์ชันนี้หากไม่ใช้ Ollama/Qwen
        # เรียกฟังก์ชัน Ollama ของ Lab 8B โดยตรง เพื่อไม่สร้าง client ซ้ำใน Lab 10
        raw = self.lab8b.ollama_generate(
            prompt, fmt=schema, timeout=self.config.request_timeout,
            model=self.config.ollama_model, num_ctx=4096, num_predict=256,
        )
        return self.lab8b.parse_json_loose(raw)

    def make_sql(self, question: str) -> str:
        structured_sql = self.lab8b.structured_question_sql(question)
        if structured_sql:
            return structured_sql

        prompt = f"""แปลงคำถามภาษาไทยเป็น SQLite SQL โดยใช้ schema นี้

{SQL_SCHEMA_CONTEXT}

กติกา:
- สร้างคำสั่งอ่านข้อมูลคำสั่งเดียว เริ่มด้วย SELECT หรือ WITH เท่านั้น
- ใช้เฉพาะตาราง คอลัมน์ และ view ที่ระบุใน schema
- ถ้ามีหลายเงื่อนไข ให้เชื่อมด้วย AND หรือ OR ตามความหมาย
- คำถามหารายวิชาตามปีหรือภาคเรียน ให้ใช้ v_plan
- ถ้าขอรายชื่อวิชา ให้คืน code, ชื่อวิชา และ credits ทุกแถวที่ตรงเงื่อนไข
- ถ้าถามสองเทอม ให้คืน year และ semester เพื่อแยกกลุ่มผลลัพธ์
- ถ้าถามจำนวนและหน่วยกิตรวมในเทอม ให้ใช้ n_courses และ credits จาก v_semester_credits
- ถ้าเปรียบเทียบจำนวนวิชาระหว่างสองเทอม ให้ใช้ v_semester_credits ทั้งสองเทอม
- ถ้าถามตำแหน่งของรหัสวิชาในแผน ให้ค้น code ใน v_plan และคืน year, semester, name_th, credits
- ถ้าถามช่องวิชาเลือก ให้คืน alt_group, code, name_th, credits และ note จาก v_plan
- คำถามหาหน่วยกิตรวม หรือจำนวนรายวิชาในภาคเรียน
  ให้ใช้ v_semester_credits
- ห้ามคำนวณ SUM(credits) จาก v_plan เพราะแถววิชาเลือกอาจถูกนับซ้ำ
- ค้นชื่อวิชาให้ใช้ LIKE
- ถ้าถามว่ามีวิชาที่ผ่านเกณฑ์หน่วยกิตและขอรหัส ให้คืนทั้ง code และ credits
  พร้อมระบุ alias ตารางและชื่อคอลัมน์ให้ชัด
- ถ้าคำถามระบุรหัสวิชา 8 หลัก ให้ใช้รหัสนั้นตรงตามที่ถาม
- ห้ามเขียนคำอธิบายหรือ Markdown ให้คืน JSON ที่มี key ชื่อ sql เท่านั้น

ตัวอย่าง:

คำถาม: ตามแผนการศึกษา ปี 1 เทอม 1 มีวิชาอะไรบ้าง ขอรหัส ชื่อวิชา และหน่วยกิตของแต่ละวิชา
SQL: SELECT year, semester, code, name_th, credits
     FROM v_plan WHERE year = 1 AND semester = 1 ORDER BY code

คำถาม: ปี 1 มีวิชาอะไรบ้างในเทอม 1 และเทอม 2 ช่วยแยกรายชื่อ รหัส และหน่วยกิตตามเทอม
SQL: SELECT year, semester, code, name_th, credits
     FROM v_plan WHERE year = 1 AND semester IN (1, 2) ORDER BY semester, code

คำถาม: ปี 1 เทอม 1 มีทั้งหมดกี่วิชา และมีหน่วยกิตรวมเท่าไร
SQL: SELECT n_courses AS course_count, credits AS total_credits
     FROM v_semester_credits WHERE year = 1 AND semester = 1

คำถาม: ปี 1 เทอม 1 กับเทอม 2 เทอมไหนมีวิชามากกว่า และต่างกันกี่วิชา
SQL: SELECT year, semester, n_courses FROM v_semester_credits
     WHERE year = 1 AND semester IN (1, 2) ORDER BY semester

คำถาม: วิชา 06026200 อยู่ในแผนการเรียนปีไหน เทอมไหน และมีชื่อกับหน่วยกิตเท่าไร
SQL: SELECT year, semester, code, name_th, credits
     FROM v_plan WHERE code = '06026200' ORDER BY year, semester

คำถาม: ปี 2 เทอม 1 มีวิชาเลือกอะไรบ้าง และมีตัวเลือกใดให้เลือกแทนกันได้
SQL: SELECT year, semester, alt_group, code, name_th, credits, note
     FROM v_plan
     WHERE year = 2 AND semester = 1
       AND (alt_group IS NOT NULL OR note LIKE '%เลือก%')
     ORDER BY alt_group, code

คำถาม: {question}
ตอบเป็น JSON รูปแบบ {{\"sql\": \"คำสั่ง SQL\"}} เท่านั้น
"""

        sql = str(
            self._chat(prompt, SQL_SCHEMA).get("sql", "")
        ).strip()

        sql = re.sub(
            r"^```(?:sql)?|```$",
            "",
            sql,
            flags=re.MULTILINE
        ).strip()

        # ถ้าคำถามมีรหัสวิชา 8 หลัก
        # ใช้รหัสจากคำถามเป็น source of truth
        code_match = re.search(r"(?<!\d)(\d{8})(?!\d)", question)

        if code_match:
            course_code = code_match.group(1)

            # บังคับแก้ค่าหลัง code= ให้เป็นรหัสจากคำถาม
            sql = re.sub(
                r"""(\bcode\s*=\s*['"])[^'"]*(['"])""",
                rf"\g<1>{course_code}\2",
                sql,
                flags=re.IGNORECASE
            )

        return sql

    def summarize(
        self, question: str, rows: list[dict[str, Any]], sql: str = "",
    ) -> str:
        prompt = f"""ตอบภาษาไทยจากผลฐานข้อมูลเท่านั้น
คำถาม: {question}
ผลฐานข้อมูล: {json.dumps(rows[:40], ensure_ascii=False)}
ถ้าผลฐานข้อมูลมีแถว ห้ามตอบว่าไม่พบข้อมูล
ตอบ JSON ที่มี key ชื่อ answer และห้ามเพิ่มข้อมูลที่ไม่มีในผล"""
        answer = str(self._chat(prompt, ANSWER_SCHEMA).get("answer", "")).strip()
        if self.lab8b.answer_conflicts_with_rows(answer, rows):
            return self.lab8b.answer_from_rows(question, rows, sql)
        return answer

    def ask(self, database: CurriculumDatabase, question: str) -> dict:
        sql, rows = database.query_from_model(self.make_sql(question))
        structured_answer = self.lab8b.answer_structured_question(question, rows)
        threshold_answer = self.lab8b.answer_threshold_course_question(
            question, rows, sql
        )
        if structured_answer is not None:
            answer = structured_answer
        elif threshold_answer:
            answer = threshold_answer
        else:
            answer = self.summarize(question, rows, sql) if rows else "ไม่พบข้อมูลนี้ในฐานข้อมูลหลักสูตร"
        return {"question": question, "sql": sql, "rows": rows, "answer": answer}
