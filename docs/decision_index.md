<!-- # Decision Index
| # | Decision | Alternatives rejected | Evidence label (CASE/EXTERNAL/ASSUMPTION/UNKNOWN) | Owner |
|---|---|---|---|---| -->





# NyayaFlow: Decision Index (draft v1, 13 Oct 2026)

Every row is a decision the team can be asked to defend. **Origin** says where the idea came from: Team, AI-accepted, AI-modified, or Team-overrode-AI. Evidence labels: CASE / EXTERNAL / ASSUMPTION / UNKNOWN.

**Before submitting:** fill the Owner column (who will explain it in the ownership check) and correct any row that does not match what you really decided. This draft was written by an AI assistant from the chat history, so treat it as a starting point.

| # | Decision | Alternatives rejected | Why | Evidence label | Origin | Owner | Where documented |
|---|---|---|---|---|---|---|---|
| D-01 | Pick Case 07 (Governance: One Complaint, Five Departments) | AI for All case (kept as fallback) | Rubric rewards diagnosis, evidence, human ownership and testability; a routing-with-abstention layer plus audit ledger fits; a real working slice is possible on synthetic data | ASSUMPTION (our reading of the rubric) | AI-accepted | TBD | Draft doc, section 1 |
| D-02 | Treat the 23% reassignment figure as a simulated number that shows frequency, not cause | Using it as proof that misrouting is the main problem | The case figure is simulated; it says nothing about why complaints are reassigned | CASE (simulated) | AI-accepted | TBD | Draft doc, sections 1 and 5 |
| D-03 | Build a small working slice now (Engines 1 to 6) even though the AI advised waiting until after shortlisting | Waiting and producing only documents first | Team wanted real evidence (a baseline result and a demo) early; scope kept small and documents still produced | ASSUMPTION | Team-overrode-AI | TBD | AI log entry 4 |
| D-04 | Cut the 113-feature plan to a V1 of: intake extraction, multi-issue split proposal, keyword routing with abstention, ownership-overlap flags, human review, append-only ledger, challenge, evaluation | Building all 10 engines (duplicates, safety flags, status explanations, voice, hotspots, simulator) | Judges do not reward feature count; time is limited; everything else is future scope | ASSUMPTION | AI-modified | TBD | Draft doc, 6.3 and 6.6 |
| D-05 | Keyword baseline first; TF-IDF model written but not yet evaluated or wired in | Starting with an LLM or a heavy model | A simple baseline shows where AI is actually needed and keeps results honest | ASSUMPTION | AI-accepted | TBD | Draft doc, section 8 |
| D-06 | Use synthetic complaints in a Gwalior setting (96 rows: 32 families x English, Hinglish, Hindi) | Real municipal data (no access); scraping portals | No access to real complaint data; Gwalior names used only as scene-setting | ASSUMPTION | AI-accepted | TBD | DATASET_CARD.md |
| D-07 | Split train, validation and test by complaint family | Random row split | Versions of the same complaint must not appear on both sides or accuracy is inflated | ASSUMPTION | AI-accepted | TBD | DATASET_CARD.md |
| D-08 | Let the AI assistant write and re-check the labels instead of an independent teammate | Independent human labelling (AI recommended it) | Team chose to save time; the consequence is circularity risk, disclosed in the dataset card and the draft doc | ASSUMPTION | Team-overrode-AI | TBD | AI log entry 9; DATASET_CARD.md |
| D-09 | Rebalance the test set after the label audit (Drainage was 9 of 27 rows) | Keeping the original split | A skewed test set can mislead the per-department result; new test set has 6 Roads, 6 Drainage, 3 each of the others | ASSUMPTION | AI-accepted | TBD | DATASET_CARD.md |
| D-10 | Mark the whole responsibility table as ASSUMPTION | Presenting it as the Gwalior charter | Only the existence of a Gwalior grievance service was confirmed; no public department-wise charter was found | EXTERNAL (existence only) / ASSUMPTION (split) | AI-accepted | TBD | responsibility_table.csv |
| D-11 | Choose D (multi-issue split plus ownership-overlap flags) with A (routing) as the leading hypothesis; the choice is decided by real evidence under the frozen decision rule, not by the synthetic baseline score | Declaring routing the problem; using synthetic results to choose | We wrote the synthetic data ourselves, so it cannot prove which problem is real | UNKNOWN | AI-modified | TBD | Draft doc, sections 3 and 4 |
| D-12 | Freeze decision-rule thresholds before looking at evidence (20% compound, 15 minimum examples, 10% kill rule) | Setting thresholds after seeing data | Prevents choosing numbers to fit the answer; thresholds were proposed by the AI and the team edited the doc | ASSUMPTION | AI-modified | TBD | Draft doc, section 4 |
| D-13 | Ledger is append-only, enforced by database triggers; corrections add rows | Editable log; hash chain | Simple and testable; we do **not** claim cryptographic tamper-evidence | ASSUMPTION | AI-accepted | TBD | schema.sql; draft doc 6.3 |
| D-14 | Confidence threshold 0.40 is a placeholder | Claiming it is calibrated | Not tuned on a validation split yet | UNKNOWN | AI-accepted | TBD | config.py; draft doc section 8 |
| D-15 | Do not claim routing, AI classification or multilingual input is new; our claim is auditable, uncertainty-aware first touch at municipal level, stated as a hypothesis | Claiming novelty | CPGRAMS is reported to already use AI classification and routing with a multilingual voice chatbot | EXTERNAL (secondary sources) | AI-accepted | TBD | Draft doc, section 5b |
| D-16 | Real stakeholder evidence: **fill in what you actually did** (interviews held? how many? portal inspection done?) | n/a | If none, write "not available" and keep claims as ASSUMPTION | UNKNOWN until filled | Team | TBD | Draft doc, section 5 |
| D-17 | Result of the decision rule after collecting evidence: **fill in** (examples collected, how many were compound, which row applied) | n/a | Required to close the loop on D-11 | UNKNOWN until filled | Team | TBD | Draft doc, section 4 |
| D-18 | Stack: Python, Streamlit, SQLite, scikit-learn | Web framework with separate frontend | Fastest to a working demo; no frontend work | ASSUMPTION | AI-accepted | TBD | README |

## Rejected or not-adopted AI suggestions (keep at least one, with the reason)

1. **"Do not start building the app yet."** Rejected by the team (D-03). Reason: wanted a baseline result and demo as evidence; scope kept small.
2. **"Have a teammate who did not write the complaints label them."** Not followed (D-08). Reason: team preferred AI labelling to save time; risk disclosed.
3. **"Run 3 to 5 interviews and a small human-benefit pilot."** Status: fill in. If not done, say "not available".
4. **"Build all engines and 113 features."** Cut by the team to V1 scope (D-04).