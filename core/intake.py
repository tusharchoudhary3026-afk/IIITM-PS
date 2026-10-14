# # """Engine 1: intake + extraction. Rule-based. Never invents missing facts."""
# # import re

# # HINGLISH_WORDS = {"nahi", "hai", "hain", "pe", "par", "mein", "me", "ka", "ki", "ke", "aur", "bhi",
# #                   "paani", "pani", "sadak", "kachra", "bijli", "nali", "gali", "kab", "kyun"}
# # NORMALIZE = {"pani": "paani", "sadak": "road", "kachra": "garbage", "bijli": "electricity",
# #              "nali": "drain", "gali": "lane"}
# # LOCATION_PATTERNS = [
# #     r"ward\s*(?:no\.?|number)?\s*\d+",
# #     r"(?:near|nearby|paas)\s+[A-Za-z\u0900-\u097F ]{3,30}",
# #     r"[A-Za-z\u0900-\u097F]+(?: [A-Za-z\u0900-\u097F]+)?\s+(?:road|marg|chowk|colony|nagar|lane)",
# # ]
# # REQUIRED_FIELDS = ["location", "issue"]


# # def detect_language(text: str) -> str:
# #     has_dev = bool(re.search(r"[\u0900-\u097F]", text))
# #     words = set(re.findall(r"[a-z]+", text.lower()))
# #     hing = len(words & HINGLISH_WORDS)
# #     if has_dev and words:
# #         return "uncertain"          # mixed script: a human decides
# #     if has_dev:
# #         return "hindi"
# #     if hing >= 2:
# #         return "hinglish"
# #     if words and hing == 0:
# #         return "english"
# #     return "uncertain"


# # def normalize(text: str) -> str:
# #     """Stored in a SEPARATE field. The original text is never touched."""
# #     words = re.findall(r"\S+", text.lower())
# #     return " ".join(NORMALIZE.get(w.strip(".,!?"), w) for w in words)


# # VAGUE = re.compile(r"\b(my|our|the|this|that|your|mere|meri|mere ghar)\b|\b(house|home|ghar)\b", re.I)


# # def extract_location(text: str) -> str:
# #     for p in LOCATION_PATTERNS:
# #         m = re.search(p, text, flags=re.I)
# #         if m and not VAGUE.search(m.group(0)):   # "near my house" is not a usable location
# #             return m.group(0).strip()
# #     return "unknown"                # never invent


# # def extract_issue(text: str) -> str:
# #     return text.strip().split(".")[0][:120]   # TODO: replace with keyword-based issue label


# # def process(text: str, channel: str = "portal", location_hint: str | None = None) -> dict:
# #     loc = location_hint.strip() if location_hint and location_hint.strip() else extract_location(text)
# #     rec = {
# #         "original_text": text,
# #         "language": detect_language(text),
# #         "normalized_text": normalize(text),
# #         "channel": channel,
# #         "location": loc,
# #         "issue": extract_issue(text),
# #         "requested_action": None,        # TODO: extract (e.g. 'repair', 'clean', 'inspect')
# #         "is_synthetic": 1,
# #     }
# #     missing = [f for f in REQUIRED_FIELDS if not rec.get(f) or rec[f] == "unknown"]
# #     rec["missing_fields"] = ",".join(missing)
# #     return rec


# # def clarification_question(rec: dict) -> str | None:
# #     """One targeted question only."""
# #     if "location" in (rec.get("missing_fields") or ""):
# #         return "Which ward, street or nearby landmark is this about?"
# #     if "issue" in (rec.get("missing_fields") or ""):
# #         return "Can you describe the problem in one sentence?"
# #     return None



# """Engine 1: intake + extraction. Rule-based. Never invents missing facts."""
# import re

# HINGLISH_WORDS = {"nahi", "hai", "hain", "pe", "par", "mein", "me", "ka", "ki", "ke", "aur", "bhi",
#                   "paani", "pani", "sadak", "kachra", "bijli", "nali", "gali", "kab", "kyun",
#                   "se", "ko", "ho", "raha", "rahi", "hua", "hui", "gaya", "gayi", "band", "kharab",
#                   "din", "ek", "hamare", "hamari", "mera", "meri", "paas", "bahut", "kam"}
# NORMALIZE = {"pani": "paani", "sadak": "road", "kachra": "garbage", "bijli": "electricity",
#              "nali": "drain", "gali": "lane"}
# LOCATION_PATTERNS = [
#     r"ward\s*(?:no\.?|number)?\s*\d+",
#     r"(?:near|nearby|paas)\s+[A-Za-z\u0900-\u097F ]{3,30}",
#     r"[A-Za-z\u0900-\u097F]+(?: [A-Za-z\u0900-\u097F]+)?\s+(?:road|marg|chowk|colony|nagar|lane)",
# ]
# REQUIRED_FIELDS = ["location", "issue"]

