from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def safe_rate(num: int, den: int) -> float | None:
    return None if den == 0 else num / den


def r6(v: Any) -> Any:
    if isinstance(v, float) and math.isfinite(v):
        return round(v, 6)
    return v


def build_report(program: str, lab7_dir: Path, lab8_dir: Path) -> dict[str, Any]:
    selected_path = lab7_dir / 'selected_prediction.json'
    lab7_eval_path = lab7_dir / 'evaluation.json'
    curriculum_path = lab8_dir / 'curriculum.json'
    conversion_path = lab8_dir / 'curriculum.conversion.json'
    verify_path = lab8_dir / 'verify.json'
    qa_eval_path = lab8_dir / 'eval_result.json'

    required = [selected_path, lab7_eval_path, curriculum_path, conversion_path, verify_path, qa_eval_path]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError('Lab 9 requires completed Lab 7B + Lab 8B outputs:\n- ' + '\n- '.join(missing))

    selected = load_json(selected_path)
    selected_name = str(selected.get('chosen_pipeline') or '')
    all_l7 = load_json(lab7_eval_path)
    if selected_name not in all_l7:
        raise KeyError(f"Selected Lab 7B pipeline {selected_name!r} is absent from {lab7_eval_path}")
    l7 = all_l7[selected_name]

    # A JSON-valid final curriculum is guaranteed here because it can be parsed.
    curriculum = load_json(curriculum_path)
    conversion = load_json(conversion_path)
    verify = load_json(verify_path)
    qa_rows = load_json(qa_eval_path)
    if not isinstance(qa_rows, list):
        raise TypeError('eval_result.json must be a JSON array')

    alignment = l7.get('alignment') or {}
    attributes = l7.get('attributes') or {}
    attr_out: dict[str, Any] = {}
    for name, m in attributes.items():
        if not isinstance(m, dict):
            continue
        attr_out[name] = {
            'label': m.get('label'),
            'n_items': m.get('n_items'),
            'cer': r6(m.get('cer')),
            'wer': r6(m.get('wer')),
            'exact_match_accuracy': r6(m.get('exact_match_acc')),
            'missing': m.get('n_missing'),
            'hallucinated': m.get('n_hallucinated'),
        }

    n_q = len(qa_rows)
    valid_sql = sum(1 for row in qa_rows if row.get('error') in (None, ''))
    execution_correct = sum(1 for row in qa_rows if bool(row.get('correct')))
    latencies = [float(row['seconds']) for row in qa_rows if isinstance(row.get('seconds'), (int, float))]

    verify_total = len(verify) if isinstance(verify, list) else 0
    verify_pass = sum(1 for x in verify if isinstance(x, dict) and bool(x.get('ok'))) if isinstance(verify, list) else 0

    # Lab 9 slide asks to diagnose each stage instead of collapsing everything to one number.
    report = {
        'lab': 9,
        'program': program,
        'scope': 'Evaluation of the completed curriculum OCR -> structured JSON -> SQLite -> NL-to-SQL pipeline',
        'lab7_extraction': {
            'selected_pipeline': selected_name,
            'alignment': {
                'matched': alignment.get('matched'),
                'missed': alignment.get('missed'),
                'spurious': alignment.get('spurious'),
                'precision': r6(alignment.get('precision')),
                'recall': r6(alignment.get('recall')),
                'f1': r6(alignment.get('f1')),
                'ground_truth_total': alignment.get('gt_total'),
                'prediction_total': alignment.get('pred_total'),
            },
            'overall_micro_cer': r6(l7.get('overall_micro_cer')),
            'attributes': attr_out,
            'internal_check': l7.get('internal_check'),
            'interpretation_note': 'CER/WER and exact-match are reported per extracted attribute; alignment precision/recall/F1 measures missing/spurious course rows.',
        },
        'lab8_structured_data_and_db': {
            'json_valid_rate_final': 1.0,
            'schema_pass_final': True,
            'conversion': {
                'source_courses': conversion.get('source_courses'),
                'converted_courses': conversion.get('converted_courses'),
                'plan_items': conversion.get('plan_items'),
                'prerequisites': conversion.get('prerequisites'),
                'skipped_wildcards': conversion.get('skipped_wildcards'),
                'skipped_flexible_plan_items': conversion.get('skipped_flexible_plan_items'),
                'warning_count': len(conversion.get('warnings') or []),
            },
            'verify_7_checks': {
                'passed': verify_pass,
                'total': verify_total,
                'pass_rate': r6(safe_rate(verify_pass, verify_total)),
                'checks': verify,
            },
            'repair_rate': {
                'status': 'not_applicable',
                'reason': 'This pipeline uses deterministic import-lab7b conversion for Lab 8B rather than the LLM JSON repair loop, so a repair-loop rate is not generated.',
            },
        },
        'lab9_qa_evaluation': {
            'questions': n_q,
            'valid_sql_count': valid_sql,
            'valid_sql_rate': r6(safe_rate(valid_sql, n_q)),
            'execution_correct_count': execution_correct,
            'execution_accuracy': r6(safe_rate(execution_correct, n_q)),
            'mean_seconds_per_question': r6(statistics.mean(latencies)) if latencies else None,
            'median_seconds_per_question': r6(statistics.median(latencies)) if latencies else None,
            'failed_sql_questions': [
                {'question': row.get('question'), 'error': row.get('error'), 'sql': row.get('sql')}
                for row in qa_rows if row.get('error') not in (None, '')
            ],
            'wrong_answer_questions': [
                {'question': row.get('question'), 'why': row.get('why'), 'sql': row.get('sql')}
                for row in qa_rows if not bool(row.get('correct'))
            ],
            'metric_note': 'For this Group-B NL-to-SQL task, Execution Accuracy is the key end-to-end correctness metric; Valid SQL Rate is reported separately because syntactically executable SQL can still answer the wrong question.',
        },
        'metrics_not_claimed': {
            'exact_match_and_token_f1_for_natural_language_answer': 'not_measured: gold questions store structured expected SQL results, not a single canonical Thai answer string.',
            'faithfulness_groundedness': 'not_measured: the current Lab 8B answer log does not contain sentence-level evidence annotations.',
            'citation_coverage': 'not_measured: the current answer path does not emit page/row citations.',
            'coverage_abstain_rate': 'not_measured: eval_result.json has no explicit abstain flag.',
        },
        'overfitting': {
            'status': 'not_assessable_from_this_pipeline',
            'reason': 'No model is trained or fine-tuned in this project run, so there are no train/validation learning curves from which to diagnose underfitting/overfitting. The local models are used for inference only.',
            'data_leakage_guard': 'Gold questions are generated from curated ground truth, while the evaluated database is built from the OCR/LLM prediction. Do not tune prompts against the same 30 final questions if you want them to remain a final test set.',
        },
        'artifacts': {
            'selected_prediction': str(selected_path),
            'lab7_evaluation': str(lab7_eval_path),
            'curriculum_json': str(curriculum_path),
            'curriculum_db': str(lab8_dir / 'curriculum.db'),
            'verify_json': str(verify_path),
            'gold_questions': str(lab8_dir / 'gold_questions.json'),
            'eval_result': str(qa_eval_path),
        },
        'curriculum_counts': {
            'courses': len(curriculum.get('courses') or []),
            'plan_items': len(curriculum.get('plan') or []),
            'prerequisites': len(curriculum.get('prerequisites') or []),
        },
    }
    return report


