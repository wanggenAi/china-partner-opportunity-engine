import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from china_partner_engine.engine import assess, message_hash, render_contact_message, read_json


ROOT = Path(__file__).resolve().parents[1]


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.lead = read_json(ROOT / "research/examples/opportunity.example.json")
        self.profile = read_json(ROOT / "templates/founder_profile.example.json")

    def test_public_example_has_bounded_fit(self):
        result = assess(self.lead, self.profile)
        self.assertEqual(result["founder_fit_score"], 50)
        self.assertEqual(result["qualification"], "candidate_needs_confirmation")

    def test_contact_requires_exact_human_approval(self):
        template = "A continuation channel: ${TELEGRAM_CONTACT}"
        approval = {
            "approved_by": "human",
            "lead_id": self.lead["id"],
            "draft_sha256": message_hash(template),
            "expires_at": "2099-01-01T00:00:00Z",
            "context": "continuation_agreed",
        }
        rendered = render_contact_message(
            template, approval, {"TELEGRAM_CONTACT": "@example"}, self.lead,
            now=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        self.assertEqual(rendered, "A continuation channel: @example")

    def test_contact_rejects_expired_approval(self):
        template = "A continuation channel: ${TELEGRAM_CONTACT}"
        approval = {
            "approved_by": "human", "lead_id": self.lead["id"],
            "draft_sha256": message_hash(template),
            "expires_at": "2020-01-01T00:00:00Z", "context": "requested_contact",
        }
        with self.assertRaises(ValueError):
            render_contact_message(template, approval, {"TELEGRAM_CONTACT": "@example"}, self.lead)

    def test_contact_rejects_multiple_channels(self):
        template = "${WECHAT_CONTACT} or ${TELEGRAM_CONTACT}"
        approval = {
            "approved_by": "human", "lead_id": self.lead["id"],
            "draft_sha256": message_hash(template),
            "expires_at": "2099-01-01T00:00:00Z", "context": "requested_contact",
        }
        with self.assertRaises(ValueError):
            render_contact_message(template, approval, {"WECHAT_CONTACT": "x", "TELEGRAM_CONTACT": "y"}, self.lead)


if __name__ == "__main__":
    unittest.main()
