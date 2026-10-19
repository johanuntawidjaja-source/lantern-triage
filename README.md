# Lentera Triage

A working, privacy-first prototype for classifying logistics incident reports,
routing urgent cases, and abstaining to human review when confidence is low.

> **Live demo:** https://johanuntawidjaja-source.github.io/lantern-triage/

## What the examiner can verify

- **Working system:** browser demo in `web/`; no API key or server required.
- **Documented data:** 840 deterministic, fictional reports; provenance in
  [`data/DATA_CARD.md`](data/DATA_CARD.md).
- **Blinded internal label check:** 50 human labels and the immutable texts actually
  shown to Johan are preserved in `data/human_review*.csv`.
- **Two approaches:** transparent keyword baseline and subword-enhanced multinomial
  Naive Bayes with an ambiguity guard.
- **Evaluation:** accuracy-on-decided-cases, coverage/abstention, urgent misses,
  costly misroutes, latency, and cost.
- **Changed requirements:** a stricter review threshold raises human-review load
  from 49 to 62 of 280 policy-test reports. A separate before/after experiment introduces
  a new customs queue and measures its effect on customs misroutes.
- **Independent critiques:** complete examiner and logistics-expert reports, plus the
  revision response, are preserved in `evaluation/`.
- **Business case:** [`BUSINESS_SUMMARY.md`](BUSINESS_SUMMARY.md).

## Results

| Approach | Coverage | Accuracy when decided | Urgent misses | Costly misroutes | Median latency | Cost / 1,000 |
|---|---:|---:|---:|---:|---:|---:|
| Keyword baseline | 33.2% | 100% | 9 | 0 | ~0.006 ms | $0 |
| Subword Naive Bayes + abstention | 81.1% | 100% | 0 | 0 | ~0.210 ms | $0 |

These results are deliberately not presented as production accuracy: the dataset is
synthetic and templated. Their value is reproducibility and demonstration of the
evaluation method. See [`evaluation/ERROR_ANALYSIS.md`](evaluation/ERROR_ANALYSIS.md).

The train and test sets use disjoint template families and contain no exact text
overlap. Accuracy is conditional on direct routing; coverage reports how often the
model did not abstain.

### Blinded internal label check

**Johan Untawidjaja, the repository owner, personally classified all 50 reports**
without seeing their generated labels or model predictions. Codex presented the
blinded records and calculated agreement only after Johan completed the labels.
All 50 decisions agreed with the reference labels. This shows
that the template labels are internally clear; it does not substitute for review by
logistics specialists on real, de-identified reports. See
[`evaluation/HUMAN_REVIEW.md`](evaluation/HUMAN_REVIEW.md).
The reviewed text is stored separately from the regenerable model dataset so future
dataset revisions cannot silently change what those decisions refer to.

### Changed requirements

| Change | Before | After | Operational effect |
|---|---:|---:|---|
| Confidence threshold 0.95 → 0.99 | 49 human reviews | 62 human reviews | Higher caution increases dispatcher workload |
| Add `CUSTOMS_HOLD` queue | 0% raw customs recall; 40 forced errors | 55% raw recall; 18 forced errors | New label helps, but held-out wording exposes remaining model limits |

The held-out result remains synthetic and must not be extrapolated to production.
The scripts preserve the experiment so it can be repeated on better data.

## Run locally

Python 3.10+ is sufficient; there are no third-party Python dependencies.

```bash
python scripts/generate_data.py
python scripts/evaluate.py
python scripts/robustness.py
python scripts/randomized_evaluation.py # fresh random seed
python scripts/randomized_evaluation.py --seed 20261019 --output evaluation/randomized-iteration-1.json
python scripts/randomized_evaluation.py --seed 20261020 --output evaluation/randomized-iteration-2.json
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

## Independent review and iteration evidence

Two read-only `gpt-5.6-sol` reviews were run on 19 October 2026. Their reports are
included without hiding the original criticisms:

- [`evaluation/EXAMINER_REVIEW.md`](evaluation/EXAMINER_REVIEW.md)
- [`evaluation/INDUSTRY_REVIEW.md`](evaluation/INDUSTRY_REVIEW.md)
- [`evaluation/REVIEW_RESPONSE.md`](evaluation/REVIEW_RESPONSE.md)

The reviewers found severe leakage and unsafe negation/safety behavior in commit
`11a17be`. The revision introduced disjoint template families, safety escalation,
negation/resolution and conflict guards, and randomized adversarial testing.

Across two recorded 135-report randomized guard-ablation comparisons, route accuracy improved from
60.7%→81.5% and 60.0%→88.1%; urgent accuracy improved from 80.0%→98.5% and
79.3%→96.3%; dangerous direct routes fell from 34 and 38 to zero. These are synthetic
stress tests, not a replay of the old commit or production performance claims.

## Open references and provenance

No external incident record was copied into the dataset: every report remains
deterministic and fictional. Open sources informed the terminology and model design:

- The [UN/CEFACT Multimodal Transport Status Request vocabulary](https://service.unece.org/trade/uncefact/publication/Transport-Logistics/MMT-TSR/HTML/058.htm)
  includes transport states such as damaged, delayed, and customs clearance; it was
  used as a terminology cross-check, not as a source of incident text.
- Bojanowski et al., [*Enriching Word Vectors with Subword Information*](https://aclanthology.org/Q17-1010/),
  motivate character n-grams for unseen and morphologically related words.
- Joulin et al., [*Bag of Tricks for Efficient Text Classification*](https://aclanthology.org/E17-2068/),
  supports the choice of a fast, inspectable n-gram classifier for a local demo.
- The [scikit-learn text feature extraction guide](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
  notes that character n-grams are resilient to misspellings and derivations.

Lentera implements its own dependency-free word/character n-gram Naive Bayes model;
it does not bundle fastText or scikit-learn and does not claim their benchmark results.

## Collaboration and AI disclosure

Johan Untawidjaja defined the product direction, personally completed the 50-report
blinded label review, and accepted the final scope. OpenAI Codex was used to
generate the initial code and synthetic templates, present the blinded review items, run
tests, perform a privacy scan, and critique the submission. Two additional isolated
Codex reviewers served as an exam assessor and logistics/applied-ML reviewer
against the exam brief. All generated evidence is reproducible from the scripts.
No private chat transcript, account credential, personal dataset, or unrelated
project configuration is included in this repository.

## Limitations and next step

The main limitation is domain validity: synthetic text is easier than real incident
reports. A 42-case fixed robustness suite and two 135-case randomized adversarial
runs test short reports, synonyms, typos, safety, negation, and ambiguity. The next
step is a shadow-mode pilot using
consented, de-identified data and two logistics operators for blinded label
adjudication. Human dispatchers must retain final authority.