# # First-match order matters (specific before general). Matching runs on the ORIGINAL text.
# ISSUES = {
#     "waterlogging": ["waterlogging", "paani bhara", "पानी भर"],
#     "drain/sewer/manhole": ["drain", "sewer", "nali", "manhole", "नाली", "सीवर", "मैनहोल"],
#     "garbage/sanitation": ["garbage", "kachra", "dustbin", "toilet", "dead dog", "dead animal",
#                            "कचरा", "कूड़ेदान", "शौचालय", "मरा हुआ"],
#     "streetlight/wire": ["streetlight", "street light", "bijli", "taar", "wire", "स्ट्रीटलाइट",
#                          "स्ट्रीट लाइट", "बिजली", "तार"],
#     "water supply/pipe": ["water supply", "pipeline", "pipe", "tap", "पाइप", "नल", "पानी की आपूर्ति"],
#     "road damage": ["pothole", "gadda", "footpath", "speed breaker", "road", "sadak",
#                     "गड्ढा", "फुटपाथ", "स्पीड ब्रेकर", "सड़क"],
# }
# ACTIONS = {
#     "repair": ["fix", "repair", "theek", "sahi", "ठीक", "मरम्मत"],
#     "clean/remove": ["clean", "safai", "remove", "utha", "hatao", "साफ", "सफाई", "उठा", "हटा"],
#     "inspect": ["check", "dekh", "inspect", "bhejiye", "send someone", "भेज", "देख"],
#     "restore": ["restore", "chalu", "resume"],
#     "take action": ["action", "कार्रवाई"],
# }


# def detect_language(text: str) -> str:
#     has_dev = bool(re.search(r"[\u0900-\u097F]", text))
#     words = set(re.findall(r"[a-z]+", text.lower()))
#     hing = len(words & HINGLISH_WORDS)
#     if has_dev and words:
#         return "uncertain"          # mixed script: a human decides
#     if has_dev:
#         return "hindi"
#     if hing >= 2:
#         return "hinglish"
#     if words and hing == 0:
#         return "english"
#     return "uncertain"


# def normalize(text: str) -> str:
#     """Stored in a SEPARATE field. The original text is never touched."""
#     words = re.findall(r"\S+", text.lower())
#     return " ".join(NORMALIZE.get(w.strip(".,!?"), w) for w in words)


# VAGUE = re.compile(r"\b(my|our|the|this|that|your|mere|meri|mere ghar)\b|\b(house|home|ghar)\b", re.I)


# def extract_location(text: str) -> str:
#     for p in LOCATION_PATTERNS:
#         m = re.search(p, text, flags=re.I)
#         if m and not VAGUE.search(m.group(0)):
#             return m.group(0).strip()
#     return "unknown"                # never invent


# def _find(table: dict, text: str):
#     t = text.lower()
#     return [label for label, words in table.items() if any(w in t for w in words)]


# def extract_issue(text: str) -> str:
#     found = _find(ISSUES, text)
#     return " | ".join(found) if found else "unknown"


# def extract_requested_action(text: str) -> str:
#     found = _find(ACTIONS, text)
#     return " | ".join(found) if found else "unspecified"   # never guessed


# def process(text: str, channel: str = "portal", location_hint: str | None = None) -> dict:
#     loc = location_hint.strip() if location_hint and location_hint.strip() else extract_location(text)
#     rec = {
#         "original_text": text, "language": detect_language(text), "normalized_text": normalize(text),
#         "channel": channel, "location": loc, "issue": extract_issue(text),
#         "requested_action": extract_requested_action(text), "is_synthetic": 1,
#     }
#     missing = [f for f in REQUIRED_FIELDS if not rec.get(f) or rec[f] == "unknown"]
#     rec["missing_fields"] = ",".join(missing)
#     return rec


# def clarification_question(rec: dict) -> str | None:
#     """One targeted question only (issue first: without it, routing is guesswork)."""
#     mf = rec.get("missing_fields") or ""
#     if "issue" in mf:
#         return "Can you describe the problem in one sentence (what is broken or missing)?"
#     if "location" in mf:
#         return "Which ward, street or nearby landmark is this about?"
#     return None




"""Engine 1: intake + extraction. Rule-based. Never invents missing facts."""
import re

HINGLISH_WORDS = {"nahi", "hai", "hain", "pe", "par", "mein", "me", "ka", "ki", "ke", "aur", "bhi",
                  "paani", "pani", "sadak", "kachra", "bijli", "nali", "gali", "kab", "kyun",
                  "se", "ko", "ho", "raha", "rahi", "hua", "hui", "gaya", "gayi", "band", "kharab",
                  "din", "ek", "hamare", "hamari", "mera", "meri", "paas", "bahut", "kam"}
NORMALIZE = {"pani": "paani", "sadak": "road", "kachra": "garbage", "bijli": "electricity",
             "nali": "drain", "gali": "lane"}
