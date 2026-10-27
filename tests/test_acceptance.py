import pandas as pd
import pytest
from core import intake, router_baseline, splitter, ownership
from core.config import COMPLAINTS
from core.db import insert_complaint, insert_suggestion, fetch_all
from core.ledger import log_event, history, save_correction


def _save(text, case):
    rec = intake.process(text)
    rec["case_id"], rec["parent_id"] = case, None
    cid = insert_complaint(rec)
    r = router_baseline.route(text)
    insert_suggestion(cid, "baseline", r["top3"], r["evidence"], r["confidence"], r["abstained"])
    top = r["top3"][0]["dept"] if r["top3"] and not r["abstained"] else None
    log_event(cid, "suggested", "system", suggested_dept=top)
    return cid


def test_AT01_clear_complaint():
    r = router_baseline.route("The streetlight is not working near City Centre.")
    assert not r["abstained"] and r["top3"][0]["dept"] == "Electricity Dept"
    # "beats baseline" part is measured on the Evaluation page (evaluate_full), not here.


def test_AT02_vague_asks_and_invents_nothing():
    text = "Problem near my house, please fix."
    rec = intake.process(text)
    assert router_baseline.route(text)["abstained"]
    assert rec["location"] == "unknown" and rec["issue"] == "unknown"
    assert intake.clarification_question(rec)


def test_AT03_duplicates_not_built():
    pytest.skip("Engine 7 (duplicate linking) is not built in V1 scope")


def test_AT04_override_stores_correction(db):
    cid = _save("The streetlight is not working near City Centre.", "CASE-T4")
    with pytest.raises(ValueError):
        log_event(cid, "edit", "reviewer", final_dept="Roads Dept", reason="", reason_code="wrong_category")
    with pytest.raises(ValueError):
        log_event(cid, "edit", "reviewer", final_dept="Roads Dept", reason="x", reason_code=None)
    first = history(cid)[0]
    log_event(cid, "edit", "reviewer", suggested_dept="Electricity Dept", final_dept="Roads Dept",
              reason="Pole is on a road-widening site", reason_code="wrong_category")
    save_correction(cid, "text", "Electricity Dept", "Roads Dept")
    h = history(cid)
    assert [e["event_type"] for e in h] == ["suggested", "edit"]
    assert h[0] == first and h[1]["reason"] and h[1]["suggested_dept"] == "Electricity Dept"
    assert len(fetch_all("SELECT * FROM corrections WHERE complaint_id=?", (cid,))) == 1


def test_AT05_safety_not_built():
    pytest.skip("Engine 8 (safety flagging) is not built in V1 scope")


def test_AT06_language_results_reported():
    df = pd.read_csv(COMPLAINTS, encoding="utf-8-sig")
    df = df[~df["owner_label"].isin(["MULTI", "UNCLEAR"])]
    kw = router_baseline.load_keywords()
    out = {}
    for lang, g in df.groupby("language"):
        ok = sum((not (r := router_baseline.route(t, kw))["abstained"]) and r["top3"][0]["dept"] == y
                 for t, y in zip(g["text"], g["owner_label"]))
        out[lang] = (ok, len(g))
    print("AT-06 per-language correct/n (all splits):", out)
    assert set(out) == {"english", "hindi", "hinglish"} and all(n > 0 for _, n in out.values())


def test_AT07_compound_split_and_merge_back(db):
    text = "Streetlight is not working in Thatipur and garbage is also piled up near the park."
    sp = splitter.propose_split(text)
    assert sp["is_compound"] and len(sp["parts"]) == 2
    one = splitter.propose_split("The drain is blocked and the sewer is overflowing near Morar.")
    assert not one["is_compound"]                      # looks compound, one owner: kept intact
    cid = _save(text, "CASE-T7")
    ids = splitter.confirm_split(cid, "CASE-T7", sp["parts"])
    assert len(ids) == 2
    with pytest.raises(ValueError):
        splitter.confirm_split(cid, "CASE-T7", sp["parts"])
    assert splitter.merge_back(cid) == 2
    with pytest.raises(ValueError):
        splitter.merge_back(cid)
    assert len(fetch_all("SELECT id FROM complaints WHERE parent_id=?", (cid,))) == 2  # never deleted


def test_AT08_overlap_flagged_with_source():
    o = ownership.check_suggestions(["Drainage Dept", "Roads Dept"],
                                    "Waterlogging on the road in front of the bus depot")
    assert o and o[0]["source"] and o[0]["verification"]
    assert ownership.check_suggestions(["Drainage Dept", "Roads Dept"], "The streetlight is not working") == []


def test_E6_bounce_pattern():
    h = [{"suggested_dept": "Roads Dept", "final_dept": "Drainage Dept"}, {"final_dept": "Roads Dept"}]
    assert ownership.detect_bounce(h)["pattern"] == "Roads Dept -> Drainage Dept -> Roads Dept"