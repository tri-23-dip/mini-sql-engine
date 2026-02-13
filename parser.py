import re

def parse_query(query):
    query = query.strip()

    pattern = re.compile(
        r"SELECT (.+) FROM (\w+)"
        r"(?: WHERE (.+?))?"
        r"(?: ORDER BY (\w+)(?: (ASC|DESC))?)?"
        r"(?: LIMIT (\d+))?$",
        re.IGNORECASE
    )

    match = pattern.match(query)

    if not match:
        raise ValueError("Invalid query format")

    columns = match.group(1)
    table = match.group(2)
    where_clause = match.group(3)
    order_by = match.group(4)
    order_dir = match.group(5)
    limit = match.group(6)

    if columns != "*":
        columns = [col.strip() for col in columns.split(",")]

    return {
        "columns": columns,
        "table": table,
        "where": where_clause,
        "order_by": order_by,
        "order_dir": order_dir,
        "limit": int(limit) if limit else None
    }