LOCATION_PATTERNS = [
    r"ward\s*(?:no\.?|number)?\s*\d+",
    r"(?:near|nearby|paas)\s+[A-Za-z\u0900-\u097F ]{3,30}?(?=\s+(?:and|aur|but|which|that)\b|[.,;]|$)",
    r"[A-Za-z\u0900-\u097F]+(?: [A-Za-z\u0900-\u097F]+)?\s+(?:road|marg|chowk|colony|nagar|lane)",
]
POSSESSIVE = re.compile(r"\b(my|our|your|mere|meri|hamare|hamari)\b|\b(house|home|ghar)\b", re.I)
PLACE_AFTER_PREP = re.compile(r"\b(?:in|at|from)\s+([A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+)?)")   # capitalised names
REQUIRED_FIELDS = ["location", "issue"]

# First-match order matters (specific before general). Matching runs on the ORIGINAL text.
ISSUES = {
    "waterlogging": ["waterlogging", "paani bhara", "पानी भर"],
    "drain/sewer/manhole": ["drain", "sewer", "nali", "manhole", "नाली", "सीवर", "मैनहोल"],
    "garbage/sanitation": ["garbage", "kachra", "dustbin", "toilet", "dead dog", "dead animal",
                           "कचरा", "कूड़ेदान", "शौचालय", "मरा हुआ"],
    "streetlight/wire": ["streetlight", "street light", "bijli", "taar", "wire", "स्ट्रीटलाइट",
                         "स्ट्रीट लाइट", "बिजली", "तार"],
    "water supply/pipe": ["water supply", "pipeline", "pipe", "tap", "पाइप", "नल", "पानी की आपूर्ति"],
    "road damage": ["pothole", "gadda", "footpath", "speed breaker", "road", "sadak",
                    "गड्ढा", "फुटपाथ", "स्पीड ब्रेकर", "सड़क"],
}
ACTIONS = {
    "repair": ["fix", "repair", "theek", "sahi", "ठीक", "मरम्मत"],
    "clean/remove": ["clean", "safai", "remove", "utha", "hatao", "साफ", "सफाई", "उठा", "हटा"],
    "inspect": ["check", "dekh", "inspect", "bhejiye", "send someone", "भेज", "देख"],
    "restore": ["restore", "chalu", "resume"],
    "take action": ["action", "कार्रवाई"],
}


def detect_language(text: str) -> str:
    has_dev = bool(re.search(r"[\u0900-\u097F]", text))
    words = set(re.findall(r"[a-z]+", text.lower()))
    hing = len(words & HINGLISH_WORDS)
    if has_dev and words:
        return "uncertain"          # mixed script: a human decides
    if has_dev:
        return "hindi"
    if hing >= 2:
        return "hinglish"
    if words and hing == 0:
        return "english"
    return "uncertain"


def normalize(text: str) -> str:
    """Stored in a SEPARATE field. The original text is never touched."""
    words = re.findall(r"\S+", text.lower())
    return " ".join(NORMALIZE.get(w.strip(".,!?"), w) for w in words)


def extract_location(text: str) -> str:
    for p in LOCATION_PATTERNS:
        m = re.search(p, text, flags=re.I)
        if m and not POSSESSIVE.search(m.group(0)):
            return re.sub(r"^((?:on|at|in|the)\s+)+", "", m.group(0).strip(), flags=re.I)
    m = PLACE_AFTER_PREP.search(text)
    return m.group(1) if m else "unknown"      # never invent


def _find(table: dict, text: str):
    t = text.lower()
    return [label for label, words in table.items() if any(w in t for w in words)]


def extract_issue(text: str) -> str:
    found = _find(ISSUES, text)
    return " | ".join(found) if found else "unknown"


def extract_requested_action(text: str) -> str:
    found = _find(ACTIONS, text)
    return " | ".join(found) if found else "unspecified"   # never guessed


def process(text: str, channel: str = "portal", location_hint: str | None = None) -> dict:
    loc = location_hint.strip() if location_hint and location_hint.strip() else extract_location(text)
    rec = {
        "original_text": text, "language": detect_language(text), "normalized_text": normalize(text),
        "channel": channel, "location": loc, "issue": extract_issue(text),
        "requested_action": extract_requested_action(text), "is_synthetic": 1,
    }
    missing = [f for f in REQUIRED_FIELDS if not rec.get(f) or rec[f] == "unknown"]
    rec["missing_fields"] = ",".join(missing)
    return rec


def clarification_question(rec: dict) -> str | None:
    """One targeted question only (issue first: without it, routing is guesswork)."""
    mf = rec.get("missing_fields") or ""
    if "issue" in mf:
        return "Can you describe the problem in one sentence (what is broken or missing)?"
    if "location" in mf:
        return "Which ward, street or nearby landmark is this about?"
    return None