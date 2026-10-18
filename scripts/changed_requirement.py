"""Measure a stricter urgent-case policy without changing the original test."""
from __future__ import annotations
import csv, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from src.triage import NaiveBayes

with (ROOT/"data"/"incidents.csv").open(encoding="utf-8") as f: rows=list(csv.DictReader(f))
model=NaiveBayes().fit(rows[:560]); test=rows[560:]
result=[]
for threshold in (0.86,0.92):
    pred=[model.predict(r["report_text"],threshold) for r in test]
    result.append({"policy":"original" if threshold==.86 else "stricter_human_review",
      "threshold":threshold,"human_review_count":sum(p["abstain"] for p in pred),
      "urgent_misses":sum(r["urgent"]=="true" and not p["urgent"] for r,p in zip(test,pred)),
      "costly_misroutes":sum(r["category"] in {"TEMPERATURE_EXCURSION","CUSTOMS_HOLD"} and not p["abstain"] and p["category"]!=r["category"] for r,p in zip(test,pred))})
(ROOT/"evaluation"/"changed_requirement.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))

