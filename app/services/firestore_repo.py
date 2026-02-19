import os
from google.cloud import firestore
from datetime import datetime, timezone

def get_db():
    return firestore.Client(project=os.environ["PROJECT_ID"])

def save_analysis(doc: dict) -> str:
    db = get_db()
    doc["createdAt"] = datetime.now(timezone.utc)
    ref = db.collection("analyses").document()
    ref.set(doc)
    return ref.id

def list_recent(limit: int = 20):
    db = get_db()
    docs = (
        db.collection("analyses")
        .order_by("createdAt", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    out = []
    for d in docs:
        item = d.to_dict()
        item["id"] = d.id
        out.append(item)
    return out

def get_one(doc_id: str):
    db = get_db()
    snap = db.collection("analyses").document(doc_id).get()
    if not snap.exists:
        return None
    data = snap.to_dict()
    data["id"] = snap.id
    return data
