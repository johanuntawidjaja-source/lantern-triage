# Review-driven iteration record

## Review 1 — commit `11a17be`

Two independent `gpt-5.6-sol` reviewers audited the repository read-only. Their full
reports are preserved in `EXAMINER_REVIEW.md` and `INDUSTRY_REVIEW.md`.

## Changes made

- Replaced the leaking row split with disjoint train/test template families.
- Added a regression test that forbids exact report overlap across the split.
- Raised the default direct-route threshold from 0.80 to 0.95.
- Renamed browser “confidence” to **model score**.
- Replaced seven literal ambiguity phrases with broader generic-language handling.
- Added an independent safety escalation for injury, collision, fire, spill, hazmat,
  and theft language.
- Added negation/resolution handling; these inputs go to human review and do not
  create false urgency.
- Added a randomized compositional adversarial generator with optional seeds.
- Preserved the exact 50 originally reviewed texts in `data/human_review_items.csv`
  after the examiner noticed that regenerated IDs alone were insufficient evidence.

## Automated iteration evidence

Each run creates 135 fresh combinations from held-out clear, safety, negated, and
ambiguous phrase banks. With no `--seed`, the seed is random; the two recorded runs
use fixed seeds so examiners can reproduce them.

| Seed | Version | Route accuracy | Urgent accuracy | Dangerous direct routes |
|---:|---|---:|---:|---:|
| 20261019 | Guards disabled (ablation) | 60.7% | 80.0% | 34 |
| 20261019 | Revised guarded system | 81.5% | 98.5% | 0 |
| 20261020 | Guards disabled (ablation) | 60.0% | 79.3% | 38 |
| 20261020 | Revised guarded system | 88.1% | 96.3% | 0 |

## Post-revision independent check

The same reviewers re-ran their probes. The logistics reviewer called the revision
credible as an exam prototype and confirmed zero exact overlap, safe handling of the
original injury/fire/spill/negation probes, model-score wording, and conservative
abstention. The examiner estimated **76–83/100** on the revised working tree, then
identified two final evidence defects: reviewed IDs no longer preserved the exact
old text, and “before review” overstated what was actually a guard-disabled ablation.
Both were corrected: exact review texts are now immutable, and the ablation is named
accurately. Three further regression tests cover multi-issue reports, clause-scoped
urgency, and unsupported-language urgency uncertainty; the suite now has 12 tests.

The ablation uses the revised corpus/model with selected safeguards disabled; it is
not a replay of commit `11a17be`. These synthetic checks isolate the safeguards'
effect, not production validity. The fixed held-out evaluation and human review
remain separate.
