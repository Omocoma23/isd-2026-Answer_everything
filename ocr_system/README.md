# ISD 2026 — Raw PDF → OCR/LLM → Database → Lab 9

ชุดนี้จบที่ **Lab 9 (Evaluation and Overfitting)** เท่านั้น — **ไม่มี Web App / FastAPI / frontend**

เป้าหมายคือให้เริ่มจากไฟล์หลักสูตร **PDF ดิบฉบับเต็มจริง** ทั้ง 4 หลักสูตร แล้วรันคำสั่งเดียวจนได้ฐานข้อมูลของแต่ละหลักสูตรและรายงานประเมิน Lab 9

```text
data/raw/AI.pdf
        BIT.pdf
        IT.pdf
        DSBA.pdf
           │
           ▼
   เลือกหน้าจาก RAW PDF ตอน runtime
           │
           ▼
   baseline OCR / Lab 6 evaluation
           │
           ▼
   Lab 7B: PDF text + Typhoon VLM + Qwen
           │
           ▼
   structured curriculum prediction
           │
           ▼
   Lab 8B: schema → SQLite → verify 7 checks
           │
           ▼
   30 gold questions → NL-to-SQL → eval_result.json
           │
           ▼
   Lab 9: per-stage evaluation report
           │
           └── END
```

## ทำไม Lab 9 ไม่ใช่ Web App

Lab 9 ของวิชานี้เป็นเรื่อง **Evaluation and Overfitting** ดังนั้นขั้นสุดท้ายของชุดนี้คือการวัดคุณภาพของระบบที่ทำมาถึง Lab 8B ไม่ใช่การสร้าง UI ใหม่

สำหรับงานหลักสูตร / NL-to-SQL รายงาน Lab 9 แยกวัดทีละจุด เช่น

- OCR / extraction: CER, WER, exact-match ราย field และ course alignment Precision / Recall / F1
- structured data: JSON/schema validity และผล `verify` 7 checks
- QA / NL-to-SQL: `Valid SQL Rate` และ `Execution Accuracy`
- ไม่สร้าง metric ที่ไม่มีหลักฐาน เช่น Faithfulness/Citation ถ้า pipeline ยังไม่ได้ log evidence/citation จริง
- Overfitting จะรายงานว่า **ประเมินจาก learning curve ไม่ได้** ในชุดนี้ เพราะใช้ pretrained local models แบบ inference ไม่มี train/validation history

> สำหรับ Group B ในสไลด์ Lab 9, `Execution Accuracy (SQL)` เป็น metric สำคัญที่สุดของ NL-to-SQL ส่วน `Valid SQL Rate` ต้องรายงานแยก เพราะ SQL รันได้ไม่ได้แปลว่าตอบถูก

---

## 1. โครงสร้างสำคัญ

```text
ocr_system_lab9_ready/
├── data/
│   ├── raw/
│   │   ├── AI.pdf
│   │   ├── BIT.pdf
│   │   ├── IT.pdf
│   │   ├── DSBA.pdf
│   │   └── SOURCES.json
│   └── ground_truth/
├── config/programs.json
├── src/ocr_system/
│   ├── lab7b_curriculum.py
│   ├── lab8b_curriculum_db.py
│   ├── lab6_evaluation.py
│   └── ...
├── generate_gold_questions.py
├── lab9_evaluate.py
├── run_all.py             # entry point หลัก
├── run_all.bat
├── requirements.txt
└── README.md
```

`data/raw/*.pdf` คือไฟล์ต้นฉบับเต็ม ไม่ใช่ไฟล์ที่ตัดหน้ามาแล้ว ส่วนหน้าที่ใช้ OCR/LLM จะถูกเลือก **ตอนรัน** ตาม `config/programs.json` และบันทึกภาพไว้ให้ตรวจย้อนหลัง

---

## 2. ติดตั้งบน Windows

แนะนำ Python 3.10 หรือ 3.11

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### Tesseract

ต้องมี `tesseract` และภาษา `tha`, `eng`

```powershell
tesseract --version
tesseract --list-langs
```

### Ollama

ติดตั้ง/เปิด Ollama แล้ว pull model:

```powershell
ollama pull scb10x/typhoon-ocr1.5-3b
ollama pull qwen3:4b
```

ถ้ายังไม่ได้เปิด service:

```powershell
ollama serve
```

---

## 3. ตรวจความพร้อม

```powershell
python run_all.py --check
```

จะตรวจ:

- RAW PDF ทั้ง 4 เล่ม
- ground truth + page map
- Ollama + local models
- Lab 7B environment
- Lab 8B selftest
- Lab 9 selftest

---

## 4. Dry run ก่อน

```powershell
python run_all.py --program all --dry-run
```

