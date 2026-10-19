"""Verify decisions against the immutable texts actually shown to the reviewer."""
from __future__ import annotations
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/"data"/"human_review_items.csv").open(encoding="utf-8") as f:
    truth={r["incident_id"]:r for r in csv.DictReader(f)}
with (ROOT/"data"/"human_review.csv").open(encoding="utf-8") as f:
    reviews=list(csv.DictReader(f))
if len(reviews)<50: raise SystemExit(f"need at least 50 reviews; found {len(reviews)}")
seen=set(); disagreements=[]
for row in reviews:
    iid=row["incident_id"]
    if iid in seen: raise SystemExit(f"duplicate review: {iid}")
    if iid not in truth: raise SystemExit(f"unknown incident: {iid}")
    seen.add(iid)
    if row["reviewed_label"] != truth[iid]["reference_label"] or row["reviewed_label"] != truth[iid]["reviewed_label"]:
        disagreements.append({"incident_id":iid,"reference":truth[iid]["reference_label"],"reviewed":row["reviewed_label"]})
result={"reviewed":len(reviews),"agreements":len(reviews)-len(disagreements),
        "agreement_rate":(len(reviews)-len(disagreements))/len(reviews),
        "disagreements":disagreements,"method":"blinded_chat_review_immutable_items"}
(ROOT/"evaluation"/"human_review_results.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
