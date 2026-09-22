# คู่มือโครงสร้างไฟล์และวิธีรัน

โปรเจกต์นี้สกัดข้อมูลหลักสูตรจาก PDF ด้วย OCR/LLM บนเครื่อง แล้วสร้าง SQLite เพื่อถามตอบผ่าน SQL และประเมินผลถึง Lab 9 ไม่มีเว็บแอป

## 1. เริ่มอ่านตรงนี้

โฟลเดอร์ repository คือ `D:\ocr\isd-2026-Answer_everything` แต่ **โฟลเดอร์ที่ใช้รันคำสั่งคือ `ocr_system` ภายในนั้น**

```text
isd-2026-Answer_everything/
├── PROJECT_GUIDE.md          คู่มือนี้
├── README.md                 ข้อมูลกลุ่มและทางเข้าคู่มือ
├── Member                    รายชื่อสมาชิก
├── archive/                  ไฟล์เก่า/สำรอง ไม่ใช้ใน pipeline หลัก
└── ocr_system/               โฟลเดอร์ทำงานและรันคำสั่ง
    ├── run_all.py            จุดรันหลัก
    ├── config/               การตั้งค่าหลักสูตร
    ├── data/
    │   ├── raw/              PDF ต้นฉบับ
    │   └── ground_truth/     เฉลยอ้างอิง
    ├── src/                  โค้ดระบบ
    ├── scripts/              เครื่องมือช่วยงาน ไม่จำเป็นต่อการรันปกติ
    ├── tests/                ชุดทดสอบ
    ├── docs/                 เอกสารประกอบแล็บ
    ├── work/                 ผลรันแยกตามหลักสูตร
    └── .venv/                Python และแพ็กเกจเฉพาะเครื่อง
```

`ocr_system/src/ocr_system` เป็นโครงสร้างแพ็กเกจ Python ไม่ใช่โปรเจกต์อีกชุด จึงยังคงตำแหน่งนี้ไว้

## 2. ไฟล์ที่ใช้บ่อย

พาธในตารางต่อจากนี้อ้างอิงจากโฟลเดอร์ทำงาน `ocr_system` เว้นแต่ระบุเป็นอย่างอื่น

| ไฟล์ | หน้าที่ |
|---|---|
| `README.md` | รายละเอียด pipeline และการติดตั้งเดิม |
| `run_all.py` | คุมตั้งแต่ PDF → Lab 7B → Lab 8B → Lab 9 |
| `run_all.bat` | เรียก `python run_all.py --program all`; ต้องมี Python ใน PATH/เปิด venv แล้ว |
| `setup_windows.ps1` | ช่วยสร้างและเปิด venv แล้วติดตั้งแพ็กเกจ; ถ้า PowerShell บล็อก Activate ให้ใช้คำสั่งในคู่มือนี้แทน |
| `requirements.txt` | แพ็กเกจหลัก |
| `requirements-optional.txt` | แพ็กเกจสำหรับ OCR ทางเลือก เช่น PaddleOCR/TrOCR และ pdf2image |
| `pyproject.toml` | ชื่อแพ็กเกจ รุ่น Python และตำแหน่งแพ็กเกจใน `src` |
| `config/programs.json` | PDF หน้าที่เลือก เฉลย page map หน่วยกิตและระยะเวลาเรียนของแต่ละหลักสูตร |
| `generate_gold_questions.py` | สร้างคำถามและคำตอบที่คาดหวัง โดย pipeline หลักใช้ ground truth |
| `lab9_evaluate.py` | รวมผล extraction, ฐานข้อมูล และ QA เป็นรายงาน Lab 9 |
| `.gitignore` | กำหนดไฟล์ที่ไม่ติดตามใน Git เช่น venv และผลรัน |
| `.gitattributes` | กฎจัดการไฟล์ของ Git |

## 3. ข้อมูลต้นทางและเฉลย

