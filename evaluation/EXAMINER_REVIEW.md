# Independent examiner review — pre-revision

- **Reviewer:** independent Codex task, `gpt-5.6-sol`, low reasoning
- **Date:** 19 October 2026
- **Scope:** exam criteria, repository, data, evaluation, tests, and browser demo
- **Repository state reviewed:** commit `11a17be`
- **Editing authority:** read-only; the reviewer changed no files

## Verdict

The reviewer described the project as polished, reproducible, well documented, and
genuinely demonstrable, but estimated only **65–72/100** because the headline result
did not constitute a valid generalization test.

## Findings

1. **Critical train/test leakage.** It found 168/190 test texts duplicated in
   training, 183/190 sharing a normalized template, and only 293 unique texts among
   840 rows. The 99.5% result therefore mainly measured template memorization.
2. **Circular ambiguity evidence.** The seven ambiguity probes appeared verbatim in
   the hard-coded guard, so 7/7 abstention was a rule test rather than independent
   robustness evidence.
3. **Uncalibrated percentage.** Temperature scaling was heuristic; the UI should say
   “model score,” not “confidence,” unless calibration evidence is supplied.
4. **Weak threshold experiment.** The earlier stricter threshold changed workload
   without showing a safety improvement.
5. **Missing evidence.** Add unconditional routing accuracy, confusion evidence,
   urgent false positives, leakage-free template-family splits, adversarial cases,
   and browser/Python parity checks.
6. **Human review wording.** The 50 labels are valuable as a blinded internal label
   check but are not independent domain validation.

## What already passed

All then-existing tests and the privacy audit passed; generated evidence reproduced;
the browser demo was real and keyless; documentation, taxonomy, provenance,
limitations, security language, business framing, and AI disclosure were strong.

## Revision response

The project now uses disjoint train/test template families, removes exact test-text
duplicates, labels the percentage as a model score, uses unseen randomized safety and
ambiguity probes, and reports the review candidly. See `REVIEW_RESPONSE.md` and the
two `randomized-iteration-*.json` files.

## Post-revision verification

The reviewer raised the likely score to **76–83/100** and confirmed that leakage,
circular ambiguity evidence, score wording, safety/negation handling, and claim
restraint were substantially corrected. It caught two final provenance/naming issues:
the regenerated dataset had changed text behind reviewed IDs, and the comparison was
an ablation rather than a literal old-system replay. Both are corrected in the final
repository via `human_review_items.csv` and accurate ablation labels.
