"""Why does TF-IDF abstain? Uses TRAIN and VALIDATION only, never the test split."""
import pandas as pd
from core import router_ml
from core.config import COMPLAINTS

df = pd.read_csv(COMPLAINTS, encoding="utf-8-sig")
tr = router_ml.single_owner_rows(df[df.split == "train"])
va = router_ml.single_owner_rows(df[df.split == "val"])
for C in [1, 10, 100]:
    r = router_ml.TfidfRouter()
    r.clf.set_params(C=C)
    r.fit(tr["text"], tr["owner_label"])
    outs = [r.route(t, 0.0) for t in va["text"]]
    correct = sum(o["top3"][0]["dept"] == y for o, y in zip(outs, va["owner_label"]))
    confs = [o["confidence"] for o in outs]
    no_overlap = sum(not o["evidence"]["matched_terms"] for o in outs)
    print(f"C={C}: val top-1 {correct}/{len(va)} | confidence {min(confs):.2f}-{max(confs):.2f} "
          f"| rows with no shared words {no_overlap}")