# AI Powered SQL Analytics Assistant

An end-to-end AI-powered SQL analytics assistant that converts natural language questions into validated SQL queries using schema-aware prompting. The system safely executes queries and presents results with summaries and visualizations through an interactive Streamlit interface.

This project is designed to mirror real-world GenAI system architecture, emphasizing reliability, safety, modularity, and cost-aware AI integration.

---

# Key Features

- Natural language to SQL conversion  
- Schema-aware prompting using live database metadata  
- Automated SQL validation (SELECT-only, safe joins, LIMIT enforcement)  
- Secure query execution with result visualization  
- Streamlit-based self-service analytics UI  
- Modular LLM layer with Vertex AI Gemini and local fallback  

---

## System Architecture

```
User Question
   ↓
Metadata Extraction (schema + sample rows)
   ↓
Prompt Engineering
   ↓
LLM Layer (Gemini via Vertex AI OR Local Fallback)
   ↓
SQL Validation Guardrails
   ↓
SQL Execution Engine
   ↓
Results + Summary + Charts
```

---

## Tech Stack

- **Language:** Python  
- **Frontend:** Streamlit  
- **Database:** SQLite (local demo)  
- **AI / LLM:** Vertex AI Gemini, LangChain  
- **Data Processing:** Pandas  
- **Design Concepts:** Prompt Engineering, Guardrails, Modular AI Pipelines  

---

## Run the Project Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-sql-assistant.git
cd ai-sql-assistant
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create demo database
```bash
python data/setup_db.py
```

### 5. Launch the application
```bash
streamlit run app/streamlit_app.py
```

---

## Vertex AI Gemini Integration

The system integrates **Vertex AI Gemini** using LangChain for natural language to SQL generation.

To ensure cost efficiency and easy local demos:
- Gemini integration is configurable
- A local fallback SQL generator is used when cloud billing is disabled

This reflects real-world production systems where AI usage is governed by cost, reliability, and environment constraints.

---

## Example Queries

- Show total amount spent by each customer  
- Number of orders by city  
- List all orders placed in December  
- Which customer spent the most money  

---

## Security & Best Practices

- Service account credentials are excluded via `.gitignore`
- No secrets or databases are committed to the repository
- SQL validation prevents unsafe query execution
- Modular design enables easy upgrades and replacements


---

## Future Enhancements

- BigQuery integration for large-scale datasets - Role-based access control  
- Query confidence scoring  
- Caching and performance optimization  
- Deployment to cloud platforms (Streamlit Cloud / Cloud Run)  

---

