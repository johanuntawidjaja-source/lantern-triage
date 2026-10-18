# One-page business summary — Lantern Triage

## Problem
Logistics teams receive incident reports through inconsistent free text. Manual
sorting delays urgent cases, while an incorrect automated route can be costly.

## Prototype
Lantern Triage classifies a report into one of seven operational queues, flags
urgent language, explains the signals it recognized, and sends uncertain cases to
human review. It is a decision-support queue, not autonomous dispatch.

## Evidence
The repository contains a deterministic 720-report synthetic dataset, a documented
60-report secondary label review, a keyword baseline, a probabilistic model,
latency/cost/error measurements, and a changed-requirement experiment. The demo is
browser-only and incurs no model/API cost.

## Business value
The expected benefit is faster first response and fewer high-cost misroutes. The
right pilot metric is not raw accuracy alone: measure urgent recall, costly
misroutes, median time-to-correct-queue, review workload, and operator overrides.

## Pilot plan
Run a four-week shadow pilot on consented, de-identified reports. Human dispatchers
retain control. Calibrate thresholds weekly, require review for high-risk cargo,
and stop the pilot if urgent recall falls below the agreed safety threshold.

## Risks
Synthetic data is not representative; confidence may be miscalibrated; multilingual
or multi-issue reports may fail; operational text may contain personal data. These
risks are visible in the data card, error analysis, and security notes.

## Economics
This prototype has zero inference cost. Production cost is primarily human review
and integration. A paid model is justified only if a measured reduction in handling
time exceeds its inference and governance cost.

