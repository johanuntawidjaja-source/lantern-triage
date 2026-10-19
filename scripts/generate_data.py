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
 "Reefer too warm.", "Cold chain broken.", "Tempature alarm on chilled cargo.",
 "Frozen goods are thawing at {place}.", "Cooling unit failed overnight.",
],
"DAMAGE": [
 "Pallet arrived crushed; {n} cartons are damaged and one is leaking.",
 "Package was wet and torn during unloading at {place}.",
 "Forklift impact broke the outer crate; contents require inspection.",
 "Shipment damaged.", "Box smashed in transit.", "Damagd parcel received.",
 "Goods arrived dented at {place}.", "Carton ripped open.",
],
"DELAY": [
 "Truck is late after traffic near {place}; ETA moved by {n} hours.",
 "Shipment missed the connection and is stuck at the transfer depot.",
 "Carrier reported a delay; delivery is now expected tomorrow.",
 "Delivery late.", "Truck overdue.", "Shipmnt delyed by {n} hours.",
 "Consignment has not arrived.", "ETA slipped again at {place}.",
],
"WRONG_DESTINATION": [
 "Shipment was sent to the wrong depot in {place}.",
 "Label contains an incorrect destination and parcel is misrouted.",
 "Driver reports the wrong address on the delivery instruction.",
 "Sent to wrong place.", "Parcel at incorrect hub.", "Misrouted shipmnt.",
 "Delivered to another warehouse.", "Destination label is wrong.",
],
"DOCUMENTATION": [
 "Commercial invoice is missing from the document pouch.",
 "Manifest number does not match the paperwork for the shipment.",
 "Delivery requires a signature but the proof-of-delivery form is blank.",
 "Invoice missing.", "Docs incomplete.", "Manfest error blocks dispatch.",
 "No signed delivery note.", "Paperwork has the wrong reference.",
],
"CUSTOMS_HOLD": [
 "Customs placed the cargo on hold pending inspection at the border.",
 "Clearance is blocked because the duty declaration is incomplete.",
 "Border agent requested a tariff code before releasing the shipment.",
 "Held at customs.", "Border release refused.", "Customs clerance pending.",
 "Cargo detained for duty review.", "Import entry rejected.",
],
"OTHER": [
 "Customer asked to update the preferred delivery window.",
 "Warehouse requests confirmation of reusable container ownership.",
 "General inquiry about packaging options for a future shipment.",
 "Please call customer.", "Change delivery window.", "Packaging question.",
 "Update contact preference.", "Container return query.",
]}

PLACES = ["North Hub", "Harbor Depot", "Central Yard", "Airport Warehouse", "West Gate"]
TRAIN_CONTEXT = ["Logged at {place} during shift {n}.", "Operations at {place} opened case {n}.", "Dispatch recorded this at {place}, sequence {n}."]
TEST_CONTEXT = ["Record {n} was filed from {place}.", "Entry {n} was logged at {place}."]

def main():
    rows=[]; cats=list(TEMPLATES); per_cat={c:0 for c in cats}
    for i in range(840):
        cat=cats[i % len(cats)]; j=per_cat[cat]; per_cat[cat]+=1
        split="train" if i < 650 else "test"
        family=TEMPLATES[cat][:5] if split=="train" else TEMPLATES[cat][5:]
        place=PLACES[(j*3+i) % len(PLACES)]; n=(j % 97)+2
        base=family[j % len(family)].format(n=n, place=place)
        context=(TRAIN_CONTEXT if split=="train" else TEST_CONTEXT)[j % (3 if split=="train" else 2)]
        text=f"{base} {context.format(n=j+1,place=place)}"
        urgent = cat in {"TEMPERATURE_EXCURSION"} or any(x in text.lower() for x in ["leaking", "spoiled", "medicine", "vaccine"])
        rows.append({"incident_id":f"SYN-{i+1:04d}","report_text":text,
                     "category":cat,"urgent":str(urgent).lower(),
                     "source":f"synthetic_{split}_template_family_v3","split":split})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} fictional reports to {OUT}")

if __name__ == "__main__": main()