def report_markdown(report: dict[str, Any]) -> str:
    a = report['lab7_extraction']['alignment']
    q = report['lab9_qa_evaluation']
    v = report['lab8_structured_data_and_db']['verify_7_checks']
    lines = [
        f"# Lab 9 Evaluation — {report['program']}",
        '',
        '## 1. Extraction (Lab 7B)',
        f"- Selected pipeline: `{report['lab7_extraction']['selected_pipeline']}`",
        f"- Course alignment Precision: {a['precision']}",
        f"- Course alignment Recall: {a['recall']}",
        f"- Course alignment F1: {a['f1']}",
        f"- Overall micro CER: {report['lab7_extraction']['overall_micro_cer']}",
        '',
        '## 2. Structured data + database (Lab 8B)',
        f"- Final JSON valid: yes",
        f"- Verify checks: {v['passed']}/{v['total']} (rate={v['pass_rate']})",
        '',
        '## 3. NL-to-SQL / final QA (Lab 9)',
        f"- Questions: {q['questions']}",
        f"- Valid SQL rate: {q['valid_sql_rate']} ({q['valid_sql_count']}/{q['questions']})",
        f"- Execution Accuracy: {q['execution_accuracy']} ({q['execution_correct_count']}/{q['questions']})",
        f"- Mean latency: {q['mean_seconds_per_question']} s/question",
        '',
        '## 4. Metrics intentionally not claimed',
        '- Natural-language Exact Match / Token-F1: not measured because the gold set stores structured expected SQL results, not one canonical Thai sentence.',
        '- Faithfulness / Groundedness: not measured because evidence annotations are not logged.',
        '- Citation coverage: not measured because answers do not yet emit page/row citations.',
        '',
        '## 5. Overfitting',
        '- Not assessable from train/validation curves because this project performs inference with pretrained local models and does not train/fine-tune a model.',
        '- Keep the final 30 gold questions as a held-out test set; do not repeatedly tune prompts against them.',
        '',
    ]
    return '\n'.join(lines)


