# Error analysis and abstention

The keyword baseline is transparent but brittle: one word can dominate, synonyms
are missed, and mixed incidents are forced into one route. The candidate combines
word features, adjacent-word features, and character 3–5-grams in a Naive Bayes
model. The subword features improve tolerance of short reports and typing errors,
but the synthetic templates still make its scores look better than production
performance will be.

The separate robustness suite directly routes 29 of 35 clear short/synonym/typo
cases correctly; the remaining six abstain rather than misroute. All seven
deliberately vague cases go to human review. These cases were created as an explicit
challenge set and are not evidence of field performance.

Costly errors are counted separately for temperature and customs incidents because
misrouting them may spoil goods or miss regulatory deadlines. Low-confidence cases
abstain to human review. A stricter threshold increases review workload in exchange
for reducing forced misroutes; `changed_requirement.py` records that trade-off.

Before production: test real de-identified text, calibrate confidence, add a
multi-label path for incidents containing two problems, and monitor performance by
language and facility without recording raw report text in analytics.

