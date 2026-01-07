from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage
import vertexai
import os

# === CONFIG ===
PROJECT_ID = "ai-sql-assistant-483420"   # keep your real project id
LOCATION = "us-central1"

# Toggle this flag
USE_GEMINI = False   # <-- set True only when billing is enabled

def generate_sql_with_gemini(prompt: str) -> str:
    if not USE_GEMINI:
        raise RuntimeError("Gemini disabled (billing not enabled)")

    vertexai.init(project=PROJECT_ID, location=LOCATION)

    llm = ChatVertexAI(
        model="gemini-1.5-flash",
        temperature=0.0,
        max_output_tokens=512,
    )

    response = llm.invoke([HumanMessage(content=prompt)])

    if not response or not response.content:
        return ""

    return response.content.strip()