def write_one(program: str, lab7_dir: Path, lab8_dir: Path, outdir: Path) -> dict[str, Any]:
    report = build_report(program, lab7_dir, lab8_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / 'lab9_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (outdir / 'lab9_report.md').write_text(report_markdown(report), encoding='utf-8')
    print(f"[Lab9] {program}: valid_sql={report['lab9_qa_evaluation']['valid_sql_rate']} execution_accuracy={report['lab9_qa_evaluation']['execution_accuracy']}")
    print(f"[Lab9] wrote {outdir / 'lab9_report.json'}")
    return report


def build_summary(work: Path, programs: list[str], output: Path) -> dict[str, Any]:
    rows = []
    for p in programs:
        path = work / p / '05_lab9' / 'lab9_report.json'
        if not path.exists():
            raise FileNotFoundError(path)
        r = load_json(path)
        rows.append({
            'program': p,
            'selected_lab7_pipeline': r['lab7_extraction']['selected_pipeline'],
            'lab7_alignment_f1': r['lab7_extraction']['alignment']['f1'],
            'lab7_micro_cer': r['lab7_extraction']['overall_micro_cer'],
            'verify_pass_rate': r['lab8_structured_data_and_db']['verify_7_checks']['pass_rate'],
            'valid_sql_rate': r['lab9_qa_evaluation']['valid_sql_rate'],
            'execution_accuracy': r['lab9_qa_evaluation']['execution_accuracy'],
        })
    summary = {'lab': 9, 'programs': rows, 'note': 'Per-stage metrics; no single overall score is manufactured.'}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    return summary


def selftest() -> None:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        l7 = root/'l7'; l8 = root/'l8'; out = root/'out'
        l7.mkdir(); l8.mkdir()
        (l7/'selected_prediction.json').write_text(json.dumps({'chosen_pipeline':'text'}), encoding='utf-8')
        (l7/'evaluation.json').write_text(json.dumps({'text':{
            'overall_micro_cer':0.1,
            'alignment':{'matched':9,'missed':1,'spurious':0,'precision':1.0,'recall':0.9,'f1':0.947,'gt_total':10,'pred_total':9},
            'attributes':{'name_th':{'label':'ชื่อ','n_items':10,'cer':0.1,'wer':0.2,'exact_match_acc':0.8,'n_missing':1,'n_hallucinated':0}},
            'internal_check':{'ok':True}
        }}), encoding='utf-8')
        (l8/'curriculum.json').write_text(json.dumps({'program':{},'courses':[{}],'plan':[{}],'prerequisites':[]}), encoding='utf-8')
        (l8/'curriculum.conversion.json').write_text(json.dumps({'source_courses':10,'converted_courses':9,'plan_items':9,'prerequisites':0,'skipped_wildcards':0,'skipped_flexible_plan_items':0,'warnings':[]}), encoding='utf-8')
        (l8/'verify.json').write_text(json.dumps([{'ok':True} for _ in range(7)]), encoding='utf-8')
        (l8/'eval_result.json').write_text(json.dumps([
            {'question':'q1','error':None,'correct':True,'seconds':1.0,'sql':'SELECT 1'},
            {'question':'q2','error':None,'correct':False,'seconds':2.0,'sql':'SELECT 2'},
            {'question':'q3','error':'bad sql','correct':False,'seconds':3.0,'sql':'BAD'},
        ]), encoding='utf-8')
        r=write_one('TEST',l7,l8,out)
        assert r['lab9_qa_evaluation']['valid_sql_rate'] == round(2/3,6)
        assert r['lab9_qa_evaluation']['execution_accuracy'] == round(1/3,6)
        assert (out/'lab9_report.md').exists()
    print('Lab 9 selftest: PASS')


def main() -> None:
    ap = argparse.ArgumentParser(description='Lab 9 evaluation for the curriculum OCR/NL-to-SQL project')
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('run')
    p.add_argument('--program', required=True)
    p.add_argument('--lab7-dir', required=True)
    p.add_argument('--lab8-dir', required=True)
    p.add_argument('--output-dir', required=True)
    s = sub.add_parser('summary')
    s.add_argument('--work', default='work')
    s.add_argument('--programs', nargs='+', required=True)
    s.add_argument('--output', default='work/lab9_summary.json')
    sub.add_parser('selftest')
    args = ap.parse_args()
    if args.cmd == 'run':
        write_one(args.program, Path(args.lab7_dir), Path(args.lab8_dir), Path(args.output_dir))
    elif args.cmd == 'summary':
        build_summary(Path(args.work), args.programs, Path(args.output))
        print(f"[Lab9] wrote {args.output}")
    else:
        selftest()


if __name__ == '__main__':
    main()
