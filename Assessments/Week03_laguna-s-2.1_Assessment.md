# Assessment by laguna-s-2.1

# Week 03 Prompting
- Awarded: 5b out of 5b
- Commentary: The submission is thorough and internally consistent across all four tasks. Task 1 selects three distinct non-ROSES frameworks (CAR, RACE, RISE), writes structured prompts, and reports their sources. Task 2 generates per-prompt prediction files plus an accuracy chart and measured timing. Task 3 implements a precision metric in code and reports values, and Task 4 delivers a detailed statistical comparison with permutation testing, multiple tables/graphs, and a discussion of prompt, model, and coding-agent factors. The only weakness is self-reported answer exposure (CAR used a rule-based generator, all agents read the labels CSV), which the student honestly flags; this is a reporting limitation rather than a missing deliverable.

## Task 1
- Awarded: 1b   (max 1b)
- Commentary: Chose CAR, RACE and RISE from frompting.com (not ROSES, not zero-shot). Each prompt is written in the framework's sectioned structure (Challenge/Action/Result, Role/Action/Context/Example, Request/Input/Scenario/Expectation) with the schema, file paths, an example SQL, and explicit output expectations. Report.md explains the rationale for each framework and links to its source page. All required outputs (data files + report with sources) are present and correct.

## Task 2
- Awarded: 1b   (max 1b)
- Commentary: Prediction files restaurants_dataset_predictions_CAR.csv, _RACE.csv and _RISE.csv are provided with question,predicted_sql columns. Report.md reports accuracy per prompt (80/155, 85/155, 143/155) and inference times (138.8s, 130.6s, 185.2s), identifies the model (gpt-5.6-luna via GitHub Copilot in separate sessions), and includes the accuracy.png visualization. The brief comparison and timing requirements are satisfied.

## Task 3
- Awarded: 1b   (max 1b)
- Commentary: Proposed mean per-question result precision (matched rows / predicted rows), argued it complements accuracy by measuring extra/incorrect results, and discussed that it measures surplus but not missing results. Implemented evaluate_metrics.py (reuses Task 2's load_database) with empty-result and SQL-error handling, computed values RISE 54.26%, RACE 60.76%, CAR 98.25%, and produced Report.md comparing them. Full implementation, calculation, and report are present.

## Task 4
- Awarded: 2b   (max 2b)
- Commentary: Detailed report with a comparison table (accuracy, precision, agent time), references to metric_comparison.png and generation_times.png (not viewable by this model, but described in context), a paired permutation test with Holm correction at alpha 0.05, and a p-value table. Correctly concludes RACE vs RISE is not significant while CAR differs significantly on both metrics. Discusses factors: prompt structure (CAR simple, RACE role, RISE input/scenario split), the single-run-per-prompt limitation, and coding-agent behaviour (CAR used a rule-based generator, all agents read the labels CSV = answer exposure, non-controlled concurrent timing, repeated question patterns). Interpretation and limitations are well reasoned.
