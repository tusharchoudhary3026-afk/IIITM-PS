"""Engine 1 / Dashboard: Secure Photo Attachment Module (No Image Analysis)."""
import os
from pathlib import Path
from .config import ROOT
from .db import execute, fetch_all

ATTACHMENT_DIR = ROOT / "data" / "attachments"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE_MB = 5


def save_attachment(complaint_id: int, uploaded_file) -> str:
    """Validates and securely stores an uploaded photo, linking its reference to a complaint ID."""
    if not uploaded_file:
        return None  # No file uploaded, nothing to save
    
    # Validate file extension
    ext = Path(uploaded_file.name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type '{ext}'. Allowed types: {list(ALLOWED_EXTENSIONS)}")
    
    # Validate file size (approximate check from uploaded file bytes)
    bytes_data = uploaded_file.getvalue()
    if len(bytes_data) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValueError(f"File size exceeds limit of {MAX_FILE_SIZE_MB}MB.")
    
    # Ensure secure storage directory exists
    ATTACHMENT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save file with unique naming to prevent collisions
    filename = f"complaint_{complaint_id}_{uploaded_file.name}"
    file_path = ATTACHMENT_DIR / filename
    
    with open(file_path, "wb") as f:
        f.write(bytes_data)
        
    # Record file reference in database
    execute(
        "INSERT INTO attachments (complaint_id, filename, file_path) VALUES (?, ?, ?)",
        (complaint_id, filename, str(file_path))
    )
    
    return str(file_path)


def get_attachments(complaint_id: int):
    """Retrieves all photo attachments linked to a specific complaint for authorized staff review."""
    return fetch_all("SELECT * FROM attachments WHERE complaint_id=?", (complaint_id,))