| ไฟล์/รูปแบบชื่อ | หน้าที่ |
|---|---|
| `data/raw/AI.pdf`, `BIT.pdf`, `IT.pdf`, `DSBA.pdf` | PDF หลักสูตรฉบับเต็ม ต้องเตรียมเองสำหรับหลักสูตรที่จะรัน |
| `data/raw/SOURCES.json` | บันทึกชื่อ ขนาด และ SHA-256 ของไฟล์อ้างอิง ไม่ใช่ตัว PDF และไม่ดาวน์โหลด PDF ให้ |
| `data/ground_truth/{BIT,IT,DSBA}_academic_plan_coop.json` | เฉลยแผนสหกิจศึกษา ซึ่งค่า config ปัจจุบันเลือกใช้ |
| `data/ground_truth/{BIT,IT,DSBA}_academic_plan_no_coop.json` | เฉลยแผนไม่สหกิจ ไม่ใช่แผนที่ config ปัจจุบันเลือก |
| `data/ground_truth/AI_academic_plan_corrected_v2.json` | เฉลย AI ที่ config ปัจจุบันเลือกใช้ |
| `data/ground_truth/AI_academic_plan_corrected.json` | เฉลย AI อีกเวอร์ชัน เก็บไว้สำหรับอ้างอิง |
| `data/ground_truth/AIT_academic_plan.json` | ข้อมูลเฉลยเดิม ไม่ใช่ไฟล์ที่ config ปัจจุบันเลือก |
| `data/ground_truth/example_ground_truth.json` | ตัวอย่างโครงสร้างเฉลย |
| `data/ground_truth/{AI,BIT,IT,DSBA}_page_map.csv` | เชื่อมข้อมูลรายวิชากับหน้าเอกสารสำหรับการประเมิน |
| `docs/Lab7B_Curriculum_LocalLLM1.pdf` | เอกสารประกอบ Lab 7B |

เฉลยกับผลที่โมเดลสกัดเป็นคนละชุด หากชื่อหรือรหัสขัดกันต้องตรวจ PDF ก่อน ไม่ควรแก้เฉลยให้ตามโมเดลโดยไม่มีหลักฐาน

## 4. โค้ดระบบแต่ละไฟล์

| ไฟล์ใน `src/` | หน้าที่ |
|---|---|
| `lab7_metrics.py` | เครื่องมือจับคู่รายวิชาและคำนวณตัวชี้วัด Lab 7 |
| `ocr_system/lab7b_curriculum.py` | สกัดด้วย baseline/text/VLM แบ่งข้อความเป็นส่วน รวมผล และเทียบเฉลย; มีการแปลงรหัสวรรณยุกต์พิเศษจาก PDF |
| `ocr_system/lab8b_curriculum_db.py` | schema, แปลงผล Lab 7B, สร้าง SQLite, ตรวจข้อมูล, แปลงคำถามเป็น SQL และตรวจคำตอบ; `SQL_PROMPT` และฟังก์ชันตัดคำเกริ่นอยู่ที่นี่ |
| `ocr_system/lab6_evaluation.py` | ประเมิน baseline สำหรับ Lab 6 โดยใช้เฉลยและ page map |
| `ocr_system/cli.py` | command line สำหรับ OCR และการประเมินในชุด OCR ทั่วไป |
| `ocr_system/config.py` | ค่า OCR เช่น engine ภาษา DPI และพาธผลลัพธ์ |
| `ocr_system/document_loader.py` | โหลดเอกสารและเตรียมภาพแต่ละหน้า |
| `ocr_system/preprocessing.py` | เตรียมภาพก่อน OCR เช่นแก้ความเอียง |
| `ocr_system/engine_factory.py` | เลือกและสร้าง OCR engine |
| `ocr_system/pipeline.py` | ประมวลผล OCR แต่ละหน้าและบันทึกข้อความ/JSON |
| `ocr_system/schemas.py` | โครงสร้างผล OCR |
| `ocr_system/field_extraction.py` | สกัดฟิลด์จากข้อความ |
| `ocr_system/curriculum_extraction.py` | แยกข้อมูลหลักสูตรจากข้อความ OCR |
| `ocr_system/curriculum_profiles.py` | โปรไฟล์ที่ใช้กับตัวสกัดหลักสูตร |
| `ocr_system/extract_only.py` | ขั้นตอนสกัดจากข้อมูลที่เตรียมไว้ |
| `ocr_system/evaluation.py` | ประเมินข้อมูลที่สกัดกับ ground truth |
| `ocr_system/engines/base.py` | interface ของ OCR engine |
| `ocr_system/engines/tesseract_engine.py` | Tesseract OCR |
| `ocr_system/engines/paddle_engine.py` | PaddleOCR |
| `ocr_system/engines/trocr_engine.py` | TrOCR |
| `ocr_system/engines/ensemble_engine.py` | รวมผลจากหลาย OCR engine |
| `ocr_system/utils/io.py` | สร้างโฟลเดอร์และอ่าน/เขียนข้อมูล |
| `ocr_system/__init__.py`, `engines/__init__.py`, `utils/__init__.py` | ไฟล์กำหนดแพ็กเกจ Python |
| `isd_curriculum_ocr.egg-info/PKG-INFO` | metadata ของแพ็กเกจที่ติดตั้ง |
| `isd_curriculum_ocr.egg-info/SOURCES.txt` | รายการไฟล์ที่เครื่องมือ packaging สร้างไว้ อาจเปลี่ยนเมื่อ install ใหม่ |
| `isd_curriculum_ocr.egg-info/top_level.txt` | ชื่อแพ็กเกจระดับบน |
| `isd_curriculum_ocr.egg-info/dependency_links.txt` | metadata ลิงก์ dependency |

