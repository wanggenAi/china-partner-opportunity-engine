# Source architecture

`src/china_partner_engine/engine.py` validates input, matches supported strengths, checks credential gaps, prepares a report and resolves a single approved contact. `cli.py` provides local commands. JSON Schema contracts cover leads, evidence and the private founder profile.

Evidence is acquired manually from public originals. There is no autonomous collector, live inbox, payment integration or sending adapter in v0.1. This avoids claiming those workflows exist. Research can use ordinary public fetches, with Chrome for pages that need rendering; logins remain a human step.

Data flow: source → local evidence → local lead card → founder fit → freshness/platform recheck → reply review → approved action → verified outcome.

The lead card stores the facts needed to answer who needs help, why China matters, why this founder fits, what to omit, client concerns, useful advice, trial scope, response plan, channel timing, pricing hypothesis and expansion path. Local evidence IDs trace those claims back to originals.

Fit weights: research 20, local execution 20, problem solving 15, communication 15, ownership 15, honesty 15. Scores describe a narrow task using human-selected relevant strengths. Missing mandatory credentials cap fit at 40 and hold the lead. A lead qualifies only with confirmed overseas status, confirmed current need, verified contact permission, a bounded task and fit ≥60. Financial and broader delivery risks still require human review.

All real intelligence stays under ignored `private/`. Git safeguards scan staged/public tracked files against configured private contacts and reject private paths. They supplement explicit staging and review; they are not a universal secret detector.
