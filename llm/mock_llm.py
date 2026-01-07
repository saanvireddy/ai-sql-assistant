def generate_sql_from_question(question: str) -> str:
    q = question.lower()

    if "total" in q and "customer" in q:
        return """
SELECT c.name,
       SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o
  ON c.customer_id = o.customer_id
GROUP BY c.name
ORDER BY total_spent DESC
LIMIT 100;
""".strip()

    if "orders" in q and "city" in q:
        return """
SELECT c.city,
       COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o
  ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY total_orders DESC
LIMIT 100;
""".strip()

    if "all orders" in q or "show orders" in q:
        return """
SELECT *
FROM orders
LIMIT 100;
""".strip()

    return """
SELECT *
FROM customers
LIMIT 100;
""".strip()
