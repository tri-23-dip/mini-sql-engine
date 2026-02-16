import csv
from parser import parse_query


def evaluate_condition(row, condition):
    """
    Supports:
    column=value
    column>value
    column<value
    column>=value    (NEW)
    column<=value    (NEW)
    AND / OR logic
    """

    if " AND " in condition:
        parts = condition.split(" AND ")
        return all(evaluate_condition(row, part) for part in parts)

    if " OR " in condition:
        parts = condition.split(" OR ")
        return any(evaluate_condition(row, part) for part in parts)

    # NEW: Handle >= operator
    if ">=" in condition:
        col, val = condition.split(">=")
        return float(row[col.strip()]) >= float(val.strip())

    # NEW: Handle <= operator
    if "<=" in condition:
        col, val = condition.split("<=")
        return float(row[col.strip()]) <= float(val.strip())

    if "=" in condition:
        col, val = condition.split("=")
        # Check if it's numeric comparison
        try:
            return float(row[col.strip()]) == float(val.strip())
        except ValueError:
            return row[col.strip()] == val.strip()

    if ">" in condition:
        col, val = condition.split(">")
        return float(row[col.strip()]) > float(val.strip())

    if "<" in condition:
        col, val = condition.split("<")
        return float(row[col.strip()]) < float(val.strip())

    return False


def execute_query(query):
    parsed = parse_query(query)

    table_file = parsed["table"] + ".csv"
    results = []

    with open(table_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if parsed["where"]:
                if evaluate_condition(row, parsed["where"]):
                    results.append(row)
            else:
                results.append(row)

    # SELECT specific columns
    if parsed["columns"] != "*":
        results = [
            {col: row[col] for col in parsed["columns"]}
            for row in results
        ]

    # ORDER BY
    if parsed["order_by"]:
        reverse = parsed["order_dir"] and parsed["order_dir"].upper() == "DESC"
        results.sort(key=lambda x: x[parsed["order_by"]], reverse=reverse)

    # LIMIT
    if parsed["limit"]:
        results = results[:parsed["limit"]]

    return results


if __name__ == "__main__":
    print("Advanced Mini SQL Engine")
    print("Example:")
    print("SELECT name,age FROM data WHERE age>=25 AND age<=30 ORDER BY age DESC LIMIT 2")

    query = input("Enter query: ")

    try:
        results = execute_query(query)
        print("\nResults:")
        for row in results:
            print(row)
    except Exception as e:
        print("Error:", e)