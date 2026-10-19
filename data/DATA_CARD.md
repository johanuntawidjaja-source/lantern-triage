# Dataset card

- **Purpose:** evaluate routing of fictional logistics incident reports.
- **Size:** 840 reports across seven categories.
- **Provenance:** deterministic templates in `scripts/generate_data.py`; no customer
  records, scraped content, personal data, or confidential company information.
- **Split:** first 650 rows use training-only template families; final 190 use
  disjoint test-only families. There is no exact report-text overlap.
- **Variation:** templates include full and short reports, synonyms, operational
  paraphrases, and deliberately misspelled forms. A separate 42-case challenge
  set in `scripts/robustness.py` is not part of the training file.
- **Known limitation:** templated data is cleaner than production text and therefore
  inflates measured accuracy. Results establish reproducibility, not field validity.
- **Blinded internal label check:** `human_review.csv` records 50 classifications;
  `human_review_items.csv` immutably preserves the exact text, reference label, and
  reviewed label from the completed exercise. It is intentionally independent of
  regenerated `incidents.csv`. The decisions were
  personally supplied by repository owner Johan Untawidjaja without seeing generated
  labels or predictions. Codex presented the records but did not select his answers.
  Fifty decisions were completed before comparison; agreement results are recorded
  in `evaluation/human_review_results.json`.
- **Production requirement:** obtain consented, de-identified samples and have at
  least two operations specialists adjudicate a blinded evaluation set.

