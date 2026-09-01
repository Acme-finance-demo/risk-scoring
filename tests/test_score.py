import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from risk_scoring import load_rules, score


class ScoreTest(unittest.TestCase):
    def setUp(self):
        self.rules = load_rules()

    def test_small_transaction_is_approved(self):
        decision = score({"amount": 1000, "country": "JP"}, self.rules)
        self.assertEqual(decision.outcome, "approve")
        self.assertEqual(decision.score, 0)

    def test_over_the_limit_goes_to_review(self):
        decision = score({"amount": 900000, "country": "JP"}, self.rules)
        self.assertEqual(decision.outcome, "review")
        self.assertIn("amount_over_limit", decision.reasons)

    def test_watchlist_and_limit_together_block(self):
        decision = score(
            {"amount": 900000, "country": "zz", "new_beneficiary": True},
            self.rules,
            watchlist={"ZZ"},
        )
        self.assertEqual(decision.outcome, "block")
        self.assertEqual(decision.score, 95)

    def test_rules_come_from_yaml(self):
        self.assertEqual(self.rules.limits["amount"], 500000)
        self.assertEqual(self.rules.thresholds["block"], 70)


if __name__ == "__main__":
    unittest.main()