ไม่ต้องแก้ `.venv`, `__pycache__` หรือ `*.egg-info` เพื่อปรับพฤติกรรมระบบ ให้แก้โค้ดหรือ config แทน

## 5. สคริปต์ช่วยงานที่ย้ายมา `scripts/`

ยังใช้ตรรกะเดิม ให้รันจากโฟลเดอร์ `ocr_system` เสมอ ไม่ใช่เข้าไปยืนใน `scripts` เพราะหลายไฟล์ใช้พาธสัมพัทธ์

| ไฟล์ | หน้าที่ |
|---|---|
| `scripts/build_page_maps.py` | สร้าง page map จาก ground truth และผล OCR JSON เดิม โดยไม่รัน OCR ใหม่ |
| `scripts/reocr_pages.py` | OCR ใหม่เฉพาะหน้าที่เลือก; ใช้ Tesseract และ pdf2image/Poppler |
| `scripts/fix_ai_gt_metadata.py` | ปรับ metadata ระดับบนของเฉลย AI |
| `scripts/fix_ai_gt_suspicious_row.py` | ตรวจแถวต้องสงสัยในเฉลย AI; ต้องใช้ `--apply` จึงเขียนฉบับแก้ไข |
| `scripts/lab6_all_programs.py` | เครื่องมือประเมินหลายหลักสูตรของ workflow Lab 6 เดิม |
| `scripts/lab6_readiness_check.py` | ตรวจความพร้อมผลประเมินเดิมใน `outputs/` |
| `scripts/lab6_final_readiness.py` | สรุปความพร้อมผล Lab 6 เดิมใน `outputs/` |
| `tests/test_qa_scoring.py` | ทดสอบการเทียบคำตอบและจัดการ SQL error |
| `tests/test_thai_extraction.py` | ทดสอบรหัสวรรณยุกต์พิเศษและการคืนชื่อไทยจากต้นฉบับ |

ดูตัวเลือกก่อนใช้เครื่องมือ เช่น:

ในเครื่องที่ตรวจครั้งนี้ยังไม่มี `pdf2image` จึงยังเรียก `reocr_pages.py` ไม่ได้ ต้องติดตั้ง dependency ของเครื่องมือนี้ก่อน ซึ่งไม่กระทบ pipeline แบบ text

```powershell
.\.venv\Scripts\python.exe scripts\build_page_maps.py --help
```

## 6. ผลรันอยู่ที่ไหน

ตัวอย่าง `work/DSBA/` หลักสูตรอื่นใช้ชื่อของตัวเองแทน DSBA

