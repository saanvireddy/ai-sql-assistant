import sqlite3
from typing import Dict, List, Any

def get_tables(conn: sqlite3.Connection) -> List[str]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    return [row[0] for row in cursor.fetchall()]

def get_table_schema(conn: sqlite3.Connection, table_name: str) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    schema = []
    for col in columns:
        schema.append({
            "column_name": col[1],
            "data_type": col[2],
            "is_primary_key": bool(col[5])
        })
    return schema

def get_sample_rows(conn: sqlite3.Connection, table_name: str, limit: int = 3) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
    col_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    samples = []
    for row in rows:
        samples.append(dict(zip(col_names, row)))

    return samples

def extract_metadata(db_path: str) -> Dict[str, Any]:
    conn = sqlite3.connect(db_path)
    tables = get_tables(conn)

    metadata = {}
    for table in tables:
        metadata[table] = {
            "schema": get_table_schema(conn, table),
            "sample_rows": get_sample_rows(conn, table)
        }

    conn.close()
    return metadata
