# Lab 9 Evaluation — AI

## 1. Extraction (Lab 7B)
- Selected pipeline: `text`
- Course alignment Precision: 0.9167
- Course alignment Recall: 0.9821
- Course alignment F1: 0.9483
- Overall micro CER: 0.126897

## 2. Structured data + database (Lab 8B)
- Final JSON valid: yes
- Verify checks: 6/7 (rate=0.857143)

## 3. NL-to-SQL / final QA (Lab 9)
- Questions: 30
- Valid SQL rate: 1.0 (30/30)
- Execution Accuracy: 0.9 (27/30)
- Mean latency: 1.046667 s/question

## 4. Metrics intentionally not claimed
- Natural-language Exact Match / Token-F1: not measured because the gold set stores structured expected SQL results, not one canonical Thai sentence.
- Faithfulness / Groundedness: not measured because evidence annotations are not logged.
- Citation coverage: not measured because answers do not yet emit page/row citations.

## 5. Overfitting
- Not assessable from train/validation curves because this project performs inference with pretrained local models and does not train/fine-tune a model.
- Keep the final 30 gold questions as a held-out test set; do not repeatedly tune prompts against them.
