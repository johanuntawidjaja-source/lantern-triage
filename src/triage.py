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
    "DOCUMENTATION": ["invoice", "document", "paperwork", "manifest", "manfest", "signature", "permit"],
    "CUSTOMS_HOLD": ["customs", "border", "inspection", "duty", "tariff", "clearance", "import", "export", "detained"],
}

URGENT_TERMS = [
    "urgent", "critical", "hospital", "medicine", "vaccine", "spoiled",
    "leaking", "hazard", "fire", "24 hours", "today", "immediately",
    "frozen", "thawing", "chiller", "cooling", "reefer",
]
SAFETY_TERMS = ["injured", "injury", "unconscious", "crash", "collision", "fire",
                "spill", "hazardous", "hazmat", "toxic", "theft", "stolen"]
GENERIC_TERMS = ["issue", "problem", "investigate", "attention", "unclear", "help", "wrong"]
NEGATION_TERMS = ["no", "not", "without", "resolved", "cleared", "safe", "safely"]

def unnegated(text: str, term: str) -> bool:
    words=re.findall(r"[a-z0-9]+",text); needle=term.split()
    for i in range(len(words)-len(needle)+1):
        if words[i:i+len(needle)]==needle:
            before=words[max(0,i-4):i]
            if "but" in before: before=before[before.index("but")+1:]
            if not any(w in NEGATION_TERMS for w in before): return True
    return False

def tokens(text: str) -> list[str]:
    """Return word, word-bigram, and character-subword features."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    features = list(words)
    features.extend(f"w2:{a}_{b}" for a, b in zip(words, words[1:]))
    for word in words:
        padded = f"^{word}$"
        for n in (3, 4, 5):
            features.extend(f"c:{padded[i:i+n]}" for i in range(len(padded)-n+1))
    return features

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

    def predict(self, text: str, threshold: float = 0.95) -> dict:
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
        # Modest temperature scaling avoids presenting raw synthetic-corpus scores
        # as certainty while retaining useful separation on short reports.
        probs = {k: math.exp((v - peak) / 4.0) for k, v in scored.items()}
        z = sum(probs.values())
        probs = {k: v / z for k, v in probs.items()}
        category = max(probs, key=probs.get)
        confidence = probs[category]
        lower = text.lower()
        safety = any(unnegated(lower, term) for term in SAFETY_TERMS)
        negated_or_resolved = any(term in lower.split() for term in NEGATION_TERMS)
        generic_only = any(term in lower.split() for term in GENERIC_TERMS) and not any(
            anchor in lower for phrases in KEYWORDS.values() for anchor in phrases
        )
        anchor_labels={label for label,anchors in KEYWORDS.items() if any(a in lower for a in anchors)}
        conflicting = bool(anchor_labels) and category not in anchor_labels
        multi_issue = len(anchor_labels) > 1
        unsupported = not bool(re.search(r"[a-z]", lower))
        urgent = safety or any(unnegated(lower, term) for term in URGENT_TERMS) or \
                 (category == "TEMPERATURE_EXCURSION" and not conflicting and not negated_or_resolved)
        abstain = confidence < threshold or generic_only or safety or negated_or_resolved or conflicting or multi_issue or unsupported
        reason = ("safety_escalation" if safety else "negated_or_resolved" if negated_or_resolved
                  else "unsupported_language" if unsupported else "multi_issue" if multi_issue
                  else "conflicting_signals" if conflicting
                  else "ambiguous_language" if generic_only else
                  "low_confidence" if confidence < threshold else None)
        return {"category": category, "urgent": urgent, "confidence": confidence,
                "abstain": abstain, "route": "HUMAN_REVIEW" if abstain else category,
                "abstain_reason": reason, "urgency_unknown": unsupported,
                "probabilities": probs}

    def to_json(self, path: Path) -> None:
        payload = {"labels": self.labels, "priors": self.priors,
                   "counts": {k: dict(v) for k, v in self.counts.items()},
                   "totals": self.totals, "vocabSize": len(self.vocab),
                   "urgentTerms": URGENT_TERMS, "threshold": 0.95,
                   "safetyTerms": SAFETY_TERMS, "genericTerms": GENERIC_TERMS,
                   "negationTerms": NEGATION_TERMS,
                   "categoryAnchors": [a for phrases in KEYWORDS.values() for a in phrases],
                   "keywordMap": KEYWORDS,
                   "temperature": 4.0,
                   "featureVersion": "word-char-ngram-v2"}
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

