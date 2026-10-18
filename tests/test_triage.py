import unittest
from src.triage import baseline

class TriageTests(unittest.TestCase):
    def test_customs(self): self.assertEqual(baseline("customs inspection at border")["category"],"CUSTOMS_HOLD")
    def test_urgent(self): self.assertTrue(baseline("urgent leaking pallet")["urgent"])
    def test_abstains_on_unknown(self): self.assertTrue(baseline("please call me")["abstain"])
    def test_no_sensitive_output(self):
        p=baseline("driver email person@example.test says delay")
        self.assertNotIn("example",str(p))

if __name__=="__main__": unittest.main()

