import hashlib
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.prompts import build_prompt
from app.services.pdf_extract import extract_text_from_pdf
from app.services.gemini_repo import generate_structured_json
from app.services.firestore_repo import save_analysis, list_recent, get_one
from app.services.storage_repo import upload_pdf
from app.risk_rules import score_risk

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/analyze")
async def analyze(
    text: str = Form(default=""),
    file: UploadFile | None = File(default=None),
):
    source = "paste" if text else "upload"
    file_url = None

    if file is not None:
        pdf_bytes = await file.read()
        file_url = upload_pdf(pdf_bytes, file.filename)
        extracted_text = extract_text_from_pdf(pdf_bytes)
    else:
        extracted_text = text

    extracted_text = (extracted_text or "").strip()
    if not extracted_text:
        return {"error": "No text extracted. Please paste text or upload a readable (text-based) PDF."}

    text_hash = hashlib.sha256(extracted_text.encode("utf-8")).hexdigest()[:16]

    prompt = build_prompt(extracted_text)
    llm_json = generate_structured_json(prompt)

    key_terms = llm_json.get("key_terms", {}) or {}
    red_flag_candidates = llm_json.get("red_flag_candidates", []) or []

    risk_level, risk_score, final_flags = score_risk(key_terms, red_flag_candidates)

    doc = {
        "docType": llm_json.get("doc_type", "unknown"),
        "source": source,
        "fileUrl": file_url,
        "textHash": text_hash,
        "extracted": llm_json,
        "risk": {
            "riskLevel": risk_level,
            "score": risk_score,
            "redFlags": final_flags,
        },
        "modelInfo": {
            "provider": "Vertex AI",
            "model": llm_json.get("model", "unknown"),
            "promptVersion": "v1-json",
        },
    }

    analysis_id = save_analysis(doc)
    return {"analysis_id": analysis_id, **doc}

@app.get("/api/history")
def history():
    return list_recent(20)

@app.get("/api/analysis/{analysis_id}")
def read_one(analysis_id: str):
    data = get_one(analysis_id)
    return data or {"error": "Not found"}
