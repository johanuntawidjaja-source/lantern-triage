# Logistics and applied-ML expert review — pre-revision

- **Reviewer:** independent Codex task, `gpt-5.6-sol`, low reasoning
- **Date:** 19 October 2026
- **Scope:** operational taxonomy, urgent handling, abstention, failure modes,
  privacy, and human-in-the-loop design
- **Repository state reviewed:** commit `11a17be`
- **Editing authority:** read-only; the reviewer changed no files

## Verdict

The reviewer found a promising exam prototype whose reliability claims were inflated
by leakage and whose safety handling needed to be independent from queue prediction.

## Findings and concrete probes

1. **Leakage:** 168/190 test texts were exact training duplicates.
2. **Safety was not an override:** `driver injured and unconscious after crash` was
   not urgent; `chemical spill from hazardous cargo` and `fire in the truck` received
   ordinary operational queues.
3. **Negation/resolution failed:** `not urgent, no leak and no fire`, `no damage found
   after inspection`, and `vaccine delivered safely at correct temperature` produced
   misleading urgency or routes.
4. **Out-of-distribution overconfidence:** generic unfamiliar text could receive a
   high score; the displayed percentage was not calibrated.
5. **Single-label limits:** mixed incidents can require multiple signals. For this
   exam scope, safety and multi-issue signals should force human review.
6. **Evidence gaps:** the curated suite did not cover enough safety, negation,
   resolved, multi-issue, multilingual, or out-of-domain cases.
7. **Operational limitation:** the prototype recommends review but does not implement
   a production review queue, SLA, owner, override log, or feedback loop.
8. **Positive privacy finding:** browser-local inference and the warning beside the
   input are appropriate for a static exam demo.

## Recommended minimum revision

Use a template-family-held-out split; add randomized adversarial tests; rename the
percentage “model score”; add safety escalation and negation/resolution handling;
describe the 50-label exercise as an internal blinded check; retain human authority.

## Revision response

Those exam-sized recommendations were implemented. Safety and negated/resolved text
now force human review, safety events are urgent, literal ambiguity phrases were
replaced by broader signals, and two seeded randomized evaluations quantify the
effect of enabled versus disabled guards. Production workflow features remain
explicitly out of scope.

## Post-revision verification

The reviewer judged the revision **credible and substantially improved as an exam
prototype**. It confirmed 0/190 exact overlap, the corrected dangerous probes,
conservative fixed-suite behavior, model-score wording, and candid documentation.
Its remaining cautions—mixed incidents, clause-scoped negation, unsupported-language
urgency, and browser/Python parity—led to three additional guards/tests before the
final release. Scores remain uncalibrated and all evidence remains synthetic.
