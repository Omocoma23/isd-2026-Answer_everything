1. ต้องเอาไฟล์ AI BIT IT DSBA .pdf ไปใส่ใน data/raw ก่อน
2. จากนั้นรันใน powershell
3. py -m venv .venv
4. .\.venv\Scripts\Activate.ps1
5. pip install -r requirements.txt
6. pip install -e .
7. ollama pull scb10x/typhoon-ocr1.5-3b
8. ollama pull qwen3:4b
9. python run_all.py --check
10. python run_all.py --program all
11. ถ้าจะดูผลสุดท้ายให้ดูที่ work/AI/05_lab9/ ,work/BIT/05_lab9/ ,work/IT/05_lab9/ ,work/DSBA/05_lab9/
12. ถ้าจะดูผลของ LAB8 ให้เข้าไปที่ work/AI/04_lab8b/
