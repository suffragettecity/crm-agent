# agent core - Gemini 1.5 Flash with function calling

import json 
import google.generativeai as genai

from config.settings import GOOGLE_API_KEY, GEMINI_MODEL, MAX_AGENT_TURNS
from config.prompts import SYSTEM_PROMPT
from integrations.salesforce import (get_deal, get_contact, get_lead, update_lead_score)

from scoring.lead_scoring import score_lead

genai.configure(api_key=GOOGLE_API_KEY)

TOOLS = [
    genai.protos.Tool(function_declarations = [
        
        genai.protos.FunctionDeclaration(
            name = "get_deal_info",
            description = "Fetch Opportunity/Deal details from Salesforce by deal name.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "deal_name": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="The name (or partial name) of the deal to look up."
                    )
                },
                required=["deal_name"]
            )
        ),

        genai.protos.FunctionDeclaration(
            name="get_contact_info",
            description="Fetch contact details from Salesforce by person name.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "name": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Full or partial name of the contact."
                    )
                },
                required=["name"]
            )
        ),

        genai.protos.FunctionDeclaration(
            name="get_lead_info",
            description="Fetch Lead details from Salesforce by person name.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "name": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Full or partial name of the lead."
                    )
                },
                required=["name"]
            )
        ),

        genai.protos.FunctionDeclaration(
            name="qualify_lead",
            description=(
                "Score and qualify a lead using the BANT framework, "
                "then update the score in Salesforce."
            ),
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "lead_id":  genai.protos.Schema(type=genai.protos.Type.STRING, description="Salesforce Lead ID (18-char)"),
                    "annual_revenue": genai.protos.Schema(type=genai.protos.Type.NUMBER, description="Company annual revenue in USD"),
                    "title": genai.protos.Schema(type=genai.protos.Type.STRING, description="Lead's job title"),
                    "industry": genai.protos.Schema(type=genai.protos.Type.STRING, description="Lead's industry"),
                    "close_date_days": genai.protos.Schema(type=genai.protos.Type.NUMBER, description="Days until expected close / decision"),
                    "has_budget": genai.protos.Schema(type=genai.protos.Type.BOOLEAN, description="True if budget has been confirmed"),
                },
                required=["lead_id"]
            )
        ),
    ])
]


# tool executor

def _execute_tool(name: str, args: dict) -> str:
    try:
        if name == "get_deal_info":
            return json.dumps(get_deal(args["deal_name"]), default=str)
        elif name == "get_contact_info":
            return json.dumps(get_contact(args["name"]), default=str)
        elif name == "get_lead_info":
            return json.dumps(get_lead(args["name"]), default=str)
        elif name == "qualify_lead":
            result = score_lead(args)
            lead_id = args["lead_id"]
            update_lead_score(lead_id, result["score"], result["summary"])
            return json.dumps(result)
        else:
            return json.dumps({"error": f"Unknown tool: {name}"})
        
    except Exception as e:
        return json.dumps({"error": str(e)})
    

# agent loop

def run_agent(user_message: str, history: list[dict]) -> str:
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=SYSTEM_PROMPT,
        tools=TOOLS,
    )

    history.append({"role": "user", "parts": [{"text": user_message}]})

    for turn in range(MAX_AGENT_TURNS):
        response = model.generate_content(history)
        candidate = response.candidates[0]
        parts = candidate.content.parts

        # check for function calls in the response
        func_calls = [p for p in parts if hasattr(p, "function_call") and p.function_call.name]

        if not func_calls:
            # no more tool calls - extract text reply
            reply = "".join(p.text for p in parts if hasattr(p, "text") and p.text)
            history.append({"role": "model", "parts": [{"text": reply}]})
            return reply
        
        # execute every function call Gemini requested

        tool_results = []
        for part in func_calls:
            fc = part.function_call
            result = _execute_tool(fc.name, dict(fc.args))
            tool_results.append(
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=fc.name,
                        response={"result": result},
                    )
                )
            )

        history.append({"role": "model", "parts": [{"text": ""}]}) # model turn placeholder
        history.append({"role": "user", "parts": tool_results}) # tool results as user turn

    return "I'm sorry, I hit my reasoning limit. Please give me a simpler question!"