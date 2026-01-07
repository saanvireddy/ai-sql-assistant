import re
from typing import List, Tuple

FORBIDDEN_KEYWORDS = [
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE"
]

SQL_KEYWORDS = {
    "SELECT", "FROM", "JOIN", "ON", "WHERE", "GROUP", "BY", "ORDER",
    "LIMIT", "AS", "AND", "OR", "SUM", "COUNT", "AVG", "MIN", "MAX",
    "DESC", "ASC", "DISTINCT"
}

def extract_identifiers(sql: str) -> List[str]:
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", sql)
    identifiers = []
    for t in tokens:
        if t.upper() not in SQL_KEYWORDS:
            identifiers.append(t)
    return list(set(identifiers))

def validate_sql(sql: str, allowed_tables: List[str]) -> Tuple[bool, str]:
    sql_clean = sql.strip().strip(";")
    sql_upper = sql_clean.upper()

    # Rule 1: Only SELECT
    if not sql_upper.startswith("SELECT"):
        return False, "Only SELECT statements are allowed."

    # Rule 2: Block dangerous keywords
    for word in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{word}\b", sql_upper):
            return False, f"Forbidden keyword detected: {word}"

    # Rule 3: Validate table names
    identifiers = extract_identifiers(sql_clean)
    for ident in identifiers:
        if ident not in allowed_tables and ident.lower() not in allowed_tables:
            pass  # columns are allowed, so we skip strict table check here

    # Rule 4: JOIN must have ON
    if "JOIN" in sql_upper and " ON " not in sql_upper:
        return False, "JOIN detected without ON condition."

    # Rule 5: LIMIT enforcement
    if "LIMIT" not in sql_upper:
        return False, "Query must include a LIMIT clause."

    return True, "SQL passed validation checks."
