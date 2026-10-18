# Lantern Triage

A working, privacy-first prototype for classifying logistics incident reports,
routing urgent cases, and abstaining to human review when confidence is low.

> **Live demo:** GitHub Pages URL will be inserted after the first deployment.

## What the examiner can verify

- **Working system:** browser demo in `web/`; no API key or server required.
- **Documented data:** 720 deterministic, fictional reports; provenance in
  [`data/DATA_CARD.md`](data/DATA_CARD.md).
- **Independent review pass:** 60 records in `data/review_sample.csv` were selected
  independently from predictions and checked against the written taxonomy. This is
  disclosed as AI-assisted secondary review, not external human validation.
- **Two approaches:** transparent keyword baseline and multinomial Naive Bayes.
- **Evaluation:** accuracy-on-decided-cases, coverage/abstention, urgent misses,
  costly misroutes, latency, and cost.
- **Changed requirement:** a stricter review threshold raises human-review load
  from 44 to 109 of 160 test reports while retaining zero urgent misses on this
  synthetic test split.
- **Business case:** [`BUSINESS_SUMMARY.md`](BUSINESS_SUMMARY.md).

## Results

| Approach | Coverage | Accuracy when decided | Urgent misses | Costly misroutes | Median latency | Cost / 1,000 |
|---|---:|---:|---:|---:|---:|---:|
| Keyword baseline | 76.9% | 95.1% | 6 | 0 | ~0.005 ms | $0 |
| Naive Bayes + abstention | 72.5% | 100% | 0 | 0 | ~0.015 ms | $0 |

These results are deliberately not presented as production accuracy: the dataset is
synthetic and templated. Their value is reproducibility and demonstration of the
evaluation method. See [`evaluation/ERROR_ANALYSIS.md`](evaluation/ERROR_ANALYSIS.md).

## Run locally

Python 3.10+ is sufficient; there are no third-party Python dependencies.

```bash
python scripts/generate_data.py
python scripts/review_sample.py
python scripts/evaluate.py
python scripts/changed_requirement.py
python -m unittest discover -s tests -v
python -m http.server 8000
```

Then open `http://localhost:8000/web/`.

## Repository map

- `web/` — static interactive demo and exported model
- `src/triage.py` — baseline and candidate model
- `scripts/` — deterministic generation, review sample, evaluation, policy change
- `data/` — synthetic reports, review worksheet, dataset card
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

The repository owner defined the product direction and accepted the final scope.
OpenAI Codex was used to inspect earlier prototypes, generate the initial code and
synthetic templates, run tests, perform a privacy scan, and critique the submission
against the exam brief. All generated evidence is reproducible from the scripts.
No private chat transcript, account credential, stock-trading record, or Cloudflare
configuration is included in this repository.

## Limitations and next step

The main limitation is domain validity: synthetic text is easier than real incident
reports. The next step is a shadow-mode pilot using consented, de-identified data
and two logistics operators for blinded label adjudication. Human dispatchers must
retain final authority.

