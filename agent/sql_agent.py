import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from langchain_groq import ChatGroq
from metadata.sqlite_metadata import extract_metadata
from validation.sql_validator import validate_sql
from execution.sqlite_runner import execute_sql

DB_PATH = "data/demo.db"

# ── LLM ───────────────────────────────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0,
)


# ── Helpers ───────────────────────────────────────────────────────────────────
def _build_schema_str() -> str:
    metadata = extract_metadata(DB_PATH)
    lines = []
    for table, info in metadata.items():
        col_names = [col["column_name"] for col in info.get("schema", [])]
        sample = info.get("sample_rows", [{}])[0]
        lines.append(f"Table `{table}` — exact columns: {', '.join(col_names)}")
        lines.append(f"  Sample row: {sample}")
        lines.append(f"  IMPORTANT: Only use these exact column names for `{table}`: {', '.join(col_names)}")
    return "\n".join(lines)


def _build_history_str(chat_history: list[dict], n: int = 6) -> str:
    if not chat_history:
        return ""
    lines = [f"{m['role'].upper()}: {m['content']}" for m in chat_history[-n:]]
    return "\nConversation so far:\n" + "\n".join(lines) + "\n"


# ── Step 1: Generate SQL ───────────────────────────────────────────────────────
def _generate_sql(question: str, chat_history: list[dict]) -> str:
    schema_str = _build_schema_str()
    history_str = _build_history_str(chat_history)

    prompt = f"""You are a SQLite expert. Use ONLY the exact column names listed below.

Schema:
{schema_str}
{history_str}
Current question: "{question}"

If this is a follow-up question, use the conversation above to understand context.

Rules:
- SELECT only — no INSERT, UPDATE, DELETE, DROP
- Use ONLY the exact column names shown in the schema above
- Always add LIMIT 100
- Return ONLY the raw SQL query, no markdown, no backticks, no explanation
"""
    response = llm.invoke(prompt)
    sql = response.content.strip()
    for tag in ["```sql", "```"]:
        sql = sql.replace(tag, "")
    return sql.strip()


# ── Step 2: Validate + Execute ────────────────────────────────────────────────
def _execute_query(sql: str) -> tuple[str, str]:
    metadata = extract_metadata(DB_PATH)
    allowed_tables = list(metadata.keys())
    ok, message = validate_sql(sql, allowed_tables)
    if not ok:
        return "", f"Validation failed: {message}"
    try:
        df = execute_sql(DB_PATH, sql)
        if df.empty:
            return "", "Query returned no rows."
        return df.head(100).to_json(orient="records"), ""
    except Exception as e:
        return "", f"Execution error: {str(e)}"


# ── Step 3: Explain ───────────────────────────────────────────────────────────
def _explain_results(results_json: str, question: str, chat_history: list[dict]) -> str:
    history_str = _build_history_str(chat_history, n=4)
    prompt = f"""You are a helpful data analyst.
{history_str}
The user asked: "{question}"

The database returned this data (JSON):
{results_json[:3000]}

Write a clear 2-3 sentence answer directly addressing the question.
Do not mention SQL, JSON, or technical details.
Speak naturally as if explaining to a business user."""
    response = llm.invoke(prompt)
    return response.content.strip()


# ── Public interface ──────────────────────────────────────────────────────────
def run_agent(question: str, chat_history: list[dict]) -> dict:
    try:
        sql = _generate_sql(question, chat_history)
        results_json, error = _execute_query(sql)

        if error:
            return {
                "answer": f"I couldn't execute that query: {error}",
                "sql": sql,
                "results_json": "",
                "error": None,
            }

        answer = _explain_results(results_json, question, chat_history)

        return {
            "answer": answer,
            "sql": sql,
            "results_json": results_json,
            "error": None,
        }

    except Exception as e:
        return {
            "answer": "",
            "sql": "",
            "results_json": "",
            "error": str(e),
        }