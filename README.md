# China Partner Opportunity Engine

## Single-repository focus — Reddit-first overseas customer acquisition (2026-10-26)

**This repository is the only active operating home for this business.** Do not create another repository, duplicate CRM, dashboard, or competing opportunity radar. The immediate objective is **more real conversations with overseas buyers, then paid transactions and repeat customers**—not more crawlers, commits, or abstract opportunity scores.

- **Primary acquisition channel:** Reddit. Start with original, buyer-authored requests for help with China sourcing, supplier comparison, small-batch/custom products, QC/sample coordination, Chinese platforms and China-side execution. Other channels are optional only when demonstrated useful.
- **One workflow:** discover public demand → verify the original post, freshness and contact rules → deduplicate by author/request → check service fit → prepare a short individualized helpful reply → human-approved contact on a permitted channel → record actual delivery/response → qualify scope/destination/deadline → human-approved quote → paid delivery → follow-up/repeat.
- **One private source of truth:** local ignored `private/` contains original post links, real contacts, conversation evidence, quote and delivery records. Public repository contains only source code, synthetic templates, aggregate metrics and privacy-safe recovery notes. Never publish names, phone numbers, handles linked to private chats, or screenshots.
- **One useful daily output:** a concise, locally generated `private/reports/TODAY.md` with new qualified opportunities, contacts awaiting a reply, interested conversations needing action, quotes/deliveries and real funnel totals. Zero qualified leads is valid; access failures must be visible.
- **Only real metrics:** verified first contacts, actual replies, qualified needs, quotes sent, paid tasks, realized revenue, gross margin and repeat customers. Never infer conversion or revenue from a drafted message or a public Reddit comment.
- **Acquisition constraints:** no blanket outreach, bulk unsolicited DMs, karma bypass, CAPTCHA/rate-limit evasion, or unapproved off-platform contact. If automated Reddit access is blocked or unauthorized, keep a manual/browser-assisted evidence intake path rather than fabricate fresh scans.
- **One-person constraint:** prioritize small, bounded paid trials, reusable supplier-check and sourcing workflows, and repeat relationships. Avoid buying stock, paying third-party costs, or promising factories/logistics/inspection capacity without authorization and proof.

The general demand radar (`wanggenAi/demand-opportunity-engine`) and broad opportunity research (`wanggenAi/opportunity-routing-engine`) are **historical reference repositories**, not places to resume day-to-day execution. Reuse proven, relevant ideas here only when they materially improve real Reddit-to-revenue outcomes. Do not destroy their historical data. Any old scheduled jobs should be retired only after verifying that they are no longer needed.

See `TASK_STATE.md` for the historical outreach baseline and `AGENTS.md` for privacy and execution rules.

Discover overseas people and businesses with a real China-related problem, identify a small task the founder can realistically deliver, and build trust through useful, verifiable work.

The first release is a local Python workflow for evidence capture, lead validation, transparent founder fit, and human-reviewed reply preparation. It does not scrape accounts, send messages, quote clients, spend money or perform offline actions.

## Start

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e .
cp .env.example .env.local
mkdir -p private
cp templates/founder_profile.example.json private/founder_profile.local.json
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/china-partner validate research/examples/opportunity.example.json
.venv/bin/china-partner assess research/examples/opportunity.example.json
.venv/bin/china-partner report research/examples/opportunity.example.json --output private/reports/example.md
```

Fill the private profile with truthful facts. The initialized working checkout already has founder-supplied background and the first research batch under `private/`; a fresh clone does not contain them. Never overwrite those local files with the examples.

## Workflow

1. Read original public demand; record author, original date, access time, facts and unknowns.
2. Assess the smallest deliverable against actual capabilities; mark missing credentials and evidence.
3. Recheck whether the request is still active and whether the platform allows contact.
4. Write one natural, specific reply: show understanding, offer a useful observation, suggest a small next step.
5. Obtain human approval for the exact outbound message and any quote. Record real outcomes with evidence.
6. Deliver what was agreed; explore repeat support only when the client needs it.

Fit is a transparent heuristic for a bounded task, not a probability of sale. An unconfirmed need stays a candidate. No milestone is claimed from draft messages.

## Repository boundaries

Public: source, schemas, templates, rules, synthetic examples and anonymous recovery state.
Local only: complete founder profile, actual contacts, real lead cards, raw evidence, drafts, approvals and client activity.

See `docs/ARCHITECTURE.md`, `docs/TRUST_MODEL.md`, `docs/OUTREACH_PRINCIPLES.md` and `TASK_STATE.md`. Before committing, run `.venv/bin/python scripts/check_public.py`. The only official repository is `wanggenAi/china-partner-opportunity-engine`, branch `main`.
