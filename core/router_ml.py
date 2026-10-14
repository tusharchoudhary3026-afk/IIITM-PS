"""Engine 3: TF-IDF + Logistic Regression. Compared against the baseline on the same frozen test set."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from .config import COMPLAINTS, TFIDF_THRESHOLD

# Default tokenizer splits Devanagari words at vowel signs; this keeps them whole.
TOKEN = r"[^\s.,!?।;:()\"']+"


class TfidfRouter:
    def __init__(self):
        self.vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True, token_pattern=TOKEN)
        self.clf = LogisticRegression(max_iter=1000)

    def fit(self, texts, labels):
        self.clf.fit(self.vec.fit_transform(texts), labels)
        return self

    def route(self, text, threshold=None):
        threshold = TFIDF_THRESHOLD if threshold is None else threshold
        X = self.vec.transform([text])
        probs = self.clf.predict_proba(X)[0]
        order = probs.argsort()[::-1][:3]
        top3 = [{"dept": self.clf.classes_[i], "score": round(float(probs[i]), 2)} for i in order]
        # Evidence: only terms that push the score TOWARD the top department (not every word in the text)
        names = self.vec.get_feature_names_out()
        row = X.tocoo()
        top = int(order[0])
        coef = self.clf.coef_
        w = coef[top] if coef.shape[0] > 1 else (coef[0] if top == 1 else -coef[0])   # binary case has 1 row
        contrib = sorted(((w[j] * v, names[j]) for j, v in zip(row.col, row.data)), reverse=True)
        evidence = {"matched_terms": [t for c, t in contrib if c > 0][:5]}
        conf = top3[0]["score"]          # NOT assumed calibrated
        return {"top3": top3, "evidence": evidence, "confidence": conf,
                "abstained": conf < threshold or not evidence["matched_terms"]}


def single_owner_rows(df):
    return df[~df["owner_label"].isin(["MULTI", "UNCLEAR"])]


def fit_default(df=None):
    df = pd.read_csv(COMPLAINTS, encoding="utf-8-sig") if df is None else df
    tr = single_owner_rows(df[df["split"] == "train"])
    return TfidfRouter().fit(tr["text"], tr["owner_label"])


_cache = {}
def default_router():
    if "r" not in _cache:
        _cache["r"] = fit_default()
    return _cache["r"]


def choose_threshold(router, val_df, target_acc=0.80):
    """Lowest threshold (most coverage) whose accuracy on answered validation rows >= target.
    Returns (threshold, curve). Provisional: validation is small."""
    v = single_owner_rows(val_df)
    curve, best = [], None
    for th in [round(x * 0.05, 2) for x in range(4, 19)]:
        ans = [(router.route(t, th), y) for t, y in zip(v["text"], v["owner_label"])]
        ans = [(r["top3"][0]["dept"] == y) for r, y in ans if not r["abstained"]]
        cov = len(ans) / max(len(v), 1)
        acc = sum(ans) / len(ans) if ans else None
        curve.append({"threshold": th, "coverage": round(cov, 3), "accuracy": None if acc is None else round(acc, 3),
                      "answered": len(ans), "n": len(v)})
        if best is None and acc is not None and acc >= target_acc:
            best = th
    return best, curve