from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class KeyTerms(BaseModel):
    parties: Optional[str] = None
    effective_date: Optional[str] = None
    term: Optional[str] = None
    rent: Optional[str] = None
    deposit: Optional[str] = None
    late_fee: Optional[str] = None
    renewal: Optional[str] = None
    termination: Optional[str] = None
    maintenance: Optional[str] = None
    dispute_resolution: Optional[str] = None

class RedFlagCandidate(BaseModel):
    flag: str
    rationale: str
    clause_quote: Optional[str] = None

class ExtractedContract(BaseModel):
    doc_type: str = Field(default="unknown")
    summary: str
    key_terms: KeyTerms
    red_flag_candidates: List[RedFlagCandidate] = Field(default_factory=list)
    questions_to_ask: List[str] = Field(default_factory=list)
