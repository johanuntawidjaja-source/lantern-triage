"""Generate a deterministic, fictional, non-confidential logistics dataset."""
from __future__ import annotations
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "incidents.csv"
random.seed(20261019)

TEMPLATES = {
"TEMPERATURE_EXCURSION": [
 "Reefer sensor shows {n} celsius above the permitted range for medicine shipment.",
 "Cold-chain alert: cargo became warm during transfer at {place}.",
 "Temperature logger failed and vaccine cartons may be spoiled.",
],
"DAMAGE": [
 "Pallet arrived crushed; {n} cartons are damaged and one is leaking.",
 "Package was wet and torn during unloading at {place}.",
 "Forklift impact broke the outer crate; contents require inspection.",
],
"DELAY": [
 "Truck is late after traffic near {place}; ETA moved by {n} hours.",
 "Shipment missed the connection and is stuck at the transfer depot.",
 "Carrier reported a delay; delivery is now expected tomorrow.",
],
"WRONG_DESTINATION": [
 "Shipment was sent to the wrong depot in {place}.",
 "Label contains an incorrect destination and parcel is misrouted.",
 "Driver reports the wrong address on the delivery instruction.",
],
"DOCUMENTATION": [
 "Commercial invoice is missing from the document pouch.",
 "Manifest number does not match the paperwork for the shipment.",
 "Delivery requires a signature but the proof-of-delivery form is blank.",
],
"CUSTOMS_HOLD": [
 "Customs placed the cargo on hold pending inspection at the border.",
 "Clearance is blocked because the duty declaration is incomplete.",
 "Border agent requested a tariff code before releasing the shipment.",
],
"OTHER": [
 "Customer asked to update the preferred delivery window.",
 "Warehouse requests confirmation of reusable container ownership.",
 "General inquiry about packaging options for a future shipment.",
]}

PLACES = ["North Hub", "Harbor Depot", "Central Yard", "Airport Warehouse", "West Gate"]
NOISE = ["", " Please advise.", " Driver has notified dispatch.", " Logged by operations."]

def main():
    rows=[]
    cats=list(TEMPLATES)
    for i in range(720):
        cat=cats[i % len(cats)]
        text=random.choice(TEMPLATES[cat]).format(n=random.randint(2,18), place=random.choice(PLACES))
        text += random.choice(NOISE)
        urgent = cat in {"TEMPERATURE_EXCURSION"} or any(x in text.lower() for x in ["leaking", "spoiled", "medicine", "vaccine"])
        rows.append({"incident_id":f"SYN-{i+1:04d}","report_text":text,
                     "category":cat,"urgent":str(urgent).lower(),"source":"synthetic_template_v1"})
    random.shuffle(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} fictional reports to {OUT}")

if __name__ == "__main__": main()

