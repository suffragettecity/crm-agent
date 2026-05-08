def score_lead(data: dict) -> dict:
    """
    BANT Lead scoring

    Expected keys (all optional - missing keys score 0):
      annual_revenue (number)
      title (str)
      industry (str)
      close_date_days (int - dats until expected close)
      lead_source (str)
      has_budget  (bool)
    """
    score = 0 
    reasons = []

    # budget
    revenue = data.get("annual_revenue") or 0
    if data.get("has_budget"):
        score += 25
        reasons.append("Budget confirmed (+25)")
    elif revenue > 1_000_000:
        score += 25
        reasons.append(f"Revenue ${revenue:,.0f} - strong budget signal (+25)")
    elif revenue >= 250_000:
        score += 12
        reasons.append(f"Revenue ${revenue:,.0f} - moderate budget signal (+12)")


    # authority - is this the decision maker?

    title = (data.get("title") or "").lower()
    decision_maker_keywords = ["ceo", "cto", "cfo", "coo", "vp", "vice president", 
                               "director", "head of", "owner", "founder", "president"]
    if any(kw in title for kw in decision_maker_keywords):
        score +=25
        reasons.append(f"Decision-maker title: {data.get('title')} (+25)")
    elif title:
        score += 8
        reasons.append(f"Title on record (8+)")

    if data.get("industry") in ["Technology", "Finance", "Healthcare"]:
        score += 20
        reasons.append("Target industry (+20)")

    # timeline
    if data.get("close_date_days", 999) < 90:
        score += 25
        reasons.append("Short close timeline (+25)")

    # grade
    if score >= 80: grade = "Hot"
    elif score >= 50: grade ="Warm"
    else: grade = "Cold"

    return {"score": score, "grade": grade, "reasons": reasons}
