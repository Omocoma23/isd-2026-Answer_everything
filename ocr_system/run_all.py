from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable
LAB7 = ROOT / "src" / "ocr_system" / "lab7b_curriculum.py"
LAB8 = ROOT / "src" / "ocr_system" / "lab8b_curriculum_db.py"
LAB6_EVAL = ROOT / "src" / "ocr_system" / "lab6_evaluation.py"
LAB9 = ROOT / "lab9_evaluate.py"
PROFILES_PATH = ROOT / "config" / "programs.json"
PROGRAM_ORDER = ("AI", "BIT", "IT", "DSBA")


def log(msg: str) -> None:
    print(f"\n[PIPELINE] {msg}", flush=True)


def run(args: list[object], *, env: dict[str, str] | None = None, dry: bool = False) -> None:
    cmd = [PYTHON, *(str(x) for x in args)]
    print("$ " + " ".join(f'"{x}"' if " " in x else x for x in cmd), flush=True)
    if not dry:
        subprocess.run(cmd, cwd=ROOT, env=env, check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parse_page_spec(spec: str) -> list[int]:
    pages: set[int] = set()
    for token in spec.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            a, b = token.split("-", 1)
            pages.update(range(int(a), int(b) + 1))
        else:
            pages.add(int(token))
    return sorted(pages)


def render_selected_pages(pdf: Path, page_spec: str, outdir: Path, dpi: int = 120) -> None:
    import fitz

    outdir.mkdir(parents=True, exist_ok=True)
    wanted = parse_page_spec(page_spec)
    with fitz.open(pdf) as doc:
        for page_no in wanted:
            if not 1 <= page_no <= len(doc):
                raise ValueError(f"{pdf.name}: page {page_no} out of range 1..{len(doc)}")
            out = outdir / f"source_page_{page_no:03d}.png"
            if out.exists():
                continue
            pix = doc[page_no - 1].get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
            pix.save(out)


def choose_prediction(lab7_out: Path) -> tuple[Path, str, float | None]:
    priority = {"text": 3, "vlm": 2, "baseline": 1}
    candidates = []
    evaluation = lab7_out / "evaluation.json"
    scores: dict[str, float] = {}
    if evaluation.exists():
        data = json.loads(evaluation.read_text(encoding="utf-8"))
        for name, result in data.items():
            try:
                scores[name] = float(result.get("alignment", {}).get("f1", 0.0))
            except Exception:
                scores[name] = 0.0

    for name in ("text", "vlm", "baseline"):
        p = lab7_out / f"pred_{name}.json"
        if p.exists():
            score = scores.get(name, -1.0)
            candidates.append((score, priority[name], name, p))
    if not candidates:
        raise RuntimeError(f"No Lab 7B prediction found in {lab7_out}")
    score, _, name, path = max(candidates)
    return path, name, (None if score < 0 else score)


def check_files(profiles: dict, programs: list[str]) -> bool:
    ok = True
    print("\nRAW INPUTS")
    for code in programs:
        cfg = profiles[code]
        for key in ("pdf", "ground_truth", "page_map"):
            p = ROOT / cfg[key]
            print(f"  {'OK' if p.exists() else 'MISSING':7s} {code:4s} {key:12s} {p}")
            ok = ok and p.exists()
    print("\nCOMMANDS")
    for cmd in ("tesseract", "ollama"):
        found = shutil.which(cmd)
        print(f"  {'OK' if found else 'MISSING':7s} {cmd} {found or ''}")
        if cmd == "ollama":
            ok = ok and bool(found)
    return ok


def make_env(skip_baseline: bool) -> dict[str, str]:
    env = os.environ.copy()
    env.update({
        "PYTHONUTF8": "1",
        "PYTHONPATH": str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", ""),
        "LAB7_CHUNK": env.get("LAB7_CHUNK", "1"),
        "LAB7B_NUM_CTX": env.get("LAB7B_NUM_CTX", "4096"),
        "LAB7B_NUM_PREDICT": env.get("LAB7B_NUM_PREDICT", "2000"),
        "LAB7B_OCR_NUM_CTX": env.get("LAB7B_OCR_NUM_CTX", "4096"),
        "LAB7B_OCR_NUM_PREDICT": env.get("LAB7B_OCR_NUM_PREDICT", "1200"),
    })
    if skip_baseline:
        env["LAB7_SKIP_BASELINE"] = "1"
    return env


def run_program(code: str, cfg: dict, args: argparse.Namespace, env: dict[str, str]) -> dict:
    t0 = time.time()
    work = ROOT / "work" / code
    pages_out = work / "01_selected_pages"
    lab6_out = work / "02_lab6"
    lab7_out = work / "03_lab7b"
    lab8_out = work / "04_lab8b"
    lab9_out = work / "05_lab9"
    for d in (pages_out, lab6_out, lab7_out, lab8_out, lab9_out):
        d.mkdir(parents=True, exist_ok=True)

    pdf = ROOT / cfg["pdf"]
    gt = ROOT / cfg["ground_truth"]
    page_map = ROOT / cfg["page_map"]

    log(f"{code}: Stage 0 - validate full raw PDF")
    if not pdf.exists():
        raise FileNotFoundError(pdf)
    source_manifest = {
        "program": code,
        "source_pdf": str(pdf.relative_to(ROOT)),
        "source_size_bytes": pdf.stat().st_size,
        "source_sha256": None if args.dry_run else sha256(pdf),
        "selected_pages": cfg["page_spec"],
        "note": "Input is the original full PDF. Page selection is performed only inside the pipeline.",
    }
    (work / "source_manifest.json").write_text(
        json.dumps(source_manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    log(f"{code}: Stage 1 - render selected pages from RAW PDF")
    if args.dry_run:
        print(f"Would render pages {cfg['page_spec']} from {pdf}")
    else:
        render_selected_pages(pdf, cfg["page_spec"], pages_out)

    log(f"{code}: Stage 2/3 - Lab 7B: baseline OCR + digital text + VLM/LLM")
    pipeline = args.lab7_pipeline
    if args.skip_baseline and pipeline == "all":
        pipeline = "all"  # Lab 7 will honor LAB7_SKIP_BASELINE=1
    run([
        LAB7,
        "-i", pdf,
        "-g", gt,
        "-o", lab7_out,
        "-p", pipeline,
        "--pages", cfg["page_spec"],
    ], env=env, dry=args.dry_run)

    if args.dry_run:
        log(f"{code}: Stage 4 - Lab 6 evaluation (planned)")
        log(f"{code}: Stage 5 - Lab 8B schema -> SQLite -> verify (planned)")
        log(f"{code}: Stage 6 - 30 gold questions + NL-to-SQL evaluation (planned)")
        log(f"{code}: Stage 7 - Lab 9 evaluation report (planned)")
        return {"program": code, "status": "DRY_RUN", "seconds": 0}

    log(f"{code}: Stage 4 - Lab 6 evaluation for classic OCR baseline (when available)")
    baseline = lab7_out / "pred_baseline.json"
    if baseline.exists() and not args.skip_baseline:
        run([
            LAB6_EVAL,
            "--ground-truth", gt,
            "--prediction", baseline,
            "--page-map", page_map,
            "--output-dir", lab6_out,
        ], env=env)
    else:
        (lab6_out / "SKIPPED.txt").write_text(
            "Classic OCR baseline was skipped or unavailable. Lab 7B text/VLM and Lab 8B continue normally.\n",
            encoding="utf-8",
        )

    prediction, chosen_name, score = choose_prediction(lab7_out)
    selection = {"chosen_pipeline": chosen_name, "path": str(prediction.relative_to(ROOT)), "alignment_f1": score}
    (lab7_out / "selected_prediction.json").write_text(
        json.dumps(selection, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log(f"{code}: selected Lab 7B prediction = {chosen_name} (F1={score})")

    log(f"{code}: Stage 5 - Lab 8B schema -> import -> SQLite -> verify")
    run([LAB8, "schema", "-o", lab8_out / "schema"], env=env)
    run([
        LAB8, "import-lab7b",
        "-i", prediction,
        "-o", lab8_out / "curriculum.json",
        "--program-id", cfg["program_id"],
        "--program-name", cfg["program_name"],
        "--total-credits", cfg["total_credits"],
        "--years", cfg["years"],
    ], env=env)
    run([
        LAB8, "load",
        "-i", lab8_out / "curriculum.json",
        "-d", lab8_out / "curriculum.db",
        "--replace",
    ], env=env)
    run([
        LAB8, "verify",
        "-d", lab8_out / "curriculum.db",
        "-o", lab8_out / "verify.json",
    ], env=env)

    log(f"{code}: Stage 6 - generate 30 grounded gold questions + final evaluation")
    run([
        ROOT / "generate_gold_questions.py",
        "--ground-truth", gt,
        "--total-credits", cfg["total_credits"],
        "--years", cfg["years"],
        "--output", lab8_out / "gold_questions.json",
        "--count", 30,
    ], env=env)
    run([
        LAB8, "eval",
        "-d", lab8_out / "curriculum.db",
        "-q", lab8_out / "gold_questions.json",
        "-o", lab8_out / "eval_result.json",
    ], env=env)

    required = [
        lab8_out / "schema" / "curriculum.schema.json",
        lab8_out / "schema" / "schema.sql",
        lab8_out / "curriculum.json",
        lab8_out / "curriculum.db",
        lab8_out / "verify.json",
        lab8_out / "gold_questions.json",
    ]
    required.append(lab8_out / "eval_result.json")
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("Missing final outputs:\n- " + "\n- ".join(missing))

    log(f"{code}: Stage 7 - Lab 9 evaluation: extraction + schema/DB + NL-to-SQL metrics")
    run([
        LAB9, "run",
        "--program", code,
        "--lab7-dir", lab7_out,
        "--lab8-dir", lab8_out,
        "--output-dir", lab9_out,
    ], env=env)

    for p in (lab9_out / "lab9_report.json", lab9_out / "lab9_report.md"):
        if not p.exists():
            raise RuntimeError(f"Missing Lab 9 output: {p}")

    return {
        "program": code,
        "status": "DONE",
        "chosen_lab7_pipeline": chosen_name,
        "lab7_alignment_f1": score,
        "seconds": round(time.time() - t0, 1),
        "lab8_dir": str(lab8_out.relative_to(ROOT)),
        "lab9_dir": str(lab9_out.relative_to(ROOT)),
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Full raw-PDF pipeline: AI/BIT/IT/DSBA -> Lab 7B -> Lab 8B -> Lab 9 evaluation"
    )
    ap.add_argument("--program", choices=["all", *PROGRAM_ORDER], default="all")
    ap.add_argument("--lab7-pipeline", choices=["all", "baseline", "text", "vlm"], default="all")
    ap.add_argument("--skip-baseline", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    profiles = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
    programs = list(PROGRAM_ORDER) if args.program == "all" else [args.program]
    env = make_env(args.skip_baseline)

    if args.check:
        files_ok = check_files(profiles, programs)
        print("\nLAB 7B ENVIRONMENT")
        r = subprocess.run([PYTHON, str(LAB7), "--check"], cwd=ROOT, env=env)
        print("\nLAB 8B SELFTEST")
        s = subprocess.run([PYTHON, str(LAB8), "selftest"], cwd=ROOT, env=env)
        print("\nLAB 9 SELFTEST")
        t = subprocess.run([PYTHON, str(LAB9), "selftest"], cwd=ROOT, env=env)
        raise SystemExit(0 if files_ok and r.returncode == 0 and s.returncode == 0 and t.returncode == 0 else 1)

    results = []
    for code in programs:
        results.append(run_program(code, profiles[code], args, env))

    summary = ROOT / "work" / "all_programs_summary.json"
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n" + "=" * 78)
    print("PIPELINE COMPLETE" if not args.dry_run else "DRY RUN COMPLETE")
    print("=" * 78)
    for r in results:
        print(f"{r['program']:4s}  {r['status']:8s}  {r.get('seconds', 0):>8}s")
    if not args.dry_run:
        run([
            LAB9, "summary",
            "--work", ROOT / "work",
            "--programs", *programs,
            "--output", ROOT / "work" / "lab9_summary.json",
        ], env=env)
        print(f"Lab 9 summary: {ROOT / 'work/lab9_summary.json'}")


if __name__ == "__main__":
    main()
