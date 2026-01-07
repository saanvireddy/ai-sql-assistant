# AI Powered SQL Analytics Assistant

An end-to-end AI-powered SQL assistant that converts natural language questions into validated SQL queries using schema-aware prompting, executes them safely, and presents results with summaries and visualizations through an interactive Streamlit interface.

This project demonstrates real-world GenAI system design, including metadata extraction, prompt engineering, LLM integration, validation guardrails, and modular architecture.

---

## 🚀 Features

- Natural language to SQL conversion  
- Schema-aware prompting using live database metadata  
- Automated SQL validation (SELECT-only, safe joins, LIMIT enforcement)  
- Secure query execution with result visualization  
- Streamlit-based self-service analytics UI  
- Modular LLM design with Gemini (Vertex AI) + local fallback  

---

## 🧠 System Architecture

User Question  
→ Metadata Extraction (schema + sample rows)  
→ Prompt Engineering  
→ LLM Layer (Gemini via Vertex AI OR local fallback)  
→ SQL Validation Guardrails  
→ SQL Execution Engine  
→ Results + Summary + Charts  

---

## 🛠️ Tech Stack

- Language: Python  
- Frontend: Streamlit  
- Database: SQLite (local demo)  
- AI / LLM: Vertex AI Gemini, LangChain  
- Data Handling: Pandas  
- Design Concepts: Prompt Engineering, Guardrails, Modular AI Pipelines  

---

## 📂 Project Structure

ai-sql-assistant/  
├── app/          # Streamlit UI  
├── llm/          # Gemini + fallback SQL generation  
├── metadata/     # Schema & sample row extraction  
├── validation/   # SQL safety and validation logic  
├── execution/    # Query execution engine  
├── data/         # Demo database setup  

---

## ▶️ How to Run Locally

### 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-sql-assistant.git  
cd ai-sql-assistant  

### 2. Create virtual environment
python -m venv venv  
venv\Scripts\activate  

### 3. Install dependencies
pip install -r requirements.txt  

### 4. Create demo database
python data/setup_db.py  

### 5. Run the application
streamlit run app/streamlit_app.py  

---

## 💡 Notes on Gemini Integration

The system integrates Vertex AI Gemini using LangChain.  
For cost-efficient demos, a fallback SQL generator is enabled when cloud billing is disabled.

This design mirrors real-world production systems where LLM usage is controlled by configuration and cost constraints.

---

## 📌 Example Questions

- Show total amount spent by each customer  
- Number of orders by city  
- List all orders placed in December  
- Which customer spent the most money  

---

## 📄 Resume Description

Built an AI-powered SQL analytics assistant using Vertex AI Gemini and LangChain to translate natural language questions into schema-aware SQL. Implemented metadata extraction pipelines, prompt engineering, SQL validation guardrails, and a Streamlit-based self-service analytics interface with visualizations.
