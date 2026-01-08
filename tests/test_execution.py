from execution.sqlite_runner import execute_sql

sql = """
SELECT c.name, SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name
ORDER BY total_spent DESC
LIMIT 100;
"""

df = execute_sql("data/demo.db", sql)
print(df)
