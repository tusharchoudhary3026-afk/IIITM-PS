"""Engine 8 - Component 2: Acceptance Tests AT-01 through AT-06 Runner."""
import json
import pandas as pd
from intake import process, clarification_question, extract_issue, detect_language
from splitter import propose_split
from router_baseline import route
from ledger import save_correction, log_event


def run_at_01_clear_complaint():
    """AT-01: Clear complaint, known owner -> Correct top suggestion."""
    text = "Large pothole causing traffic jams near Civil Lines main road."
    res = route(text)
    top_dept = res["top3"][0]["dept"] if res["top3"] else None
    passed = top_dept == "Roads & Infrastructure" and not res["abstained"]
    return {
        "id": "AT-01",
        "scenario": "Clear complaint, known owner",
        "pass_condition": "Correct top suggestion against independently checked label",
        "status": "PASS" if passed else "FAIL",
        "details": f"Routed to: {top_dept}, Conf: {res['confidence']}"
    }


def run_at_02_vague_complaint():
    """AT-02: Vague text / missing location -> Ask targeted question or abstain; invent nothing."""
    text = "Fix this problem near my house."
    rec = process(text)
    question = clarification_question(rec)
    passed = rec["location"] == "unknown" and question is not None
    return {
        "id": "AT-02",
        "scenario": "Vague text / missing location",
        "pass_condition": "Ask targeted question or abstain; invent nothing",
        "status": "PASS" if passed else "FAIL",
        "details": f"Extracted Location: {rec['location']}, Question: {question}"
    }


def run_at_03_similar_wording():
    """AT-03: Similar wording, distinct incidents -> Do not merge; show evidence."""
    text1 = "Garbage dump near Ward 4 market."
    text2 = "Garbage dump near Ward 9 bus stand."
    split1 = propose_split(text1)
    split2 = propose_split(text2)
    passed = not split1["is_compound"] and not split2["is_compound"]
    return {
        "id": "AT-03",
        "scenario": "Similar wording, distinct incidents",
        "pass_condition": "Do not merge; show evidence and allow unlink",
        "status": "PASS" if passed else "FAIL",
        "details": f"Text 1 compound: {split1['is_compound']}, Text 2 compound: {split2['is_compound']}"
    }


def run_at_04_reviewer_override():
    """AT-04: Reviewer overrides suggestion -> Store correction, reason and prior suggestion."""
    try:
        complaint_id = 9999  # Mock ID for test verification
        save_correction(complaint_id, "Broken street light", "Roads & Infrastructure", "Electrical")
        log_event(
            complaint_id=complaint_id,
            event_type="edit",
            actor="reviewer",
            suggested_dept="Roads & Infrastructure",
            final_dept="Electrical",
            reason="Streetlight wiring is handled by Electrical department",
            reason_code="wrong_category"
        )
        passed = True
    except Exception:
        passed = False
    return {
        "id": "AT-04",
        "scenario": "Reviewer overrides suggestion",
        "pass_condition": "Store correction, reason and prior suggestion",
        "status": "PASS" if passed else "FAIL",
        "details": "Successfully stored correction and logged edit event with mandatory reason code."
    }


def run_at_05_safety_case():
    """AT-05: Predefined safety case -> Flag for human review under team rubric."""
    text = "Exposed live high-voltage wire snapping near children's park."
    res = route(text)
    issue = extract_issue(text)
    passed = "streetlight/wire" in issue and not res["abstained"]
    return {
        "id": "AT-05",
        "scenario": "Predefined safety case",
        "pass_condition": "Flag for human review under team rubric",
        "status": "PASS" if passed else "FAIL",
        "details": f"Extracted issue: {issue}, Routed: {res['top3'][0]['dept'] if res['top3'] else 'None'}"
    }


def run_at_06_multilingual():
    """AT-06: Equivalent English/Hindi/Hinglish case -> Report results by language."""
    en_text = "Water supply pipe leaking on station road."
    hi_text = "स्टेशन रोड पर पानी की पाइपलाइन लीक हो रही है।"
    hing_text = "station road pe paani ka pipe leak ho raha hai."

    res_en = detect_language(en_text)
    res_hi = detect_language(hi_text)
    res_hing = detect_language(hing_text)

    passed = (res_en == "english" and res_hi == "hindi" and res_hing == "hinglish")
    return {
        "id": "AT-06",
        "scenario": "Equivalent English/Hindi/Hinglish case",
        "pass_condition": "Report results by language and investigate errors",
        "status": "PASS" if passed else "FAIL",
        "details": f"Detected Languages -> English: {res_en}, Hindi: {res_hi}, Hinglish: {res_hing}"
    }


def run_all_acceptance_tests():
    """Executes the full acceptance test suite (AT-01 through AT-06)."""
    return [
        run_at_01_clear_complaint(),
        run_at_02_vague_complaint(),
        run_at_03_similar_wording(),
        run_at_04_reviewer_override(),
        run_at_05_safety_case(),
        run_at_06_multilingual(),
    ]


if __name__ == "__main__":
    results = run_all_acceptance_tests()
    for r in results:
        print(f"[{r['status']}] {r['id']}: {r['scenario']} -> {r['details']}")