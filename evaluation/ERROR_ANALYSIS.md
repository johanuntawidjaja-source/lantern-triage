# Error analysis and abstention

The keyword baseline is transparent but brittle: one word can dominate, synonyms
are missed, and mixed incidents are forced into one route. The Naive Bayes model
uses all observed words and estimates confidence, but the synthetic templates make
its scores look better than production performance will be.

Costly errors are counted separately for temperature and customs incidents because
misrouting them may spoil goods or miss regulatory deadlines. Low-confidence cases
abstain to human review. A stricter threshold increases review workload in exchange
for reducing forced misroutes; `changed_requirement.py` records that trade-off.

Before production: test real de-identified text, calibrate confidence, add a
multi-label path for incidents containing two problems, and monitor performance by
language and facility without recording raw report text in analytics.

