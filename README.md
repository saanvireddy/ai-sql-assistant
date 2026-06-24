---
title: AI SQL Assistant
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.32.0"
app_file: app/streamlit_app.py
pinned: false
---
# 🤖 AI SQL Analytics Assistant

An agentic NL-to-SQL system that converts plain-English questions into validated SQL queries, executes them, and explains the results — with conversational memory for follow-up questions.

Live Demo → [Hugging Face Space](https://huggingface.co/spaces/saanvireddy/ai-sql-assistant)

---

## Architecture

```
User Question
      ↓
LangGraph ReAct Agent
      ↓
┌─────────────────────────────────────┐
│  Step 1: SQL Generation             │
│  Llama 3.3 70B + schema-aware prompt│
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  Step 2: Validation + Execution     │
│  Guardrails → SQLite runner         │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  Step 3: Result Explanation         │
│  LLM summarizes in plain English    │
└────────────────┬────────────────────┘
                 ↓
     Chat UI + Auto Chart
```

---

## Key Features

- **LangGraph agentic pipeline** — 3-step ReAct agent (generate → execute → explain)
- **Conversational memory** — follow-up questions like "now show only the top 5" work seamlessly
- **Schema-aware prompting** — live DB metadata injected into every prompt
- **SQL guardrails** — SELECT-only enforcement, JOIN validation, LIMIT enforcement
- **Auto chart generation** — bar charts auto-rendered from query results
- **Learning mode** — toggleable prompt, metadata, SQL, and validation views

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Llama 3.3 70B via Groq |
| Agent framework | LangGraph |
| LLM orchestration | LangChain |
| Frontend | Streamlit |
| Database | SQLite |
| Validation | Custom SQL guardrails |
| Data processing | Pandas |

---

## Run Locally

```bash
git clone https://github.com/saanvireddy/ai-sql-assistant.git
cd ai-sql-assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python data/setup_db.py
```

Set your API key:
```bash
$env:GROQ_API_KEY="your_groq_api_key"
```

Run:
```bash
streamlit run app/streamlit_app.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

---

## Example Queries

- *Show total revenue by customer*
- *How many orders were placed in December?*
- *Which city has the most orders?*
- *Now show only the top 3* ← follow-up with memory

---

## Project Structure

```
ai-sql-assistant/
├── agent/
│   └── sql_agent.py        # LangGraph pipeline (3-step agent)
├── app/
│   └── streamlit_app.py    # Chat UI with toggle display options
├── data/
│   └── setup_db.py         # SQLite demo database setup
├── execution/
│   └── sqlite_runner.py    # Query execution engine
├── llm/
│   ├── gemini_llm.py       # Gemini integration (original)
│   ├── mock_llm.py         # Fallback SQL generator
│   └── prompt_builder.py   # Schema-aware prompt builder
├── metadata/
│   └── sqlite_metadata.py  # Live schema + sample row extractor
├── validation/
│   └── sql_validator.py    # SQL guardrails
└── requirements.txt
```

---

## Author

**Saanvi Reddy Baradi**
MS AI & Business Analytics — University of South Florida
[Portfolio](https://saanvireddy.github.io/saanvi-portfolio/) · [LinkedIn](https://www.linkedin.com/in/saanvi-reddy-baradi/) · [GitHub](https://github.com/saanvireddy)