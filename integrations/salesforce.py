from simple_salesforce import Salesforce, SalesforceLogin, SFType
from config.settings import SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN
import json

def _get_sf() -> Salesforce:
    return Salesforce(
        username=SF_USERNAME,
        password=SF_PASSWORD,
        security_token=SF_SECURITY_TOKEN,
    )

# read operations

def get_deal(deal_name: str) -> list[dict]:
    """search opportinities by name (partial match)"""
    sf = _get_sf()
    soql = f"""
        SELECT Id, Name, StageName, Amount, CloseDate,
               Account.Name, Owner.Name, Probability
        FROM Opportunity
        WHERE Name LIKE '%{deal_name}%'
        LIMIT 5
    """
    result = sf.query(soql)
    return result.get("records", [])

def get_contact(name: str) -> list[dict]:
    """Search Contacts by name."""
    sf = _get_sf()
    soql = f"""
        SELECT Id, Name, Title, Email, Phone, Account.Name
        FROM Contact 
        WHERE Name LIKE '%{name}%'
        LIMIT 5
    """
    result = sf.query(soql)
    return result.get("records", [])

def get_lead(name: str) -> list[dict]:
    """Search leads by name"""
    sf = _get_sf()
    soql = f"""
        SELECT Id, Name, Title, Company, Industry,
               AnnualRevenue, Email, Status, LeadSource
        FROM Lead
        WHERE Name LIKE '%{name}%'
          AND IsConverted = false
        LIMIT 5
    """
    result = sf.query(soql)
    return result.get("records", [])

def update_lead_score(lead_id: str, score: int, notes: str) -> dict:
    """
    Write the qualification score back to Salesforce

    Requires two custom fields on the Lead object:
      Lead_Score__c (Number)
      Qual_Notes__c (Long Text Area)
    Create them in Salesforce Setup -> Object Manager -> Lead -> Fields.
    """
    sf = _get_sf()
    sf.Lead.update(lead_id, {
        "Lead_Score__c": score,
        "Qual_Notes__c": notes,
    })
    return {"updated": True, "lead_id": lead_id, "score": score}