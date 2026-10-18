# Independent label review

The repository owner classified 50 randomly selected synthetic reports without
seeing their generated labels or model predictions. Decisions were collected in
five planned batches through chat: 10, 10, and a final 30. The labels were saved to
`data/human_review.csv` before comparison with `data/incidents.csv`.

All 50 decisions agreed with the generated reference labels. This supports internal
consistency of the clear template examples, but it does **not** establish real-world
validity. The reports are deliberately simpler than production messages. A field
pilot should repeat blinded adjudication with de-identified operational text and at
least two logistics specialists, measuring inter-rater agreement and resolving
ambiguous or multi-label cases.
