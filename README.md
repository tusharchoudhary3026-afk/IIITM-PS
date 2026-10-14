# NyayaFlow (Round 1 skeleton)
Explainable grievance routing with abstention, human review and an append-only ledger.
All data is SYNTHETIC. Nothing is auto-closed, auto-rejected or auto-merged.

## Run
    python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    python scripts/init_db.py
    python scripts/evaluate.py        # baseline on the test split
    streamlit run app.py

## Structure
- core/    engines (intake, splitter, routers, ownership, ledger, db)
- pages/   Streamlit screens (Intake, Review, Challenge, Evaluation)
- db/      schema.sql (ledger is append-only via triggers)
- data/    responsibility table, keywords, complaints, dataset card (replace samples with your data)
- docs/    AI log, decision index

## First TODOs
1. Replace data/responsibility_table.csv with rules from ONE city's citizen charter (add URL + date).
2. Write 80-100 complaints in data/complaints.csv; a teammate labels them; freeze the test split.
3. Run scripts/evaluate.py and save the failure list.
4. Then wire in core/router_ml.py and choose the confidence threshold on the validation split.
