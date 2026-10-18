# Dataset card

- **Purpose:** evaluate routing of fictional logistics incident reports.
- **Size:** 720 reports across seven categories.
- **Provenance:** deterministic templates in `scripts/generate_data.py`; no customer
  records, scraped content, personal data, or confidential company information.
- **Split:** first 560 shuffled rows train; final 160 rows test. Seed: `20261019`.
- **Known limitation:** templated data is cleaner than production text and therefore
  inflates measured accuracy. Results establish reproducibility, not field validity.
- **Independent label review:** `review_sample.csv` contains 60 records selected
  independently of model output and reviewed against the written taxonomy. This is
  an AI-assisted secondary review, not a claim of external human validation.
- **Production requirement:** obtain consented, de-identified samples and have at
  least two operations specialists adjudicate a blinded evaluation set.

