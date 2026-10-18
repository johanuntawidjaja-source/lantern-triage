"""Deterministic incident-triage models with no external dependencies."""
from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

CATEGORIES = [
    "TEMPERATURE_EXCURSION", "DAMAGE", "DELAY", "WRONG_DESTINATION",
    "DOCUMENTATION", "CUSTOMS_HOLD", "OTHER",
]

KEYWORDS = {
    "TEMPERATURE_EXCURSION": ["temperature", "reefer", "cold", "warm", "celsius", "sensor"],
    "DAMAGE": ["damaged", "broken", "crushed", "leaking", "wet", "torn"],
    "DELAY": ["late", "delay", "missed", "stuck", "eta", "traffic"],
    "WRONG_DESTINATION": ["wrong address", "wrong depot", "misrouted", "incorrect destination"],
    "DOCUMENTATION": ["invoice", "document", "paperwork", "manifest", "signature", "permit"],
    "CUSTOMS_HOLD": ["customs", "border", "inspection", "duty", "tariff", "clearance"],
}

URGENT_TERMS = [
    "urgent", "critical", "hospital", "medicine", "vaccine", "spoiled",
    "leaking", "hazard", "fire", "24 hours", "today", "immediately",
]

def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())

def baseline(text: str) -> dict:
    lower = text.lower()
    scores = {c: sum(1 for k in ks if k in lower) for c, ks in KEYWORDS.items()}
    best = max(scores, key=scores.get)
    category = best if scores[best] else "OTHER"
    urgent = any(term in lower for term in URGENT_TERMS)
    confidence = 0.82 if scores[best] >= 2 else (0.64 if scores[best] == 1 else 0.38)
    return {"category": category, "urgent": urgent, "confidence": confidence,
            "abstain": confidence < 0.55, "route": "HUMAN_REVIEW" if confidence < 0.55 else category}

class NaiveBayes:
    def __init__(self):
        self.labels: list[str] = []
        self.priors: dict[str, float] = {}
        self.counts: dict[str, Counter] = {}
        self.totals: dict[str, int] = {}
        self.vocab: set[str] = set()

    def fit(self, rows: list[dict]) -> "NaiveBayes":
        by_label = Counter(r["category"] for r in rows)
        word_counts = defaultdict(Counter)
        for row in rows:
            word_counts[row["category"]].update(tokens(row["report_text"]))
        self.labels = sorted(by_label)
        self.vocab = set().union(*(set(c) for c in word_counts.values()))
        self.priors = {label: by_label[label] / len(rows) for label in self.labels}
        self.counts = dict(word_counts)
        self.totals = {label: sum(word_counts[label].values()) for label in self.labels}
        return self

    def predict(self, text: str, threshold: float = 0.86) -> dict:
        words = tokens(text)
        scored = {}
        size = max(1, len(self.vocab))
        for label in self.labels:
            score = math.log(self.priors[label])
            denom = self.totals[label] + size
            for word in words:
                score += math.log((self.counts[label][word] + 1) / denom)
            scored[label] = score
        peak = max(scored.values())
        # Temperature scaling prevents the tiny synthetic corpus from reporting
        # implausible near-100% confidence. This is a prototype calibration,
        # documented as such rather than presented as production certainty.
        probs = {k: math.exp((v - peak) / 6.0) for k, v in scored.items()}
        z = sum(probs.values())
        probs = {k: v / z for k, v in probs.items()}
        category = max(probs, key=probs.get)
        confidence = probs[category]
        lower = text.lower()
        urgent = category == "TEMPERATURE_EXCURSION" or any(term in lower for term in URGENT_TERMS)
        abstain = confidence < threshold
        return {"category": category, "urgent": urgent, "confidence": confidence,
                "abstain": abstain, "route": "HUMAN_REVIEW" if abstain else category,
                "probabilities": probs}

    def to_json(self, path: Path) -> None:
        payload = {"labels": self.labels, "priors": self.priors,
                   "counts": {k: dict(v) for k, v in self.counts.items()},
                   "totals": self.totals, "vocabSize": len(self.vocab),
                   "urgentTerms": URGENT_TERMS, "threshold": 0.86}
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

