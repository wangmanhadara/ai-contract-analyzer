SCHEMA_INSTRUCTIONS = """
You are an assistant that extracts information from contracts and leases.

Important rules:
- Do NOT provide legal advice. Provide informational summaries only.
- If a field is missing or unclear, use null or "unknown". Do NOT invent facts.
- Output MUST be valid JSON matching the schema below.
- Do NOT include markdown fences (no ```json).

JSON schema:
{
  "doc_type": "lease|employment|service|unknown",
  "summary": "string",
  "key_terms": {
    "parties": "string|null",
    "effective_date": "string|null",
    "term": "string|null",
    "rent": "string|null",
    "deposit": "string|null",
    "late_fee": "string|null",
    "renewal": "string|null",
    "termination": "string|null",
    "maintenance": "string|null",
    "dispute_resolution": "string|null"
  },
  "red_flag_candidates": [
    {"flag":"string","rationale":"string","clause_quote":"string|null"}
  ],
  "questions_to_ask": ["string"]
}
"""

def build_prompt(contract_text: str) -> str:
    # Keep input size reasonable for the model
    safe_text = contract_text[:18000]
    return f"""{SCHEMA_INSTRUCTIONS}

CONTRACT TEXT:
{safe_text}
"""
