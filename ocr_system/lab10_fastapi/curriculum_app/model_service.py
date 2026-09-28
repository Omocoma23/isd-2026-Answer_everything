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
        prompt = f"""แปลงคำถามเป็น SQLite SQL จาก schema นี้
{SQL_SCHEMA_CONTEXT}

กติกา:
- ตอบ SELECT หรือ WITH คำสั่งเดียว
- ถามหน่วยกิตรายเทอมให้ใช้ v_semester_credits
- ถามรายวิชาตามแผนให้ใช้ v_plan
- ห้ามแก้ไขฐานข้อมูล
- รหัสวิชาเป็นตัวเลข 8 หลักติดกัน
- ถ้าคำถามมีรหัสวิชา ให้คัดลอกรหัสนั้นตรง ๆ ห้ามเปลี่ยน
- ถ้าค้นหารายวิชาจากชื่อ ห้ามใช้ = ให้ใช้ LIKE เสมอ
- การค้นชื่อภาษาไทยใช้รูปแบบ name_th LIKE '%ชื่อวิชา%'
- คำว่า "วิชา" ในคำถามเป็นคำบอกประเภท ไม่ใช่ส่วนหนึ่งของชื่อวิชา
- ห้ามเติมคำว่า "วิชา" เข้าไปในค่าที่ค้นหา

ตัวอย่าง:
คำถาม: วิชาพื้นฐานทางธุรกิจสำหรับเทคโนโลยีสารสนเทศมีรหัสอะไร
SQL: SELECT code FROM course
     WHERE name_th LIKE '%พื้นฐานทางธุรกิจสำหรับเทคโนโลยีสารสนเทศ%'

คำถาม: วิชา 06026202 มีกี่หน่วยกิต
คำถาม: หลักสูตรนี้มีกี่หน่วยกิต
SQL: SELECT total_credits FROM program

คำถาม: วิชา 06026202 มีกี่หน่วยกิต
SQL: SELECT credits FROM course WHERE code='06026202'

คำถาม: {question}
ตอบ JSON ที่มี key ชื่อ sql"""

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

    def summarize(self, question: str, rows: list[dict[str, Any]]) -> str:
        prompt = f"""ตอบภาษาไทยจากผลฐานข้อมูลเท่านั้น
คำถาม: {question}
ผลฐานข้อมูล: {json.dumps(rows[:40], ensure_ascii=False)}
ตอบ JSON ที่มี key ชื่อ answer และห้ามเพิ่มข้อมูลที่ไม่มีในผล"""
        return str(self._chat(prompt, ANSWER_SCHEMA).get("answer", "")).strip()

    def ask(self, database: CurriculumDatabase, question: str) -> dict:
        sql, rows = database.query_from_model(self.make_sql(question))
        answer = self.summarize(question, rows) if rows else "ไม่พบข้อมูลนี้ในฐานข้อมูลหลักสูตร"
        return {"question": question, "sql": sql, "rows": rows, "answer": answer}
