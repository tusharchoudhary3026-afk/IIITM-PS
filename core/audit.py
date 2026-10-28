"""Engine 11 - Component 2: Audit Trail & Ledger Export."""
import json
from core.db import fetch_all

def generate_audit_export() -> str:
    """Exports all immutable ledger events into a structured JSON audit string for compliance."""
    events = fetch_all("SELECT * FROM ledger ORDER BY id ASC")
    audit_package = {
        "system": "NyayaFlow Municipal Audit Export",
        "total_events": len(events),
        "events": events
    }
    return json.dumps(audit_package, indent=2)