| ไฟล์/โฟลเดอร์ | หน้าที่ |
|---|---|
| `source_manifest.json` | พาธ ขนาด SHA-256 และหน้าที่เลือกจาก PDF รอบนั้น |
| `01_selected_pages/source_page_*.png` | ภาพหน้าที่เลือกสำหรับตรวจย้อนหลัง; ภาพเดิมอาจถูกใช้ซ้ำถ้ามีอยู่แล้ว |
| `02_lab6/` | ผลประเมิน baseline; `SKIPPED.txt` ระบุเมื่อไม่ได้ทำขั้นตอนนี้ |
| `03_lab7b/pred_text.json` | ผลสกัดจากข้อความใน PDF ผ่านโมเดล |
| `03_lab7b/pred_baseline.json`, `pred_vlm.json` | ผลสกัดทางเลือก มีเฉพาะเมื่อรันเส้นทางนั้น |
| `03_lab7b/evaluation.json`, `comparison.csv` | คะแนนและการเปรียบเทียบวิธีสกัด |
| `03_lab7b/selected_prediction.json` | วิธีสกัดที่เลือกส่งต่อไปฐานข้อมูล |
| `04_lab8b/schema/curriculum.schema.json` | JSON Schema |
| `04_lab8b/schema/schema.sql` | โครงสร้างตารางและ view |
| `04_lab8b/curriculum.json` | ข้อมูลหลังแปลงสำหรับนำเข้าฐานข้อมูล เปิดอ่านใน editor ได้ |
| `04_lab8b/curriculum.conversion.json` | จำนวนรายการและคำเตือนตอนแปลง |
| `04_lab8b/curriculum.db` | ฐานข้อมูล SQLite ที่ใช้ตอบคำถามจริง |
| `04_lab8b/verify.json` | ผลตรวจความสอดคล้องฐานข้อมูล 7 ข้อ |
| `04_lab8b/gold_questions.json` | คำถามใน `question` และเฉลยใน `expect` |
| `04_lab8b/gold_questions.meta.json` | ที่มาและจำนวนคำถาม |
| `04_lab8b/eval_result.json` | SQL ผลแถว คำตอบ และผลถูก/ผิดแต่ละข้อ |
| `05_lab9/lab9_report.json`, `lab9_report.md` | รายงาน Lab 9 |
| `work/all_programs_summary.json` | สถานะการรันรวม |
| `work/lab9_summary.json` | คะแนน Lab 9 รวมของหลักสูตรที่รัน |
| `work/.gitkeep` | เก็บโฟลเดอร์ว่างใน Git |

`work` เป็นผลที่สร้างใหม่ได้ แต่หากแก้คำถามด้วยมือให้สำรองก่อนรันทั้งหมด เพราะ `run_all.py` สร้างคำถามจาก ground truth ใหม่ และโหลดฐานข้อมูลด้วย `--replace`

การแก้ `curriculum.json` ไม่ได้เปลี่ยน `.db` ทันที ต้องนำเข้าใหม่ ส่วนการรัน `eval` อย่างเดียวไม่สกัด PDF ใหม่

## 7. ติดตั้งและรันบน PowerShell

### เตรียมครั้งแรก

ต้องติดตั้ง Python 3.10 ขึ้นไป (README เดิมแนะนำ 3.10/3.11) และ Ollama ให้เรียกจาก terminal ได้ เปิด Ollama และเตรียม PDF ฉบับเต็มไว้ใน `data/raw`

```powershell
cd D:\ocr\isd-2026-Answer_everything\ocr_system
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .
ollama pull qwen3:4b
```

ถ้ามี `.venv` ที่ใช้ได้แล้ว ไม่ต้องสร้างใหม่ คำสั่งที่เรียก Python ใน venv โดยตรงไม่ต้อง Activate จึงไม่ติดปัญหา execution policy ของ PowerShell

### รัน DSBA แบบ text ตั้งแต่ PDF จนจบ

```powershell
.\.venv\Scripts\python.exe run_all.py --program DSBA --lab7-pipeline text
```

