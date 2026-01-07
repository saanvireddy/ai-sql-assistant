# AI Powered SQL Analytics Assistant

An end-to-end AI-powered SQL assistant that converts natural language questions into validated SQL queries using schema-aware prompting, executes them safely, and presents results with summaries and visualizations through an interactive Streamlit interface.

This project demonstrates real-world GenAI system design, including metadata extraction, prompt engineering, LLM integration, validation guardrails, and modular architecture.

---

## Features

- Natural language to SQL conversion  
- Schema-aware prompting using live database metadata  
- Automated SQL validation (SELECT-only, safe joins, LIMIT enforcement)  
- Secure query execution with result visualization  
- Streamlit-based self-service analytics UI  
- Modular LLM design with Gemini (Vertex AI) + local fallback  

---

## System Architecture

User Question  
→ Metadata Extraction (schema + sample rows)  
→ Prompt Engineering  
→ LLM Layer (Gemini via Vertex AI OR local fallback)  
→ SQL Validation Guardrails  
→ SQL Execution Engine  
→ Results + Summary + Charts  

---

## Tech Stack

- Language: Python  
- Frontend: Streamlit  
- Database: SQLite (local demo)  
- AI / LLM: Vertex AI Gemini, LangChain  
- Data Handling: Pandas  
- Design Concepts: Prompt Engineering, Guardrails, Modular AI Pipelines  

---
