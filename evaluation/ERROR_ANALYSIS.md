# Error analysis and abstention

The keyword baseline is transparent but brittle: one word can dominate, synonyms
are missed, and mixed incidents are forced into one route. The candidate combines
word features, adjacent-word features, and character 3–5-grams in a Naive Bayes
model. The subword features improve tolerance of short reports and typing errors,
but the synthetic templates still make its scores look better than production
performance will be.

The fixed robustness suite and randomized adversarial generator test short reports,
expanded documentation terms, one-character mutations, vague and benign language,
safety events, and negated/resolved incidents. A user-found failure—“Receipts have
been omitted; informed parties involved”—showed that the earlier suite was too
template-driven and that a temperature prediction incorrectly manufactured urgency.
The regression suite now includes that sentence and its misspelled variant. The two
latest 235-case random seeds separately count false urgency, unseen documentation,
temperature false positives, and dangerous direct routes. They are not evidence of
field performance.

Costly errors are counted separately for temperature and customs incidents because
misrouting them may spoil goods or miss regulatory deadlines. Low-confidence cases
abstain to human review. A stricter threshold increases review workload in exchange
for reducing forced misroutes; `changed_requirement.py` records that trade-off.

Before production: test real de-identified text, calibrate confidence, add a
multi-label path for incidents containing two problems, and monitor performance by
language and facility without recording raw report text in analytics.

