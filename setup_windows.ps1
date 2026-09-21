$ErrorActionPreference = "Stop"
if (-not (Test-Path .venv)) { py -m venv .venv }
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
Write-Host "Python environment ready."
Write-Host "Next: install Tesseract (tha+eng), install/start Ollama, pull the two models, then run:"
Write-Host "  python run_all.py --check"
Write-Host "  python run_all.py --program all"
