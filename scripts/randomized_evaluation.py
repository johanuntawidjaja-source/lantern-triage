"""Generate a fresh adversarial suite; use --seed for a reproducible run."""
from __future__ import annotations
import argparse, csv, json, random, secrets, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from src.triage import NaiveBayes, URGENT_TERMS

CLEAR={
"TEMPERATURE_EXCURSION":["cooling failed", "reefer is heating", "frozen load is thawing"],
"DAMAGE":["freight arrived crushed", "outer case is torn", "goods have dents"],
"DELAY":["arrival is overdue", "vehicle is running behind", "connection was missed"],
"WRONG_DESTINATION":["cargo reached the incorrect site", "parcel went to another hub", "route points elsewhere"],
"DOCUMENTATION":["invoice cannot be located", "shipping form is incomplete", "signature is missing"],
"CUSTOMS_HOLD":["border authority detained cargo", "import release is pending", "duty review blocks release"],
"OTHER":["customer asks about packaging", "change the preferred time window", "container return question"],
}
SAFETY=["driver injured after collision", "fire inside the truck", "hazardous chemical spill", "worker unconscious after crash"]
NEGATED=["no damage found after inspection", "delay was resolved safely", "no fire and no leak", "vaccine delivered safely at correct temperature"]
AMBIG=["an operational issue needs checking", "please help with this shipment", "status remains unclear", "a problem needs attention"]
CONTEXT=["at the coastal depot", "during the night shift", "after handover", "near the distribution hub"]

def legacy(model,text):
    p=model.predict(text,threshold=0.95); lower=text.lower()
    p["route"]="HUMAN_REVIEW" if p["confidence"]<.95 else p["category"]
    p["urgent"]=p["category"]=="TEMPERATURE_EXCURSION" or any(t in lower for t in URGENT_TERMS)
    return p

def build(rng):
    cases=[]
    for label,phrases in CLEAR.items():
        for _ in range(10): cases.append((f"{rng.choice(phrases)} {rng.choice(CONTEXT)}",label,label=="TEMPERATURE_EXCURSION","clear"))
    for _ in range(25): cases.append((f"{rng.choice(SAFETY)} {rng.choice(CONTEXT)}","HUMAN_REVIEW",True,"safety"))
    for _ in range(20): cases.append((f"{rng.choice(NEGATED)} {rng.choice(CONTEXT)}","HUMAN_REVIEW",False,"negated"))
    for _ in range(20): cases.append((f"{rng.choice(AMBIG)} {rng.choice(CONTEXT)}","HUMAN_REVIEW",False,"ambiguous"))
    rng.shuffle(cases); return cases

def score(name,fn,cases):
    ps=[fn(t) for t,_,_,_ in cases]
    return {"iteration":name,"reports":len(cases),
      "route_accuracy":sum(p["route"]==route for p,(_,route,_,_) in zip(ps,cases))/len(cases),
      "urgent_accuracy":sum(p["urgent"]==urgent for p,(_,_,urgent,_) in zip(ps,cases))/len(cases),
      "dangerous_direct_routes":sum(slice_ in {"safety","negated","ambiguous"} and p["route"]!="HUMAN_REVIEW" for p,(_,_,_,slice_) in zip(ps,cases)),
      "clear_correct_routes":sum(slice_=="clear" and p["route"]==route for p,(_,route,_,slice_) in zip(ps,cases))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--seed",type=int); ap.add_argument("--output")
    a=ap.parse_args(); seed=a.seed if a.seed is not None else secrets.randbelow(2**31)
    rows=list(csv.DictReader((ROOT/"data"/"incidents.csv").open(encoding="utf-8")))
    model=NaiveBayes().fit(rows[:650]); cases=build(random.Random(seed))
    result={"seed":seed,"method":"randomized compositional synthetic adversarial suite",
            "results":[score("guards_disabled_ablation",lambda t:legacy(model,t),cases),
                       score("revised_guarded_system",model.predict,cases)]}
    path=ROOT/(a.output or f"evaluation/randomized-{seed}.json"); path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result,indent=2),encoding="utf-8"); print(json.dumps(result,indent=2))
if __name__=="__main__": main()
