import sys
import os
import subprocess
import json

if not os.path.exists("data/demo.db"):
    subprocess.run(["python", "data/setup_db.py"], check=True)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

from metadata.sqlite_metadata import extract_metadata
from llm.prompt_builder import build_prompt
from validation.sql_validator import validate_sql
from agent.sql_agent import run_agent

DB_PATH = "data/demo.db"

st.set_page_config(page_title="AI SQL Assistant", page_icon="🤖", layout="wide")
st.title("🤖 AI SQL Analytics Assistant")
st.caption("Powered by Llama 3.3 70B (Groq) · LangGraph ReAct Agent · Conversational Memory")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
**Stack**
- 🧠 Llama 3.3 70B via Groq
- 🔗 LangGraph ReAct Agent
- 💬 Conversational memory
- 🛡️ SQL validation guardrails
- 📊 Auto chart generation

**Try asking:**
- *Show total revenue by customer*
- *How many orders were placed in December?*
- *Which city has the most orders?*
- *Now show only the top 5* ← tests memory!
    """)
    st.divider()
    st.subheader("⚙️ Display options")
    show_sql        = st.toggle("Show generated SQL", value=True)
    show_chart      = st.toggle("Show chart", value=True)
    show_metadata   = st.toggle("Show schema metadata", value=False)
    show_prompt     = st.toggle("Show prompt (learning mode)", value=False)
    show_validation = st.toggle("Show validation result", value=False)
    st.divider()
    if st.button("🗑️ Clear conversation"):
        for key in ["chat_history", "last_result", "last_question"]:
            st.session_state[key] = [] if key == "chat_history" else {}
        st.rerun()

# ── Session state ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = {}
if "last_question" not in st.session_state:
    st.session_state.last_question = ""


# ── Helper: render extras for a result ───────────────────────────────────────
def render_extras(result: dict, question: str):
    if show_metadata:
        metadata = extract_metadata(DB_PATH)
        with st.expander("🗂️ Schema metadata", expanded=True):
            st.json(metadata)

    if show_prompt:
        metadata = extract_metadata(DB_PATH)
        prompt = build_prompt(question, metadata)
        with st.expander("📋 Prompt sent to model", expanded=True):
            st.code(prompt)

    if show_sql and result.get("sql"):
        with st.expander("📝 Generated SQL", expanded=True):
            st.code(result["sql"], language="sql")

    if show_validation and result.get("sql"):
        metadata = extract_metadata(DB_PATH)
        ok, message = validate_sql(result["sql"], list(metadata.keys()))
        with st.expander("🛡️ Validation", expanded=True):
            if ok:
                st.success(message)
            else:
                st.error(message)

    results_json = result.get("results_json", "")
    if results_json and not results_json.startswith(("Validation", "Execution", "Query")):
        try:
            df = pd.DataFrame(json.loads(results_json))
            with st.expander("📊 Results table", expanded=True):
                st.dataframe(df, use_container_width=True)
                st.caption(f"{len(df)} rows · {len(df.columns)} columns")
            if show_chart:
                numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
                text_cols = df.select_dtypes(include=["object"]).columns.tolist()
                if numeric_cols and len(df) > 1:
                    chart_df = df[numeric_cols].copy()
                    if text_cols:
                        chart_df.index = df[text_cols[0]]
                    st.bar_chart(chart_df)
        except Exception:
            pass


# ── Chat history display ──────────────────────────────────────────────────────
for i, msg in enumerate(st.session_state.chat_history):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Re-render extras for last assistant message with current toggle state
        is_last = (i == len(st.session_state.chat_history) - 1)
        if msg["role"] == "assistant" and is_last and st.session_state.last_result:
            render_extras(st.session_state.last_result, st.session_state.last_question)

# ── Input ─────────────────────────────────────────────────────────────────────
question = st.chat_input("Ask a question about your data...")

if question:
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.chat_history.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = run_agent(question, st.session_state.chat_history[:-1])

        if result["error"]:
            answer = f"Agent error: {result['error']}"
            st.error(answer)
        else:
            answer = result["answer"] or "Query executed. See results below."
            st.markdown(answer)
            render_extras(result, question)

        # Store last result for toggle re-renders
        st.session_state.last_result = result
        st.session_state.last_question = question

    st.session_state.chat_history.append({"role": "assistant", "content": answer})