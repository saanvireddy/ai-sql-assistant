from metadata.sqlite_metadata import extract_metadata

metadata = extract_metadata("data/demo.db")

for table, info in metadata.items():
    print(f"\nTABLE: {table}")
    print("SCHEMA:")
    for col in info["schema"]:
        print(col)
    print("SAMPLE ROWS:")
    for row in info["sample_rows"]:
        print(row)
