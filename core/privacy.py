"""Engine 11 - Component 1: PII Privacy Masking & Redaction."""
import re

def mask_pii(text: str) -> str:
    """Masks personally identifiable information (phone numbers, emails) in complaint text."""
    if not text:
        return ""
    
    # Mask 10-digit phone numbers
    text_masked = re.sub(r'\b\d{10}\b', '[REDACTED_PHONE]', text)
    
    # Mask email addresses
    text_masked = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[REDACTED_EMAIL]', text_masked)
    
    return text_masked

def sanitize_complaint_record(record: dict) -> dict:
    """Returns a sanitized copy of a complaint record safe for public telemetry/export."""
    sanitized = record.copy()
    if "original_text" in sanitized:
        sanitized["original_text"] = mask_pii(sanitized["original_text"])
    if "normalized_text" in sanitized:
        sanitized["normalized_text"] = mask_pii(sanitized["normalized_text"])
    return sanitized