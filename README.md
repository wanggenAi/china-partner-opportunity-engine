# China Partner Opportunity Engine

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
