# ขั้นตอนจาก PDF หลักสูตรถึงเว็บถามตอบ

คู่มือนี้พาทำตั้งแต่ติดตั้งโปรแกรมที่จำเป็น เตรียมไฟล์ PDF สกัดข้อมูล สร้างฐานข้อมูล ไปจนถึงเปิดเว็บถามตอบ เหมาะสำหรับ Windows และ PowerShell

> เปิดโฟลเดอร์โปรเจกต์ ocr_system ใน VS Code แล้วเลือก Terminal → New Terminal

## 1. ติดตั้งโปรแกรมพื้นฐาน

### 1.1 Python

โปรเจกต์ต้องใช้ Python 3.10 ขึ้นไป คู่มือนี้ใช้ Python 3.11 สำหรับ environment ของโปรเจกต์ ดาวน์โหลดจาก [Python for Windows](https://www.python.org/downloads/windows/) แล้วตรวจใน PowerShell:

~~~powershell
py -3.11 --version
~~~

ถ้าเครื่องติดตั้ง Python รุ่นอื่นที่รองรับอยู่แล้ว ให้ตรวจด้วย py --version

### 1.2 Tesseract OCR

Tesseract ใช้เป็น OCR baseline ต้องติดตั้งทั้งตัวโปรแกรมและข้อมูลภาษาไทยกับอังกฤษ

1. อ่านคำแนะนำ Windows จาก [UB Mannheim Tesseract Windows Guide](https://github.com/UB-Mannheim/Tesseract_Dokumentation/blob/main/Tesseract_Doku_Windows.md)
2. ระหว่างติดตั้ง ให้เลือก language data สำหรับ Thai (tha) และ English (eng)
3. ปิดแล้วเปิด Terminal ใหม่ จากนั้นตรวจ:

~~~powershell
tesseract --version
tesseract --list-langs
~~~

ในผลคำสั่งที่สองควรเห็น tha และ eng หาก PowerShell แจ้งว่าไม่รู้จักคำสั่ง tesseract ให้เพิ่มโฟลเดอร์ติดตั้ง เช่น C:\Program Files\Tesseract-OCR ใน Windows PATH แล้วเปิด Terminal ใหม่

### 1.3 Ollama และโมเดล

1. ดาวน์โหลดและติดตั้ง [Ollama for Windows](https://ollama.com/download/windows)
2. เปิดแอป Ollama จาก Start Menu ให้ทำงานอยู่เบื้องหลัง
3. เปิด PowerShell ใหม่ แล้วดาวน์โหลดโมเดลที่โปรเจกต์ใช้:

~~~powershell
ollama pull qwen3:4b
ollama pull scb10x/typhoon-ocr1.5-3b
~~~

4. ตรวจว่า Ollama เห็นโมเดลแล้ว:

~~~powershell
ollama list
~~~

การดาวน์โหลดโมเดลครั้งแรกต้องใช้อินเทอร์เน็ตและพื้นที่เก็บข้อมูล โมเดลจะทำงานบนเครื่องผ่าน Ollama หลังติดตั้งแล้ว หาก ollama ไม่ใช่คำสั่งที่รู้จัก ให้เปิด Terminal ใหม่หลังติดตั้ง

## 2. ตรวจไฟล์ของโปรเจกต์

โปรเจกต์ต้องมี PDF, Ground Truth และ page map อยู่ในตำแหน่งตาม config/programs.json:

~~~text
data/
├── raw/
│   ├── AI.pdf
│   ├── BIT.pdf
│   ├── IT.pdf
│   └── DSBA.pdf
└── ground_truth/
    ├── ... .json
    └── ... _page_map.csv

config/
└── programs.json
~~~

ค่าเริ่มต้นเลือกหน้าเหล่านี้:

| หลักสูตร | หน้าที่ประมวลผล |
|---|---|
| AI | 21–26 |
| BIT | 22–25, 31–35 |
| IT | 26–29, 38–44 |
| DSBA | 19–22, 30–36 |

หากไฟล์ต้นฉบับอยู่คนละตำแหน่ง ให้แก้ path ใน config/programs.json ก่อนเริ่มรัน

## 3. สร้าง Python environment และติดตั้ง dependencies

จาก PowerShell ที่อยู่ในโฟลเดอร์ ocr_system Path ต้องอยู่ที่ ocr_system ก่อนที่จะรัน:

~~~powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pip install -r lab10_fastapi\curriculum_app\requirements.txt
~~~

## 4. ตรวจความพร้อมก่อนประมวลผล PDF

ให้เปิด Ollama ไว้ แล้วรันจากโฟลเดอร์โปรเจกต์:

~~~powershell
python run_all.py --check
~~~

คำสั่งนี้ตรวจไฟล์ PDF, Ground Truth, page map, Tesseract, Ollama และความพร้อมของส่วน Lab 7B–Lab 9 แก้รายการที่ขึ้น MISSING ก่อนเริ่มรันจริง

## 5. รัน PDF ตั้งแต่ต้นจนได้ฐานข้อมูลและรายงาน

ทดสอบการประมวลผลครั้งเดียว:

~~~powershell
python run_all.py --program all
~~~

### ไฟล์ผลลัพธ์อยู่ที่ไหน

ตัวอย่างของหลักสูตร AI:

~~~text
work/AI/
├── source_manifest.json
├── 01_selected_pages/         ภาพหน้าที่เลือกจาก PDF
├── 02_lab6/                   ผลประเมิน OCR baseline
├── 03_lab7b/
│   ├── pred_baseline.json
│   ├── pred_text.json
│   ├── pred_vlm.json
│   ├── evaluation.json
│   └── selected_prediction.json
├── 04_lab8b/
│   ├── curriculum.json
│   ├── curriculum.db
│   ├── verify.json
│   ├── gold_questions.json
│   └── eval_result.json
└── 05_lab9/
    ├── lab9_report.md
    └── lab9_report.json
~~~

### อ่านผลประเมิน

- 03_lab7b/evaluation.json เปรียบเทียบผลของแต่ละ candidate กับ Ground Truth
- 04_lab8b/verify.json แสดงผลตรวจฐานข้อมูล
- 04_lab8b/eval_result.json แสดงผลคำถามประเมิน NL-to-SQL
- 05_lab9/lab9_report.md เป็นรายงานสรุปที่อ่านได้ และไฟล์ .json เป็นข้อมูลผลประเมิน

## 6. เปิดเว็บถามตอบหลักสูตร

เว็บใช้ฐานข้อมูลที่สร้างเสร็จจากขั้นก่อนหน้า ตาม lab10_fastapi/curriculum_app/config.py:

| หลักสูตร | ไฟล์ฐานข้อมูลที่เว็บใช้ |
|---|---|
| IT | work/IT/04_lab8b/curriculum.db |
| AI | work/AI/04_lab8b/curriculum.db |
| BIT | work/BIT/04_lab8b/curriculum.db |
| DSBA | work/DSBA/04_lab8b/curriculum.db |

### เปิดเซิร์ฟเวอร์

1. รันเว็บ:

~~~powershell
python -m uvicorn lab10_fastapi.curriculum_app.main:app --reload --host 127.0.0.1 --port 8000
~~~

2. เปิดเบราว์เซอร์ไปที่:

- หน้าเว็บถามตอบ: <http://127.0.0.1:8000/>
- สถานะ API/ฐานข้อมูล/Ollama: <http://127.0.0.1:8000/api/health>
- หน้าทดลอง API: <http://127.0.0.1:8000/docs>

## 9. ลำดับคำสั่งฉบับย่อ

เมื่อ Python, Tesseract และ Ollama ติดตั้งแล้ว คำสั่งหลักคือ:

~~~powershell
cd "C:\path\to\ocr_system"
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pip install -r lab10_fastapi\curriculum_app\requirements.txt
ollama pull qwen3:4b
ollama pull scb10x/typhoon-ocr1.5-3b
python run_all.py --check
python run_all.py --program all
python -m uvicorn lab10_fastapi.curriculum_app.main:app --reload --host 127.0.0.1 --port 8000
~~~

จากนั้นเปิด <http://127.0.0.1:8000/> เพื่อเข้าเว็บถามตอบ