โหมดนี้ใช้ Qwen กับข้อความใน PDF ไม่ต้องมี Typhoon สำหรับการรัน text แต่ต้องมี `data/raw/DSBA.pdf` หากเป็นเอกสารสแกนที่ไม่มีข้อความ โหมดนี้อาจใช้ไม่ได้

### รันทุกวิธี/ทุกหลักสูตร

ต้องมี PDF ครบ AI/BIT/IT/DSBA, Tesseract พร้อมภาษา tha/eng และโมเดล OCR เพิ่มเติม:

```powershell
ollama pull scb10x/typhoon-ocr1.5-3b
.\.venv\Scripts\python.exe run_all.py --check
.\.venv\Scripts\python.exe run_all.py --program all
```

`--check` ตรวจสภาพแวดล้อมหลายส่วนรวมทั้ง selftest ไม่ใช่เพียงตรวจโหมด text และ `--dry-run` ยังต้องมี PDF พร้อมทั้งอาจสร้างโฟลเดอร์/manifest จึงไม่ใช่โหมดอ่านอย่างเดียว

### ประเมินคำถามใหม่โดยไม่สกัด PDF ซ้ำ

ต้องมีฐานข้อมูลและไฟล์คำถามแล้ว เปิด Ollama พร้อม Qwen:

```powershell
.\.venv\Scripts\python.exe src\ocr_system\lab8b_curriculum_db.py eval -d work\DSBA\04_lab8b\curriculum.db -q work\DSBA\04_lab8b\gold_questions.json -o work\DSBA\04_lab8b\eval_result.json
```

### ถามเองหนึ่งข้อ

```powershell
.\.venv\Scripts\python.exe src\ocr_system\lab8b_curriculum_db.py ask -d work\DSBA\04_lab8b\curriculum.db -q "วิชา 90641001 มีกี่หน่วยกิต"
```

### สร้างคำถามใหม่หลังแก้เฉลย

DSBA ใน config ปัจจุบันกำหนด 132 หน่วยกิต และ 4 ปี:

```powershell
.\.venv\Scripts\python.exe generate_gold_questions.py --ground-truth data\ground_truth\DSBA_academic_plan_coop.json --total-credits 132 --years 4 --count 30 --output work\DSBA\04_lab8b\gold_questions.json
```

คำสั่งนี้เขียนคำถามใหม่ จากนั้นรัน `eval` อีกครั้ง สำหรับหลักสูตรอื่นให้ใช้ค่าจาก `config/programs.json`

### อัปเดตรายงานหลังประเมินใหม่

```powershell
.\.venv\Scripts\python.exe lab9_evaluate.py run --program DSBA --lab7-dir work\DSBA\03_lab7b --lab8-dir work\DSBA\04_lab8b --output-dir work\DSBA\05_lab9
.\.venv\Scripts\python.exe lab9_evaluate.py summary --work work --programs DSBA --output work\lab9_summary.json
```

### ทดสอบโค้ดโดยไม่เรียกโมเดล

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

## 8. ไฟล์ที่เก็บใน archive

`archive` อยู่ที่ระดับ repository (ข้างโฟลเดอร์ `ocr_system`) ไม่ใช่ภายในโฟลเดอร์ทำงาน

| ไฟล์ | ตำแหน่งเดิมและเหตุผล |
|---|---|
| `archive/ocr_system.rar` | ย้ายจากชั้นนอก เป็นชุดบีบอัดเดิม ยังไม่ได้ยืนยันว่าเหมือนโค้ดปัจจุบัน ไม่ใช่จุดรัน |
| `archive/curriculum.empty.json` | เดิมคือ `curriculum.json` ชั้นนอก มี `courses: []` ไม่ใช่ฐานข้อมูลผลรัน |
| `archive/lab8b_curriculum_db_backup.py` | เดิมอยู่ใน `src/ocr_system` เป็นสำเนาสำรอง เก็บเพื่ออ้างอิง ไม่เรียกจาก pipeline หลัก |

การจัดครั้งนี้ย้ายเฉพาะไฟล์ช่วยงาน/สำรอง ไม่ย้าย venv, PDF, ground truth, ผลรัน, package หรือ entry point และไม่แก้ตรรกะ OCR/SQL
