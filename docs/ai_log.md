<!-- # AI Log (keep updating from day 1)
| Date | Tool | Prompt / link | Output summary | Accepted / Changed / Rejected | Verification | Reason |
|---|---|---|---|---|---|---|
| 2026-10-13 | Claude | 'Create Gwalior-setting synthetic dataset and review the labels yourself' | 96 complaints, responsibility table, keywords, 2nd-pass label audit; rebalanced test split (Drainage was 9/27) | Accepted | Structural checks run in Python; semantic labels NOT human-verified | Team chose to rely on AI labelling; disclosed in dataset card | -->







# NyayaFlow: AI Log (draft v1, 13 Oct 2026)

Tool used throughout: Claude (Anthropic), via claude.ai. Prompts below are **paraphrased** from the chat; keep the original chat export or link as the raw record.

**Before submitting:** this log was reconstructed by the AI assistant from the chat history. Check each date and each Decision cell against what your team actually did, and add anything missing. Do not add entries for things that did not happen.

| # | Date | Prompt (paraphrased) | What the AI produced | Decision | How we verified | Notes |
|---|---|---|---|---|---|---|
| 1 | Earlier chat (add date) | Evaluate the Governance problem statement and give the best workflow | Verdict: a good pick with caveats (weak evidence base, crowded space, feature bloat); a 7-stage Round 1 workflow and an 8-stage product flow | Accepted | Compared with the case rubric | Fallback case kept: AI for All |
| 2 | Earlier chat (add date) | How can the workflow be improved to reach the best problem? | Break "misrouting" into causes, decision rule with kill criteria, early probe, honest synthetic data, human-benefit test, citizen appeal path | Accepted in part | Reviewed against the submission checklist | Human-benefit pilot not adopted yet (see entry 14) |
| 3 | Earlier chat (add date) | Write the final workflow, features and datasets file | A document with 113 features across 10 engines, tiers, datasets and a build order | Changed | Team reduced scope (entry 5) | Feature count was too large to build |
| 4 | 13 Oct 2026 | Should we start coding or do something else? | Advice: do not build the full app yet; do evidence and documents first | **Rejected** | n/a | Team chose to build a small working slice anyway (decision D-03) |
| 5 | 13 Oct 2026 | Complete Engines 1 to 6 today; give a fast plan | Build order for a Streamlit and SQLite slice, with a cut list | Accepted | Followed in later entries | Scope kept to Engines 1 to 6 |
| 6 | 13 Oct 2026 | Create the project skeleton | Folder structure, schema (append-only ledger via triggers), engines, four Streamlit pages | Accepted | AI ran Python tests on location extraction, split proposal, reason enforcement, ledger update and delete blocking, and bounce detection; team ran `init_db.py`, `evaluate.py` and launched the app | AI found and fixed 3 bugs in its own code (a vague "near my house" accepted as a location, A to B to A transfer not detected, database locked after a failed write) and retested |
| 7 | 13 Oct 2026 | Make the synthetic dataset in a Gwalior setting so we can paste it directly | 96 complaints (32 families x English, Hinglish, Hindi), responsibility table, keywords, dataset card | Accepted | AI ran structure checks (consistent labels per family, valid department names, no duplicates, Devanagari present only in Hindi rows); not independently labelled | Labels are AI-written (see entry 8). Responsibility table is an assumption |
| 8 | 13 Oct 2026 | Fix the "needs teammate review" label; AI should review the labels, not us | Warned this is not independent labelling; relabelled the column as AI_LABELLED_AI_REVIEWED; rebalanced the test split (Drainage was 9 of 27); added the AI-labelling disclosure to the dataset card | **Team overrode AI advice** | Re-ran the audit and `evaluate.py`; baseline result changed from 9/21 to 6/21 on the new test set | Disclosure kept in dataset card and draft document |
| 9 | 13 Oct 2026 | Which CSV format should we save from Excel? | Choose CSV UTF-8 (Comma delimited) | Accepted | Pipeline reads `utf-8-sig`; Hindi text displayed correctly in VS Code | Avoids corrupted Hindi |
| 10 | 13 Oct 2026 | Our folder is empty or misnamed; send every file | One setup script that writes all files to the right places and removes misplaced ones | Accepted | AI tested the script on a simulated messy folder; team ran it, then `init_db.py`, `evaluate.py` and `streamlit run` | Team had to use `python -m pip` because `pip` was not on PATH |
| 11 | 13 Oct 2026 | Write the decision rule, problem statement and SRS in one document | A Claude Doc: problem statement, framings, decision rule, evidence register, SRS, acceptance tests, baseline result, open items | Accepted, then edited by the team | Team edited the doc (added a thresholds paragraph) and ran the 9 acceptance tests in the app: all passed (team-reported) | Thresholds (20%, 15, 10%) were AI-proposed, confirmed or changed by the team |
| 12 | 13 Oct 2026 | Do the landscape check yourself and edit the document | Looked at CPGRAMS, Swachhata, MP CM Helpline 181 and the Gwalior Municipal Corporation listing; added section 5b; changed the claim from "routing is new" to a narrower hypothesis | Accepted | Based on search-result extracts and secondary sources only; official portals not yet opened | Team to open each portal and screenshot one complaint flow |
| 13 | 13 Oct 2026 | Draft the decision index and AI log | This file and `decision_index.md` | Pending team review | Team to check every row against what really happened | |
| 14 | n/a | AI suggestions not adopted (so far) | 3 to 5 stakeholder interviews; a small human-benefit pilot with 3 to 5 volunteers | Not adopted (update if this changes) | n/a | If still not done, state "not available" in the submission |

## Rejected AI suggestions (required: at least one, with the reason)
- **Entry 4:** "Do not build the app yet." Rejected because the team wanted a baseline result and a demo as evidence.
- **Entry 8:** "Have a teammate label the data independently." Not followed to save time; the risk is disclosed.
- **Entry 3:** The 113-feature plan was cut to a V1 slice.

## Verification summary
- Run by the team: `init_db.py`, `evaluate.py` (27 test rows; 6 of 21 single-owner correct, 3 of 3 vague abstained, 3 of 3 compound flagged), the Streamlit app, and the 9 acceptance tests (reported as passed).
- Not independently verified: the labels, the responsibility table, and the portal descriptions (secondary sources only).