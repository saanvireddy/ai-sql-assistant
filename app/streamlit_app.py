import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

from metadata.sqlite_metadata import extract_metadata
from llm.prompt_builder import build_prompt
from llm.gemini_llm import generate_sql_with_gemini
from llm.mock_llm import generate_sql_from_question
from validation.sql_validator import validate_sql
from execution.sqlite_runner import execute_sql

DB_PATH = "data/demo.db"

st.set_page_config(page_title="AI SQL Assistant", layout="wide")
st.title("AI Powered SQL Assistant (Local Version)")

st.write(
    "Type a plain-English question. The system generates SQL, validates it, executes it, and shows results."
)

question = st.text_input(
    "Your question",
    placeholder="Example: Show total amount spent by each customer",
)

col1, col2 = st.columns([1, 1])

with col1:
    show_prompt = st.checkbox("Show prompt (learning mode)", value=True)

with col2:
    show_metadata = st.checkbox("Show metadata (schema + samples)", value=False)

if st.button("Run"):
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    # 1) Extract metadata (schema + sample rows)
    metadata = extract_metadata(DB_PATH)
    allowed_tables = list(metadata.keys())

    if show_metadata:
        st.subheader("Extracted Metadata")
        st.json(metadata)

    # 2) Build prompt
    prompt = build_prompt(question, metadata)

    if show_prompt:
        st.subheader("Prompt sent to the model")
        st.code(prompt)

    try:
        sql = generate_sql_with_gemini(prompt)
        st.info("SQL generated using Gemini (Vertex AI)")
    except Exception:
        sql = generate_sql_from_question(question)
        st.info("Gemini disabled – using fallback SQL generator")



    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    # 4) Validate SQL
    ok, message = validate_sql(sql, allowed_tables)

    st.subheader("Validation")
    if ok:
        st.success(message)
    else:
        st.error(message)
        st.stop()

    # 5) Execute SQL
    try:
        df = execute_sql(DB_PATH, sql)
    except Exception as e:
        st.error(f"SQL execution failed: {e}")
        st.stop()

    # 6) Show results
    st.subheader("Results")
    if df.empty:
        st.info("No rows returned.")
        st.stop()

    st.dataframe(df, width=True)

    # 7) Simple summary
    st.subheader("Summary")
    st.write(f"Returned **{len(df)}** rows and **{len(df.columns)}** columns.")

    # 8) Chart (auto)
    st.subheader("Chart")
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if numeric_cols:
        st.bar_chart(df[numeric_cols])
    else:
        st.info("No numeric columns available to chart.")
