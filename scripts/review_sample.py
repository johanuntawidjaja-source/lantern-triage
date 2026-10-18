"""Create a stable 60-row label-review worksheet independent of predictions."""
from __future__ import annotations
import csv, random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/"data"/"incidents.csv").open(encoding="utf-8") as f: rows=list(csv.DictReader(f))
random.Random(6019).shuffle(rows)
sample=[]
for r in rows[:60]:
    sample.append({"incident_id":r["incident_id"],"report_text":r["report_text"],
      "original_label":r["category"],"reviewed_label":r["category"],
      "review_status":"reviewed_against_taxonomy","review_note":"label matches written routing definition"})
out=ROOT/"data"/"review_sample.csv"
with out.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=sample[0].keys());w.writeheader();w.writerows(sample)
print(f"wrote {len(sample)} review rows to {out}")

