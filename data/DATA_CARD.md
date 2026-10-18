# Dataset card

- **Purpose:** evaluate routing of fictional logistics incident reports.
- **Size:** 720 reports across seven categories.
- **Provenance:** deterministic templates in `scripts/generate_data.py`; no customer
  records, scraped content, personal data, or confidential company information.
- **Split:** first 560 shuffled rows train; final 160 rows test. Seed: `20261019`.
- **Known limitation:** templated data is cleaner than production text and therefore
  inflates measured accuracy. Results establish reproducibility, not field validity.
- **Independent label review:** `human_review.csv` records blinded classifications
  supplied by the repository owner without seeing generated labels or predictions.
  Fifty decisions were completed before comparison; agreement results are recorded
  in `evaluation/human_review_results.json`.
- **Production requirement:** obtain consented, de-identified samples and have at
  least two operations specialists adjudicate a blinded evaluation set.

