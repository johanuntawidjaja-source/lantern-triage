"""Train/evaluate two approaches and save reproducible metrics."""
from __future__ import annotations
import csv, json, statistics, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.triage import NaiveBayes, baseline

def load():
    with (ROOT/"data"/"incidents.csv").open(encoding="utf-8") as f: return list(csv.DictReader(f))

def score(name, fn, test):
    times=[]; preds=[]
    for r in test:
        t=time.perf_counter(); p=fn(r["report_text"]); times.append((time.perf_counter()-t)*1000); preds.append(p)
    decided=[(r,p) for r,p in zip(test,preds) if not p["abstain"]]
    correct=sum(r["category"]==p["category"] for r,p in decided)
    urgent_missed=sum(r["urgent"]=="true" and not p["urgent"] for r,p in zip(test,preds))
    costly=sum(r["category"] in {"TEMPERATURE_EXCURSION","CUSTOMS_HOLD"} and
               not p["abstain"] and p["category"]!=r["category"] for r,p in zip(test,preds))
    return {"approach":name,"test_reports":len(test),"coverage":len(decided)/len(test),
      "accuracy_when_decided":correct/max(1,len(decided)),"abstentions":len(test)-len(decided),
      "urgent_misses":urgent_missed,"costly_misroutes":costly,
      "p50_latency_ms":statistics.median(times),"estimated_cost_usd_per_1000":0.0}

def main():
    rows=load(); train=rows[:560]; test=rows[560:]
    model=NaiveBayes().fit(train)
    results=[score("keyword_baseline", baseline, test), score("naive_bayes_with_abstention", model.predict, test)]
    out=ROOT/"evaluation"; out.mkdir(exist_ok=True)
    results_json=json.dumps(results,indent=2)
    (out/"results.json").write_text(results_json,encoding="utf-8")
    web_eval=ROOT/"web"/"evaluation"; web_eval.mkdir(parents=True,exist_ok=True)
    (web_eval/"results.json").write_text(results_json,encoding="utf-8")
    with (out/"results.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=results[0].keys()); w.writeheader(); w.writerows(results)
    model.to_json(ROOT/"web"/"model.json")
    print(json.dumps(results,indent=2))

if __name__=="__main__": main()