คำสั่งนี้ยังไม่เรียก AI แต่จะแสดง flow ที่จะรันครบถึง Lab 9

---

## 5. รันจริง 4 หลักสูตรตั้งแต่ PDF ดิบจนจบ Lab 9

```powershell
python run_all.py --program all
```

หรือดับเบิลคลิก/รัน:

```powershell
run_all.bat
```

รันทีละหลักสูตรได้:

```powershell
python run_all.py --program AI
python run_all.py --program BIT
python run_all.py --program IT
python run_all.py --program DSBA
```

---

## 6. หน้า PDF ที่ pipeline ใช้

source ยังเป็น raw PDF เต็มเล่ม แต่เพื่อลด context และเวลา pipeline เลือกเฉพาะหน้าที่เกี่ยวข้องกับแผนการศึกษา/รายวิชาตอน runtime:

```text
AI    21-26
BIT   22-25,31-35
IT    26-29,38-44
DSBA  19-22,30-36
```

แก้ได้ที่ `config/programs.json`

ภาพ page จริงที่ render จาก PDF ดิบจะอยู่ใน:

```text
work/<PROGRAM>/01_selected_pages/
```

และ `work/<PROGRAM>/source_manifest.json` จะบันทึก SHA-256 ของ PDF ต้นทาง

---

## 7. Output ต่อหลักสูตร

ตัวอย่าง DSBA:

```text
work/DSBA/
├── source_manifest.json
├── 01_selected_pages/
├── 02_lab6/
│   └── ... evaluation baseline ...
├── 03_lab7b/
│   ├── pred_baseline.json
│   ├── pred_text.json
│   ├── pred_vlm.json
│   ├── evaluation.json
│   └── selected_prediction.json
├── 04_lab8b/
│   ├── schema/
│   │   ├── curriculum.schema.json
│   │   └── schema.sql
│   ├── curriculum.json
│   ├── curriculum.conversion.json
│   ├── curriculum.db
│   ├── verify.json
│   ├── gold_questions.json
│   ├── gold_questions.meta.json
│   └── eval_result.json
└── 05_lab9/
    ├── lab9_report.json
    └── lab9_report.md
```

เมื่อรัน `--program all` จะมี summary รวม:

```text
work/lab9_summary.json
```

ไม่มี `webapp/` และไม่มี combined web database เพราะชุดนี้ตั้งใจ **หยุดที่ Lab 9**

---

## 8. Lab 9 report วัดอะไร

`05_lab9/lab9_report.json` แยกเป็น 4 ส่วนหลัก:

1. `lab7_extraction`
   - selected pipeline
   - alignment Precision / Recall / F1
   - overall micro CER
   - CER/WER/exact match ราย attribute

2. `lab8_structured_data_and_db`
   - final JSON validity
   - conversion statistics
   - verify 7 checks

3. `lab9_qa_evaluation`
   - จำนวน gold questions
   - Valid SQL Rate
   - Execution Accuracy
   - latency
   - รายการ SQL ที่ error / คำถามที่ตอบผิด

4. `metrics_not_claimed` + `overfitting`
   - บอก metric ที่ pipeline ยังไม่ได้เก็บหลักฐาน จึงไม่แต่งตัวเลขขึ้นมา
   - บอกข้อจำกัดเรื่อง overfitting อย่างตรงไปตรงมา

---

## 9. รัน Lab 9 ใหม่อย่างเดียว

ถ้า Lab 7B/8B รันเสร็จแล้ว ไม่ต้อง OCR ใหม่:

```powershell
python lab9_evaluate.py run ^
  --program DSBA ^
  --lab7-dir work/DSBA/03_lab7b ^
  --lab8-dir work/DSBA/04_lab8b ^
  --output-dir work/DSBA/05_lab9
```

ทดสอบ Lab 9 evaluator:

```powershell
python lab9_evaluate.py selftest
```

---

## 10. หมายเหตุเรื่อง final test

`gold_questions.json` สร้าง expected result จาก ground truth และเอาไปทดสอบ database ที่สร้างจาก prediction เพื่อไม่ให้ evaluation วนกลับไปเฉลยจาก database ตัวเอง

ถ้าต้องการใช้ 30 ข้อนี้เป็น final test จริง ไม่ควรปรับ prompt ซ้ำ ๆ โดยดูผล 30 ข้อนี้ทุกครั้ง เพราะจะเริ่มเกิด evaluation leakage ได้

---

## คำสั่งสั้นที่สุด

```powershell
python run_all.py --check
python run_all.py --program all
```

เมื่อเห็น `PIPELINE COMPLETE` และมี `work/lab9_summary.json` แปลว่า flow จบถึง Lab 9 แล้ว
