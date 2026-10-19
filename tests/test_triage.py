import csv, unittest
from src.triage import NaiveBayes, baseline, tokens

class TriageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("data/incidents.csv",encoding="utf-8") as f: rows=list(csv.DictReader(f))
        cls.model=NaiveBayes().fit(rows[:650]); cls.rows=rows
    def test_customs(self): self.assertEqual(baseline("customs inspection at border")["category"],"CUSTOMS_HOLD")
    def test_urgent(self): self.assertTrue(baseline("urgent leaking pallet")["urgent"])
    def test_abstains_on_unknown(self): self.assertTrue(baseline("please call me")["abstain"])
    def test_no_sensitive_output(self):
        p=baseline("driver email person@example.test says delay")
        self.assertNotIn("example",str(p))
    def test_subword_features_cover_typo(self):
        self.assertIn("c:dam", tokens("damagd"))
    def test_short_damage_report(self):
        rows=[{"category":"DAMAGE","report_text":"shipment damaged"} for _ in range(5)] + \
             [{"category":"DELAY","report_text":"truck delayed"} for _ in range(5)]
        self.assertEqual(NaiveBayes().fit(rows).predict("shipmnt damagd", threshold=0.0)["category"], "DAMAGE")
    def test_safety_event_escalates(self):
        p=self.model.predict("driver injured and unconscious after crash")
        self.assertEqual(p["route"],"HUMAN_REVIEW"); self.assertTrue(p["urgent"])
    def test_negated_hazard_not_urgent(self):
        p=self.model.predict("not urgent, no leak and no fire")
        self.assertEqual(p["route"],"HUMAN_REVIEW"); self.assertFalse(p["urgent"])
    def test_template_families_do_not_cross_split(self):
        train={r["report_text"] for r in self.rows[:650]}
        self.assertFalse(any(r["report_text"] in train for r in self.rows[650:]))
    def test_multi_issue_forces_review(self):
        self.assertEqual(self.model.predict("wrong address and medicine is warm")["route"],"HUMAN_REVIEW")
    def test_active_issue_after_resolved_clause_is_urgent(self):
        p=self.model.predict("customs issue resolved but reefer is heating up")
        self.assertEqual(p["route"],"HUMAN_REVIEW"); self.assertTrue(p["urgent"])
    def test_unsupported_language_marks_unknown(self):
        p=self.model.predict("清关延误，疫苗正在变热")
        self.assertTrue(p["urgency_unknown"]); self.assertEqual(p["route"],"HUMAN_REVIEW")

if __name__=="__main__": unittest.main()

