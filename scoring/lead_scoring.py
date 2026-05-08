def score_lead(lead_data: dict) -> dict:
    score = 0 
    reasons = []

    if lead_data.get("annual_revenue", 0) > 500000:
        score += 30
        reasons.append("High revenue company (+30)")

    # authority - is this the decision maker?

    title = lead_data.get("title", "").lower()
    if any(t in title for t in ["ceo", "cto", "vp", "director", "head"]):
        score += 25
        reasons.append("Decisions maker title (+25)")
