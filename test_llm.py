from llm.mock_llm import generate_sql_from_question

questions = [
    "Show total amount spent by each customer",
    "Number of orders by city",
    "Show all orders"
]

for q in questions:
    print("\nQUESTION:", q)
    print(generate_sql_from_question(q))
