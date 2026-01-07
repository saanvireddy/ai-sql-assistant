import sqlite3
from pathlib import Path

DB_PATH = Path("data/demo.db")

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS customers;")
    cur.execute("DROP TABLE IF EXISTS orders;")

    cur.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );
    """)

    customers = [
        (1, "Asha", "Tampa"),
        (2, "Rahul", "Orlando"),
        (3, "Meera", "Miami"),
    ]
    orders = [
        (1, 1, "2025-11-01", 120.50),
        (2, 1, "2025-11-15", 75.00),
        (3, 2, "2025-12-02", 210.00),
        (4, 3, "2025-12-18", 50.25),
    ]

    cur.executemany("INSERT INTO customers VALUES (?, ?, ?);", customers)
    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?);", orders)

    conn.commit()
    conn.close()
    print("Database created successfully")

if __name__ == "__main__":
    main()
