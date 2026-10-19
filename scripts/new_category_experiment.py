"""Demonstrate response to a newly introduced CUSTOMS_HOLD category."""
from __future__ import annotations
import csv, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import src.triage as triage
from src.triage import NaiveBayes

with (ROOT/"data"/"incidents.csv").open(encoding="utf-8") as f:
    rows=list(csv.DictReader(f))
train,test=rows[:560],rows[560:]
legacy_train=[]
for row in train:
    copied=dict(row)
    if copied["category"]=="CUSTOMS_HOLD": copied["category"]="DOCUMENTATION"
    legacy_train.append(copied)

def measure(name,model):
    pred=[model.predict(r["report_text"],threshold=0.0) for r in test]
    customs=[(r,p) for r,p in zip(test,pred) if r["category"]=="CUSTOMS_HOLD"]
    return {"system":name,"test_reports":len(test),"customs_reports":len(customs),
      "customs_direct_route_recall":sum(p["category"]=="CUSTOMS_HOLD" for r,p in customs)/len(customs),
      "overall_accuracy":sum(r["category"]==p["category"] for r,p in zip(test,pred))/len(test),
      "costly_customs_misroutes":sum(p["category"]!="CUSTOMS_HOLD" for r,p in customs)}

# Reproduce the old six-queue policy without allowing the new customs vocabulary
# guard to leak into the legacy comparison.
all_keywords=triage.KEYWORDS
try:
    triage.KEYWORDS={k:v for k,v in all_keywords.items() if k!="CUSTOMS_HOLD"}
    legacy=measure("legacy_six_category",NaiveBayes().fit(legacy_train))
finally:
    triage.KEYWORDS=all_keywords
updated=measure("updated_seven_category",NaiveBayes().fit(train))
results=[legacy,updated]
(ROOT/"evaluation"/"new_category.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
print(json.dumps(results,indent=2))
