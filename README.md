# Lantern Triage

A working, privacy-first prototype for classifying logistics incident reports,
routing urgent cases, and abstaining to human review when confidence is low.

> **Live demo:** https://johanuntawidjaja-source.github.io/lantern-triage/

## What the examiner can verify

- **Working system:** browser demo in `web/`; no API key or server required.
- **Documented data:** 720 deterministic, fictional reports; provenance in
  [`data/DATA_CARD.md`](data/DATA_CARD.md).
- **Independent review:** 50 blinded human labels are recorded in
  `data/human_review.csv` and verified separately before comparison.
- **Two approaches:** transparent keyword baseline and multinomial Naive Bayes.
- **Evaluation:** accuracy-on-decided-cases, coverage/abstention, urgent misses,
  costly misroutes, latency, and cost.
- **Changed requirements:** a stricter review threshold raises human-review load
  from 44 to 109 of 160 test reports. A separate before/after experiment introduces
  a new customs queue and measures its effect on customs misroutes.
- **Business case:** [`BUSINESS_SUMMARY.md`](BUSINESS_SUMMARY.md).

## Results

| Approach | Coverage | Accuracy when decided | Urgent misses | Costly misroutes | Median latency | Cost / 1,000 |
|---|---:|---:|---:|---:|---:|---:|
| Keyword baseline | 76.9% | 95.1% | 6 | 0 | ~0.005 ms | $0 |
| Naive Bayes + abstention | 72.5% | 100% | 0 | 0 | ~0.015 ms | $0 |

These results are deliberately not presented as production accuracy: the dataset is
synthetic and templated. Their value is reproducibility and demonstration of the
evaluation method. See [`evaluation/ERROR_ANALYSIS.md`](evaluation/ERROR_ANALYSIS.md).

### Independent label review

**Johan Untawidjaja, the repository owner, personally classified all 50 reports**
without seeing their generated labels or model predictions. Codex presented the
blinded records and calculated agreement only after Johan completed the labels.
All 50 decisions agreed with the reference labels. This shows
that the template labels are internally clear; it does not substitute for review by
logistics specialists on real, de-identified reports. See
[`evaluation/HUMAN_REVIEW.md`](evaluation/HUMAN_REVIEW.md).

### Changed requirements

| Change | Before | After | Operational effect |
|---|---:|---:|---|
| Confidence threshold 0.86 → 0.92 | 44 human reviews | 109 human reviews | Higher caution substantially increases dispatcher workload |
| Add `CUSTOMS_HOLD` queue | 0% customs direct-route recall; 24 misroutes | 100% recall; 0 misroutes | New queue captures all 24 synthetic customs cases |

The perfect after-result reflects the clean templates and must not be extrapolated
to production. The scripts preserve the experiment so it can be repeated on better data.

## Run locally

Python 3.10+ is sufficient; there are no third-party Python dependencies.

```bash
python scripts/generate_data.py
python scripts/evaluate.py
python scripts/changed_requirement.py
python scripts/new_category_experiment.py
python scripts/verify_human_review.py
python -m unittest discover -s tests -v
python -m http.server 8000
```

Then open `http://localhost:8000/web/`.

## Repository map

- `web/` — static interactive demo and exported model
- `src/triage.py` — baseline and candidate model
- `scripts/` — deterministic generation, evaluation, and policy-change experiment
- `data/` — synthetic reports, blinded human-review decisions, and dataset card
- `evaluation/` — machine-readable results, taxonomy, and error analysis
- `tests/` — fast regression tests

## Design decisions

1. **Abstention is a feature.** Low confidence becomes `HUMAN_REVIEW`.
2. **High-cost errors are first-class metrics.** Temperature and customs errors are
   counted separately from average correctness.
3. **No incident text telemetry.** The public demo runs in the browser and sends no
   report content anywhere.
4. **No opaque paid model.** This keeps the evidence reproducible and the cost zero.

## Collaboration and AI disclosure

Johan Untawidjaja defined the product direction, personally completed the 50-report
blinded label review, and accepted the final scope. OpenAI Codex was used to
generate the initial code and synthetic templates, present the blinded review items, run
tests, perform a privacy scan, and critique the submission
against the exam brief. All generated evidence is reproducible from the scripts.
No private chat transcript, account credential, personal dataset, or unrelated
project configuration is included in this repository.

## Limitations and next step

The main limitation is domain validity: synthetic text is easier than real incident
reports. The next step is a shadow-mode pilot using consented, de-identified data
and two logistics operators for blinded label adjudication. Human dispatchers must
retain final authority.

