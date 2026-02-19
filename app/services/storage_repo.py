import os
from google.cloud import storage
from datetime import datetime, timezone

def upload_pdf(pdf_bytes: bytes, filename: str) -> str:
    bucket_name = os.environ["BUCKET_NAME"]
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    safe_name = filename.replace("/", "_").replace("\\", "_")
    blob = bucket.blob(f"uploads/{ts}-{safe_name}")
    blob.upload_from_string(pdf_bytes, content_type="application/pdf")

    # For demo simplicity; for production use signed URLs instead.
    blob.make_public()
    return blob.public_url
