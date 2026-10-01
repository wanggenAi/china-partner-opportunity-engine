"""Transparent fit assessment and contextual message preparation."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from string import Template
from typing import Optional, Union

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
STRENGTH_WEIGHTS = {
    "problem_solving": 15, "research": 20, "local_execution": 20,
    "communication": 15, "ownership": 15, "honesty": 15,
}
CONTACTS = {"WECHAT_CONTACT", "TELEGRAM_CONTACT", "MOBILE_CONTACT"}
CONTACT_CONTEXTS = {"requested_contact", "continuation_agreed", "initial_trust_established"}


def read_json(path: Union[str, Path]) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate(data: dict, schema_name: str) -> None:
    schema = read_json(ROOT / schema_name)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(data)


def assess(lead: dict, profile: dict) -> dict:
    """Fit measures support for a bounded task, never purchase intent or expertise."""
    validate(lead, "schemas/opportunity.schema.json")
    validate(profile, "profiles/founder_profile.schema.json")
    supported = set(profile["strengths"])
    matched = [s for s in lead["relevant_founder_strengths"] if s in supported]
    raw_score = sum(STRENGTH_WEIGHTS.get(s, 0) for s in set(matched))
    reasons = []
    if not lead["first_small_task"]:
        reasons.append("A bounded deliverable is missing")
    unavailable = set(lead["required_credentials"]) - set(profile["credentials"])
    if unavailable:
        reasons.append("Required credentials are not established")
    qualified = (lead["overseas_status"] == "confirmed"
                 and lead["current_need_status"] == "confirmed_active"
                 and lead["contact_permission"] == "verified_allowed"
                 and not reasons and raw_score >= 60)
    status = "qualified" if qualified else "candidate_needs_confirmation"
    if unavailable or lead["disposition"] in {"hold", "reject"}:
        status = "hold"
    return {
        "founder_fit_score": min(raw_score, 40) if unavailable else raw_score,
        "score_method": "weighted support for the first task, v1; human hypotheses, not a probability",
        "matched_strengths": matched,
        "qualification": status,
        "blockers": reasons,
        "unconfirmed": [k for k, target in {
            "overseas_status": "confirmed", "current_need_status": "confirmed_active",
            "contact_permission": "verified_allowed"}.items() if lead[k] != target],
    }


def message_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render_contact_message(template: str, approval: dict, env: dict,
                           lead: dict, now: Optional[datetime] = None) -> str:
    """Resolve one contact only for the exact human-approved continuation draft."""
    now = now or datetime.now(timezone.utc)
    if (approval.get("approved_by") != "human"
            or approval.get("lead_id") != lead["id"]
            or approval.get("draft_sha256") != message_hash(template)):
        raise ValueError("Exact draft requires human approval for this lead")
    expires = datetime.fromisoformat(approval["expires_at"].replace("Z", "+00:00"))
    if expires.tzinfo is None or expires <= now:
        raise ValueError("Approval expired or missing timezone")
    if approval.get("context") not in CONTACT_CONTEXTS:
        raise ValueError("Contacts require a suitable continuation context")
    if lead["contact_permission"] != "verified_allowed":
        raise ValueError("Platform permission must be verified")
    keys = [m["named"] or m["braced"] for m in Template.pattern.finditer(template)
            if m["named"] or m["braced"]]
    if len(keys) != 1 or keys[0] not in CONTACTS:
        raise ValueError("Use exactly one approved contact placeholder")
    value = env.get(keys[0], "").strip()
    if not value or value.startswith("${"):
        raise ValueError("Contact value is not configured")
    return Template(template).substitute({keys[0]: value})


def read_env(path: str | Path) -> dict:
    """Read literal values only: never execute shell code from a local file."""
    values = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.lstrip().startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            if key.strip() in CONTACTS:
                values[key.strip()] = value.strip().strip("\"'")
    return values


def lead_report(lead: dict, profile: dict) -> str:
    fit = assess(lead, profile)
    source = lead["source"]
    parts = [f"# {lead['title']}",
             f"Source: {source['url']}\nAuthor: {source['author']}\nPublished: {source['published_at']}",
             f"Fit: {fit['founder_fit_score']}/100. Status: {fit['qualification']}.",
             lead["need_summary"], lead["china_dependency"],
             f"Why you: {lead['why_me_for_this_lead']}",
             f"Keep out of the introduction: {'; '.join(lead['do_not_mention'])}",
             f"First task: {lead['first_small_task']}",
             f"Risk and proof: {'; '.join(lead['trust_barriers'] + lead['proof_needed'])}",
             "Suggested reply (draft, not sent):\n\n" + lead["first_reply"],
             f"If they reply: {lead['reply_plan']}",
             f"Contact channel: {lead['recommended_contact_channel']}",
             f"WeChat: {lead['when_to_offer_wechat']}\nTelegram: {lead['when_to_offer_telegram']}",
             f"Pricing hypothesis, approval required: {lead['pricing_model']}",
             f"Expansion, only if needed: {' → '.join(lead['relationship_expansion_path'])}",
             f"Freshness: {lead['freshness_assessment']}",
             f"Before outreach: {'; '.join(lead['next_checks'])}"]
    return "\n\n".join(parts) + "\n"
