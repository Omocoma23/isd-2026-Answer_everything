"""Application 1: curriculum database question answering."""

import json
import os
import sqlite3
import sys
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import PROJECT_ROOT, DB_MAP, settings

# เชื่อม Lab 10 -> Lab 8B โดยตรง: ใช้ open_db, guard_sql และ ollama_generate เดิม
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
os.environ["LAB8_OLLAMA_URL"] = settings.ollama_url
os.environ["LAB8_MODEL_TEXT"] = settings.ollama_model
from ocr_system import lab8b_curriculum_db as lab8b  # noqa: E402

from .database import CurriculumDatabase  # noqa: E402
from .model_service import QwenTextToSQL  # noqa: E402
from .schemas import (  # noqa: E402
    AskRequest, AskResponse, CourseCreate, CourseResponse, HealthResponse,
)


STATIC_DIR = Path(__file__).resolve().parent / "static"
app = FastAPI(
    title=f"{settings.app_name} — Curriculum",
    description="Qwen text-to-SQL + SQLite curriculum application",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
databases = {program: CurriculumDatabase(lab8b,db_path,settings.max_rows)for program, db_path in DB_MAP.items()}
model = QwenTextToSQL(settings, lab8b)


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health", response_model=HealthResponse)
def health() -> dict:
    db_ready = all(
        database.path.exists()
        for database in databases.values()
    )

    ollama_ready = model.available()

    return {
        "status": "ok" if db_ready and ollama_ready else "degraded",
        "database": ", ".join(
            f"{program}: {database.path}"
            for program, database in databases.items()
        ),
        "database_ready": db_ready,
        "model": settings.ollama_model,
        "ollama_ready": ollama_ready,
        "lab8b_module": str(Path(lab8b.__file__).resolve()),
    }


@app.get("/api/program")
def get_program(program: str = Query(default="IT")) -> dict:
    try:
        selected_database = databases[program]
        data = selected_database.program()

    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="ไม่พบหลักสูตรที่เลือก"
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc

    if data is None:
        raise HTTPException(
            status_code=404,
            detail="ไม่พบข้อมูลหลักสูตร"
        )

    return data


@app.get("/api/courses", response_model=list[CourseResponse])
def get_courses(
    program: str = Query(default="IT"),
    search: str = Query(default="", max_length=100),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[dict]:
    try:
        selected_database = databases[program]

        return selected_database.courses(
            search,
            limit,
            offset
        )

    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="ไม่พบหลักสูตรที่เลือก"
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc


@app.post(
    "/api/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def post_course(
    course: CourseCreate,
    program: str = Query(default="IT")
) -> dict:
    try:
        selected_database = databases[program]

        return selected_database.create_course(
            course.model_dump()
        )

    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="ไม่พบหลักสูตรที่เลือก"
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc

    except sqlite3.IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="รหัสวิชานี้มีอยู่แล้ว"
        ) from exc


@app.post("/api/ask", response_model=AskResponse)
def ask(request: AskRequest) -> dict:
    try:
        database = databases[request.program]

        result = model.ask(
            database,
            request.question
        )

        return {
            "program": request.program,
            **result,
        }

    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="ไม่พบหลักสูตรที่เลือก"
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc

    except requests.RequestException as exc:
        raise HTTPException(
            status_code=503,
            detail="ติดต่อ Ollama ไม่ได้"
        ) from exc

    except (
        ValueError,
        json.JSONDecodeError,
        sqlite3.Error,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc

@app.get("/api/programs")
def get_programs() -> list[dict]:
    result = []

    for code, database in databases.items():
        try:
            program = database.program()

            if program:
                result.append({
                    "code": code,
                    "name_th": program.get("name_th"),
                    "total_credits": program.get("total_credits"),
                    "years": program.get("years"),
                })

        except FileNotFoundError:
            continue

    return result