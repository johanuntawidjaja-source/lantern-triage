import unittest
from src.triage import NaiveBayes, baseline, tokens

class TriageTests(unittest.TestCase):
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

if __name__=="__main__": unittest.main()

