from typing import List, Dict, Any, Tuple

def score_risk(
    key_terms: Dict[str, Any],
    red_flags: List[Dict[str, Any]],
) -> Tuple[str, int, List[Dict[str, str]]]:
    """
    Hybrid approach:
    - The LLM extracts key terms and suggests potential red flags.
    - This rule engine applies deterministic scoring to produce a final risk score and risk level.
    """
    score = 0
    final_flags: List[Dict[str, str]] = []

    def add(points: int, flag: str, reason: str):
        nonlocal score
        score += points
        final_flags.append({"flag": flag, "reason": reason})

    renewal = (key_terms.get("renewal") or "").lower()
    termination = (key_terms.get("termination") or "").lower()
    late_fee = (key_terms.get("late_fee") or "").lower()
    deposit = (key_terms.get("deposit") or "").lower()
    dispute = (key_terms.get("dispute_resolution") or "").lower()

    # Rule examples (you can refine these later and document them in your report)
    if "auto" in renewal and any(x in renewal for x in ["30 day", "15 day", "10 day"]):
        add(2, "Auto-renewal with short notice window", "The agreement appears to auto-renew with a short notice period to cancel.")

    if any(x in termination for x in ["penalty", "fee", "forfeit", "liquidated damages"]):
        add(2, "Early termination penalty", "The agreement may impose a penalty or forfeiture for early termination.")

    if "late" in late_fee and ("%" in late_fee or "$" in late_fee):
        add(1, "Late fee clause", "A late fee is specified. Confirm the amount, trigger date, and any grace period.")

    if "non-refundable" in deposit or "nonrefundable" in deposit:
        add(2, "Non-refundable deposit", "The deposit appears non-refundable, which is higher risk.")

    if "arbitration" in dispute:
        add(1, "Arbitration clause", "The agreement includes arbitration language, which may affect dispute resolution options.")

    # Incorporate up to 5 model-suggested flags with low weight
    for rf in red_flags[:5]:
        flag = (rf.get("flag") or "").strip()[:80]
        rationale = (rf.get("rationale") or "").strip()[:200]
        if flag and rationale:
            add(1, f"Model suggestion: {flag}", rationale)

    # Map score to risk level
    if score <= 2:
        level = "Low"
    elif score <= 5:
        level = "Medium"
    else:
        level = "High"

    return level, score, final_flags
