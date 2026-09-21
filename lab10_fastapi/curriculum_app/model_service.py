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
        raw = self.lab8b.ollama_generate(
            prompt,
            fmt=schema,
            timeout=self.config.request_timeout,
            model=self.config.ollama_model,
            num_ctx=4096,
            num_predict=512,
        )

        print("\n========== QWEN RAW ==========")
        print(raw)
        print("================================\n")

        return self.lab8b.parse_json_loose(raw)

    def make_sql(self, question: str) -> str:
        prompt = f"""แปลงคำถามเป็น SQLite SQL จาก schema นี้
{SQL_SCHEMA_CONTEXT}

กติกา:
- ตอบ SELECT หรือ WITH คำสั่งเดียว
- ถามหน่วยกิตรายเทอมให้ใช้ v_semester_credits
- ถามรายวิชาตามแผนให้ใช้ v_plan
- ห้ามแก้ไขฐานข้อมูล

ตัวอย่าง:
คำถาม: หลักสูตรนี้มีกี่หน่วยกิต
SQL: SELECT total_credits FROM program
คำถาม: ต้องเรียนวิชาอะไรมาก่อนจึงจะลงเรียน 06026215 ได้
SQL: SELECT requires FROM prerequisite WHERE code='06026215' AND kind='pre'

คำถาม: {question}
ตอบ JSON ที่มี key ชื่อ sql"""
        sql = str(self._chat(prompt, SQL_SCHEMA).get("sql", "")).strip()
        return re.sub(r"^```(?:sql)?|```$", "", sql, flags=re.MULTILINE).strip()

    def summarize(self, question: str, rows: list[dict[str, Any]]) -> str:
        prompt = f"""ตอบคำถามเป็นภาษาไทยโดยใช้เฉพาะผลจากฐานข้อมูลเท่านั้น

คำถาม: {question}

ผลฐานข้อมูล:
{json.dumps(rows[:40], ensure_ascii=False, indent=2)}

กติกา:
- สรุปให้ผู้ใช้เข้าใจง่าย
- ห้ามเพิ่มข้อมูลที่ไม่มีอยู่ในผลฐานข้อมูล
- ถ้าเป็นรายการวิชา ให้บอกชื่อวิชาที่พบ
- ตอบเป็น JSON เท่านั้นในรูปแบบ:
{{"answer": "คำตอบภาษาไทย"}}
"""

        result = self._chat(prompt, ANSWER_SCHEMA)

        answer = str(result.get("answer", "")).strip()

        # ถ้า Qwen คืน JSON ไม่สมบูรณ์หรือ answer ว่าง
        if answer:
            return answer

        # fallback เพื่อไม่ให้หน้าเว็บแสดงคำตอบว่าง
        if not rows:
            return "ไม่พบข้อมูลนี้ในฐานข้อมูลหลักสูตร"

        names = [
            str(row.get("name_th")).strip()
            for row in rows
            if row.get("name_th")
        ]

        if names:
            return "รายวิชาที่พบ ได้แก่ " + ", ".join(names)

        return f"พบข้อมูลจากฐานข้อมูลทั้งหมด {len(rows)} รายการ"

    def ask(self, database: CurriculumDatabase, question: str) -> dict:
        sql, rows = database.query_from_model(self.make_sql(question))
        answer = self.summarize(question, rows) if rows else "ไม่พบข้อมูลนี้ในฐานข้อมูลหลักสูตร"
        return {"question": question, "sql": sql, "rows": rows, "answer": answer}
