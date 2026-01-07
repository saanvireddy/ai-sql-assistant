from validation.sql_validator import validate_sql

allowed_tables = ["customers", "orders"]

queries = [
    "SELECT * FROM customers LIMIT 100;",
    "DELETE FROM customers;",
    "SELECT * FROM orders;",
    "SELECT * FROM customers JOIN orders;",
]

for q in queries:
    ok, msg = validate_sql(q, allowed_tables)
    print("\nSQL:", q)
    print("VALID:", ok)
    print("MESSAGE:", msg)
