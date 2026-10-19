"""Evaluate short, synonymous, misspelled, and intentionally ambiguous reports."""
from __future__ import annotations
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.triage import NaiveBayes

CASES = {
 "TEMPERATURE_EXCURSION": ["reefer heating up", "chill was lost", "frzen cargo getting soft", "refrigeration fault", "thermal reading excessive"],
 "DAMAGE": ["freight was damaged", "merchandise got crushed", "pakage brokn on arrival", "visible dents on goods", "wrapping has ripped"],
 "DELAY": ["delivery is overdue", "truck running behind", "shipmnt has been delyed", "arrival estimate slipped", "cargo still has not arrived"],
 "WRONG_DESTINATION": ["sent to an unintended place", "parcel reached an incorrect hub", "shipmnt badly misrouted", "incorrect delivery site", "cargo went elsewhere"],
 "DOCUMENTATION": ["invoice cannot be found", "shipping docs are incomplete", "manfest contains typo", "receiver signature absent", "incorrect paperwork reference"],
 "CUSTOMS_HOLD": ["customs will not release it", "border release was refused", "clerance still pending", "unpaid duty blocks cargo", "import declaration rejected"],
 "OTHER": ["question about packing", "customer requests a call", "change requested time slot", "query on returning container", "contact preference update"],
}
AMBIGUOUS = [
 "something went wrong", "shipment issue", "please investigate", "problem at hub",
 "cargo needs attention", "status unclear", "operator requested help",
]

def main():
    with (ROOT / "data" / "incidents.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    model = NaiveBayes().fit(rows[:650])
    detailed = []
    for label, texts in CASES.items():
        for text in texts:
            p = model.predict(text)
            detailed.append({"text": text, "expected": label, "route": p["route"],
                             "confidence": round(p["confidence"], 6), "correct": p["route"] == label})
    ambiguous = []
    for text in AMBIGUOUS:
        p = model.predict(text)
        ambiguous.append({"text": text, "route": p["route"],
                          "confidence": round(p["confidence"], 6), "abstained": p["abstain"]})
    result = {
        "named_challenge_cases": len(detailed),
        "correct_direct_routes": sum(r["correct"] for r in detailed),
        "safe_abstentions": sum(r["route"] == "HUMAN_REVIEW" for r in detailed),
        "misroutes": sum(r["route"] not in {r["expected"], "HUMAN_REVIEW"} for r in detailed),
        "direct_route_accuracy": sum(r["correct"] for r in detailed) / len(detailed),
        "ambiguous_cases": len(ambiguous),
        "ambiguous_abstentions": sum(r["abstained"] for r in ambiguous),
        "cases": detailed,
        "ambiguous": ambiguous,
    }
    (ROOT / "evaluation" / "robustness.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k not in {"cases","ambiguous"}}, indent=2))

if __name__ == "__main__": main()
