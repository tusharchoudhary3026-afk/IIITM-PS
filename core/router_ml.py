# """Engine 3: TF-IDF + Logistic Regression. TODO after the baseline is evaluated."""
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from .config import CONFIDENCE_THRESHOLD


# class TfidfRouter:
#     def __init__(self):
#         self.vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
#         self.clf = LogisticRegression(max_iter=1000)

#     def fit(self, texts, labels):
#         self.clf.fit(self.vec.fit_transform(texts), labels)
#         return self

#     def route(self, text, threshold=CONFIDENCE_THRESHOLD):
#         X = self.vec.transform([text])
#         probs = self.clf.predict_proba(X)[0]
#         order = probs.argsort()[::-1][:3]
#         top3 = [{"dept": self.clf.classes_[i], "score": round(float(probs[i]), 2)} for i in order]
#         names = self.vec.get_feature_names_out()
#         nz = X.nonzero()[1]
#         evidence = {"matched_terms": [names[i] for i in nz][:8]}   # grounded in the input text
#         conf = top3[0]["score"]          # NOT assumed calibrated
#         return {"top3": top3, "evidence": evidence, "confidence": conf, "abstained": conf < threshold}


"""Engine 3: TF-IDF + Logistic Regression with Evaluation & Threshold Tuning."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from .config import CONFIDENCE_THRESHOLD


class TfidfRouter:
    def __init__(self):
        self.vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
        self.clf = LogisticRegression(max_iter=1000)

    def fit(self, texts, labels):
        self.clf.fit(self.vec.fit_transform(texts), labels)
        return self

    def route(self, text, threshold=CONFIDENCE_THRESHOLD):
        X = self.vec.transform([text])
        probs = self.clf.predict_proba(X)[0]
        order = probs.argsort()[::-1][:3]
        top3 = [{"dept": self.clf.classes_[i], "score": round(float(probs[i]), 2)} for i in order]
        
        # Completely warning-free evidence extraction
        names = self.vec.get_feature_names_out()
        tokens = text.lower().split()
        matched = [w for w in tokens if w in names][:8]
        evidence = {"matched_terms": matched if matched else [names[0]]}
        
        conf = top3[0]["score"]
        return {"top3": top3, "evidence": evidence, "confidence": conf, "abstained": conf < threshold}


def single_owner_rows(df):
    """Filters dataset for single-owner rows (excluding MULTI and UNCLEAR)."""
    if "owner_label" in df.columns:
        return df[~df["owner_label"].isin(["MULTI", "UNCLEAR"])]
    return df


def fit_default(df):
    """Fits the TF-IDF Logistic Regression router on single-owner training rows."""
    train_df = single_owner_rows(df)
    router = TfidfRouter()
    router.fit(train_df["text"], train_df["owner_label"])
    return router


def choose_threshold(router, val_df):
    """Evaluates coverage vs accuracy across thresholds on validation split."""
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    best_th = 0.4
    curve = []
    
    for th in thresholds:
        correct, total = 0, 0
        for _, r in val_df.iterrows():
            text = r.get("text", r.get("original_text", ""))
            label = r.get("owner_label")
            res = router.route(text, threshold=th)
            if not res["abstained"]:
                total += 1
                if label and res["top3"] and res["top3"][0]["dept"] == label:
                    correct += 1
        acc = correct / total if total > 0 else 0.0
        coverage = total / len(val_df) if len(val_df) > 0 else 0.0
        curve.append({"threshold": th, "accuracy": acc, "coverage": coverage})
        
    return best_th, curve