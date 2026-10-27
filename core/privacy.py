"""UI masking for phone numbers and emails. Names are NOT auto-masked (cannot be done reliably)."""
import re

PHONE = re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{9}(?!\d)")
EMAIL = re.compile(r"[\w.+-]+@([\w-]+\.[\w.-]+)")


def mask_text(text: str) -> str:
    text = PHONE.sub(lambda m: "XXXXXX" + re.sub(r"\D", "", m.group(0))[-4:], text or "")
    return EMAIL.sub(lambda m: "***@" + m.group(1), text)