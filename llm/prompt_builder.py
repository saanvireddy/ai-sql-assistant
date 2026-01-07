import json
from typing import Dict, Any

RULES = [
    "You generate SQL queries for the given database.",
    "Only generate SELECT statements.",
    "Do NOT use INSERT, UPDATE, DELETE, DROP, ALTER, or CREATE.",
    "Use correct JOIN conditions when multiple tables are involved.",
    "Use column names exactly as defined in the schema.",
    "Always include a LIMIT 100 clause.",
    "Return ONLY the SQL query and nothing else."
]

def build_prompt(question: str, metadata: Dict[str, Any]) -> str:
    rules_text = "\n".join([f"- {rule}" for rule in RULES])
    metadata_text = json.dumps(metadata, indent=2)

    prompt = f"""
You are an expert data analyst.

Rules:
{rules_text}

Database metadata (schema and sample rows):
{metadata_text}

User question:
{question}

SQL:
""".strip()

    return prompt
