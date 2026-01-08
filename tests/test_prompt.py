from metadata.sqlite_metadata import extract_metadata
from llm.prompt_builder import build_prompt

metadata = extract_metadata("data/demo.db")
question = "Show total amount spent by each customer"

prompt = build_prompt(question, metadata)
print(prompt)
